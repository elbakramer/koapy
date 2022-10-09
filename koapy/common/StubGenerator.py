import ast
import datetime

import pythoncom

from pythoncom import ProgIDFromCLSID
from pythoncom import com_error as PythonComError
from pywintypes import TimeType
from win32com.client.build import MakePublicAttributeName
from win32com.client.genpy import MakeEventMethodName

from koapy.utils.pywin32 import BuildOleItems, GetLatestTypelibSpec

comtype_to_annotation = {
    pythoncom.VT_I2: int.__name__,
    pythoncom.VT_I4: int.__name__,
    pythoncom.VT_BOOL: bool.__name__,
    pythoncom.VT_R8: float.__name__,
    pythoncom.VT_BSTR: str.__name__,
    pythoncom.VT_VARIANT: "Any",
    pythoncom.VT_UNKNOWN: "Any",
    pythoncom.VT_VOID: "None",
}


def make_args(entry, set_defaults=False):
    fdesc = entry.desc
    names = entry.names
    num_args = len(fdesc[2])
    num_opt_args = fdesc[6]
    if num_opt_args == -1:
        num_args -= 1
    args = [ast.arg("self", None)]
    defaults = []
    for i in range(num_args):
        try:
            arg_name = names[i + 1]
            named_arg = arg_name is not None
        except IndexError:
            named_arg = False
        if not named_arg:
            arg_name = f"arg{i}"
        arg_name = MakePublicAttributeName(arg_name)
        arg_desc = fdesc[2][i]
        arg_type = arg_desc[0]
        arg_type = comtype_to_annotation[arg_type]
        arg_annotation = ast.Name(arg_type, ast.Load())
        arg = ast.arg(arg_name, arg_annotation)
        args.append(arg)
        try:
            arg_flag = arg_desc[1]
        except IndexError:
            arg_flag = pythoncom.PARAMFLAG_FIN
        if arg_flag & pythoncom.PARAMFLAG_FHASDEFAULT:
            arg_default = arg_desc[2]
            if isinstance(arg_default, datetime.datetime):
                arg_default = ast.Tuple(
                    [ast.Constant(v) for v in arg_default.utctimetuple()]
                )
            elif isinstance(arg_default, TimeType):
                arg_default = ast.Call(
                    ast.Name("Time", ast.Load()),
                    [
                        ast.Constant(arg_default.year),
                        ast.Constant(arg_default.month),
                        ast.Constant(arg_default.day),
                        ast.Constant(arg_default.hour),
                        ast.Constant(arg_default.minute),
                        ast.Constant(arg_default.second),
                        ast.Constant(0),
                        ast.Constant(0),
                        ast.Constant(0),
                        ast.Constant(arg_default.msec),
                    ],
                    [],
                )
            else:
                arg_default = ast.Constant(arg_default)
        else:
            arg_default = None
        if arg_default is None and set_defaults:
            if (
                arg_desc[1] & (pythoncom.PARAMFLAG_FOUT | pythoncom.PARAMFLAG_FIN)
                == pythoncom.PARAMFLAG_FOUT
            ):
                arg_default = ast.Name("Missing", ast.Load())
            else:
                arg_default = ast.Name("Empty", ast.Load())
        defaults.append(arg_default)
    if num_opt_args == -1:
        vararg = ast.arg(names[-1], None)
    else:
        vararg = None
    args = ast.arguments([], args, vararg, [], [], None, defaults)
    return args


