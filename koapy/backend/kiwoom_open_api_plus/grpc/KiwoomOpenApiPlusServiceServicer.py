import logging

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEventHandler import (
    KiwoomOpenApiPlusEventHandler,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusScreenManager import (
    KiwoomOpenApiPlusScreenManager,
)
from koapy.backend.kiwoom_open_api_plus.grpc import (
    KiwoomOpenApiPlusService_pb2,
    KiwoomOpenApiPlusService_pb2_grpc,
)
from koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers import (
    KiwoomOpenApiPlusAllEventHandler,
    KiwoomOpenApiPlusAllOrderEventHandler,
    KiwoomOpenApiPlusBidirectionalRealEventHandler,
    KiwoomOpenApiPlusConditionEventHandler,
    KiwoomOpenApiPlusKwTrEventHandler,
    KiwoomOpenApiPlusLoadConditionEventHandler,
    KiwoomOpenApiPlusLoginEventHandler,
    KiwoomOpenApiPlusOrderEventHandler,
    KiwoomOpenApiPlusRealEventHandler,
    KiwoomOpenApiPlusSomeBidirectionalEventHandler,
    KiwoomOpenApiPlusSomeEventHandler,
    KiwoomOpenApiPlusTrEventHandler,
)
from koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceMessageUtils import (
    convert_arguments_from_protobuf_to_python,
)


class KiwoomOpenApiPlusServiceServicer(
    KiwoomOpenApiPlusService_pb2_grpc.KiwoomOpenApiPlusServiceServicer
):
    def __init__(self, control):
        super().__init__()

        self._control = control
        self._screen_manager = KiwoomOpenApiPlusScreenManager(self._control)

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
        response = KiwoomOpenApiPlusService_pb2.CallResponse()
        if isinstance(result, str):
            response.return_value.string_value = result  # pylint: disable=no-member
        elif isinstance(result, int):
            response.return_value.long_value = result  # pylint: disable=no-member
        elif result is None:
            pass
        else:
            raise TypeError(
                "Unexpected return value type from server side dynamicCall(): %s"
                % type(result)
            )
        return response

    def Listen(self, request, context):
        with KiwoomOpenApiPlusSomeEventHandler(
            self.control, request, context
        ) as handler:
            for response in handler:
                yield response

    def BidirectionalListen(self, request_iterator, context):
        with KiwoomOpenApiPlusSomeBidirectionalEventHandler(
            self.control, request_iterator, context
        ) as handler:
            for response in handler:
                yield response

    def CustomListen(self, request, context):
        code = request.code
        class_name = request.class_name
        if code and class_name:
            global_vars = {}
            local_vars = {}
            exec(code, global_vars, local_vars)  # pylint: disable=exec-used
            handler = eval(class_name, global_vars, local_vars)(
                self.control, request, context
            )  # pylint: disable=eval-used
            assert isinstance(handler, KiwoomOpenApiPlusEventHandler)
        else:
            handler = KiwoomOpenApiPlusAllEventHandler(self.control, context)
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
            global_vars = {}
            local_vars = {}
            exec(code, global_vars, local_vars)  # pylint: disable=exec-used
            handler = eval(class_name, global_vars, local_vars)(
                self.control, request, context
            )  # pylint: disable=eval-used
            assert isinstance(handler, KiwoomOpenApiPlusEventHandler)
        else:
            handler = KiwoomOpenApiPlusAllEventHandler(self.control, context)
        with handler:
            result = function(*arguments)
            response = KiwoomOpenApiPlusService_pb2.CallAndListenResponse()
            if isinstance(result, str):
                response.call_response.return_value.string_value = (
                    result  # pylint: disable=no-member
                )
            elif isinstance(result, int):
                response.call_response.return_value.long_value = (
                    result  # pylint: disable=no-member
                )
            elif result is None:
                pass
            else:
                raise TypeError(
                    "Unexpected return value type from server side dynamicCall(): %s"
                    % type(result)
                )
            yield response
            for listen_response in handler:
                response = KiwoomOpenApiPlusService_pb2.CallAndListenResponse()
                response.listen_response = listen_response
                yield response

    def LoginCall(self, request, context):
        with KiwoomOpenApiPlusLoginEventHandler(
            self.control, request, context
        ) as handler:
            for response in handler:
                yield response

    def TransactionCall(self, request, context):
        trcode = request.transaction_code.upper()

        if trcode in ["OPTKWFID", "OPTFOFID"]:
            handler = KiwoomOpenApiPlusKwTrEventHandler(
                self.control, request, context, self.screen_manager
            )
        else:
            handler = KiwoomOpenApiPlusTrEventHandler(
                self.control, request, context, self.screen_manager
            )

        with handler:
            for response in handler:
                yield response

    def OrderCall(self, request, context):
        with KiwoomOpenApiPlusOrderEventHandler(
            self.control, request, context, self.screen_manager
        ) as handler:
            for response in handler:
                yield response

    def RealCall(self, request, context):
        with KiwoomOpenApiPlusRealEventHandler(
            self.control, request, context, self.screen_manager
        ) as handler:
            for response in handler:
                yield response

    def LoadConditionCall(self, request, context):
        with KiwoomOpenApiPlusLoadConditionEventHandler(
            self.control, request, context
        ) as handler:
            for response in handler:
                yield response

    def ConditionCall(self, request, context):
        with KiwoomOpenApiPlusConditionEventHandler(
            self.control, request, context, self.screen_manager
        ) as handler:
            for response in handler:
                yield response

    def BidirectionalRealCall(self, request_iterator, context):
        with KiwoomOpenApiPlusBidirectionalRealEventHandler(
            self.control, request_iterator, context, self.screen_manager
        ) as handler:
            for response in handler:
                yield response

    def OrderListen(self, request, context):
        with KiwoomOpenApiPlusAllOrderEventHandler(self.control, context) as handler:
            for response in handler:
                yield response

    def SetLogLevel(self, request, context):
        level = request.level
        logger = request.logger
        logging.getLogger(logger).setLevel(level)
        response = KiwoomOpenApiPlusService_pb2.SetLogLevelResponse()
        return response
