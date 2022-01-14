import ast
import os

import pythoncom

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusOleItems import (
    DISPATCH_OLE_ITEM,
    EVENT_OLE_ITEM,
)


def generate_python():
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
    dispatch_class_name = "KiwoomOpenApiPlusDispatchFunctions"
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
    event_class_name = "KiwoomOpenApiPlusEventFunctions"
    event_class_def = ast.ClassDef(event_class_name, [], [], event_func_defs, [])

    script_dir = os.path.dirname(__file__)
    dispatch_functions_filename = os.path.join(
        script_dir, "..", dispatch_class_name + ".py"
    )
    event_functions_filename = os.path.join(script_dir, "..", event_class_name + ".py")

    try:
        from ast import unparse
    except ImportError:
        from astunparse import unparse

    with open(dispatch_functions_filename, "w", encoding="utf-8") as f:
        mod = ast.Module([dispatch_class_def], [])
        code = unparse(mod)
        f.write(code)

    with open(event_functions_filename, "w", encoding="utf-8") as f:
        mod = ast.Module([event_class_def], [])
        code = unparse(mod)
        f.write(code)


if __name__ == "__main__":
    generate_python()
