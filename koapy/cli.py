"""Console script for koapy."""
import click

@click.group()
def cli():
    pass

@cli.command()
@click.option('--port')
@click.argument('args', nargs=-1)
def serve(port, args):
    args = ['--port', port] + list(args)
    from koapy.pyqt5.KiwoomOpenApiTrayApplication import KiwoomOpenApiTrayApplication
    KiwoomOpenApiTrayApplication.main(args)

if __name__ == '__main__':
    cli()
