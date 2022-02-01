import click

from .python_stubs import python_stubs


@click.group(short_help="Generate openapi related files.")
def openapi():
    pass


openapi.add_command(python_stubs)
