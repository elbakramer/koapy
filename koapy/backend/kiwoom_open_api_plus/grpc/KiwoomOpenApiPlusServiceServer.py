import inspect

from concurrent.futures import ThreadPoolExecutor

import grpc

from koapy.backend.kiwoom_open_api_plus.grpc import KiwoomOpenApiPlusService_pb2_grpc
from koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceServicer import (
    KiwoomOpenApiPlusServiceServicer,
)
from koapy.config import config
from koapy.utils.logging.Logging import Logging
from koapy.utils.networking import find_free_port_for_host, is_in_private_network


class KiwoomOpenApiPlusServiceServer(Logging):
    def __init__(
        self,
        control,
        host=None,
        port=None,
        credentials=None,
        **kwargs,
    ):
        if host is None:
            host = config.get_string(
                "koapy.backend.kiwoom_open_api_plus.grpc.host", "localhost"
            )
            host = config.get_string(
                "koapy.backend.kiwoom_open_api_plus.grpc.server.host", host
            )
        if port is None:
            port = config.get_int("koapy.backend.kiwoom_open_api_plus.grpc.port", 0)
            port = config.get_int(
                "koapy.backend.kiwoom_open_api_plus.grpc.server.port", port
            )

        if port == 0:
            port = find_free_port_for_host(host)
            self.logger.info(
                "Using one of the free ports, final address would be %s:%d", host, port
            )

        self._control = control
        self._host = host
        self._port = port
        self._credentials = credentials
        self._kwargs = dict(kwargs)

        self._servicer = KiwoomOpenApiPlusServiceServicer(self._control)
        self._address = self._host + ":" + str(self._port)

        grpc_server_signature = inspect.signature(grpc.server)
        grpc_server_params = list(grpc_server_signature.parameters.keys())
        grpc_server_kwargs = {
            k: v for k, v in self._kwargs.items() if k in grpc_server_params
        }
        grpc_server_bound_arguments = grpc_server_signature.bind_partial(
            **grpc_server_kwargs
        )
        if grpc_server_bound_arguments.arguments.get("thread_pool") is None:
            thread_pool_signature = inspect.signature(ThreadPoolExecutor)
            thread_pool_params = list(thread_pool_signature.parameters.keys())
            thread_pool_kwargs = {
                k: v for k, v in self._kwargs.items() if k in thread_pool_params
            }
            thread_pool_bound_arguments = thread_pool_signature.bind(
                **thread_pool_kwargs
            )
            if thread_pool_bound_arguments.arguments.get("max_workers") is None:
                max_workers = config.get_int(
                    "koapy.backend.kiwoom_open_api_plus.grpc.server.max_workers", 8
                )
                thread_pool_bound_arguments.arguments["max_workers"] = max_workers
            thread_pool = ThreadPoolExecutor(
                *thread_pool_bound_arguments.args,
                **thread_pool_bound_arguments.kwargs,
            )
            grpc_server_bound_arguments.arguments["thread_pool"] = thread_pool
            self._thread_pool = thread_pool
        else:
            self._thread_pool = grpc_server_bound_arguments.arguments["thread_pool"]

        self._grpc_server_bound_arguments = grpc_server_bound_arguments

        self._server = None
        self._server_started = False
        self._server_stopped = False

        self.reinitialize_server()

    def reinitialize_server(self):
        if self._server is not None:
            self.stop()
            self.wait_for_termination()

        self._server = grpc.server(
            *self._grpc_server_bound_arguments.args,
            **self._grpc_server_bound_arguments.kwargs,
        )
        self._server_started = False
        self._server_stopped = False

        KiwoomOpenApiPlusService_pb2_grpc.add_KiwoomOpenApiPlusServiceServicer_to_server(
            self._servicer, self._server
        )

        if self._credentials is None:
            if not is_in_private_network(self._host):
                self.logger.warning(
                    "Adding insecure port %s to server, but the address is not private.",
                    self._address,
                )
            self._server.add_insecure_port(self._address)
        else:
            self._server.add_secure_port(self._address, self._credentials)

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

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
        self.wait_for_termination()
