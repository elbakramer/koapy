import click

from koapy.cli.utils.fail_with_usage import fail_with_usage
from koapy.cli.utils.verbose_option import verbose_option
from koapy.utils.logging import get_logger

logger = get_logger(__name__)


@click.command(short_help="Get daily OHLCV of stocks.")
@click.option("-c", "--code", metavar="CODE", help="Stock code to get.")
@click.option(
    "-o",
    "--output",
    metavar="FILENAME",
    type=click.Path(),
    help="Output filename for code.",
)
@click.option(
    "-f",
    "--format",
    metavar="FORMAT",
    type=click.Choice(["xlsx", "sqlite3"], case_sensitive=False),
    default="xlsx",
    help="Output format. (default: xlsx)",
)
@click.option(
    "-s",
    "--start-date",
    metavar="YYYY-MM-DD",
    type=click.DateTime(formats=["%Y-%m-%d", "%Y%m%d"]),
    help="Most recent date to get. Defaults to today or yesterday if market is open.",
)
@click.option(
    "-e",
    "--end-date",
    metavar="YYYY-MM-DD",
    type=click.DateTime(formats=["%Y-%m-%d", "%Y%m%d"]),
    help="Stops if reached, not included (optional).",
)
@click.option(
    "-p", "--port", metavar="PORT", help="Port number of grpc server (optional)."
)
@verbose_option()
def daily(
    code, output, format, start_date, end_date, port
):  # pylint: disable=redefined-builtin
    if (code, output, start_date, end_date) == (None, None, None, None):
        fail_with_usage()

    if output is None:
        output = "{}.{}".format(code, format)

    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEntrypoint import (
        KiwoomOpenApiPlusEntrypoint,
    )

    with KiwoomOpenApiPlusEntrypoint(port=port) as context:
        context.EnsureConnected()
        df = context.GetDailyStockDataAsDataFrame(code, start_date, end_date)

    if format == "xlsx":
        df.to_excel(output)
        logger.info("Saved data to file: %s", output)
    elif format == "sqlite3":
        from sqlalchemy import create_engine

        engine = create_engine("sqlite:///" + output)
        tablename = "A" + code
        df.to_sql(tablename, engine)
        logger.info("Saved data to file %s with tablename %s", output, tablename)
