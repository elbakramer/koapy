from inspect import Signature
from koapy.openapi.KiwoomOpenApiSignature import get_dispatch_signature_by_name, qt_function_spec_from_signature

class KiwoomOpenApiDynamicCallable:

    def __init__(self, control, name):
        self._control = control
        self._name = name
        self._signature = get_dispatch_signature_by_name(self._name)
        self._function = qt_function_spec_from_signature(self._name, self._signature)
        self._should_test_return_type = self._signature.return_annotation is not Signature.empty

    def is_valid_return_type(self, result):
        if self._should_test_return_type and not isinstance(result, self._signature.return_annotation):
            return False
        return True

    def __call__(self, *args, **kwargs):
        ba = self._signature.bind(*args, **kwargs)
        ba.apply_defaults()
        result = self._control.dynamicCall(self._function, list(ba.args))
        if not self.is_valid_return_type(result):
            raise TypeError('Return type %s expected for function call %s(), but %s found.' % (
                self._signature.return_annotation,
                self._name,
                type(result),
            ))
        return result
