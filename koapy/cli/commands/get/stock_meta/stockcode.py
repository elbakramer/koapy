import click

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
    "-n",
    "--name",
    "names",
    metavar="NAME",
    multiple=True,
    help="Name of stock. Can set multiple times.",
)
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
def stockcode(names, markets, port):
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

    markets_option = markets

    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEntrypoint import (
        KiwoomOpenApiPlusEntrypoint,
    )

    with KiwoomOpenApiPlusEntrypoint(port=port) as context:
        context.EnsureConnected()

        if not markets:
            markets = ["0"]

        codes = set()

        for market in markets:
            codes = codes.union(set(context.GetCodeListByMarketAsList(market)))

        codes = sorted(list(codes))

        if markets_option:
            for code in codes:
                click.echo(code)
        else:

            def get_names():
                if names:
                    if "-" in names:
                        with click.open_file("-", "r") as f:
                            for name in f:
                                yield name.strip()
                    else:
                        for name in names:
                            yield name
                else:
                    while True:
                        try:
                            name = click.prompt("name", prompt_suffix=" >>> ")
                            name = name.strip()
                            if name == "exit":
                                break
                            if name:
                                yield name
                        except EOFError:
                            break

            all_names = [context.GetMasterCodeName(code) for code in codes]
            codes_by_name = dict(zip(all_names, codes))

            for name in get_names():
                code = codes_by_name.get(name, None)
                if code:
                    click.echo(code)
                else:
                    click.echo("Cannot find code for given name: %s." % name)
