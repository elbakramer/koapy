import contextlib
import os
import shutil
import subprocess
import tempfile

import click

from koapy.cli.utils import verbose_option
from koapy.cli.utils.openapi import (
    download_openapi_installer,
    prepare_issfile_for_uninstall,
    run_installer_with_issfile,
)
from koapy.utils.logging import get_logger

logger = get_logger(__name__)


@click.command(short_help="Uninstall openapi module.")
@click.option(
    "--reboot/--no-reboot",
    default=False,
    help="Reboot after uninstall. (default: false)",
)
@click.option(
    "--cleanup/--no-cleanup",
    default=True,
    help="Clean up temporary directory after uninstall. (default: true)",
)
@verbose_option(default=5)
def openapi(reboot, cleanup, verbose):
    with contextlib.ExitStack() as stack:
        tempdir = tempfile.mkdtemp()
        logger.info("Created temporary directory: %s", tempdir)
        if cleanup:
            stack.callback(shutil.rmtree, tempdir)
            logger.info("Registered to remove the temporary directory after uninstall.")
        installer_filename = "OpenAPISetup.exe"
        installer_filepath = os.path.join(tempdir, installer_filename)
        logger.info("Downloading installer: %s", installer_filepath)
        download_openapi_installer(installer_filepath)
        iss_filename = "setup.iss"
        iss_filepath = os.path.join(tempdir, iss_filename)
        logger.info("Preparing .iss file: %s", iss_filepath)
        prepare_issfile_for_uninstall(iss_filepath, reboot)
        log_filename = "setup.log"
        log_filepath = os.path.join(tempdir, log_filename)
        try:
            return_code = run_installer_with_issfile(
                installer_filepath, iss_filepath, log_filepath, cwd=tempdir
            )
        except subprocess.CalledProcessError as e:
            logger.exception(
                "Failed to uninstall openapi with return code: %d", e.returncode
            )
            raise RuntimeError(
                "Failed to uninstall openapi with return code: %d" % e.returncode
            ) from e
        else:
            logger.info("Succesfully uninstalled openapi.")
