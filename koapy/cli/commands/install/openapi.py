import contextlib
import os
import shutil
import subprocess
import tempfile

import click

from koapy.cli.utils import verbose_option
from koapy.cli.utils.openapi import (
    download_openapi_installer,
    prepare_issfile_for_install,
    run_installer_with_issfile,
)
from koapy.utils.logging import get_logger

logger = get_logger(__name__)


@click.command(short_help="Install openapi module.")
@click.option(
    "-t",
    "--target",
    metavar="TARGET",
    type=click.Path(),
    default="C:\\",
    help='Target directory for installation. Will create "OpenAPI" folder under this directory for install. (default: "C:\\")',
)
@click.option(
    "--cleanup/--no-cleanup",
    default=True,
    help="Clean up temporary directory after install. (default: true)",
)
@verbose_option(default=5)
def openapi(target, cleanup, verbose):
    with contextlib.ExitStack() as stack:
        tempdir = tempfile.mkdtemp()
        logger.info("Created temporary directory: %s", tempdir)
        if cleanup:
            stack.callback(shutil.rmtree, tempdir)
            logger.info("Registered to remove the temporary directory after install.")
        installer_filename = "OpenAPISetup.exe"
        installer_filepath = os.path.join(tempdir, installer_filename)
        logger.info("Downloading installer: %s", installer_filepath)
        download_openapi_installer(installer_filepath)
        iss_filename = "setup.iss"
        iss_filepath = os.path.join(tempdir, iss_filename)
        logger.info("Preparing .iss file: %s", iss_filepath)
        prepare_issfile_for_install(iss_filepath, target)
        log_filename = "setup.log"
        log_filepath = os.path.join(tempdir, log_filename)
        try:
            return_code = run_installer_with_issfile(
                installer_filepath, iss_filepath, log_filepath, cwd=tempdir
            )
        except subprocess.CalledProcessError as e:
            logger.exception(
                "Failed to install openapi with return code: %d", e.returncode
            )
            raise RuntimeError(
                "Failed to install openapi with return code: %d" % e.returncode
            ) from e
        else:
            logger.info("Succesfully installed openapi.")
