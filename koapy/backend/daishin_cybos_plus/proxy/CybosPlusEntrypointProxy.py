from threading import RLock

import grpc

from koapy.backend.daishin_cybos_plus.core.CybosPlusEntrypointMixin import (
    CybosPlusEntrypointMixin,
)
from koapy.backend.daishin_cybos_plus.proxy.CybosPlusDispatchProxy import (
    CybosPlusDispatchProxy,
)
from koapy.common import DispatchProxyService_pb2, DispatchProxyService_pb2_grpc


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
        self._stub = DispatchProxyService_pb2_grpc.DispatchProxyServiceStub(
            self._channel
        )

        grpc.channel_ready_future(self._channel).result(timeout=5)

        self._lock = RLock()
        self._dispatch_proxies = {}

    def __getitem__(self, name):
        if name not in self._dispatch_proxies:
            with self._lock:
                if name not in self._dispatch_proxies:
                    request = DispatchProxyService_pb2.GetDispatchRequest()
                    request.iid = name
                    response = self._stub.GetDispatch(request)
                    iid = response.iid
                    proxy = CybosPlusDispatchProxy(iid, self._stub)
                    self._dispatch_proxies[name] = proxy
        proxy = self._dispatch_proxies[name]
        return proxy
