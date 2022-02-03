import click

from koapy.cli.utils.verbose_option import verbose_option


@click.command(short_help="Enable auto login.")
@click.option(
    "-p", "--port", metavar="PORT", help="Port number of grpc server (optional)."
)
@verbose_option(default=5, show_default=True)
def auto_login(port):
    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEntrypoint import (
        KiwoomOpenApiPlusEntrypoint,
    )

    with KiwoomOpenApiPlusEntrypoint(port=port) as context:
        context.EnsureConnected()
        context.EnsureAutoLoginEnabled()
