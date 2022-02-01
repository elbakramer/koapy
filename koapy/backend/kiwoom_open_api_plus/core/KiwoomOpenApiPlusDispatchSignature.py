from __future__ import annotations

from typing import Dict, List

import pythoncom

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusDispatchFunctions import (
    KiwoomOpenApiPlusDispatchFunctions,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignature import (
    KiwoomOpenApiPlusSignature,
)
from koapy.utils.builtin import dir_public


class KiwoomOpenApiPlusDispatchSignature(KiwoomOpenApiPlusSignature):

    DISPATCH_SIGNATURES_BY_NAME: Dict[str, KiwoomOpenApiPlusDispatchSignature] = {}

    @classmethod
    def from_name(cls, name: str) -> KiwoomOpenApiPlusDispatchSignature:
        signature = cls.DISPATCH_SIGNATURES_BY_NAME[name]
        return signature

    @classmethod
    def names(cls) -> List[str]:
        names = cls.DISPATCH_SIGNATURES_BY_NAME.keys()
        names = list(names)
        if not names:
            _names = dir_public(KiwoomOpenApiPlusDispatchFunctions)
        return names

    @classmethod
    def _make_dispatch_signatures_by_name(
        cls,
    ) -> Dict[str, KiwoomOpenApiPlusDispatchSignature]:
        from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusTypeLib import (
            DISPATCH_OLE_ITEM,
        )

        dispatch = DISPATCH_OLE_ITEM
        dispatch_signatures_by_name: Dict[str, KiwoomOpenApiPlusDispatchSignature] = {}
        if dispatch:
            dispatch_funcs = [
                (name, entry)
                for name, entry in dispatch.mapFuncs.items()
                if not any(
                    [
                        entry.desc[9] & pythoncom.FUNCFLAG_FRESTRICTED
                        and entry.desc[0] != pythoncom.DISPID_NEWENUM,
                        entry.desc[3] != pythoncom.FUNC_DISPATCH,
                        entry.desc[0] == pythoncom.DISPID_NEWENUM,
                    ]
                )
            ]
            for func_name, entry in dispatch_funcs:
                signature = cls._from_entry(func_name, entry)
                dispatch_signatures_by_name[func_name] = signature
        return dispatch_signatures_by_name

    @classmethod
    def _initialize(cls):
        cls.DISPATCH_SIGNATURES_BY_NAME = cls._make_dispatch_signatures_by_name()


KiwoomOpenApiPlusDispatchSignature._initialize()  # pylint: disable=protected-access
