import click

from koapy.cli.utils import verbose_option
from koapy.cli.utils.pywin32 import uninstall_pywin32


@click.command(short_help="Uninstall pywin32 and run post install script.")
@verbose_option(default=5)
def pywin32(verbose):
    uninstall_pywin32()
