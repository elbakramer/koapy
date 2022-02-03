import click

from .auto_login import auto_login


@click.group(short_help="Show many things.")
def enable():
    pass


enable.add_command(auto_login)
