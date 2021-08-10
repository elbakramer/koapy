import click

from koapy.cli.utils import verbose_option
from koapy.cli.utils.credential import get_credential


@click.group(short_help="Update openapi module and metadata.")
def update():
    pass


@update.command(short_help="Update openapi TR metadata.")
@verbose_option()
def trinfo(verbose):
    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusTrInfo import (
        KiwoomOpenApiPlusTrInfo,
    )

    KiwoomOpenApiPlusTrInfo.dump_trinfo_by_code()


@update.command(short_help="Update openapi realtype metadata.")
@verbose_option()
def realtype(verbose):
    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusRealType import (
        KiwoomOpenApiPlusRealType,
    )

    KiwoomOpenApiPlusRealType.dump_realtype_by_desc()


@update.command(short_help="Update openapi module version.")
@click.option(
    "-i", "--interactive", is_flag=True, help="Put login information with prompts."
)
@verbose_option(default=5)
def openapi(interactive, verbose):
    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusVersionUpdater import (
        KiwoomOpenApiPlusVersionUpdater,
    )

    credential = get_credential(interactive)
    updater = KiwoomOpenApiPlusVersionUpdater(credential)
    updater.update_version_if_necessary()
