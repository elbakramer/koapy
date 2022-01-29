from __future__ import annotations

from concurrent.futures import Future
from inspect import Signature
from typing import Any, Callable, Generic, List, Optional, Sequence, TypeVar

try:
    from typing import ParamSpec
except ImportError:
    from typing_extensions import ParamSpec

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusDispatchSignature import (
    KiwoomOpenApiPlusDispatchSignature,
)
from koapy.compat.pyside2.QtAxContainer import QAxWidget
from koapy.compat.pyside2.QtCore import QObject, Qt, Signal

P = ParamSpec("P")
R = TypeVar("R")


class KiwoomOpenApiPlusDynamicCallableRunnable:
    def __init__(
        self,
        future: Future,
        fn: Callable[..., Any],
        args: Sequence[Any],
    ):
        self._future = future
        self._fn = fn
        self._args = args

    def run(self):
        if not self._future.set_running_or_notify_cancel():
            return
        try:
            result = self._fn(self._args)
        except BaseException as exc:  # pylint: disable=broad-except
            self._future.set_exception(exc)
            # break a reference cycle with the exception 'exc'
            self = None  # pylint: disable=self-cls-assignment
        else:
            self._future.set_result(result)

    def cancel(self):
        return self._future.cancel()


class KiwoomOpenApiPlusDynamicCallable(QObject, Generic[P, R]):

    ready_runnable = Signal(KiwoomOpenApiPlusDynamicCallableRunnable)

    def __init__(
        self,
        control: QAxWidget,
        name: str,
        parent: Optional[QObject] = None,
    ):
        super().__init__(parent)

        self._control = control
        self._name = name

        self._signature = KiwoomOpenApiPlusDispatchSignature.from_name(self._name)
        self._function = self._signature.to_pyside2_function_prototype()
        self._has_return_value = (
            self._signature.return_annotation is not Signature.empty
        )

        self.ready_runnable.connect(self.on_ready_runnable, Qt.QueuedConnection)

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

    def async_call(self, *args: P.args, **kwargs: P.kwargs) -> Future:
        args = self.bind_dynamic_call_args(*args, **kwargs)
        future = Future()
        runnable = KiwoomOpenApiPlusDynamicCallableRunnable(
            future, self.dynamic_call_and_check, args
        )
        self.ready_runnable.emit(runnable)
        return future

    def on_ready_runnable(self, runnable: KiwoomOpenApiPlusDynamicCallableRunnable):
        runnable.run()

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        return self.call(*args, **kwargs)
