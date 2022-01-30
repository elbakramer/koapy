import os
import shutil
import subprocess

import requests

from koapy.utils.logging import get_logger
from koapy.utils.subprocess import quote

logger = get_logger(__name__)

iss_file_encoding = "euc-kr"


def download_openapi_installer(filepath):
    url = "https://download.kiwoom.com/web/openapi/OpenAPISetup.exe"
    response = requests.get(url)
    with open(filepath, "wb") as f:
        f.write(response.content)


def prepare_issfile_for_install(filepath, target=None):
    iss_filedir = os.path.join(
        os.path.dirname(__file__),
        "../../backend/kiwoom_open_api_plus/data/scripts/",
    )
    iss_filename = "install.iss"
    iss_filepath = os.path.join(iss_filedir, iss_filename)
    shutil.copy(iss_filepath, filepath)
    if target is not None:
        with open(filepath, "r", encoding=iss_file_encoding) as f:
            lines = [line for line in f]
        for i, line in enumerate(lines):
            if line.startswith("szDir="):
                lines[i] = "szDir={}\n".format(target)
                break
        with open(filepath, "w", encoding=iss_file_encoding) as f:
            for line in lines:
                f.write(line)


def prepare_issfile_for_uninstall(filepath, reboot=False):
    iss_filedir = os.path.join(
        os.path.dirname(__file__),
        "../../backend/kiwoom_open_api_plus/data/scripts/",
    )
    iss_filename = "uninstall.iss"
    iss_filepath = os.path.join(iss_filedir, iss_filename)
    shutil.copy(iss_filepath, filepath)
    if reboot:
        with open(filepath, "r", encoding=iss_file_encoding) as f:
            lines = [line for line in f]
        for i, line in enumerate(lines):
            if line.startswith("BootOption="):
                boot_option = 3
                lines[i] = "BootOption={}\n".format(boot_option)
                break
        with open(filepath, "w", encoding=iss_file_encoding) as f:
            for line in lines:
                f.write(line)


def run_installer_with_issfile(installer, issfile, logfile=None, cwd=None):
    cmd = [quote(installer), "/s", "/f1{}".format(quote(issfile))]
    if logfile is not None:
        cmd.extend(["/f2{}".format(quote(logfile))])
    # should use shell=True in order not to escape quotes in args
    logger.info("Running command: %s", " ".join(cmd))
    proc = subprocess.run(" ".join(cmd), shell=True, check=False, cwd=cwd)
    if proc.returncode < 0:
        raise subprocess.CalledProcessError(proc.returncode, " ".join(cmd))
    return proc.returncode
