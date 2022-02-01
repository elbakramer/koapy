"""Console script for koapy."""

import os

import click

from koapy.cli.commands.configure import configure
from koapy.cli.commands.generate import generate
from koapy.cli.commands.get import get
from koapy.cli.commands.install import install
from koapy.cli.commands.serve import serve
from koapy.cli.commands.uninstall import uninstall
from koapy.cli.commands.update import update
from koapy.cli.utils.credentials import get_credentials
from koapy.cli.utils.fail_with_usage import fail_with_usage
from koapy.cli.utils.verbose_option import verbose_option
from koapy.config import default_encoding
from koapy.utils.logging import get_logger

logger = get_logger(__name__)

help_option_names = ["-h", "--help"]
context_settings = dict(
    help_option_names=help_option_names,
)


@click.group(context_settings=context_settings)
@click.version_option(message="%(version)s")
def cli():
    pass


cli.add_command(configure)
cli.add_command(generate)
cli.add_command(get)
cli.add_command(install)
cli.add_command(serve)
cli.add_command(uninstall)
cli.add_command(update)


@cli.command(short_help="Ensure logged in when server is up.")
@click.option(
    "-i",
    "--interactive",
    is_flag=True,
    help="Put login information with prompts. Disables auto login for manual login.",
)
@click.option(
    "-d",
    "--disable-auto-login",
    is_flag=True,
    help="Disable auto login and use credentials given explicitly from config file.",
)
@click.option(
    "-p", "--port", metavar="PORT", help="Port number of grpc server (optional)."
)
@verbose_option()
def login(interactive, disable_auto_login, port):
    credentials = get_credentials(interactive)

    from koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClient import (
        KiwoomOpenApiPlusServiceClient,
    )

    with KiwoomOpenApiPlusServiceClient(port=port, check_timeout=1) as context:
        state = context.GetConnectState()
        if state == 0:
            click.echo("Logging in...")
        else:
            click.echo("Already logged in.")
        if context.IsAutoLoginEnabled():
            if not disable_auto_login:
                credentials = None
        context.EnsureConnected(credentials)
        gubun = context.GetServerGubun()
        if gubun == "1":
            click.echo("Logged into Simulation server.")
        else:
            click.echo("Logged into Real server.")


@cli.command(short_help="Watch realtime data.")
@click.option(
    "-c",
    "--code",
    "codes",
    metavar="CODE",
    multiple=True,
    help="Stock code to get. Can set multiple times.",
)
@click.option(
    "-i",
    "--input",
    metavar="FILENAME",
    type=click.Path(),
    help="Text or excel file containing codes. Alternative to --code option.",
)
@click.option(
    "-f",
    "--fid",
    "fids",
    metavar="FID",
    multiple=True,
    help="FID to get. Can set multiple times.",
)
@click.option(
    "-t", "--realtype", metavar="REALTYPE", help="Real type name. Alternative to --fid."
)
@click.option(
    "-o",
    "--output",
    metavar="FILENAME",
    type=click.File("w", lazy=True),
    default="-",
    help="Output filename (optional).",
)
@click.option(
    "-f",
    "--format",
    metavar="FORMAT",
    type=click.Choice(["json", "md"], case_sensitive=False),
    default="json",
    help="Output format [json|md].",
)
@click.option(
    "-p", "--port", metavar="PORT", help="Port number of grpc server (optional)."
)
@verbose_option()
def watch(codes, input, fids, realtype, output, format, port):
    # pylint: disable=redefined-builtin

    if (codes, fids, realtype) == (tuple(), tuple(), None):
        fail_with_usage()

    codes_len = len(codes)

    if codes_len == 0:
        if input is None:
            fail_with_usage("Either code or input should be given.")
        if not os.path.exists(input):
            fail_with_usage("Given input does not exist.")

        if os.path.isfile(input):
            if input.endswith(".xlsx"):
                import pandas as pd

                df = pd.read_excel(input, dtype=str)
                code_column = "종목코드"
                if code_column in df:
                    codes = df[code_column]
                else:
                    codes = df.iloc[0]
                codes_len = len(codes)
            elif input.endswith(".txt"):
                with open(input, "r", encoding=default_encoding) as f:
                    codes = [line.strip() for line in f]
                codes_len = len(codes)
            else:
                fail_with_usage("Unrecognized input type.")
        else:
            fail_with_usage("Unrecognized input type.")

    if realtype is not None:
        from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusRealType import (
            KiwoomOpenApiPlusRealType,
        )

        fids_from_realtype = KiwoomOpenApiPlusRealType.get_fids_by_realtype_name(
            realtype
        )
        fids = list(set(fids).union(set(fids_from_realtype)))

    if not codes:
        fail_with_usage("No codes to watch. Set --code or --input.")

    if not fids:
        fail_with_usage("Cannot infer fids to watch. Set either --fid or --realtype.")

    import datetime

    import pandas as pd

    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEntrypoint import (
        KiwoomOpenApiPlusEntrypoint,
    )
    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusRealType import (
        KiwoomOpenApiPlusRealType,
    )

    def parse_message(message):
        fids = message.single_data.names
        names = [
            KiwoomOpenApiPlusRealType.Fid.get_name_by_fid(fid, str(fid)) for fid in fids
        ]
        values = message.single_data.values
        dic = {
            name: value for fid, name, value in zip(fids, names, values) if name != fid
        }
        series = pd.Series(dic)
        return series

    if format == "json":

        def print_message(message):
            click.echo(parse_message(message).to_json(), file=output)

    else:

        def print_message(message):
            code = message.arguments[0].string_value
            name = message.arguments[1].string_value
            click.echo("[{}] [{}]".format(code, name), file=output)
            click.echo("[%s]" % datetime.datetime.now(), file=output)
            click.echo(parse_message(message).to_markdown(), file=output)

    with KiwoomOpenApiPlusEntrypoint(port=port) as context:
        context.EnsureConnected()

        for event in context.GetRealDataForCodesAsStream(codes, fids, infer_fids=True):
            print_message(event)


