import threading

import grpc

from requests.structures import CaseInsensitiveDict

from koapy.backend.daishin_cybos_plus.core.CybosPlusEntrypointMixin import (
    CybosPlusEntrypointMixin,
)
from koapy.backend.daishin_cybos_plus.proxy import (
    CybosPlusProxyService_pb2,
    CybosPlusProxyService_pb2_grpc,
)
from koapy.backend.daishin_cybos_plus.proxy.CybosPlusProxyServiceMessageUtils import (
    AssignPrimitive,
    ExtractPrimitive,
)
from koapy.utils.logging.Logging import Logging


class CybosPlusDispatchProxyMethod:
    def __init__(self, proxy, name):
        self._proxy = proxy
        self._name = name

    def __call__(self, *args, **kwargs):
        return self._proxy._InvokeMethod(self._name, args)


class CybosPlusDispatchProxy(Logging):
    def __init__(self, proxy, progid):
        self._proxy = proxy
        self._progid = progid

        self._is_trade_related = self._progid.startswith("CpTrade.")

        request = CybosPlusProxyService_pb2.DispatchRequest()
        request.prog = self._progid

        self._dispatch = self._proxy._stub.Dispatch(request)

    def _GetProperty(self, name):
        request = CybosPlusProxyService_pb2.PropertyRequest()
        request.prog = self._progid
        request.name = name
        should_stop = False
        while not should_stop:
            # pylint: disable=protected-access
            response_future = self._proxy._stub.Property.future(
                request, timeout=self._proxy._timeout
            )
            try:
                response = response_future.result()
            except grpc.RpcError:
                if response_future.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                    self.logger.warning("Property %s lookup failed, retrying...", name)
                else:
                    raise
            else:
                should_stop = True
        result = ExtractPrimitive(response.value)
        return result

    def _InvokeMethod(self, name, args):
        request = CybosPlusProxyService_pb2.MethodRequest()
        request.prog = self._progid
        request.name = name
        for arg in args:
            AssignPrimitive(request.arguments.add().value, arg)
        should_stop = False
        while not should_stop:
            # pylint: disable=protected-access
            response_future = self._proxy._stub.Method.future(
                request, timeout=self._proxy._timeout
            )
            try:
                response = response_future.result()
            except grpc.RpcError:
                if response_future.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                    self.logger.warning(
                        "Method invocation %s(%s) timed out, retrying...",
                        name,
                        ", ".join(map(repr, args)),
                    )
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
            return CybosPlusDispatchProxyMethod(self, name)
        else:
            raise AttributeError


class CybosPlusIncompleteProgIDProxy:
    def __init__(self, proxy, prefix):
        self._proxy = proxy
        self._prefix = prefix

        self._cache = {}
        self._lock = threading.RLock()

    def __getattr__(self, name):
        if name not in self._cache:
            with self._lock:
                if name not in self._cache:
                    progid = "{}.{}".format(self._prefix, name)
                    self._cache[name] = CybosPlusDispatchProxy(self._proxy, progid)
        return self._cache[name]


class CybosPlusEntrypointProxy(CybosPlusEntrypointMixin):
    def __init__(self, host=None, port=None):
        if host is None:
            host = "localhost"
        if port is None:
            port = 3031

        self._host = host
        self._port = port

        self._address = self._host + ":" + str(self._port)
        self._channel = grpc.insecure_channel(self._address)
        self._stub = CybosPlusProxyService_pb2_grpc.CybosPlusProxyServiceStub(
            self._channel
        )

        self._timeout = 10

        grpc.channel_ready_future(self._channel).result(timeout=5)

        self._attribute_mapping = {
            "CpDib": "DsCbo1",
            "CpSysDib": "CpSysDib",
            "CpTrade": "CpTrade",
            "CpUtil": "CpUtil",
            "DsCbo1": "DsCbo1",
        }
        self._attribute_mapping = CaseInsensitiveDict(self._attribute_mapping)

        self._cache = {}
        self._lock = threading.RLock()

    def __getattr__(self, name):
        if name not in self._attribute_mapping:
            raise AttributeError(
                "'{}' object has no attribute '{}'".format(type(self), name)
            )
        name = self._attribute_mapping[name]
        if name not in self._cache:
            with self._lock:
                if name not in self._cache:
                    self._cache[name] = CybosPlusIncompleteProgIDProxy(self, name)
        return self._cache[name]
