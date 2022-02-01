import click

from koapy.cli.utils.fail_with_usage import fail_with_usage
from koapy.cli.utils.verbose_option import verbose_option
from koapy.utils.logging import get_logger

logger = get_logger(__name__)

minute_intervals = [
    "1",
    "3",
    "5",
    "10",
    "15",
    "30",
    "45",
    "60",
]


@click.command(short_help="Get minute OHLCV of stocks.")
@click.option("-c", "--code", metavar="CODE", help="Stock code to get.")
@click.option(
    "-t",
    "--interval",
    metavar="INTERVAL",
    type=click.Choice(minute_intervals, case_sensitive=False),
    help="Minute interval. Possible values are [%s]" % "|".join(minute_intervals),
)
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
    metavar="YYYY-MM-DD['T'hh:mm:ss]",
    type=click.DateTime(
        formats=["%Y-%m-%d", "%Y%m%d", "%Y-%m-%dT%H:%M:%S", "%Y%m%d%H%M%S"]
    ),
    help="Most recent date to get. Defaults to today or yesterday if market is open.",
)
@click.option(
    "-e",
    "--end-date",
    metavar="YYYY-MM-DD['T'hh:mm:ss]",
    type=click.DateTime(
        formats=["%Y-%m-%d", "%Y%m%d", "%Y-%m-%dT%H:%M:%S", "%Y%m%d%H%M%S"]
    ),
    help="Stops if reached, not included (optional).",
)
@click.option(
    "-p", "--port", metavar="PORT", help="Port number of grpc server (optional)."
)
@verbose_option()
def minute(
    code, interval, output, format, start_date, end_date, port
):  # pylint: disable=redefined-builtin
    if (code, interval, output, start_date, end_date) == (None, None, None, None, None):
        fail_with_usage()

    if interval is None:
        fail_with_usage("Interval is not set.")

    if output is None:
        output = "{}.{}".format(code, format)

    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEntrypoint import (
        KiwoomOpenApiPlusEntrypoint,
    )

    with KiwoomOpenApiPlusEntrypoint(port=port) as context:
        context.EnsureConnected()
        df = context.GetMinuteStockDataAsDataFrame(code, interval, start_date, end_date)

    if format == "xlsx":
        df.to_excel(output)
        logger.info("Saved data to file: %s", output)
    elif format == "sqlite3":
        from sqlalchemy import create_engine

        engine = create_engine("sqlite:///" + output)
        tablename = "A" + code
        df.to_sql(tablename, engine)
        logger.info("Saved data to file %s with tablename %s", output, tablename)
