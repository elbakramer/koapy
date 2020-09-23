from koapy.grpc import KiwoomOpenApiService_pb2

class KiwoomOpenApiServiceClientSideDynamicCallable:

    def __init__(self, stub, name):
        self._stub = stub
        self._name = name

    @classmethod
    def _createCallRequest(cls, name, args):
        request = KiwoomOpenApiService_pb2.CallRequest()
        request.name = name
        for i, arg in enumerate(args):
            if isinstance(arg, str):
                request.arguments.add().string_value = arg # pylint: disable=no-member
            elif isinstance(arg, int):
                request.arguments.add().long_value = arg # pylint: disable=no-member
            else:
                raise TypeError('Unexpected type for argument %d: %s' % (i, type(arg)))
        return request

    @classmethod
    def _unpackResponse(cls, response):
        if response.return_value.HasField('string_value'):
            return response.return_value.string_value
        elif response.return_value.HasField('long_value'):
            return response.return_value.long_value
        else:
            return None

    def __call__(self, *args):
        request = self._createCallRequest(self._name, args)
        response = self._stub.Call(request)
        result = self._unpackResponse(response)
        return result
