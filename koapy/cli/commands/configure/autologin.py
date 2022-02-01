import click

from koapy.cli.utils.verbose_option import verbose_option


@click.command(short_help="Show configuration window for auto login.")
@click.option(
    "-p", "--port", metavar="PORT", help="Port number of grpc server (optional)."
)
@verbose_option()
def autologin(port):
    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEntrypoint import (
        KiwoomOpenApiPlusEntrypoint,
    )

    with KiwoomOpenApiPlusEntrypoint(port=port) as context:
        context.EnsureConnected()
        context.ShowAccountWindow()
