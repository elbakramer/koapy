import grpc

from koapy.backend.kiwoom_open_api_plus.grpc import KiwoomOpenApiPlusService_pb2_grpc
from koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClientStubWrapper import (
    KiwoomOpenApiPlusServiceClientStubWrapper,
)
from koapy.config import config


class KiwoomOpenApiPlusServiceClient:
    def __init__(self, host=None, port=None, credentials=None, **kwargs):
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

        self._host = host
        self._port = port
        self._credentials = credentials
        self._kwargs = kwargs

        self._target = self._host + ":" + str(self._port)

        if self._credentials is None:
            self._channel = grpc.insecure_channel(self._target, **self._kwargs)
        else:
            self._channel = grpc.secure_channel(
                self._target, self._credentials, **self._kwargs
            )

        self._stub = KiwoomOpenApiPlusService_pb2_grpc.KiwoomOpenApiPlusServiceStub(
            self._channel
        )
        self._stub_wrapped = KiwoomOpenApiPlusServiceClientStubWrapper(self._stub)

    def is_ready(self, timeout=None):
        if timeout is None:
            timeout = config.get_int(
                "koapy.backend.kiwoom_open_api_plus.grpc.client.is_ready.timeout", 10
            )
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
