import inspect

from concurrent.futures import ThreadPoolExecutor

import grpc

from koapy.backend.kiwoom_open_api_plus.grpc import KiwoomOpenApiPlusService_pb2_grpc
from koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClientStubWrapper import (
    KiwoomOpenApiPlusServiceClientStubWrapper,
)
from koapy.config import config


class KiwoomOpenApiPlusServiceClient:
    def __init__(
        self,
        host=None,
        port=None,
        credentials=None,
        thread_pool=None,
        check_timeout=None,
        **kwargs,
    ):
        if host is None:
            host = config.get_string(
                "koapy.backend.kiwoom_open_api_plus.grpc.host", "localhost"
            )
            host = config.get_string(
                "koapy.backend.kiwoom_open_api_plus.grpc.client.host", host
            )
        if port is None:
            port = config.get_int("koapy.backend.kiwoom_open_api_plus.grpc.port")
            port = config.get_int(
                "koapy.backend.kiwoom_open_api_plus.grpc.client.port", port
            )

        if check_timeout is None:
            check_timeout = config.get_int(
                "koapy.backend.kiwoom_open_api_plus.grpc.client.is_ready.timeout", 10
            )

        self._host = host
        self._port = port
        self._credentials = credentials
        self._thread_pool = thread_pool
        self._check_timeout = check_timeout
        self._kwargs = kwargs

        self._target = self._host + ":" + str(self._port)

        if self._credentials is None:
            channel_signature = inspect.signature(grpc.insecure_channel)
            channel_params = list(channel_signature.parameters.keys())
            channel_kwargs = {
                k: v for k, v in self._kwargs.items() if k in channel_params
            }
            channel_bound_arguments = channel_signature.bind_partial(**channel_kwargs)
            channel_bound_arguments.arguments["target"] = self._target
            self._channel = grpc.insecure_channel(
                *channel_bound_arguments.args,
                **channel_bound_arguments.kwargs,
            )
        else:
            channel_signature = inspect.signature(grpc.secure_channel)
            channel_params = list(channel_signature.parameters.keys())
            channel_kwargs = {
                k: v for k, v in self._kwargs.items() if k in channel_params
            }
            channel_bound_arguments = channel_signature.bind_partial(**channel_kwargs)
            channel_bound_arguments.arguments["target"] = self._target
            channel_bound_arguments.arguments["credentials"] = self._credentials
            self._channel = grpc.secure_channel(
                *channel_bound_arguments.args,
                **channel_bound_arguments.kwargs,
            )

        if self._thread_pool is None:
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
                    "koapy.backend.kiwoom_open_api_plus.grpc.client.max_workers",
                    8,
                )
                thread_pool_bound_arguments.arguments["max_workers"] = max_workers
            self._thread_pool = ThreadPoolExecutor(
                *thread_pool_bound_arguments.args,
                **thread_pool_bound_arguments.kwargs,
            )

        self._stub = KiwoomOpenApiPlusService_pb2_grpc.KiwoomOpenApiPlusServiceStub(
            self._channel
        )
        self._stub_wrapped = KiwoomOpenApiPlusServiceClientStubWrapper(
            self._stub, self._thread_pool
        )

    def is_ready(self, timeout=None):
        if timeout is None:
            timeout = self._check_timeout
        try:
            grpc.channel_ready_future(self._channel).result(timeout=timeout)
            return True
        except grpc.FutureTimeoutError:
            return False

    def get_original_stub(self):
        return self._stub

    def get_stub(self):
        return self._stub_wrapped

    def close(self):
        return self._channel.close()

    def __getattr__(self, name):
        return getattr(self._stub_wrapped, name)

    def __enter__(self):
        assert self.is_ready(), "Client is not ready"
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
