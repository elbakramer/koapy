"""Top-level package for KOAPY."""

__author__ = """Yunseong Hwang"""
__email__ = "kika1492@gmail.com"
__version__ = "0.6.2"

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from koapy.backend.daishin_cybos_plus.core.CybosPlusEntrypoint import (
        CybosPlusEntrypoint,
    )
    from koapy.backend.daishin_cybos_plus.core.CybosPlusError import (
        CybosPlusError,
        CybosPlusRequestError,
    )
    from koapy.backend.daishin_cybos_plus.proxy.CybosPlusEntrypointProxy import (
        CybosPlusEntrypointProxy,
    )
    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEntrypoint import (
        KiwoomOpenApiPlusEntrypoint,
    )
    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError import (
        KiwoomOpenApiPlusBooleanReturnCodeError,
        KiwoomOpenApiPlusError,
        KiwoomOpenApiPlusNegativeReturnCodeError,
    )
    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidget import (
        KiwoomOpenApiPlusQAxWidget,
    )
    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusRealType import (
        KiwoomOpenApiPlusRealType,
    )
    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusScreenManager import (
        KiwoomOpenApiPlusScreenManager,
    )
    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusTrInfo import (
        KiwoomOpenApiPlusTrInfo,
    )
    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusVersionUpdater import (
        KiwoomOpenApiPlusVersionUpdater,
    )
    from koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusManagerApplication import (
        KiwoomOpenApiPlusManagerApplication,
    )

__classes_to_export__ = {
    "koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEntrypoint": [
        "KiwoomOpenApiPlusEntrypoint"
    ],
    "koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidget": [
        "KiwoomOpenApiPlusQAxWidget"
    ],
    "koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusManagerApplication": [
        "KiwoomOpenApiPlusManagerApplication"
    ],
    "koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError": [
        "KiwoomOpenApiPlusError",
        "KiwoomOpenApiPlusNegativeReturnCodeError",
        "KiwoomOpenApiPlusBooleanReturnCodeError",
    ],
    "koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusTrInfo": [
        "KiwoomOpenApiPlusTrInfo"
    ],
    "koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusRealType": [
        "KiwoomOpenApiPlusRealType"
    ],
    "koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusScreenManager": [
        "KiwoomOpenApiPlusScreenManager"
    ],
    "koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusVersionUpdater": [
        "KiwoomOpenApiPlusVersionUpdater"
    ],
    "koapy.backend.daishin_cybos_plus.core.CybosPlusEntrypoint": [
        "CybosPlusEntrypoint"
    ],
    "koapy.backend.daishin_cybos_plus.core.CybosPlusError": [
        "CybosPlusError",
        "CybosPlusRequestError",
    ],
    "koapy.backend.daishin_cybos_plus.proxy.CybosPlusEntrypointProxy": [
        "CybosPlusEntrypointProxy"
    ],
}

__module_for_each_class_to_export__ = {
    name: module
    for module in __classes_to_export__
    for name in __classes_to_export__[module]
}

__all__ = [
    "KiwoomOpenApiPlusEntrypoint",
    "KiwoomOpenApiPlusQAxWidget",
    "KiwoomOpenApiPlusManagerApplication",
    "KiwoomOpenApiPlusError",
    "KiwoomOpenApiPlusNegativeReturnCodeError",
    "KiwoomOpenApiPlusBooleanReturnCodeError",
    "KiwoomOpenApiPlusTrInfo",
    "KiwoomOpenApiPlusRealType",
    "KiwoomOpenApiPlusScreenManager",
    "KiwoomOpenApiPlusVersionUpdater",
    "CybosPlusEntrypoint",
    "CybosPlusError",
    "CybosPlusRequestError",
    "CybosPlusEntrypointProxy",
]


# lazily import classes on attribute access
# https://www.python.org/dev/peps/pep-0562/
def __getattr__(name):
    if name in __all__:
        if name in __module_for_each_class_to_export__:
            module_name = __module_for_each_class_to_export__[name]
            import importlib

            module = importlib.import_module(module_name)
            return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
