import click

from click.parser import normalize_opt

from koapy.cli.extensions.functools import update_wrapper_with_click_params


class VerboseOption(click.Option):
    def __init__(self, *decls, **attrs):
        self._flag_value = attrs.pop("flag_value", None)
        super().__init__(*decls, **attrs)
        self._parser = None
        self._parser__match_long_opt = None
        self._parser__match_short_opt = None
        self._parser__get_value_from_state = None

    def _match_long_opt(self, opt, explicit_value, state):
        # pylint: disable=protected-access
        if opt in self.opts and opt in self._parser._long_opt:
            option = self._parser._long_opt[opt]
            option.action = "store"
        self._parser__match_long_opt(opt, explicit_value, state)

    def _match_short_opt(self, arg, state):
        # pylint: disable=protected-access
        prefix = arg[0]
        for ch in arg[1:]:
            opt = normalize_opt(f"{prefix}{ch}", self._parser.ctx)
            if opt in self.opts and opt in self._parser._short_opt:
                option = self._parser._short_opt[opt]
                option.action = "count"
        self._parser__match_short_opt(arg, state)

    def _get_value_from_state(self, option_name, option, state):
        # pylint: disable=protected-access
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
        # pylint: disable=protected-access
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


def verbose_flag_option(
    default=0,
    flag_value=1,
    show_default=False,
    metavar="[0...5]",
    help="Set verbosity level.",
):
    # pylint: disable=redefined-builtin
    return click.option(
        "-v",
        "--verbose",
        type=int,
        default=default,
        flag_value=flag_value,
        show_default=show_default,
        metavar=metavar,
        help=help,
        cls=VerboseOption,
    )


def no_verbose_flag_option(
    help="Force zero verbosity.",
):
    # pylint: disable=redefined-builtin
    return click.option(
        "-s",
        "--no-verbose",
        "--slient",
        is_flag=True,
        default=False,
        help=help,
    )


def verbose_option(
    dest="verbose",
    default=0,
    flag_value=1,
    callback=None,
    expose_value=False,
    show_default=False,
):
    def decorator(f):
        @click.pass_context
        @verbose_flag_option(
            default=default,
            flag_value=flag_value,
            show_default=show_default,
        )
        @no_verbose_flag_option()
        def new_func(ctx, *args, **kwargs):
            verbose = kwargs.pop("verbose")
            no_verbose = kwargs.pop("no_verbose")
            if no_verbose:
                verbose = 0
            if expose_value:
                kwargs[dest] = verbose
            if callable(callback):
                param = ctx.params.get("verbose")
                value = verbose
                callback(ctx, param, value)
            return ctx.invoke(f, *args, **kwargs)

        return update_wrapper_with_click_params(new_func, f)

    return decorator
