from __future__ import annotations

from collections import OrderedDict
from typing import Dict, List

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusOleItems import (
    EVENT_OLE_ITEM,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignature import (
    KiwoomOpenApiPlusSignature,
)


class KiwoomOpenApiPlusEventHandlerSignature(KiwoomOpenApiPlusSignature):

    EVENT_HANDLER_SIGNATURES_BY_NAME: dict[
        str, KiwoomOpenApiPlusEventHandlerSignature
    ] = {}

    @classmethod
    def from_name(cls, name: str) -> KiwoomOpenApiPlusEventHandlerSignature:
        return cls.EVENT_HANDLER_SIGNATURES_BY_NAME[name]

    @classmethod
    def names(cls) -> list[str]:
        return list(cls.EVENT_HANDLER_SIGNATURES_BY_NAME.keys())


def LoadEventHandlerSignatures():
    event = EVENT_OLE_ITEM
    if not event:
        return {}
    event_funcs = event.mapFuncs.items()
    event_handler_signatures_by_name = OrderedDict()
    for func_name, entry in event_funcs:
        # pylint: disable=protected-access
        signature = KiwoomOpenApiPlusEventHandlerSignature._from_entry(func_name, entry)
        event_handler_signatures_by_name[func_name] = signature
    return event_handler_signatures_by_name


KiwoomOpenApiPlusEventHandlerSignature.EVENT_HANDLER_SIGNATURES_BY_NAME = (
    LoadEventHandlerSignatures()
)
