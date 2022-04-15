import click

from koapy.cli.utils.verbose_option import verbose_option


@click.command(short_help="Get OpenApi module installation path.")
@verbose_option()
def modulepath():
    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusTypeLibSpec import (
        API_MODULE_PATH,
    )

    click.echo(API_MODULE_PATH)
