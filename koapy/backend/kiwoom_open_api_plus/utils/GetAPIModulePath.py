import functools

from subprocess import CalledProcessError

from pyhocon.exceptions import ConfigMissingException

from koapy.utils.logging.Logging import Logging
from koapy.utils.platform import is_32bit, is_64bit

logger = Logging.get_logger()


def GetAPIModulePathFromConfig():
    logger.debug("Checking module path from config")
    from koapy.config import config

    APIModulePath = config.get("koapy.backend.kiwoom_open_api_plus.module_path")

    return APIModulePath


def GetAPIModulePathIn32Bit():
    logger.debug("Checking module path directly in 32bit")
    import sys

    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidget import (
        KiwoomOpenApiPlusQAxWidget,
    )
    from koapy.compat.pyside2.QtWidgets import QApplication

    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    control = KiwoomOpenApiPlusQAxWidget()

    APIModulePath = control.GetAPIModulePath()

    del control
    del app

    return APIModulePath


def GetAPIModulePathIn64Bit():
    logger.debug("Checking module path in-directly in 64bit")
    import subprocess
    import sys

    from koapy.utils.subprocess import function_to_subprocess_args, get_32bit_executable

    def main():
        from koapy.backend.kiwoom_open_api_plus.utils.GetAPIModulePath import (
            GetAPIModulePathIn32Bit,
        )

        APIModulePath = GetAPIModulePathIn32Bit()
        print(APIModulePath)

    executable_32bit = get_32bit_executable()
    cmd = function_to_subprocess_args(main, executable=executable_32bit)

    APIModulePath = subprocess.check_output(
        cmd,
        encoding=sys.stdout.encoding,
        creationflags=subprocess.CREATE_NO_WINDOW,
    ).strip()

    return APIModulePath


def GetAPIModulePathForDefaultInstallation():
    logger.debug("Giving module path based on default installation")
    return r"C:\OpenAPI"


@functools.lru_cache()
def GetAPIModulePath():
    # 1. use config if set explicitly
    try:
        return GetAPIModulePathFromConfig()
    except ConfigMissingException:
        pass

    # 2. directly check in 32bit environment
    if is_32bit():
        try:
            return GetAPIModulePathIn32Bit()
        except (CalledProcessError, FileNotFoundError):
            pass

    # 3. in-directly check in 64bit environment
    if is_64bit():
        try:
            return GetAPIModulePathIn64Bit()
        except (CalledProcessError, FileNotFoundError):
            pass

    # 4. fallback to default installation path
    return GetAPIModulePathForDefaultInstallation()


if __name__ == "__main__":
    print(GetAPIModulePath())
