from concurrent.futures import ThreadPoolExecutor

import grpc

from pythoncom import CoInitialize

from koapy.backend.daishin_cybos_plus.proxy.CybosPlusDispatchProxyServiceServicer import (
    CybosPlusDispatchProxyServiceServicer,
)
from koapy.common import DispatchProxyService_pb2_grpc


class CybosPlusDispatchProxyService:
    def __init__(self, host=None, port=None, max_workers=None):
        if host is None:
            host = "localhost"
        if port is None:
            port = 3031

        if max_workers is None:
            max_workers = None

        self._host = host
        self._port = port
        self._max_workers = max_workers

        self._address = self._host + ":" + str(self._port)
        self._servicer = CybosPlusDispatchProxyServiceServicer()
        self._executor = ThreadPoolExecutor(
            max_workers=self._max_workers,
            initializer=CoInitialize,
        )

        self._server = grpc.server(self._executor)
        DispatchProxyService_pb2_grpc.add_DispatchProxyServiceServicer_to_server(
            self._servicer, self._server
        )
        self._server.add_insecure_port(self._address)

    def __getattr__(self, name):
        return getattr(self._server, name)


def main():
    service = CybosPlusDispatchProxyService()
    service.start()
    service.wait_for_termination()


if __name__ == "__main__":
    main()
