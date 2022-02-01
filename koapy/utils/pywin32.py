from typing import Dict, List, Optional, Sequence, Tuple, Union

try:
    from typing import TypeGuard
except ImportError:
    from typing_extensions import TypeGuard

import pythoncom
import win32api
import win32con

from pywintypes import IIDType
from win32com.client.genpy import (
    DispatchItem,
    EnumerationItem,
    Generator,
    RecordItem,
    VTableItem,
)
from win32com.client.selecttlb import EnumKeys, TypelibSpec

PyIID = IIDType
PyITypeLib = "PyITypeLib"

PyIIDLike = Union[PyIID, str]


def IsPyIID(value) -> TypeGuard[PyIID]:
    return isinstance(value, IIDType)


def IsPyITypeLib(value) -> TypeGuard[PyITypeLib]:
    return type(value).__name__ == PyITypeLib


def IsPyIIDLike(value) -> TypeGuard[PyIIDLike]:
    return IsPyIID(value) or isinstance(value, str)


def GetTypelibSpecs(iid: PyIIDLike) -> List[TypelibSpec]:
    specs: List[TypelibSpec] = []

    key = win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT, "TypeLib")
    key2 = win32api.RegOpenKey(key, str(iid))

    for version, tlbdesc in EnumKeys(key2):
        major_minor = version.split(".", 1)
        if len(major_minor) < 2:
            major_minor.append("0")
        major = major_minor[0]
        minor = major_minor[1]
        key3 = win32api.RegOpenKey(key2, str(version))
        try:
            flags = int(win32api.RegQueryValue(key3, "FLAGS"))
        except (win32api.error, ValueError):
            flags = 0
        for lcid, _ in EnumKeys(key3):
            try:
                lcid = int(lcid)
            except ValueError:
                continue
            try:
                key4 = win32api.RegOpenKey(key3, "{}\\win32".format(lcid))
            except win32api.error:
                try:
                    key4 = win32api.RegOpenKey(key3, "{}\\win64".format(lcid))
                except win32api.error:
                    continue
            try:
                dll, typ = win32api.RegQueryValueEx(key4, None)
                if typ == win32con.REG_EXPAND_SZ:
                    dll = win32api.ExpandEnvironmentStrings(dll)
            except win32api.error:
                dll = None
            spec = TypelibSpec(iid, lcid, major, minor, flags)
            spec.dll = dll
            spec.desc = tlbdesc
            spec.ver_desc = tlbdesc + " (" + version + ")"
            specs.append(spec)

    return specs


def GetLatestTypelibSpec(
    specs: Union[Sequence[TypelibSpec], PyIIDLike]
) -> Optional[TypelibSpec]:
    spec: Optional[TypelibSpec] = None

    if IsPyIIDLike(specs):
        specs = GetTypelibSpecs(specs)

    if len(specs) > 0:
        specs = sorted(specs)
        spec = specs[-1]

    return spec


def LoadTypeLib(spec: Union[TypelibSpec, PyIIDLike]) -> Optional[PyITypeLib]:
    tlb: Optional[PyITypeLib] = None

    if IsPyIIDLike(spec):
        spec = GetLatestTypelibSpec(spec)

    if spec:
        if spec.dll:
            tlb = pythoncom.LoadTypeLib(spec.dll)
        else:
            tlb = pythoncom.LoadRegTypeLib(
                spec.clsid,
                spec.major,
                spec.minor,
                spec.lcid,
            )

    return tlb


def BuildOleItems(
    spec: Union[TypelibSpec, PyIIDLike],
    tlb: Optional[PyITypeLib] = None,
) -> Tuple[
    Dict[PyIID, DispatchItem],
    Dict[PyIID, EnumerationItem],
    Dict[PyIID, RecordItem],
    Dict[PyIID, VTableItem],
]:
    oleItems: Dict[PyIID, DispatchItem] = {}
    enumItems: Dict[PyIID, EnumerationItem] = {}
    recordItems: Dict[PyIID, RecordItem] = {}
    vtableItems: Dict[PyIID, VTableItem] = {}

    if IsPyIIDLike(spec):
        spec = GetLatestTypelibSpec(spec)

    if spec:
        if not tlb:
            tlb = LoadTypeLib(spec)
        progressInstance = None
        gen = Generator(tlb, spec.dll, progressInstance, bBuildHidden=1)
        oleItems, enumItems, recordItems, vtableItems = gen.BuildOleItemsFromType()

    return oleItems, enumItems, recordItems, vtableItems
