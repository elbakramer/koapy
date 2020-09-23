import grpc

from koapy.grpc import KiwoomOpenApiService_pb2_grpc
from koapy.grpc.KiwoomOpenApiServiceClientStubWrapper import KiwoomOpenApiServiceClientStubWrapper
from koapy.config import config

class KiwoomOpenApiServiceClient:

    def __init__(self, host=None, port=None):
        self._host = host or config.get_string('koapy.grpc.host', 'localhost')
        self._port = port or config.get('koapy.grpc.port')

        if self._port is None:
            raise ValueError('Port is None')

        self._target = self._host + ':' + str(self._port)
        self._channel = grpc.insecure_channel(self._target)
        self._stub = KiwoomOpenApiService_pb2_grpc.KiwoomOpenApiServiceStub(self._channel)
        self._stub_wrapped = KiwoomOpenApiServiceClientStubWrapper(self._stub)

    def is_ready(self, timeout=None):
        if timeout is None:
            timeout = config.get_int('koapy.grpc.client.is_ready.timeout', 5)
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
