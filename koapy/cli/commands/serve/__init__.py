import sys

import click

from koapy.cli.utils.grpc_options import grpc_server_and_client_options
from koapy.cli.utils.verbose_option import full_verbose_option


@click.command(
    context_settings=dict(
        ignore_unknown_options=True,
    ),
    short_help="Start grpc server with tray application.",
)
@click.pass_context
@grpc_server_and_client_options()
@full_verbose_option()
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def serve(
    ctx,
    verbose,
    **kwargs,
):
    # reconstruct args so that only the first argument is program
    # and others are real arguments
    context_depth = 0
    c = ctx
    while c is not None:
        context_depth += 1
        c = c.parent
    args = sys.argv[:1] + sys.argv[context_depth:]

    # force verbosity of created applications to follow the cli option
    args.append("--verbose={}".format(verbose))

    # call main function of manager application with the prepared args
    from koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusManagerApplication import (
        KiwoomOpenApiPlusManagerApplication,
    )

    KiwoomOpenApiPlusManagerApplication.main(args)
