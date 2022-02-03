import click

from .auto_login import auto_login


@click.group(short_help="Disable many things.")
def disable():
    pass


disable.add_command(auto_login)
