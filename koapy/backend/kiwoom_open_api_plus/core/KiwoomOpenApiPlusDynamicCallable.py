from __future__ import annotations

from inspect import Signature
from typing import Any, Callable, List, Sequence

try:
    from typing import ParamSpec, TypeVar
except ImportError:
    from typing_extensions import ParamSpec
    from typing import TypeVar

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusDispatchSignature import (
    KiwoomOpenApiPlusDispatchSignature,
)
from koapy.compat.pyside2.QtAxContainer import QAxWidget

P = ParamSpec("P")
R = TypeVar("R")


class KiwoomOpenApiPlusDynamicCallable(Callable[P, R]):
    def __init__(
        self,
        control: QAxWidget,
        name: str,
    ):
        self._control = control
        self._name = name

        self._signature = KiwoomOpenApiPlusDispatchSignature.from_name(self._name)
        self._function = self._signature.to_pyside2_function_prototype()
        self._has_return_value = (
            self._signature.return_annotation is not Signature.empty
        )

        self.__name__ = self._name
        self.__signature__ = self._signature

    def bind_dynamic_call_args(self, *args, **kwargs) -> List[Any]:
        try:
            ba = self._signature.bind(*args, **kwargs)
        except TypeError as e:
            raise TypeError(
                "Exception while binding arguments for function: %s" % self._name
            ) from e
        ba.apply_defaults()
        args = list(ba.args)
        return args

    def is_valid_return_type(self, result: Any) -> bool:
        is_valid = True
        if self._has_return_value:
            if not isinstance(result, self._signature.return_annotation):
                is_valid = False
        return is_valid

    def check_return_value(self, result: Any):
        if not self.is_valid_return_type(result):
            raise TypeError(
                "Return type of %s was expected for function call %s(...), but %s was found"
                % (
                    self._signature.return_annotation,
                    self._name,
                    type(result),
                )
            )
        return result

    def dynamic_call(self, args: Sequence[Any]) -> R:
        return self._control.dynamicCall(self._function, args)

    def dynamic_call_and_check(self, args: Sequence[Any]) -> R:
        result = self.dynamic_call(args)
        self.check_return_value(result)
        return result

    def call(self, *args: P.args, **kwargs: P.kwargs) -> R:
        args = self.bind_dynamic_call_args(*args, **kwargs)
        result = self.dynamic_call_and_check(args)
        return result

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        return self.call(*args, **kwargs)
