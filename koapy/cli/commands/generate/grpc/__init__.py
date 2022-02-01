import click

from .ssl_credentials import ssl_credentials


@click.group(short_help="Generate grpc related files.")
def grpc():
    pass


grpc.add_command(ssl_credentials)
