import grpc

from concurrent.futures import ThreadPoolExecutor

from koapy.backend.cybos import CybosPlusProxyService_pb2_grpc
from koapy.backend.cybos.CybosPlusProxyServiceServicer import CybosPlusProxyServiceServicer

class CybosPlusProxyService:

    def __init__(self, host=None, port=None, max_workers=None):
        if host is None:
            host = 'localhost'
        if port is None:
            port = 3031

        if max_workers is None:
            max_workers = None

        self._host = host
        self._port = port
        self._max_workers = max_workers

        self._address = self._host + ':' + str(self._port)
        self._servicer = CybosPlusProxyServiceServicer()
        self._executor = ThreadPoolExecutor(max_workers=self._max_workers)

        self._server = grpc.server(self._executor)
        CybosPlusProxyService_pb2_grpc.add_CybosPlusProxyServiceServicer_to_server(self._servicer, self._server)
        self._server.add_insecure_port(self._address)

    def __getattr__(self, name):
        return getattr(self._server, name)

def main():
    service = CybosPlusProxyService()
    service.start()
    service.wait_for_termination()

if __name__ == '__main__':
    main()
