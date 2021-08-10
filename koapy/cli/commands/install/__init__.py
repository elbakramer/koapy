import click

from .openapi import openapi
from .pywin32 import pywin32


@click.group(short_help="Install openapi module and others.")
def install():
    pass


install.add_command(openapi)
install.add_command(pywin32)
