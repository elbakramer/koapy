import click

from .grpc import grpc
from .openapi import openapi


@click.group(short_help="Generate files related to grpc, openapi.")
def generate():
    pass


generate.add_command(grpc)
generate.add_command(openapi)
