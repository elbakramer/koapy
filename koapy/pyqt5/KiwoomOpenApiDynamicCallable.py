import logging

class KiwoomOpenApiDynamicCallable(object):

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
            return self._control.dynamicCall(function, list(args))
        else:
            return self._control.dynamicCall(function)

    def __call__(self, *args, **kwargs):
        return self._dynamicCall(*args, **kwargs)
