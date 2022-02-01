import click

from koapy.cli.utils.verbose_option import verbose_option
from koapy.utils.logging import get_logger

logger = get_logger(__name__)


@click.command(short_help="Get account evaluation.")
@click.option("-a", "--account", metavar="ACCNO", help="Account number.")
@click.option(
    "-d", "--include-delisted", is_flag=True, help="Include delisted.", default=True
)
@click.option("-D", "--exclude-delisted", is_flag=True, help="Exclude delisted.")
@click.option(
    "-e", "--for-each", is_flag=True, help="Show individual evaluation.", default=True
)
@click.option("-E", "--as-summary", is_flag=True, help="Show summarized evaluation.")
@click.option(
    "-p", "--port", metavar="PORT", help="Port number of grpc server (optional)."
)
@verbose_option()
def evaluation(account, include_delisted, exclude_delisted, for_each, as_summary, port):
    if account is None:
        logger.info("Account not given. Using first account available.")

    if exclude_delisted:
        include_delisted = False

    if as_summary:
        for_each = False
        lookup_type = "1"
    elif for_each:
        lookup_type = "2"

    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEntrypoint import (
        KiwoomOpenApiPlusEntrypoint,
    )

    with KiwoomOpenApiPlusEntrypoint(port=port) as context:
        context.EnsureConnected()

        if account is None:
            account = context.GetAccountList()[0]

        single, multi = context.GetAccountEvaluationStatusAsSeriesAndDataFrame(
            account, include_delisted
        )
        click.echo("[계좌평가현황요청] : [계좌평가현황]")
        click.echo(single.to_markdown(floatfmt=".2f"))
        click.echo()
        click.echo("[계좌평가현황요청] : [종목별계좌평가현황]")
        click.echo(multi.to_markdown())
        click.echo()

        single, multi = context.GetAccountEvaluationBalanceAsSeriesAndDataFrame(
            account, lookup_type
        )
        click.echo("[계좌평가잔고내역요청] : [계좌평가결과]")
        click.echo(single.to_markdown(floatfmt=".2f"))
        click.echo()
        click.echo("[계좌평가잔고내역요청] : [계좌평가잔고개별합산]")
        click.echo(multi.to_markdown())
