import click

from koapy.cli.extensions.verbose_option import (
    verbose_option as extensions_verbose_option,
)
from koapy.utils.logging import set_verbosity


def fail_with_usage(message=None):
    ctx = click.get_current_context()
    if message is not None:
        click.UsageError(message).show()
        click.echo()
    click.echo(ctx.get_help())
    ctx.exit(1)


def verbose_option_callback(ctx, param, value):
    set_verbosity(value)


def verbose_option(*args, **kwargs):
    if "callback" not in kwargs:
        kwargs["callback"] = verbose_option_callback
    return extensions_verbose_option(*args, **kwargs)
