from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError import (
    KiwoomOpenApiPlusError,
)
from koapy.backend.kiwoom_open_api_plus.grpc import KiwoomOpenApiPlusService_pb2
from koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlerForGrpc import (
    KiwoomOpenApiPlusEventHandlerForGrpc,
)


class KiwoomOpenApiPlusLoadConditionEventHandler(KiwoomOpenApiPlusEventHandlerForGrpc):
    def __init__(self, control, context, request):
        super().__init__(control, context)
        self._request = request

    def on_enter(self):
        KiwoomOpenApiPlusError.try_or_raise_boolean(
            self.control.GetConditionLoad(), "Failed to load condition"
        )

    def OnReceiveConditionVer(self, ret, msg):
        if ret != 1:
            error = KiwoomOpenApiPlusError(msg)
            self.observer.on_error(error)
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveConditionVer"  # pylint: disable=no-member
        response.arguments.add().long_value = ret  # pylint: disable=no-member
        response.arguments.add().string_value = msg  # pylint: disable=no-member
        self.observer.on_next(response)  # pylint: disable=no-member
        self.observer.on_completed()
