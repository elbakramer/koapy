from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusTypeLibSpec import (
    DISPATCH_CLSID,
    EVENT_CLSID,
    TYPELIB_SPEC,
)
from koapy.utils.pywin32 import BuildOleItems, LoadTypeLib

TYPELIB = LoadTypeLib(TYPELIB_SPEC)

OLE_ITEMS, ENUM_ITEMS, RECORD_ITEMS, VTABLE_ITEMS = BuildOleItems(TYPELIB_SPEC, TYPELIB)

DISPATCH_OLE_ITEM = OLE_ITEMS.get(DISPATCH_CLSID)
EVENT_OLE_ITEM = OLE_ITEMS.get(EVENT_CLSID)
