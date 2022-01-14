from concurrent.futures import Future
from inspect import Signature
from typing import Any, Callable, List, Optional, Sequence, Tuple, Union

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusDispatchSignature import (
    KiwoomOpenApiPlusDispatchSignature,
)
from koapy.compat.pyside2.QtAxContainer import QAxWidget
from koapy.compat.pyside2.QtCore import QObject, Qt, Signal


class KiwoomOpenApiPlusDynamicCallableRunnable:
    def __init__(
        self,
        future: Future,
        fn: Callable[..., Any],
        args: Union[Tuple[Any], List[Any]],
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


class KiwoomOpenApiPlusDynamicCallable(QObject):

    readyRunnable = Signal(KiwoomOpenApiPlusDynamicCallableRunnable)

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

        self.readyRunnable.connect(self.onReadyRunnable, Qt.QueuedConnection)

        self.__name__ = self._name
        self.__signature__ = self._signature

    def bind_dynamic_call_args(self, *args, **kwargs):
        try:
            ba = self._signature.bind(*args, **kwargs)
        except TypeError as e:
            raise TypeError(
                "Exception while binding arguments for function: %s" % self._name
            ) from e
        ba.apply_defaults()
        args = list(ba.args)
        return args

    def is_valid_return_type(self, result):
        if self._has_return_value and not isinstance(
            result, self._signature.return_annotation
        ):
            return False
        return True

    def check_return_value(self, result):
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

    def dynamic_call(self, args: Sequence[Any]):
        return self._control.dynamicCall(self._function, args)

    def dynamic_call_and_check(self, args: Sequence[Any]):
        result = self.dynamic_call(args)
        self.check_return_value(result)
        return result

    def call(self, *args, **kwargs):
        args = self.bind_dynamic_call_args(*args, **kwargs)
        result = self.dynamic_call_and_check(args)
        return result

    def async_call(self, *args, **kwargs):
        args = self.bind_dynamic_call_args(*args, **kwargs)
        future = Future()
        runnable = KiwoomOpenApiPlusDynamicCallableRunnable(
            future, self.dynamic_call_and_check, args
        )
        self.readyRunnable.emit(runnable)
        return future

    def onReadyRunnable(self, runnable: KiwoomOpenApiPlusDynamicCallableRunnable):
        runnable.run()

    def __call__(self, *args, **kwargs):
        return self.call(*args, **kwargs)
