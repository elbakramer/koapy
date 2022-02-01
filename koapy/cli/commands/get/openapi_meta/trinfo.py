import click

from koapy.cli.utils.verbose_option import verbose_option


@click.command(short_help="Get TR info.")
@click.option(
    "-t",
    "--trcode",
    "trcodes",
    metavar="TRCODE",
    multiple=True,
    help="TR code to get (like opt10001).",
)
@verbose_option()
def trinfo(trcodes):
    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusTrInfo import (
        KiwoomOpenApiPlusTrInfo,
    )

    def get_codes():
        if trcodes:
            if "-" in trcodes:
                with click.open_file("-", "r") as f:
                    for code in f:
                        yield code.strip()
            else:
                for code in trcodes:
                    yield code
        else:
            while True:
                try:
                    code = click.prompt("trcode", prompt_suffix=" >>> ")
                    code = code.strip()
                    if code == "exit":
                        break
                    if code:
                        yield code
                except EOFError:
                    break

    for trcode in get_codes():
        tr_info = KiwoomOpenApiPlusTrInfo.get_trinfo_by_code(trcode)
        if tr_info is not None:
            click.echo("[{}] : [{}]".format(tr_info.tr_code.upper(), tr_info.name))
            click.echo("  [INPUT]")
            for tr_input in tr_info.inputs:
                click.echo("    %s" % tr_input.name)
            if tr_info.single_outputs:
                click.echo(
                    "  [OUTPUT] [SINGLE DATA] : [%s]" % tr_info.single_outputs_name
                )
                for output in tr_info.single_outputs:
                    click.echo("    %s" % output.name)
            if tr_info.multi_outputs:
                click.echo(
                    "  [OUTPUT] [MULTI DATA]  : [%s]" % tr_info.multi_outputs_name
                )
                for output in tr_info.multi_outputs:
                    click.echo("    %s" % output.name)
        else:
            click.echo("Given trcode is invalid")
