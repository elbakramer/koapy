import click

from koapy.cli.utils.verbose_option import verbose_option


@click.command(short_help="Get user information.")
@click.option(
    "-p", "--port", metavar="PORT", help="Port number of grpc server (optional)."
)
@verbose_option()
def userinfo(port):
    import pandas as pd

    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEntrypoint import (
        KiwoomOpenApiPlusEntrypoint,
    )

    with KiwoomOpenApiPlusEntrypoint(port=port) as context:
        context.EnsureConnected()

        result = {}
        result["보유계좌수"] = context.GetLoginInfo("ACCOUNT_CNT")
        account_numbers = context.GetLoginInfo("ACCLIST").rstrip(";").split(";")
        for i, accno in enumerate(account_numbers):
            result["계좌번호 (%d/%s)" % (i + 1, result["보유계좌수"])] = accno
        result["사용자 ID"] = context.GetLoginInfo("USER_ID")
        result["사용자 명"] = context.GetLoginInfo("USER_NAME")
        result["키보드보안 해지 여부"] = {
            "0": "정상",
            "1": "해지",
        }.get(context.GetLoginInfo("KEY_BSECGB"), "알수없음")
        result["방화벽 설정 여부"] = {
            "0": "미설정",
            "1": "설정",
            "2": "해지",
        }.get(context.GetLoginInfo("FIREW_SECGB"), "알수없음")
        result["접속서버 구분"] = {
            "1": "모의투자",
        }.get(context.GetServerGubun(), "실서버")

        click.echo(pd.Series(result).to_markdown())
