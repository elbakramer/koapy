import click

from .account_window import account_window


@click.group(short_help="Show some configuration windows.")
def show():
    pass


show.add_command(account_window)
