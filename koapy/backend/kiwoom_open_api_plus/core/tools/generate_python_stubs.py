import ast

from pathlib import Path

import pythoncom

from koapy.config import default_encoding

try:
    from ast import unparse
except ImportError:
    from astunparse import unparse


def generate_python_stubs(
    dispatch_class_name=None,
    dispatch_file_path=None,
    event_class_name=None,
    event_file_path=None,
    encoding=None,
    force_overwrite=False,
):
    if dispatch_class_name is None:
        dispatch_class_name = "KiwoomOpenApiPlusDispatchFunctionsGenerated"
    if dispatch_file_path is None:
        dispatch_file_path = dispatch_class_name + ".py"

    if event_class_name is None:
        event_class_name = "KiwoomOpenApiPlusEventFunctionsGenerated"
    if event_file_path is None:
        event_file_path = event_class_name + ".py"

    if encoding is None:
        encoding = default_encoding

    from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusTypeLib import (
        DISPATCH_OLE_ITEM,
        EVENT_OLE_ITEM,
    )
    dispatch_item = DISPATCH_OLE_ITEM
    event_item = EVENT_OLE_ITEM

    ellipsis_function_body = [ast.Expr(ast.Constant(Ellipsis))]
    comtype_to_annotation = {
        pythoncom.VT_I4: int.__name__,
        pythoncom.VT_BSTR: str.__name__,
        pythoncom.VT_VARIANT: str(None),
        pythoncom.VT_VOID: str(None),
    }

    dispatch_func_defs = []
    for _name, entry in dispatch_item.mapFuncs.items():
        func_name = entry.names[0]
        arg_names = entry.names[1:]
        arg_descs = entry.desc.args
        args = [ast.arg("self", None)]
        for arg_name, (arg_type, _arg_flag, _arg_default, _arg_crap) in zip(
            arg_names, arg_descs
        ):
            arg_type = comtype_to_annotation[arg_type]
            arg_annotation = ast.Name(arg_type, ast.Load())
            arg = ast.arg(arg_name, arg_annotation)
            arg.lineno = None
            arg.col_offset = None
            args.append(arg)
        args = ast.arguments([], args, None, [], [], None, [])
        return_type = entry.desc.rettype[0]
        return_type = comtype_to_annotation[return_type]
        returns = ast.Name(return_type, ast.Load())
        func_def = ast.FunctionDef(func_name, args, ellipsis_function_body, [], returns)
        func_def.lineno = None
        func_def.col_offset = None
        dispatch_func_defs.append(func_def)
    dispatch_class_def = ast.ClassDef(
        dispatch_class_name, [], [], dispatch_func_defs, []
    )

    event_func_defs = []
    for _name, entry in event_item.mapFuncs.items():
        func_name = entry.names[0]
        arg_names = entry.names[1:]
        arg_descs = entry.desc.args
        args = [ast.arg("self", None)]
        for arg_name, (arg_type, _arg_flag, _arg_default, _arg_crap) in zip(
            arg_names, arg_descs
        ):
            arg_type = comtype_to_annotation[arg_type]
            arg_annotation = ast.Name(arg_type, ast.Load())
            arg = ast.arg(arg_name, arg_annotation)
            arg.lineno = None
            arg.col_offset = None
            args.append(arg)
        args = ast.arguments([], args, None, [], [], None, [])
        return_type = entry.desc.rettype[0]
        return_type = comtype_to_annotation[return_type]
        returns = ast.Name(return_type, ast.Load())
        func_def = ast.FunctionDef(func_name, args, ellipsis_function_body, [], returns)
        func_def.lineno = None
        func_def.col_offset = None
        event_func_defs.append(func_def)

    event_class_def = ast.ClassDef(event_class_name, [], [], event_func_defs, [])

    dispatch_file_path = Path(dispatch_file_path)
    if not dispatch_file_path.exists() or force_overwrite:
        with open(dispatch_file_path, "w", encoding=encoding) as f:
            mod = ast.Module([dispatch_class_def], [])
            code = unparse(mod)
            f.write(code)

    event_file_path = Path(event_file_path)
    if not event_file_path.exists() or force_overwrite:
        with open(event_file_path, "w", encoding=encoding) as f:
            mod = ast.Module([event_class_def], [])
            code = unparse(mod)
            f.write(code)


if __name__ == "__main__":
    generate_python_stubs()
