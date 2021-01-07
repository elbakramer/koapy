import grpc
import logging

from koapy.backend.cybos import CybosPlusProxyService_pb2
from koapy.backend.cybos import CybosPlusProxyService_pb2_grpc

from koapy.backend.cybos.CybosPlusComObjectMixin import CybosPlusComObjectMixin
from koapy.backend.cybos.CybosPlusBlockRequestRateLimiter import CybosPlusBlockRequestRateLimiter
from koapy.backend.cybos.CybosPlusBlockRequestError import CybosPlusBlockRequestError
from koapy.backend.cybos.CybosPlusMessageUtils import AssignPrimitive, ExtractPrimitive

class CybosPlusComObjectDispatchProxyMethod:

    def __init__(self, proxy, name):
        self._proxy = proxy
        self._name = name

    def __call__(self, *args, **kwargs):
        return self._proxy._InvokeMethod(self._name, args)

class CybosPlusComObjectDispatchProxy:

    def __init__(self, proxy, prefix, suffix):
        self._proxy = proxy
        self._prefix = prefix
        self._suffix = suffix

        self._prog = '%s.%s' % (self._prefix, self._suffix)

        request = CybosPlusProxyService_pb2.DispatchRequest()
        request.prog = self._prog

        self._dispatch = self._proxy._stub.Dispatch(request)

    def _GetProperty(self, name):
        request = CybosPlusProxyService_pb2.PropertyRequest()
        request.prog = self._prog
        request.name = name
        should_stop = False
        while not should_stop:
            response_future = self._proxy._stub.Property.future(request, timeout=self._proxy._timeout)
            try:
                response = response_future.result()
            except grpc.RpcError:
                if response_future.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                    logging.warning('Property %s lookup failed, retrying...', name)
                else:
                    raise
            else:
                should_stop = True
        result = ExtractPrimitive(response.value)
        return result

    def _InvokeMethod(self, name, args):
        request = CybosPlusProxyService_pb2.MethodRequest()
        request.prog = self._prog
        request.name = name
        for arg in args:
            AssignPrimitive(request.arguments.add().value, arg) # pylint: disable=no-member
        should_stop = False
        while not should_stop:
            response_future = self._proxy._stub.Method.future(request, timeout=self._proxy._timeout)
            try:
                response = response_future.result()
            except grpc.RpcError:
                if response_future.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                    logging.warning('Method invocation %s(%s) timed out, retrying...', name, ', '.join(map(repr, args)))
                else:
                    raise
            else:
                should_stop = True
        result = ExtractPrimitive(response.return_value)
        return result

    def __getattr__(self, name):
        if name in self._dispatch.properties:
            return self._GetProperty(name)
        elif name in self._dispatch.methods:
            return CybosPlusComObjectDispatchProxyMethod(self, name)
        else:
            raise AttributeError

    @CybosPlusBlockRequestRateLimiter()
    def RateLimitedBlockRequest(self):
        return CybosPlusBlockRequestError.try_or_raise(
            self.BlockRequest()
        )

class CybosPlusComObjectInnerProxy:

    def __init__(self, proxy, prefix):
        self._proxy = proxy
        self._prefix = prefix

    def __getattr__(self, name):
        return CybosPlusComObjectDispatchProxy(self._proxy, self._prefix, name)

class CybosPlusComObjectProxy(CybosPlusComObjectMixin):

    def __init__(self, host=None, port=None):
        if host is None:
            host = 'localhost'
        if port is None:
            port = 3031

        self._host = host
        self._port = port

        self._address = self._host + ':' + str(self._port)
        self._channel = grpc.insecure_channel(self._address)
        self._stub = CybosPlusProxyService_pb2_grpc.CybosPlusProxyServiceStub(self._channel)

        self._timeout = 10

        grpc.channel_ready_future(self._channel).result(timeout=5)

    def __getattr__(self, name):
        if name.startswith('Cp') or name.startswith('Ds'):
            return CybosPlusComObjectInnerProxy(self, name)
        raise AttributeError

def main():
    proxy = CybosPlusComObjectProxy()
    proxy.EnsureConnected()
    data = proxy.GetDailyStockDataAsDataFrame('A035420')
    print(data)

if __name__ == '__main__':
    main()