order_types = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
]

quote_types = [
    "00",
    "03",
    "05",
    "06",
    "07",
    "10",
    "13",
    "16",
    "20",
    "23",
    "26",
    "61",
    "62",
    "81",
]


@cli.command(short_help="Place an order.")
@click.option("--request-name", metavar="NAME")
@click.option("--screen-no", metavar="SCRNO")
@click.option("--account-no", metavar="ACCNO")
@click.option("--order-type", type=click.Choice(order_types))
@click.option("--code", metavar="CODE")
@click.option("--quantity", metavar="QTY")
@click.option("--price", metavar="PRICE")
@click.option("--quote-type", type=click.Choice(quote_types))
@click.option("--original-order-no", metavar="ORDERNO")
@click.option(
    "-f",
    "--format",
    metavar="FORMAT",
    type=click.Choice(["pretty", "json"], case_sensitive=False),
)
@click.option(
    "-p", "--port", metavar="PORT", help="Port number of grpc server (optional)."
)
@verbose_option()
def order(
    request_name,
    screen_no,
    account_no,
    order_type,
    code,
    quantity,
    price,
    quote_type,
    original_order_no,
    format,
    port,
):
    # pylint: disable=redefined-builtin

    # TODO: 주문 취소시 기존 주문에 대한 이벤트 스트림 종료되도록

    """
    \b
    [주문유형]
      1 : 신규매수
      2 : 신규매도
      3 : 매수취소
      4 : 매도취소
      5 : 매수정정
      6 : 매도정정

    \b
    [거래구분]
      모의투자에서는 지정가 주문과 시장가 주문만 가능합니다.
      00 : 지정가
      03 : 시장가
      05 : 조건부지정가
      06 : 최유리지정가
      07 : 최우선지정가
      10 : 지정가IOC
      13 : 시장가IOC
      16 : 최유리IOC
      20 : 지정가FOK
      23 : 시장가FOK
      26 : 최유리FOK
      61 : 장전시간외종가
      62 : 시간외단일가매매
      81 : 장후시간외종가
    """

    if (request_name, screen_no, account_no, order_type, code, quantity) == (
        None,
        None,
        None,
        None,
        None,
        None,
    ):
        fail_with_usage()

    if order_type is None:
        fail_with_usage()

    from google.protobuf.json_format import MessageToDict

    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEntrypoint import (
        KiwoomOpenApiPlusEntrypoint,
    )

    if format == "json":
        import json

        def print_message(message):
            click.echo(json.dumps(MessageToDict(message)))

    else:
        import pprint

        pp = pprint.PrettyPrinter()

        def print_message(message):
            click.echo(pp.pformat(MessageToDict(message)))

    with KiwoomOpenApiPlusEntrypoint(port=port) as context:
        context.EnsureConnected()

        if order_type in ["3", "4"] and (account_no is None or code is None):
            for account_no_candidate in context.GetAccountList():
                df = context.GetOrderLogAsDataFrame1(account_no_candidate)
                if "주문번호" in df.columns:
                    rows = df.loc[df["주문번호"] == original_order_no, :]
                    if rows.shape[0] > 0:
                        row = rows.iloc[0, :]
                        if account_no is None:
                            account_no = row["계좌번호"]
                        if code is None:
                            code = row["종목코드"]
                        break

        if account_no is None:
            logger.info("Account not given. Using first account available.")
            account_no = context.GetFirstAvailableAccount()

        responses = context.OrderCall(
            request_name,
            screen_no,
            account_no,
            order_type,
            code,
            quantity,
            price,
            quote_type,
            original_order_no,
        )
        for response in responses:
            print_message(response)


def main():
    cli()


if __name__ == "__main__":
    main()
