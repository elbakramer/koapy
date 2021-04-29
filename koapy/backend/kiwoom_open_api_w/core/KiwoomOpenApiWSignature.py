from collections import OrderedDict
from inspect import Parameter, Signature

import pythoncom
from win32com.client import genpy, selecttlb

from koapy.compat.pyside2.QtCore import SIGNAL


def BuildOleItems(clsid):
    tlbs = selecttlb.EnumTlbs()
    tlbs = {tlb.clsid: tlb for tlb in tlbs}

    tlbSpec = tlbs.get(clsid)

    if tlbSpec is None:
        return {}  # raise LookupError('KHOpenAPI Module not found')

    if tlbSpec.dll is None:
        tlb = pythoncom.LoadRegTypeLib(
            tlbSpec.clsid, int(tlbSpec.major, 16), int(tlbSpec.minor, 16), tlbSpec.lcid
        )
    else:
        tlb = pythoncom.LoadTypeLib(tlbSpec.dll)

    gen = genpy.Generator(tlb, tlbSpec.dll, None, bBuildHidden=1)
    oleItems, _enumItems, _recordItems, _vtableItems = gen.BuildOleItemsFromType()

    oleItems = {str(clsId): oleItem for clsId, oleItem in oleItems.items()}

    return oleItems


class KiwoomOpenApiWSignature(Signature):

    MODULE_CLSID = "{1F8A15ED-A979-488F-9694-1EDA98188FFC}"

    OLE_ITEMS = BuildOleItems(MODULE_CLSID)

    DISPATCH_CLSID = "{85B07632-4F84-4CEF-991D-C79DE781363D}"
    EVENT_CLSID = "{952B31F8-06FD-4D5A-A021-5FF57F5030AE}"

    PYTHONTYPE_TO_QTTYPE = {
        int: "int",
        str: "const QString&",
    }

    COMTYPE_TO_PYTHONTYPE = {
        pythoncom.VT_I4: int,
        pythoncom.VT_BSTR: str,
        pythoncom.VT_VARIANT: type(
            None
        ),  # QVariant does not exist in PySide2 (Currently PyQt5 only)
        pythoncom.VT_VOID: type(None),
    }

    def __init__(
        self, name, parameters=None, return_annotation=Signature.empty, entry=None
    ):
        self._name = name
        self._entry = entry
        super().__init__(parameters, return_annotation=return_annotation)

    @property
    def name(self):
        return self._name

    @classmethod
    def _pythontype_to_qttype(cls, typ):
        return cls.PYTHONTYPE_TO_QTTYPE[typ]

    def to_pyside2_function_prototype(self):
        name = self._name
        parameters = self.parameters
        parameters = parameters.values()
        parameters = [self._pythontype_to_qttype(p.annotation) for p in parameters]
        prototype = "%s(%s)" % (name, ", ".join(parameters))
        return prototype

    def to_pyside2_event_signal(self):
        return SIGNAL(self.to_pyside2_function_prototype())

    @classmethod
    def _comtype_to_pythontype(cls, typ):
        return cls.COMTYPE_TO_PYTHONTYPE[typ]

    @classmethod
    def _from_entry(cls, name, entry):
        arg_names = entry.names[1:]
        arg_types = [typ[0] for typ in entry.desc[2]]
        return_type = entry.desc[8][0]
        parameters = [
            Parameter(
                name=arg_name,
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                annotation=cls._comtype_to_pythontype(arg_type),
            )
            for arg_name, arg_type in zip(arg_names, arg_types)
        ]
        return_annotation = cls._comtype_to_pythontype(return_type)
        signature = cls(
            name=name,
            parameters=parameters,
            return_annotation=return_annotation,
            entry=entry,
        )
        return signature


class KiwoomOpenApiWDispatchSignature(KiwoomOpenApiWSignature):

    DISPATCH_SIGNATURES_BY_NAME = {}

    @classmethod
    def from_name(cls, name):
        return cls.DISPATCH_SIGNATURES_BY_NAME[name]

    @classmethod
    def names(cls):
        return list(cls.DISPATCH_SIGNATURES_BY_NAME.keys())


def LoadDispatchSignatures(oleItems, clsId):
    if clsId not in oleItems:
        return {}
    dispatch = oleItems[clsId]
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
        signature = KiwoomOpenApiWDispatchSignature._from_entry(
            func_name, entry
        )  # pylint: disable=protected-access
        dispatch_signatures_by_name[func_name] = signature
    return dispatch_signatures_by_name


KiwoomOpenApiWDispatchSignature.DISPATCH_SIGNATURES_BY_NAME = LoadDispatchSignatures(
    KiwoomOpenApiWSignature.OLE_ITEMS, KiwoomOpenApiWSignature.DISPATCH_CLSID
)


class KiwoomOpenApiWEventHandlerSignature(KiwoomOpenApiWSignature):

    EVENT_HANDLER_SIGNATURES_BY_NAME = {}

    @classmethod
    def from_name(cls, name):
        return cls.EVENT_HANDLER_SIGNATURES_BY_NAME[name]

    @classmethod
    def names(cls):
        return list(cls.EVENT_HANDLER_SIGNATURES_BY_NAME.keys())


def LoadEventHandlerSignatures(oleItems, clsId):
    if clsId not in oleItems:
        return {}
    event = oleItems[clsId]
    event_funcs = event.mapFuncs.items()
    event_handler_signatures_by_name = OrderedDict()
    for func_name, entry in event_funcs:
        signature = KiwoomOpenApiWEventHandlerSignature._from_entry(
            func_name, entry
        )  # pylint: disable=protected-access
        event_handler_signatures_by_name[func_name] = signature
    return event_handler_signatures_by_name


KiwoomOpenApiWEventHandlerSignature.EVENT_HANDLER_SIGNATURES_BY_NAME = (
    LoadEventHandlerSignatures(
        KiwoomOpenApiWSignature.OLE_ITEMS, KiwoomOpenApiWSignature.EVENT_CLSID
    )
)
