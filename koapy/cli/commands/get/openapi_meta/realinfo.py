import click

from koapy.cli.utils.verbose_option import verbose_option


@click.command(short_help="Get real type info.")
@click.option(
    "-t",
    "--realtype",
    "realtypes",
    metavar="REALTYPE",
    multiple=True,
    help="Real type name to get (like 주식시세).",
)
@verbose_option()
def realinfo(realtypes):
    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusRealType import (
        KiwoomOpenApiPlusRealType,
    )

    def get_realtypes():
        if realtypes:
            if "-" in realtypes:
                with click.open_file("-", "r") as f:
                    for realtype in f:
                        yield realtype.strip()
            else:
                for realtype in realtypes:
                    yield realtype
        else:
            while True:
                try:
                    realtype = click.prompt("realtype", prompt_suffix=" >>> ")
                    realtype = realtype.strip()
                    if realtype == "exit":
                        break
                    if realtype:
                        yield realtype
                except EOFError:
                    break

    for realtype in get_realtypes():
        fids = KiwoomOpenApiPlusRealType.get_fids_by_realtype_name(realtype)
        if fids:
            names = [
                KiwoomOpenApiPlusRealType.Fid.get_name_by_fid(fid, str(fid))
                for fid in fids
            ]
            for fid, name in zip(fids, names):
                click.echo("  [{}] = {}".format(fid, name))
        else:
            click.echo("Given realtype is invalid")
