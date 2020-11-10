import os
import pickle
import pythoncom

from inspect import Signature, Parameter
from collections import OrderedDict

from win32com.client import selecttlb, genpy

def comtype_to_pythontype(comtype):
    return {
        pythoncom.VT_I4: int,
        pythoncom.VT_BSTR: str,
        pythoncom.VT_VARIANT: type(None), # QVariant does'nt exist in PySide2
        pythoncom.VT_VOID: type(None),
    }[comtype]

def pythontype_to_qtproperty(pythontype):
    return {
        int: 'int',
        str: 'const QString&',
    }[pythontype]

def qt_function_spec_from_signature(name, signature):
    return '%s(%s)' % (name, ', '.join([pythontype_to_qtproperty(p.annotation) for p in signature.parameters.values()]))

def signature_from_entry(entry):
    arg_names = entry.names[1:]
    arg_types = [typ[0] for typ in entry.desc[2]]
    return_type = entry.desc[8][0]
    parameters = [
        Parameter(
            name=name,
            kind=Parameter.POSITIONAL_OR_KEYWORD,
            annotation=comtype_to_pythontype(typ),
        ) for name, typ in zip(arg_names, arg_types)
    ]
    return_annotation = comtype_to_pythontype(return_type)
    signature = Signature(
        parameters=parameters,
        return_annotation=return_annotation,
    )
    return signature

module_clsid = '{6D8C2B4D-EF41-4750-8AD4-C299033833FB}'

data_dir = os.path.join(os.path.dirname(__file__), 'data')

dispatch_signatures_by_name_filename = 'dispatch_signatures_by_name.pkl'
dispatch_signatures_by_name_filepath = os.path.join(data_dir, dispatch_signatures_by_name_filename)

event_signatures_by_name_filename = 'event_signatures_by_name.pkl'
event_signatures_by_name_filepath = os.path.join(data_dir, event_signatures_by_name_filename)

def dump_signatures():
    tlbs = selecttlb.EnumTlbs()
    tlbs = {tlb.clsid: tlb for tlb in tlbs}

    tlbSpec = tlbs.get(module_clsid)

    if tlbSpec is None:
        raise LookupError('KHOpenAPI Module not found')

    if tlbSpec.dll is None:
        tlb = pythoncom.LoadRegTypeLib(tlbSpec.clsid, int(tlbSpec.major, 16), int(tlbSpec.minor, 16), tlbSpec.lcid)
    else:
        tlb = pythoncom.LoadTypeLib(tlbSpec.dll)

    gen = genpy.Generator(tlb, tlbSpec.dll, None, bBuildHidden=1)
    oleItems, _enumItems, _recordItems, _vtableItems = gen.BuildOleItemsFromType()

    items = [l for l in oleItems.values() if l is not None]
    items.sort()

    iteritems = iter(items)

    dispatch = next(iteritems, None)
    event = next(iteritems, None)

    if dispatch is None:
        raise LookupError('KHOpenAPI Dispatch not found')

    if event is None:
        raise LookupError('KHOpenAPI Event not found')

    dispatch_funcs = [(name, entry) for name, entry in dispatch.mapFuncs.items() if not any([
        entry.desc[9] & pythoncom.FUNCFLAG_FRESTRICTED and entry.desc[0] != pythoncom.DISPID_NEWENUM,
        entry.desc[3] != pythoncom.FUNC_DISPATCH,
        entry.desc[0] == pythoncom.DISPID_NEWENUM])]

    dispatch_signatures_by_name = OrderedDict() # pylint: disable=redefined-outer-name

    for func_name, entry in dispatch_funcs:
        signature = signature_from_entry(entry)
        dispatch_signatures_by_name[func_name] = signature

    event_funcs = event.mapFuncs.items()

    event_signatures_by_name = OrderedDict() # pylint: disable=redefined-outer-name

    for func_name, entry in event_funcs:
        signature = signature_from_entry(entry)
        event_signatures_by_name[func_name] = signature

    with open(dispatch_signatures_by_name_filepath, 'wb') as f:
        pickle.dump(dispatch_signatures_by_name, f)

    with open(event_signatures_by_name_filepath, 'wb') as f:
        pickle.dump(event_signatures_by_name, f)

dispatch_signatures_by_name = {}
event_signatures_by_name = {}

def load_signatures():
    global dispatch_signatures_by_name # pylint: disable=global-statement
    global event_signatures_by_name # pylint: disable=global-statement

    with open(dispatch_signatures_by_name_filepath, 'rb') as f:
        dispatch_signatures_by_name = pickle.load(f)

    with open(event_signatures_by_name_filepath, 'rb') as f:
        event_signatures_by_name = pickle.load(f)

def get_dispatch_signature_by_name(name):
    return dispatch_signatures_by_name[name]

def get_event_signature_by_name(name):
    return event_signatures_by_name[name]

load_signatures()

if __name__ == '__main__':
    dump_signatures()
