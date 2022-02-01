import click

from koapy.cli.utils.pywin32 import uninstall_pywin32
from koapy.cli.utils.verbose_option import verbose_option


@click.command(short_help="Uninstall pywin32 and run post uninstall script.")
@verbose_option(default=5, show_default=True)
def pywin32():
    uninstall_pywin32()
