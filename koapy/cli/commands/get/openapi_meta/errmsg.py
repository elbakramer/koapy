import click

from koapy.cli.utils.fail_with_usage import fail_with_usage
from koapy.cli.utils.verbose_option import verbose_option


@click.command(short_help="Get error message for error code.")
@click.option("-e", "--err-code", metavar="ERR", type=int, help="Error code to check.")
@verbose_option()
def errmsg(err_code):
    if err_code is None:
        fail_with_usage()

    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError import (
        KiwoomOpenApiPlusError,
    )

    err_msg = KiwoomOpenApiPlusError.get_error_message_by_code(err_code)
    click.echo("[%d] %s" % (err_code, err_msg))