def make_method(
    entry,
    name=None,
    is_getter=False,
    is_setter=False,
    is_event=False,
    is_handler=False,
):
    if not name:
        name = entry.names[0]
        if is_event or is_handler:
            make_method_name = MakeEventMethodName
        else:
            make_method_name = MakePublicAttributeName
        name = make_method_name(name)
    if is_setter:
        assert len(entry.desc.args) == 1
    elif is_getter:
        assert len(entry.desc.args) == 0
    if is_getter:
        args = [ast.arg("self", None)]
        args = ast.arguments([], args, None, [], [], None, [])
    elif is_setter:
        arg_type = entry.desc.args[0][0]
        arg_type = comtype_to_annotation[arg_type]
        args = [
            ast.arg("self", None),
            ast.arg(name, ast.Name(arg_type, ast.Load())),
        ]
        args = ast.arguments([], args, None, [], [], None, [])
    else:
        args = make_args(entry)
    ellipsis_body = [ast.Expr(ast.Constant(Ellipsis))]
    if is_event:
        is_getter = True
    if is_getter:
        decorator_list = [ast.Name("property", ast.Load())]
    elif is_setter:
        decorator_list = [
            ast.Attribute(ast.Name(name, ast.Load()), "setter", ast.Load())
        ]
    else:
        decorator_list = []
    if is_event:
        param_spec = ast.List([arg.annotation for arg in args.args[1:]], ast.Load())
        # cannot put [] in generic type args below version 3.10
        returns = ast.Subscript(
            ast.Name("EventInstance", ast.Load()),
            param_spec,
            ast.Load(),
        )
        # so just put without param spec
        returns = ast.Name("EventInstance", ast.Load())
        # and add callable typing
        callable_type = ast.Subscript(
            ast.Name("Callable", ast.Load()),
            ast.Tuple([param_spec, ast.Constant(None)], ast.Load()),
        )
        # with union
        returns = ast.Subscript(
            ast.Name("Union", ast.Load()),
            ast.Tuple([returns, callable_type], ast.Load()),
            ast.Load(),
        )
    else:
        if is_getter and is_setter:
            returns = ast.Name("Any", ast.Load())
        else:
            return_type = entry.GetResultName()
            if not return_type:
                return_type = entry.desc.rettype[0]
                return_type = comtype_to_annotation[return_type]
            returns = ast.Name(return_type, ast.Load())
            if name == "__iter__":
                returns = ast.Subscript(
                    ast.Name("Iterator", ast.Load()), returns, ast.Load()
                )
    func_def = ast.FunctionDef(name, args, ellipsis_body, decorator_list, returns)
    return func_def


