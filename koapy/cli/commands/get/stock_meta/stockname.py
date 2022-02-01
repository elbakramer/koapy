import click

from koapy.cli.utils.verbose_option import verbose_option


@click.command(short_help="Get name for stock codes.")
@click.option(
    "-c",
    "--code",
    "codes",
    metavar="CODE",
    multiple=True,
    help="Stock code to get. Can set multiple times.",
)
@click.option(
    "-p", "--port", metavar="PORT", help="Port number of grpc server (optional)."
)
@verbose_option()
def stockname(codes, port):
    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEntrypoint import (
        KiwoomOpenApiPlusEntrypoint,
    )

    with KiwoomOpenApiPlusEntrypoint(port=port) as context:
        context.EnsureConnected()

        def get_codes():
            if codes:
                if "-" in codes:
                    with click.open_file("-", "r") as f:
                        for code in f:
                            yield code.strip()
                else:
                    for code in codes:
                        yield code
            else:
                while True:
                    try:
                        code = click.prompt("code", prompt_suffix=" >>> ")
                        code = code.strip()
                        if code == "exit":
                            break
                        if code:
                            yield code
                    except EOFError:
                        break

        for code in get_codes():
            name = context.GetMasterCodeName(code)
            click.echo(name)
