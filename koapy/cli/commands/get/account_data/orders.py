import click

from koapy.cli.utils.verbose_option import verbose_option
from koapy.utils.logging import get_logger

logger = get_logger(__name__)


@click.command(short_help="Get order history of a date.")
@click.option("-a", "--account", metavar="ACCNO", help="Account number.")
@click.option("-d", "--date", metavar="DATE", help="Date to get.")
@click.option("-r", "--reverse", is_flag=True)
@click.option("-e", "--executed-only", is_flag=True)
@click.option("-E", "--not-executed-only", is_flag=True)
@click.option("-S", "--stock-only", is_flag=True)
@click.option("-B", "--bond-only", is_flag=True)
@click.option("-s", "--sell-only", is_flag=True)
@click.option("-b", "--buy-only", is_flag=True)
@click.option("-c", "--code", metavar="CODE", help="Stock code to get.")
@click.option("-o", "--starting-order-no", metavar="ORDERNO", help="Starting order no.")
@click.option(
    "-p", "--port", metavar="PORT", help="Port number of grpc server (optional)."
)
@verbose_option()
def orders(
    account,
    date,
    reverse,
    executed_only,
    not_executed_only,
    stock_only,
    bond_only,
    sell_only,
    buy_only,
    code,
    starting_order_no,
    port,
):
    if account is None:
        logger.info("Account not given. Using first account available.")

    sort_type = "1"
    if reverse:
        sort_type = "2"
    if executed_only:
        sort_type = "3"
    if not_executed_only:
        sort_type = "4"
    asset_type = "0"
    if stock_only:
        asset_type = "1"
    if bond_only:
        asset_type = "2"
    order_type = "0"
    if sell_only:
        order_type = "1"
    if buy_only:
        order_type = "2"

    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEntrypoint import (
        KiwoomOpenApiPlusEntrypoint,
    )

    with KiwoomOpenApiPlusEntrypoint(port=port) as context:
        context.EnsureConnected()
        if account is None:
            account = context.GetFirstAvailableAccount()
        df = context.GetOrderLogAsDataFrame1(account)
        click.echo("[실시간미체결요청]")
        click.echo(df.to_markdown())
        click.echo()
        df = context.GetOrderLogAsDataFrame2(account)
        click.echo("[실시간체결요청]")
        click.echo(df.to_markdown())
        click.echo()
        df = context.GetOrderLogAsDataFrame3(
            account, date, sort_type, asset_type, order_type, code, starting_order_no
        )
        click.echo("[계좌별주문체결내역상세요청]")
        click.echo(df.to_markdown())
