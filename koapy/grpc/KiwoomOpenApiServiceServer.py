import atexit
import socket
import logging
import ipaddress

from concurrent import futures

import grpc

from koapy.grpc import KiwoomOpenApiService_pb2_grpc
from koapy.grpc.KiwoomOpenApiServiceServicer import KiwoomOpenApiServiceServicer

from koapy.config import config
from koapy.utils.networking import get_free_localhost_port

class KiwoomOpenApiServiceServer:

    def __init__(self, control, host=None, port=None, max_workers=None):
        if host is None:
            host = config.get_string('koapy.grpc.host', 'localhost')
        if port is None:
            port = config.get('koapy.grpc.port')
        if port == 0:
            port = get_free_localhost_port()
        if max_workers is None:
            max_workers = config.get_int('koapy.grpc.server.max_workers', 8)

        self._control = control
        self._host = host
        self._port = port
        self._max_workers = max_workers

        self._address = self._host + ':' + str(self._port)
        self._servicer = KiwoomOpenApiServiceServicer(self._control)
        self._executor = futures.ThreadPoolExecutor(max_workers=self._max_workers)

        self._server = None
        self._server_started = False
        self._server_stopped = False

        self.reinitialize_server()

        atexit.register(self._executor.shutdown, False)

    def __del__(self):
        atexit.unregister(self._executor.shutdown)

    def reinitialize_server(self):
        if self._server is not None:
            self.stop()
            self.wait_for_termination()

        self._server = grpc.server(self._executor)
        self._server_started = False
        self._server_stopped = False

        KiwoomOpenApiService_pb2_grpc.add_KiwoomOpenApiServiceServicer_to_server(self._servicer, self._server)

        if not ipaddress.ip_address(socket.gethostbyname(self._host)).is_private:
            logging.warning('Adding insecure port %s to server, but the address is not private.', self._address)

        self._server.add_insecure_port(self._address)

    def get_host(self):
        return self._host

    def get_port(self):
        return self._port

    def start(self):
        if self._server_started and self._server_stopped:
            self.reinitialize_server()
        if not self._server_started:
            self._server.start()
            self._server_started = True

    def wait_for_termination(self, timeout=None):
        return self._server.wait_for_termination(timeout)

    def is_running(self):
        return self.wait_for_termination(1)

    def stop(self, grace=None):
        event = self._server.stop(grace)
        self._server_stopped = True
        return event

    def __getattr__(self, name):
        return getattr(self._server, name)
