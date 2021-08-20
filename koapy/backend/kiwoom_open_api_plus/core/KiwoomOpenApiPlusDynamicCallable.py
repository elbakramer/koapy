from inspect import Signature
from queue import Queue

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignature import (
    KiwoomOpenApiPlusDispatchSignature,
)
from koapy.compat.pyside2.QtCore import QObject, Qt, Signal


class KiwoomOpenApiPlusDynamicCallable(QObject):

    ready_call = Signal(list)

    def __init__(self, control, name, parent=None):
        super().__init__(parent)

        self._control = control
        self._name = name

        self._signature = KiwoomOpenApiPlusDispatchSignature.from_name(self._name)
        self._function = self._signature.to_pyside2_function_prototype()
        self._has_return_value = (
            self._signature.return_annotation is not Signature.empty
        )

        self._result_queue = Queue()
        self.ready_call.connect(self.on_ready_call, Qt.QueuedConnection)

        def SetRealRemove(screen_no, code):
            return self.queued_call(screen_no, code)

        def CommRqData(rqname, trcode, prevnext, screen_no):
            if prevnext:
                return self.call(rqname, trcode, prevnext, screen_no)
            else:
                return self.queued_call(rqname, trcode, prevnext, screen_no)

        self._custom_calls = {
            "SetRealRemove": SetRealRemove,
            "CommRqData": CommRqData,
        }

        self._call = self._custom_calls.get(self._name, self.call)

        self.__name__ = self._name

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

    def call(self, *args, **kwargs):
        args = self.bind_dynamic_call_args(*args, **kwargs)
        result = self._control.dynamicCall(self._function, args)
        self.check_return_value(result)
        return result

    def queued_call(self, *args, **kwargs):
        args = self.bind_dynamic_call_args(*args, **kwargs)
        self.ready_call.emit(args)
        result = self._result_queue.get()
        self._result_queue.task_done()
        return result

    def on_ready_call(self, args):
        result = self._control.dynamicCall(self._function, args)
        self.check_return_value(result)
        self._result_queue.put(result)

    def __call__(self, *args, **kwargs):
        return self._call(*args, **kwargs)
