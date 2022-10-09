from typing import Dict, List, Optional, Sequence, Tuple, Union

try:
    from typing import TypeGuard
except ImportError:
    from typing_extensions import TypeGuard

from pythoncom import LoadRegTypeLib
from pythoncom import LoadTypeLib as LoadTypeLibFromDLL
from pywintypes import IIDType
from win32api import (
    ExpandEnvironmentStrings,
    RegOpenKey,
    RegQueryValue,
    RegQueryValueEx,
)
from win32api import error as Win32ApiError
from win32com.client.genpy import (
    DispatchItem,
    EnumerationItem,
    Generator,
    RecordItem,
    VTableItem,
)
from win32com.client.selecttlb import EnumKeys, TypelibSpec
from win32con import HKEY_CLASSES_ROOT, REG_EXPAND_SZ

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

    try:
        key = RegOpenKey(HKEY_CLASSES_ROOT, "TypeLib")
        key2 = RegOpenKey(key, str(iid))
    except Win32ApiError:
        enum_keys = []
    else:
        enum_keys = EnumKeys(key2)

    for version, tlbdesc in enum_keys:
        major_minor = version.split(".", 1)
        if len(major_minor) < 2:
            major_minor.append("0")
        major = major_minor[0]
        minor = major_minor[1]
        key3 = RegOpenKey(key2, str(version))
        try:
            flags = int(RegQueryValue(key3, "FLAGS"))
        except (Win32ApiError, ValueError):
            flags = 0
        for lcid, _ in EnumKeys(key3):
            try:
                lcid = int(lcid)
            except ValueError:
                continue
            try:
                key4 = RegOpenKey(key3, f"{lcid}\\win32")
            except Win32ApiError:
                try:
                    key4 = RegOpenKey(key3, f"{lcid}\\win64")
                except Win32ApiError:
                    continue
            try:
                dll, typ = RegQueryValueEx(key4, None)
                if typ == REG_EXPAND_SZ:
                    dll = ExpandEnvironmentStrings(dll)
            except Win32ApiError:
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
            tlb = LoadTypeLibFromDLL(spec.dll)
        else:
            tlb = LoadRegTypeLib(
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
    ole_items: Dict[PyIID, DispatchItem] = {}
    enum_items: Dict[PyIID, EnumerationItem] = {}
    record_items: Dict[PyIID, RecordItem] = {}
    vtable_items: Dict[PyIID, VTableItem] = {}

    if IsPyIIDLike(spec):
        spec = GetLatestTypelibSpec(spec)

    if spec:
        if not tlb:
            tlb = LoadTypeLib(spec)
        progress_instance = None
        gen = Generator(tlb, spec.dll, progress_instance, bBuildHidden=1)
        ole_items, enum_items, record_items, vtable_items = gen.BuildOleItemsFromType()

    return ole_items, enum_items, record_items, vtable_items
