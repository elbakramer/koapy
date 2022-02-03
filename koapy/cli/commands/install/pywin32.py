import click

from koapy.cli.utils.pywin32 import install_pywin32
from koapy.cli.utils.verbose_option import verbose_option


@click.command(short_help="Install pywin32 and run post install script.")
@click.option("--version", metavar="VERSION", help="Version of pywin32 to install.")
@verbose_option(default=5, show_default=True)
def pywin32(version):
    install_pywin32(version)
