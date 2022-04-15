import functools

from pathlib import Path

from deprecated import deprecated

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusTypeLibSpec import (
    API_MODULE_PATH,
)


@deprecated
@functools.lru_cache()
def GetAPIModulePath() -> Path:
    return API_MODULE_PATH


if __name__ == "__main__":
    print(GetAPIModulePath())
