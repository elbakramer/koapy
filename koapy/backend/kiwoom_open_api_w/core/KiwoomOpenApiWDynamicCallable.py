from inspect import Signature

from koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWSignature import (
    KiwoomOpenApiWDispatchSignature,
)


class KiwoomOpenApiWDynamicCallable:
    def __init__(self, control, name):
        self._control = control
        self._name = name
        self._signature = KiwoomOpenApiWDispatchSignature.from_name(self._name)
        self._function = self._signature.to_pyside2_function_prototype()
        self._should_test_return_type = (
            self._signature.return_annotation is not Signature.empty
        )

    def is_valid_return_type(self, result):
        if self._should_test_return_type and not isinstance(
            result, self._signature.return_annotation
        ):
            return False
        return True

    def __call__(self, *args, **kwargs):
        ba = self._signature.bind(*args, **kwargs)
        ba.apply_defaults()
        result = self._control.dynamicCall(self._function, list(ba.args))
        if not self.is_valid_return_type(result):
            raise TypeError(
                "Return type of %s was expected for function call %s(...), but %s was found."
                % (
                    self._signature.return_annotation,
                    self._name,
                    type(result),
                )
            )
        return result
