import pythoncom
import win32api
import win32con

from win32com.client import genpy
from win32com.client.selecttlb import EnumKeys, TypelibSpec


def GetTypelibSpecs(iid, error="raise"):
    assert error in ["raise", "coerce"]
    specs = []

    try:
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

    except:  # pylint: disable=bare-except
        if error == "raise":
            raise

    return specs


def GetTypelibSpec(iid, error="raise"):
    assert error in ["raise", "coerce"]
    spec = None

    try:
        specs = GetTypelibSpecs(iid, error)
        if len(specs) == 0:
            raise RuntimeError("No TypelibSpecs are found")
        if len(specs) > 1:
            raise RuntimeError("Unexpected number of TypelibSpecs are found")
        spec = specs[0]
    except:  # pylint: disable=bare-except
        if error == "raise":
            raise

    return spec


def LoadTypeLib(iid, error="raise"):
    assert error in ["raise", "coerce"]
    tlb, spec = None, None

    try:
        spec = GetTypelibSpec(iid, error)
        if spec.dll is None:
            tlb = pythoncom.LoadRegTypeLib(
                spec.clsid, spec.major, spec.minor, spec.lcid
            )
        else:
            tlb = pythoncom.LoadTypeLib(spec.dll)
    except:  # pylint: disable=bare-except
        if error == "raise":
            raise

    return tlb, spec


def BuildOleItems(iid, error="raise"):
    assert error in ["raise", "coerce"]
    oleItems, enumItems, recordItems, vtableItems = {}, {}, {}, {}

    try:
        tlb, spec = LoadTypeLib(iid, error)
        progressInstance = None
        gen = genpy.Generator(tlb, spec.dll, progressInstance, bBuildHidden=1)
        oleItems, enumItems, recordItems, vtableItems = gen.BuildOleItemsFromType()
    except:  # pylint: disable=bare-except
        if error == "raise":
            raise

    return oleItems, enumItems, recordItems, vtableItems
