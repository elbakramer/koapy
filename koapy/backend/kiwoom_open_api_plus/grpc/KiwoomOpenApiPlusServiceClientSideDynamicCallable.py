from koapy.backend.kiwoom_open_api_plus.grpc import KiwoomOpenApiPlusService_pb2
from koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceMessageUtils import (
    convert_arguments_from_python_to_protobuf,
)


class KiwoomOpenApiPlusServiceClientSideDynamicCallable:
    def __init__(self, stub, name):
        self._stub = stub
        self._name = name

    @classmethod
    def _create_call_request(cls, name, args):
        request = KiwoomOpenApiPlusService_pb2.CallRequest()
        request.name = name
        convert_arguments_from_python_to_protobuf(
            args, request.arguments
        )  # pylint: disable=no-member
        return request

    @classmethod
    def _unpack_response(cls, response):
        if response.return_value.HasField("string_value"):
            return response.return_value.string_value
        elif response.return_value.HasField("long_value"):
            return response.return_value.long_value
        elif response.return_value.HasField("bool_value"):
            return response.return_value.bool_value
        else:
            return None

    def __call__(self, *args):
        request = self._create_call_request(self._name, args)
        response = self._stub.Call(request)
        result = self._unpack_response(response)
        return result
