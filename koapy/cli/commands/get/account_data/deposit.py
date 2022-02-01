import click

from koapy.cli.utils.verbose_option import verbose_option
from koapy.utils.logging import get_logger

logger = get_logger(__name__)


@click.command(short_help="Get account deposit.")
@click.option("-a", "--account", metavar="ACCNO", help="Account number.")
@click.option(
    "-p", "--port", metavar="PORT", help="Port number of grpc server (optional)."
)
@verbose_option()
def deposit(account, port):
    if account is None:
        logger.info("Account not given. Using first account available.")

    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEntrypoint import (
        KiwoomOpenApiPlusEntrypoint,
    )

    with KiwoomOpenApiPlusEntrypoint(port=port) as context:
        context.EnsureConnected()

        if account is None:
            account = context.GetAccountList()[0]

        result = context.GetDepositInfo(account)
        click.echo(result.to_markdown(floatfmt=".2f"))
