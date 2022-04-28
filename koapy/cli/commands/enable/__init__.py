import click

from .auto_login import auto_login


@click.group(short_help="Enable things, including auto login.")
def enable():
    pass


enable.add_command(auto_login)