def make_class_defs(ole_item):
    class_defs = []

    class_name = ole_item.python_name
    is_sink = ole_item.bIsSink

    class_body = []
    class_body_assigns = []

    clsid = ole_item.clsid
    clsid_assign = ast.Assign(
        [ast.Name("CLSID", ast.Store())],
        ast.Call(ast.Name("IID", ast.Load()), [ast.Constant(str(clsid))], []),
    )
    class_body_assigns.append(clsid_assign)

    try:
        progid = ProgIDFromCLSID(clsid)
    except PythonComError:
        progid = None

    if progid:
        progid_assign = ast.Assign(
            [ast.Name("PROGID", ast.Store())], ast.Constant(progid)
        )
        class_body_assigns.append(progid_assign)

    class_body.extend(class_body_assigns)

    if is_sink:
        class_name = class_name.lstrip("_")

    if hasattr(ole_item, "mapFuncs"):
        for name, entry in ole_item.mapFuncs.items():
            assert entry.desc.desckind == pythoncom.DESCKIND_FUNCDESC
            if (
                entry.desc.wFuncFlags & pythoncom.FUNCFLAG_FRESTRICTED
                and entry.desc.memid != pythoncom.DISPID_NEWENUM
            ):
                continue
            if entry.desc.funckind != pythoncom.FUNC_DISPATCH:
                continue
            if entry.hidden:
                continue
            if entry.desc.memid == pythoncom.DISPID_VALUE:
                name_lower = "value"
            elif entry.desc.memid == pythoncom.DISPID_NEWENUM:
                name_lower = "_newenum"
            else:
                name_lower = name.lower()
            if name_lower == "count":
                func_def = make_method(entry, "__len__")
            elif name_lower == "item":
                func_def = make_method(entry, "__getitem__")
            elif name_lower == "value":
                func_def = make_method(entry, "__call__")
            elif name_lower == "_newenum":
                func_def = make_method(entry, "__iter__")
            else:
                func_def = make_method(entry, is_event=is_sink)
            class_body.append(func_def)

    if hasattr(ole_item, "propMap"):
        for name, entry in ole_item.propMap.items():
            if entry.desc.memid == pythoncom.DISPID_VALUE:
                name_lower = "value"
            elif entry.desc.memid == pythoncom.DISPID_NEWENUM:
                name_lower = "_newenum"
            else:
                name_lower = name.lower()

            if name_lower == "count":
                func_def = make_method(entry, "__len__")
                class_body.append(func_def)
            elif name_lower == "item":
                func_def = make_method(entry, "__getitem__")
                class_body.append(func_def)
            elif name_lower == "value":
                func_def = make_method(entry, "__call__")
                class_body.append(func_def)
            elif name_lower == "_newenum":
                func_def = make_method(entry, "__iter__")
                class_body.append(func_def)
            else:
                func_def = make_method(entry, is_getter=True)
                class_body.append(func_def)

                func_def = make_method(entry, is_setter=True)
                class_body.append(func_def)

    if hasattr(ole_item, "propMapGet"):
        for name, entry in ole_item.propMapGet.items():
            if entry.desc.memid == pythoncom.DISPID_VALUE:
                name_lower = "value"
            elif entry.desc.memid == pythoncom.DISPID_NEWENUM:
                name_lower = "_newenum"
            else:
                name_lower = name.lower()

            if name_lower == "count":
                func_def = make_method(entry, "__len__")
            elif name_lower == "item":
                func_def = make_method(entry, "__getitem__")
            elif name_lower == "value":
                func_def = make_method(entry, "__call__")
            elif name_lower == "_newenum":
                func_def = make_method(entry, "__iter__")
            else:
                func_def = make_method(entry, is_getter=True)

            class_body.append(func_def)

    if hasattr(ole_item, "propMapPut"):
        for name, entry in ole_item.propMapPut.items():
            if name not in ole_item.propMap and name not in ole_item.propMapGet:
                func_def = make_method(entry, is_getter=True, is_setter=True)
                class_body.append(func_def)

            func_def = make_method(entry, is_setter=True)
            class_body.append(func_def)

    if not class_body:
        class_body = [ast.Expr(ast.Constant(Ellipsis))]

    class_bases = []

    if hasattr(ole_item, "interfaces"):
        class_bases_interfaces = [
            ast.Name(interface.python_name, ast.Load())
            for interface, flag in ole_item.interfaces
        ]
        class_bases.extend(class_bases_interfaces)

    if hasattr(ole_item, "sources"):
        class_bases_sources = [
            ast.Name(source.python_name.lstrip("_"), ast.Load())
            for source, flag in ole_item.sources
        ]
        class_bases.extend(class_bases_sources)

    class_def = ast.ClassDef(class_name, class_bases, [], class_body, [])
    class_defs.append(class_def)

    if is_sink:
        class_name += "Handler"

        class_body = []
        class_body.extend(class_body_assigns)

        if hasattr(ole_item, "mapFuncs"):
            for name, entry in ole_item.mapFuncs.items():
                assert entry.desc.desckind == pythoncom.DESCKIND_FUNCDESC
                if (
                    entry.desc.wFuncFlags & pythoncom.FUNCFLAG_FRESTRICTED
                    and entry.desc.memid != pythoncom.DISPID_NEWENUM
                ):
                    continue
                if entry.desc.funckind != pythoncom.FUNC_DISPATCH:
                    continue
                if entry.hidden:
                    continue
                if entry.desc.memid == pythoncom.DISPID_VALUE:
                    name_lower = "value"
                elif entry.desc.memid == pythoncom.DISPID_NEWENUM:
                    name_lower = "_newenum"
                else:
                    name_lower = name.lower()
                if name_lower == "count":
                    continue
                elif name_lower == "item":
                    continue
                elif name_lower == "value":
                    continue
                elif name_lower == "_newenum":
                    continue
                else:
                    func_def = make_method(entry, is_handler=is_sink)
                    class_body.append(func_def)

            class_def = ast.ClassDef(class_name, [], [], class_body, [])
            class_defs.append(class_def)

    return class_defs


def make_stub_module(clsid):
    spec = GetLatestTypelibSpec(clsid)
    ole_items, _, _, _ = BuildOleItems(spec)
    import_froms = [
        ast.ImportFrom("collections.abc", [ast.alias("Iterator")], 0),
        ast.ImportFrom(
            "typing", [ast.alias("Any"), ast.alias("Callable"), ast.alias("Union")], 0
        ),
        ast.ImportFrom("pythoncom", [ast.alias("Empty"), ast.alias("Missing")], 0),
        ast.ImportFrom("pywintypes", [ast.alias("IID"), ast.alias("Time")], 0),
        ast.ImportFrom("koapy.common", [ast.alias("EventInstance")], 0),
    ]
    class_defs = []
    for clsid, ole_item in ole_items.items():
        item_class_defs = make_class_defs(ole_item)
        class_defs.extend(item_class_defs)
    mod_body = import_froms + class_defs
    mod = ast.Module(mod_body, [])
    return mod
