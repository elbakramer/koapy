import os
import subprocess
import sys
import tempfile

import requests

from koapy.utils.logging import get_logger

logger = get_logger(__name__)


def get_pywin32_postinstall_script(filepath):
    url = (
        "https://raw.githubusercontent.com/mhammond/pywin32/main/pywin32_postinstall.py"
    )
    response = requests.get(url)
    with open(filepath, "wb") as f:
        f.write(response.content)


def install_pywin32(version=None):
    if version is None:
        version = "302"
    cmd = ["pip", "install", "pywin32>={}".format(version)]
    logger.info("Running command: %s", subprocess.list2cmdline(cmd))
    subprocess.check_call(cmd)
    with tempfile.TemporaryDirectory() as tempdir:
        script_filename = "pywin32_postinstall.py"
        script_filepath = os.path.join(tempdir, script_filename)
        get_pywin32_postinstall_script(script_filepath)
        cmd = [sys.executable, script_filepath, "-install"]
        logger.info("Running command: %s", subprocess.list2cmdline(cmd))
        subprocess.check_call(cmd)


def uninstall_pywin32():
    with tempfile.TemporaryDirectory() as tempdir:
        script_filename = "pywin32_postinstall.py"
        script_filepath = os.path.join(tempdir, script_filename)
        get_pywin32_postinstall_script(script_filepath)
        cmd = [sys.executable, script_filepath, "-remove"]
        logger.info("Running command: %s", subprocess.list2cmdline(cmd))
        subprocess.check_call(cmd)
    cmd = ["pip", "uninstall", "pywin32"]
    logger.info("Running command: %s", subprocess.list2cmdline(cmd))
    subprocess.check_call(cmd)
