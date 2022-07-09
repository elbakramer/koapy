from google.protobuf.json_format import MessageToDict

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError import (
    KiwoomOpenApiPlusError,
    KiwoomOpenApiPlusNegativeReturnCodeError,
)
from koapy.backend.kiwoom_open_api_plus.grpc import KiwoomOpenApiPlusService_pb2
from koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlerForGrpc import (
    KiwoomOpenApiPlusEventHandlerForGrpc,
)


class KiwoomOpenApiPlusLoginEventHandler(KiwoomOpenApiPlusEventHandlerForGrpc):
    def __init__(self, control, request, context):
        super().__init__(control, context)
        self._request = request

        if self._request.HasField("credentials"):
            self._credentials = self._request.credentials
            self._credentials = MessageToDict(
                self._credentials, preserving_proto_field_name=True
            )
        else:
            self._credentials = None

    def on_enter(self):
        if self._credentials is not None:
            self.control.DisableAutoLogin()
            KiwoomOpenApiPlusError.try_or_raise(self.control.CommConnect())
            self.control.LoginUsingPywinauto(self._credentials)
        else:
            KiwoomOpenApiPlusError.try_or_raise(self.control.CommConnect())

    def OnEventConnect(self, errcode):
        if errcode < 0:
            error = KiwoomOpenApiPlusNegativeReturnCodeError(errcode)
            self.observer.on_error(error)
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnEventConnect"
        response.arguments.add().long_value = errcode
        self.observer.on_next(response)
        self.observer.on_completed()
