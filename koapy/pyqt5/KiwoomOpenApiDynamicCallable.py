import logging

class KiwoomOpenApiDynamicCallable:

    _void_method_names = [
        'SetInputValue',
        'DisconnectRealData',
        'SetRealRemove',
        'SetCondition',
        'SetConditionStop',
    ]

    def __init__(self, control, name):
        self._control = control
        self._name = name

    @classmethod
    def _getInputParameterType(cls, param):
        if isinstance(param, str):
            return 'const QString&'
        elif isinstance(param, int):
            return 'int' # giving 'long' breaks behavior of CommRqData()
        else:
            raise TypeError('Cannot recognize type for input param: %s' % type(param))

    @classmethod
    def _createDynamicCallFunction(cls, name, args):
        return '%s(%s)' % (name, ', '.join(map(cls._getInputParameterType, args)))

    def _staticCall(self, *args, **kwargs):
        return getattr(self._control, self._name)(*args, **kwargs)

    def _dynamicCall(self, *args, **kwargs):
        if kwargs:
            logging.warning('Ignoring given kwargs..')
        function = self._createDynamicCallFunction(self._name, args)
        # logging.debug('Calling dynamicCall(%r, %r)', function, args)
        if len(args) > 0:
            # giving args as tuple raises an error, ex) _.dynamicCall('...', args)
            # giving unpacked args has length limitation, ex) _.dynamicCall('...', *args)
            result = self._control.dynamicCall(function, list(args))
        else:
            result = self._control.dynamicCall(function)
        # 파라미터 개수가 틀리거나 타입이 틀리거나 같은 경우에 에러체킹이 안됨
        # 뾰족한 방법이 없어보여서 아래처럼 구현
        if result is None and self._name not in self._void_method_names:
            logging.error('Non-void method returned None.')
            raise ValueError('Non-void method returned None.')
        return result

    def __call__(self, *args, **kwargs):
        return self._dynamicCall(*args, **kwargs)
