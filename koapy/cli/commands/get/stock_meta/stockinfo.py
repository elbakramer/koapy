import click

from koapy.cli.utils.fail_with_usage import fail_with_usage
from koapy.cli.utils.verbose_option import verbose_option
from koapy.config import default_encoding


@click.command(short_help="Get basic information of stocks.")
@click.option("-c", "--code", metavar="CODE", help="Stock code to get.")
@click.option(
    "-o",
    "--output",
    metavar="FILENAME",
    type=click.Path(),
    help="Output filename. Optional for single code (prints to console).",
)
@click.option(
    "-f",
    "--format",
    type=click.Choice(["md", "xlsx", "json"], case_sensitive=False),
    help="Output format. (default: md)",
    default="md",
    show_choices=True,
)
@click.option(
    "-p", "--port", metavar="PORT", help="Port number of grpc server (optional)."
)
@verbose_option()
def stockinfo(code, output, format, port):  # pylint: disable=redefined-builtin
    if (code, output) == (None, None):
        fail_with_usage()

    if output is None:
        if format is None:
            format = "md"
    else:
        if format is None:
            format = "xlsx"
        if format == "xlsx":
            if not output.endswith(".xlsx"):
                output += ".xlsx"
        elif format == "md":
            if not output.endswith(".md"):
                output += ".md"
        elif format == "json":
            if not output.endswith(".json"):
                output += ".json"

    import pandas as pd

    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEntrypoint import (
        KiwoomOpenApiPlusEntrypoint,
    )

    with KiwoomOpenApiPlusEntrypoint(port=port) as context:
        context.EnsureConnected()
        dic = context.GetStockBasicInfoAsDict(code)
        series = pd.Series(dic)

        if not output:
            if format == "md":
                click.echo(series.to_markdown())
            elif format == "json":
                click.echo(series.to_json())
        else:
            if format == "xlsx":
                series.to_excel(output, header=False)
            elif format == "json":
                with open(output, "w", encoding=default_encoding) as f:
                    click.echo(series.to_json(), file=f)
