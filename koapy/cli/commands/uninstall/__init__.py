import click

from .openapi import openapi
from .pywin32 import pywin32


@click.group(short_help="Uninstall openapi module and others.")
def uninstall():
    pass


uninstall.add_command(openapi)
uninstall.add_command(pywin32)
