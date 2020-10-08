import threading

from koapy.grpc import KiwoomOpenApiService_pb2, KiwoomOpenApiService_pb2_grpc
from koapy.grpc.event.KiwoomOpenApiEventHandler import KiwoomOpenApiEventHandler

from koapy.grpc.event.KiwoomOpenApiEventHandlers import KiwoomOpenApiAllEventHandler
from koapy.grpc.event.KiwoomOpenApiEventHandlers import KiwoomOpenApiSomeEventHandler
from koapy.grpc.event.KiwoomOpenApiEventHandlers import KiwoomOpenApiLoginEventHandler
from koapy.grpc.event.KiwoomOpenApiEventHandlers import KiwoomOpenApiTrEventHandler
from koapy.grpc.event.KiwoomOpenApiEventHandlers import KiwoomOpenApiOrderEventHandler
from koapy.grpc.event.KiwoomOpenApiEventHandlers import KiwoomOpenApiRealEventHandler
from koapy.grpc.event.KiwoomOpenApiEventHandlers import KiwoomOpenApiSomeBidirectionalEventHandler
from koapy.grpc.event.KiwoomOpenApiEventHandlers import KiwoomOpenApiLoadConditionEventHandler
from koapy.grpc.event.KiwoomOpenApiEventHandlers import KiwoomOpenApiConditionEventHandler
from koapy.grpc.event.KiwoomOpenApiEventHandlers import KiwoomOpenApiBidirectionalRealEventHandler

from koapy.grpc.KiwoomOpenApiService import convert_arguments_from_protobuf_to_python

from koapy.openapi.ScreenManager import ScreenManager

from koapy.utils.logging import set_loglevel

class KiwoomOpenApiServiceServicer(KiwoomOpenApiService_pb2_grpc.KiwoomOpenApiServiceServicer):

    _listen_id_to_handler = {}
    _listen_id_to_handler_lock = threading.RLock()

    def __init__(self, control):
        super().__init__()

        self._control = control
        self._screen_manager = ScreenManager(self._control)

    @property
    def control(self):
        return self._control

    @property
    def screen_manager(self):
        return self._screen_manager

    def Call(self, request, context):
        name = request.name
        arguments = convert_arguments_from_protobuf_to_python(request.arguments)
        function = getattr(self.control, name)
        result = function(*arguments)
        response = KiwoomOpenApiService_pb2.CallResponse()
        if isinstance(result, str):
            response.return_value.string_value = result # pylint: disable=no-member
        elif isinstance(result, int):
            response.return_value.long_value = result # pylint: disable=no-member
        elif result is None:
            pass
        else:
            raise TypeError('Unexpected return value type from server side dynamicCall(): %s' % type(result))
        return response

    def _RegisterHandler(self, handler_id, handler):
        with self._listen_id_to_handler_lock:
            self._UnregisterHandler(handler_id)
            self._listen_id_to_handler[handler_id] = handler

    def _UnregisterHandler(self, handler_id):
        with self._listen_id_to_handler_lock:
            if handler_id in self._listen_id_to_handler:
                self._listen_id_to_handler[handler_id].observer.on_completed()
                del self._listen_id_to_handler[handler_id]
                return True
        return False

    def Listen(self, request, context):
        handler = KiwoomOpenApiSomeEventHandler(self.control, request, context)
        self._RegisterHandler(request.id, handler)
        handler.add_callback(self._UnregisterHandler, request.id)
        with handler:
            for response in handler:
                yield response

    def StopListen(self, request, context):
        response = KiwoomOpenApiService_pb2.StopListenResponse()
        response.successful = self._UnregisterHandler(request.id)
        return response

    def BidirectionalListen(self, request_iterator, context):
        with KiwoomOpenApiSomeBidirectionalEventHandler(self.control, request_iterator, context) as handler:
            for response in handler:
                yield response

    def CustomListen(self, request, context):
        code = request.code
        class_name = request.class_name
        if code and class_name:
            g = {}
            l = {}
            exec(code, g, l) # pylint: disable=exec-used
            handler = eval(class_name, g, l)(self.control, request, context) # pylint: disable=eval-used
            assert isinstance(handler, KiwoomOpenApiEventHandler)
        else:
            handler = KiwoomOpenApiAllEventHandler(self.control, context)
        with handler:
            for response in handler:
                yield response

    def CustomCallAndListen(self, request, context):
        name = request.name
        arguments = convert_arguments_from_protobuf_to_python(request.arguments)
        function = getattr(self.control, name)
        code = request.listen_request.code
        class_name = request.listen_request.class_name
        if code and class_name:
            g = {}
            l = {}
            exec(code, g, l) # pylint: disable=exec-used
            handler = eval(class_name, g, l)(self.control, request, context) # pylint: disable=eval-used
            assert isinstance(handler, KiwoomOpenApiEventHandler)
        else:
            handler = KiwoomOpenApiAllEventHandler(self.control, context)
        with handler:
            result = function(*arguments)
            response = KiwoomOpenApiService_pb2.CallAndListenResponse()
            if isinstance(result, str):
                response.call_response.return_value.string_value = result # pylint: disable=no-member
            elif isinstance(result, int):
                response.call_response.return_value.long_value = result # pylint: disable=no-member
            elif result is None:
                pass
            else:
                raise TypeError('Unexpected return value type from server side dynamicCall(): %s' % type(result))
            yield response
            for response in handler:
                yield response

    def LoginCall(self, request, context):
        with KiwoomOpenApiLoginEventHandler(self.control, request, context) as handler:
            for response in handler:
                yield response

    def TransactionCall(self, request, context):
        with KiwoomOpenApiTrEventHandler(self.control, request, context, self.screen_manager) as handler:
            for response in handler:
                yield response

    def OrderCall(self, request, context):
        with KiwoomOpenApiOrderEventHandler(self.control, request, context, self.screen_manager) as handler:
            for response in handler:
                yield response

    def RealCall(self, request, context):
        with KiwoomOpenApiRealEventHandler(self.control, request, context, self.screen_manager) as handler:
            for response in handler:
                yield response

    def LoadConditionCall(self, request, context):
        with KiwoomOpenApiLoadConditionEventHandler(self.control, request, context) as handler:
            for response in handler:
                yield response

    def ConditionCall(self, request, context):
        with KiwoomOpenApiConditionEventHandler(self.control, request, context, self.screen_manager) as handler:
            for response in handler:
                yield response

    def BidirectionalRealCall(self, request_iterator, context):
        with KiwoomOpenApiBidirectionalRealEventHandler(self.control, request_iterator, context, self.screen_manager) as handler:
            for response in handler:
                yield response

    def SetLogLevel(self, request, context):
        level = request.level
        logger = request.logger
        set_loglevel(level, logger)
        response = KiwoomOpenApiService_pb2.SetLogLevelResponse()
        return response
