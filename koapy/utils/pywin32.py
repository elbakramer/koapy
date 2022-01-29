from typing import Dict, List, Tuple, Union

import pythoncom
import win32api
import win32con

from win32com.client.genpy import (
    DispatchItem,
    EnumerationItem,
    Generator,
    RecordItem,
    VTableItem,
)
from win32com.client.selecttlb import EnumKeys, TypelibSpec

from koapy.utils.logging import get_logger

logger = get_logger(__name__)

PyIID = "PyIID"
PyITypeLib = "PyITypeLib"


def GetTypelibSpecs(iid: Union[PyIID, str]) -> List[TypelibSpec]:
    specs: List[TypelibSpec] = []

    key = win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT, "Typelib")
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


def GetTypelibSpec(iid: Union[PyIID, str]) -> TypelibSpec:
    specs = GetTypelibSpecs(iid)

    if len(specs) == 0:
        raise RuntimeError("No TypelibSpecs are found")
    if len(specs) > 1:
        raise RuntimeError("Unexpected number of TypelibSpecs are found")

    spec = specs[0]

    return spec


def LoadTypeLib(iid: Union[PyIID, str]) -> Tuple[PyITypeLib, TypelibSpec]:
    spec = GetTypelibSpec(iid)

    if spec.dll is None:
        tlb = pythoncom.LoadRegTypeLib(spec.clsid, spec.major, spec.minor, spec.lcid)
    else:
        tlb = pythoncom.LoadTypeLib(spec.dll)

    return tlb, spec


def BuildOleItems(
    iid: Union[PyIID, str]
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

    tlb, spec = LoadTypeLib(iid)
    progressInstance = None
    gen = Generator(tlb, spec.dll, progressInstance, bBuildHidden=1)
    oleItems, enumItems, recordItems, vtableItems = gen.BuildOleItemsFromType()

    return oleItems, enumItems, recordItems, vtableItems


def TryBuildOleItems(
    iid: Union[PyIID, str],
    error="coerce",
) -> Tuple[
    Dict[PyIID, DispatchItem],
    Dict[PyIID, EnumerationItem],
    Dict[PyIID, RecordItem],
    Dict[PyIID, VTableItem],
]:
    assert error in ["coerce", "raise"]

    oleItems: Dict[PyIID, DispatchItem] = {}
    enumItems: Dict[PyIID, EnumerationItem] = {}
    recordItems: Dict[PyIID, RecordItem] = {}
    vtableItems: Dict[PyIID, VTableItem] = {}

    try:
        oleItems, enumItems, recordItems, vtableItems = BuildOleItems(iid)
    except Exception as e:  # pylint: disable=broad-except
        if error == "raise":
            raise e
        else:
            logger.warning(e)

    return oleItems, enumItems, recordItems, vtableItems
