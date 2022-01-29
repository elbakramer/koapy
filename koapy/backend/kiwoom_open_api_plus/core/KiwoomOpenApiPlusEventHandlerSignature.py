from __future__ import annotations

from typing import Dict, List

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEventFunctions import (
    KiwoomOpenApiPlusEventFunctions,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignature import (
    KiwoomOpenApiPlusSignature,
)
from koapy.utils.builtin import dir_public


class KiwoomOpenApiPlusEventHandlerSignature(KiwoomOpenApiPlusSignature):

    EVENT_HANDLER_SIGNATURES_BY_NAME: Dict[
        str, KiwoomOpenApiPlusEventHandlerSignature
    ] = {}

    @classmethod
    def from_name(cls, name: str) -> KiwoomOpenApiPlusEventHandlerSignature:
        signature = cls.EVENT_HANDLER_SIGNATURES_BY_NAME[name]
        return signature

    @classmethod
    def names(cls) -> List[str]:
        names = cls.EVENT_HANDLER_SIGNATURES_BY_NAME.keys()
        names = list(names)
        if not names:
            _names = dir_public(KiwoomOpenApiPlusEventFunctions)
        return names

    @classmethod
    def _make_event_handler_signatures_by_name(
        cls,
    ) -> Dict[str, KiwoomOpenApiPlusEventHandlerSignature]:
        from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusOleItems import (
            EVENT_OLE_ITEM,
        )

        event = EVENT_OLE_ITEM
        event_handler_signatures_by_name: Dict[
            str, KiwoomOpenApiPlusEventHandlerSignature
        ] = {}
        if event:
            event_funcs = event.mapFuncs.items()
            event_handler_signatures_by_name = {}
            for func_name, entry in event_funcs:
                signature = cls._from_entry(func_name, entry)
                event_handler_signatures_by_name[func_name] = signature
        return event_handler_signatures_by_name

    @classmethod
    def _initialize(cls):
        cls.EVENT_HANDLER_SIGNATURES_BY_NAME = (
            cls._make_event_handler_signatures_by_name()
        )


KiwoomOpenApiPlusEventHandlerSignature._initialize()  # pylint: disable=protected-access
