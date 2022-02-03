import click

from .account_window import account_window


@click.group(short_help="Show many things.")
def show():
    pass


show.add_command(account_window)
