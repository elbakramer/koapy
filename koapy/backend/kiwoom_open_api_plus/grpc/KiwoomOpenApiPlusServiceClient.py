import grpc

from koapy.backend.kiwoom_open_api_plus.grpc import KiwoomOpenApiPlusService_pb2_grpc
from koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClientStubWrapper import KiwoomOpenApiPlusServiceClientStubWrapper

from koapy.config import config

class KiwoomOpenApiPlusServiceClient:

    def __init__(self, host=None, port=None):
        self._host = host or config.get_string('koapy.backend.kiwoom_open_api_plus.grpc.host', 'localhost')
        self._port = port or config.get('koapy.backend.kiwoom_open_api_plus.grpc.port')

        if self._port is None:
            raise ValueError('Port is None')

        self._target = self._host + ':' + str(self._port)
        self._channel = grpc.insecure_channel(self._target)
        self._stub = KiwoomOpenApiPlusService_pb2_grpc.KiwoomOpenApiPlusServiceStub(self._channel)
        self._stub_wrapped = KiwoomOpenApiPlusServiceClientStubWrapper(self._stub)

    def is_ready(self, timeout=None):
        if timeout is None:
            timeout = config.get_int('koapy.backend.kiwoom_open_api_plus.grpc.client.is_ready.timeout', 10)
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
