import click

from koapy.cli.utils.verbose_option import verbose_option


def disable_auto_login_after_login(port):
    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEntrypoint import (
        KiwoomOpenApiPlusEntrypoint,
    )

    with KiwoomOpenApiPlusEntrypoint(port=port) as context:
        context.EnsureConnected()
        context.DisableAutoLogin()


def disable_auto_login_without_login():
    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin import (
        KiwoomOpenApiPlusQAxWidgetUniversalMixin,
    )
    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusTypeLibSpec import (
        API_MODULE_PATH,
    )

    class GetAPIModulePathStub:
        def GetAPIModulePath(self):
            return API_MODULE_PATH

    class DisableAutoLoginStub(
        GetAPIModulePathStub,
        KiwoomOpenApiPlusQAxWidgetUniversalMixin,
    ):
        pass

    stub = DisableAutoLoginStub()
    stub.DisableAutoLogin()


@click.command(short_help="Disable auto login.")
@click.option(
    "-p", "--port", metavar="PORT", help="Port number of grpc server (optional)."
)
@verbose_option(default=5, show_default=True)
def auto_login(port):
    disable_auto_login_without_login()
