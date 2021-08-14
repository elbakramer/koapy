from functools import update_wrapper

import click

from click.parser import normalize_opt


class VerboseOption(click.Option):
    def __init__(self, *decls, **attrs):
        self._flag_value = attrs.pop("flag_value", None)
        super().__init__(*decls, **attrs)
        self._parser = None
        self._parser__match_long_opt = None
        self._parser__match_short_opt = None
        self._parser__get_value_from_state = None

    def _match_long_opt(self, opt, explicit_value, state):
        if opt in self.opts and opt in self._parser._long_opt:
            option = self._parser._long_opt[opt]
            option.action = "store"
        self._parser__match_long_opt(opt, explicit_value, state)

    def _match_short_opt(self, arg, state):
        prefix = arg[0]
        for ch in arg[1:]:
            opt = normalize_opt(f"{prefix}{ch}", self._parser.ctx)
            if opt in self.opts and opt in self._parser._short_opt:
                option = self._parser._short_opt[opt]
                option.action = "count"
        self._parser__match_short_opt(arg, state)

    def _get_value_from_state(self, option_name, option, state):
        try:
            value = self._parser__get_value_from_state(option_name, option, state)
        except click.BadOptionUsage:
            value = self._flag_value
        else:
            if option_name in self.opts:
                if (
                    isinstance(value, str)
                    and value[:1] in self._parser._opt_prefixes
                    and len(value) > 1
                ):
                    state.rargs.insert(0, value)
                    value = self._flag_value
        return value

    def _patch_parser(self, parser):
        self._parser = parser
        self._parser__match_short_opt = self._parser._match_short_opt
        self._parser._match_short_opt = self._match_short_opt
        self._parser__match_long_opt = self._parser._match_long_opt
        self._parser._match_long_opt = self._match_long_opt
        self._parser__get_value_from_state = self._parser._get_value_from_state
        self._parser._get_value_from_state = self._get_value_from_state

    def add_to_parser(self, parser, ctx):
        self._patch_parser(parser)
        super().add_to_parser(parser, ctx)


def verbose_option(
    dest=None,
    default=None,
    flag_value=None,
    expose_value=None,
    callback=None,
):
    if dest is None:
        dest = "verbose"
    if default is None:
        default = 0
    if flag_value is None:
        flag_value = 1
    if expose_value is None:
        expose_value = True

    dest1 = "_verbose"
    dest2 = "_no_verbose"

    def decorator(f):
        @click.option(
            "-v",
            "--verbose",
            dest1,
            type=int,
            flag_value=flag_value,
            default=default,
            metavar="[0...5]",
            help="Set verbosity level.",
            cls=VerboseOption,
        )
        @click.option(
            "-V",
            "--no-verbose",
            dest2,
            is_flag=True,
            default=False,
            help="Force zero verbosity.",
        )
        @click.pass_context
        def new_func(ctx, *args, **kwargs):
            verbose = kwargs.pop(dest1)
            no_verbose = kwargs.pop(dest2)
            if no_verbose:
                verbose = 0
            if expose_value:
                kwargs[dest] = verbose
            if callable(callback):
                param = ctx.params.get(dest1)
                value = verbose
                callback(ctx, param, value)
            return ctx.invoke(f, *args, **kwargs)

        return update_wrapper(new_func, f)

    return decorator
