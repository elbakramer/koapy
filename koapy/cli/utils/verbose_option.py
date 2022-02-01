from koapy.cli.extensions.verbose_option import (
    verbose_option as extensions_verbose_option,
)
from koapy.utils.logging import set_verbosity

full_verbosity = 5


def verbose_option_callback(ctx, param, value):
    set_verbosity(value)


def verbose_option(*args, **kwargs):
    if "callback" not in kwargs:
        kwargs["callback"] = verbose_option_callback
    return extensions_verbose_option(*args, **kwargs)


def full_verbose_option(*args, **kwargs):
    default_kwargs = dict(
        default=full_verbosity,
        show_default=True,
        expose_value=True,
    )
    kwargs = dict(kwargs)
    kwargs.update(default_kwargs)
    return verbose_option(*args, **kwargs)
