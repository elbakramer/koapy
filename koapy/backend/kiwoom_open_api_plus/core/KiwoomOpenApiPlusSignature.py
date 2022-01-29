from inspect import Parameter, Signature
from typing import Dict

import pythoncom

from koapy.compat.pyside2 import PYSIDE2

if PYSIDE2:
    from koapy.compat.pyside2.QtCore import SIGNAL

try:
    from types import NoneType
except ImportError:
    NoneType = type(None)


class KiwoomOpenApiPlusSignature(Signature):

    PYTHONTYPE_TO_QTTYPE = {
        int: "int",
        str: "const QString&",
    }

    COMTYPE_TO_PYTHONTYPE = {
        pythoncom.VT_I4: int,
        pythoncom.VT_BSTR: str,
        pythoncom.VT_VARIANT: Parameter.empty,
        pythoncom.VT_VOID: NoneType,
    }

    def __init__(
        self,
        name: str,
        parameters: Dict[str, Parameter] = None,
        return_annotation=Signature.empty,
    ):
        self._name = name
        super().__init__(parameters, return_annotation=return_annotation)

    @property
    def name(self) -> str:
        return self._name

    @classmethod
    def _pythontype_to_qttype(cls, typ):
        return cls.PYTHONTYPE_TO_QTTYPE[typ]

    def to_pyside2_function_prototype(self) -> str:
        name = self._name
        parameters = self.parameters
        parameters = parameters.values()
        parameters = [self._pythontype_to_qttype(p.annotation) for p in parameters]
        prototype = "{}({})".format(name, ", ".join(parameters))
        return prototype

    if PYSIDE2:

        def to_pyside2_event_signal(self) -> str:
            return SIGNAL(self.to_pyside2_function_prototype())

    @classmethod
    def _comtype_to_pythontype(cls, typ):
        return cls.COMTYPE_TO_PYTHONTYPE.get(typ, Parameter.empty)

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
        )
        return signature
