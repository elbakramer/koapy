import click

from koapy.cli.utils.credentials import get_credentials
from koapy.cli.utils.verbose_option import verbose_option


@click.group(short_help="Update openapi module and metadata.")
def update():
    pass


@update.command(short_help="Update openapi TR metadata.")
@verbose_option()
def trinfo():
    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusTrInfo import (
        KiwoomOpenApiPlusTrInfo,
    )

    KiwoomOpenApiPlusTrInfo.dump_trinfo_by_code()


@update.command(short_help="Update openapi realtype metadata.")
@verbose_option()
def realtype():
    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusRealType import (
        KiwoomOpenApiPlusRealType,
    )

    KiwoomOpenApiPlusRealType.dump_realtype_by_desc()


@update.command(short_help="Update openapi module version.")
@click.option(
    "-i", "--interactive", is_flag=True, help="Put login information with prompts."
)
@verbose_option(default=5, show_default=True)
def openapi(interactive):
    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusVersionUpdater import (
        KiwoomOpenApiPlusVersionUpdater,
    )

    credentials = get_credentials(interactive)
    updater = KiwoomOpenApiPlusVersionUpdater(credentials)
    updater.update_version_if_necessary()


@update.command(short_help="Update gRPC stub files by compiling proto files.")
def proto():
    from koapy.backend.kiwoom_open_api_plus.grpc.tools.compile_proto import (
        compile_proto,
    )

    compile_proto()
