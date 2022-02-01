import click

from .autologin import autologin


@click.group(short_help="Configure many things.")
def configure():
    pass


configure.add_command(autologin)
