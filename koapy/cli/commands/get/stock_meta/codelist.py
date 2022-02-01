import click

from koapy.cli.commands.get.stock_meta.codelist_interactive import codelist_interactive
from koapy.cli.utils.verbose_option import verbose_option

market_codes = [
    "0",
    "10",
    "3",
    "8",
    "50",
    "4",
    "5",
    "6",
    "9",
    "30",
    "all",
]


@click.command(short_help="Get stock codes.")
@click.option(
    "-m",
    "--market",
    "markets",
    metavar="MARKET",
    multiple=True,
    type=click.Choice(market_codes, case_sensitive=False),
    help="Stock market code to get. Can set multiple times.",
)
@click.option(
    "-p", "--port", metavar="PORT", help="Port number of grpc server (optional)."
)
@verbose_option()
def codelist(markets, port):
    """
    \b
    Possible market codes are:
      0 : 장내
      10 : 코스닥
      3 : ELW
      8 : ETF
      50 : KONEX
      4 : 뮤추얼펀드
      5 : 신주인수권
      6 : 리츠
      9 : 하이얼펀드
      30 : K-OTC
    """

    if not markets and click.get_text_stream("stdin").isatty():
        return codelist_interactive()

    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEntrypoint import (
        KiwoomOpenApiPlusEntrypoint,
    )

    with KiwoomOpenApiPlusEntrypoint(port=port) as context:
        context.EnsureConnected()
        codes = set()
        for market in markets:
            codes = codes.union(set(context.GetCodeListByMarketAsList(market)))
        codes = sorted(list(codes))
        for code in codes:
            click.echo(code)


def main():
    codelist()  # pylint: disable=no-value-for-parameter


if __name__ == "__main__":
    main()
