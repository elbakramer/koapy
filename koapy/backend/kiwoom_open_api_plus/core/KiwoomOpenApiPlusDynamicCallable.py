from inspect import Signature

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignature import (
    KiwoomOpenApiPlusDispatchSignature,
)


class KiwoomOpenApiPlusDynamicCallable:
    def __init__(self, control, name):
        self._control = control
        self._name = name
        self._signature = KiwoomOpenApiPlusDispatchSignature.from_name(self._name)
        self._function = self._signature.to_pyside2_function_prototype()
        self._should_test_return_type = (
            self._signature.return_annotation is not Signature.empty
        )

        self.__name__ = self._name

    def is_valid_return_type(self, result):
        if self._should_test_return_type and not isinstance(
            result, self._signature.return_annotation
        ):
            return False
        return True

    def call(self, *args, **kwargs):
        try:
            ba = self._signature.bind(*args, **kwargs)
        except TypeError as e:
            raise TypeError(
                "Exception while binding arguments for function: %s" % self._name
            ) from e
        ba.apply_defaults()
        result = self._control.dynamicCall(self._function, list(ba.args))
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

    def __call__(self, *args, **kwargs):
        return self.call(*args, **kwargs)
