import grpc

from concurrent import futures

from koapy.grpc import KiwoomOpenApiService_pb2_grpc
from koapy.grpc.KiwoomOpenApiServiceServicer import KiwoomOpenApiServiceServicer

from koapy.config import config
from koapy.utils.networking import get_free_localhost_port

class KiwoomOpenApiServiceServer(object):

    def __init__(self, control, host=None, port=None, max_workers=None):
        self._control = control
        if host is None:
            host = config.get_string('koapy.grpc.host', 'localhost')
        if port is None:
            port = config.get('koapy.grpc.port')
        if port == 0:
            port = get_free_localhost_port()

        self._host = host
        self._port = port

        if self._port is None:
            raise ValueError('Argument port cannot be None')

        if max_workers is None:
            max_workers = config.get_int('koapy.grpc.server.max_workers', 8)

        self._max_workers = max_workers

        self._servicer = KiwoomOpenApiServiceServicer(control)
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=self._max_workers))
        KiwoomOpenApiService_pb2_grpc.add_KiwoomOpenApiServiceServicer_to_server(self._servicer, self._server)

        self._target = self._host + ':' + str(self._port)
        self._server.add_insecure_port(self._target)

    def get_host(self):
        return self._host

    def get_port(self):
        return self._port

    def start(self):
        return self._server.start()

    def wait_for_termination(self, timeout=None):
        return self._server.wait_for_termination(timeout)

    def stop(self, grace=None):
        rcode = self._server.stop(grace)
        return rcode

    def __getattr__(self, name):
        return getattr(self._server, name)
