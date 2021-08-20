import functools

from subprocess import CalledProcessError

from pyhocon.exceptions import ConfigMissingException

from koapy.config import debug
from koapy.utils.logging import get_logger
from koapy.utils.platform import is_32bit, is_64bit

logger = get_logger(__name__)


def GetAPIModulePathFromConfig():
    from koapy.config import config

    APIModulePath = config.get("koapy.backend.kiwoom_open_api_plus.module_path")

    return APIModulePath


def GetAPIModulePathFromServer():
    from koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClient import (
        KiwoomOpenApiPlusServiceClient,
    )

    with KiwoomOpenApiPlusServiceClient(check_timeout=1) as entrypoint:
        APIModulePath = entrypoint.GetAPIModulePath()

    return APIModulePath


def GetAPIModulePathIn32Bit():
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
    import subprocess
    import sys

    from koapy.config import get_32bit_executable
    from koapy.utils.subprocess import function_to_subprocess_args

    def main():
        from koapy.backend.kiwoom_open_api_plus.utils.module_path import (
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
    return r"C:\OpenAPI"


@functools.lru_cache()
def GetAPIModulePath():
    # 1. use config if set explicitly
    try:
        if debug:
            logger.debug("Checking module path from config")
        return GetAPIModulePathFromConfig()
    except ConfigMissingException:
        pass

    # 2. use server if exists
    try:
        if debug:
            logger.debug("Checking module path from existing server if applicable")
        return GetAPIModulePathFromServer()
    except AssertionError:
        pass

    # 3. directly check in 32bit environment
    if is_32bit():
        try:
            if debug:
                logger.debug("Checking module path directly in 32bit")
            return GetAPIModulePathIn32Bit()
        except (CalledProcessError, FileNotFoundError):
            pass

    # 4. in-directly check in 64bit environment
    if is_64bit():
        try:
            if debug:
                logger.debug("Checking module path in-directly in 64bit")
            return GetAPIModulePathIn64Bit()
        except (CalledProcessError, FileNotFoundError):
            pass

    # 5. fallback to default installation path
    if debug:
        logger.debug("Giving module path based on default installation")
    return GetAPIModulePathForDefaultInstallation()


if __name__ == "__main__":
    print(GetAPIModulePath())
