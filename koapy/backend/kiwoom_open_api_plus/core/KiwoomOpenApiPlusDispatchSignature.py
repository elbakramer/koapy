from __future__ import annotations

from collections import OrderedDict
from typing import Dict, List

import pythoncom

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusOleItems import (
    DISPATCH_OLE_ITEM,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignature import (
    KiwoomOpenApiPlusSignature,
)


class KiwoomOpenApiPlusDispatchSignature(KiwoomOpenApiPlusSignature):

    DISPATCH_SIGNATURES_BY_NAME: dict[str, KiwoomOpenApiPlusDispatchSignature] = {}

    @classmethod
    def from_name(cls, name: str) -> KiwoomOpenApiPlusDispatchSignature:
        return cls.DISPATCH_SIGNATURES_BY_NAME[name]

    @classmethod
    def names(cls) -> list[str]:
        return list(cls.DISPATCH_SIGNATURES_BY_NAME.keys())


def LoadDispatchSignatures():
    dispatch = DISPATCH_OLE_ITEM
    if not dispatch:
        return {}
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
    dispatch_signatures_by_name = OrderedDict()
    for func_name, entry in dispatch_funcs:
        # pylint: disable=protected-access
        signature = KiwoomOpenApiPlusDispatchSignature._from_entry(func_name, entry)
        dispatch_signatures_by_name[func_name] = signature
    return dispatch_signatures_by_name


KiwoomOpenApiPlusDispatchSignature.DISPATCH_SIGNATURES_BY_NAME = (
    LoadDispatchSignatures()
)
