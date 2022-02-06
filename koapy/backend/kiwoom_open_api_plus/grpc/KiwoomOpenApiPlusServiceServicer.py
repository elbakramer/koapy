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
from koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusConditionEventHandler import (
    KiwoomOpenApiPlusConditionEventHandler,
)
from koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers import (
    KiwoomOpenApiPlusAllEventHandler,
    KiwoomOpenApiPlusSomeBidirectionalEventHandler,
    KiwoomOpenApiPlusSomeEventHandler,
)
from koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusKwTrEventHandler import (
    KiwoomOpenApiPlusKwTrEventHandler,
)
from koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusLoadConditionEventHandler import (
    KiwoomOpenApiPlusLoadConditionEventHandler,
)
from koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusLoginEventHandler import (
    KiwoomOpenApiPlusLoginEventHandler,
)
from koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusOrderEventHandler import (
    KiwoomOpenApiPlusAllOrderEventHandler,
    KiwoomOpenApiPlusOrderEventHandler,
)
from koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusRealEventHandler import (
    KiwoomOpenApiPlusBidirectionalRealEventHandler,
    KiwoomOpenApiPlusRealEventHandler,
)
from koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusTrEventHandler import (
    KiwoomOpenApiPlusTrEventHandler,
)
from koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceMessageUtils import (
    convert_arguments_from_protobuf_to_python,
)


class KiwoomOpenApiPlusServiceServicer(
    KiwoomOpenApiPlusService_pb2_grpc.KiwoomOpenApiPlusServiceServicer
):
    """
    KiwoomOpenApiPlusService RPC 의 구현체 입니다.
    """

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

    # 1. rpcs for general function calls

    def Call(self, request, context):
        """
        임의의 함수 호출을 위한 RPC 입니다.

        함수의 이름과 파라미터를 요청 메시지를 통해 전달받아 서버측에서 해당 함수를 호출하고
        호출결과를 응답 메시지를 통해 전달합니다.

        함수의 파라미터와 리턴값은 문자열/숫자/불리언 등의 단순한 타입만 지원합니다.
        """
        name = request.name
        arguments = convert_arguments_from_protobuf_to_python(request.arguments)
        function = getattr(self.control, name)
        result = function(*arguments)
        response = KiwoomOpenApiPlusService_pb2.CallResponse()
        if isinstance(result, str):
            response.return_value.string_value = result
        elif isinstance(result, bool):
            response.return_value.bool_value = result
        elif isinstance(result, int):
            response.return_value.long_value = result
        elif result is None:
            pass
        else:
            raise TypeError(
                "Unexpected return value type from server side dynamicCall(): %s"
                % type(result)
            )
        return response

    # 2. rpcs for listening and handling events

    def Listen(self, request, context):
        """
        단일 혹은 복수개의 이벤트에 대해 이벤트 발생시 해당 이벤트 내용을 전달하는 RPC 입니다.

        전달받고자 하는 이벤트 이름 목록을 요청 메시지를 통해 전달받습니다.
        이후 서버에서 목록에 포함되는 이벤트가 발생하면 해당 이벤트의 내용을 응답 메세지를 통해 전달합니다.

        서버측의 이벤트 핸들러 함수는 해당 이벤트를 클라이언트에 전송한 이후 즉시 종료됩니다.
        """
        with KiwoomOpenApiPlusSomeEventHandler(
            self.control, request, context
        ) as handler:
            for response in handler:
                yield response

    def BidirectionalListen(self, request_iterator, context):
        """
        단일 혹은 복수개의 이벤트에 대해 이벤트 발생시 해당 이벤트 내용을 전달하는 RPC 입니다.

        전달받고자 하는 이벤트 이름 목록을 요청 메시지를 통해 전달받습니다.
        이후 서버에서 목록에 포함되는 이벤트가 발생하면 해당 이벤트의 내용을 응답 메세지를 통해 전달합니다.

        앞선 Listen() RPC 와 다르게 해당 RPC 는 이벤트 발생시 서버측에서는 이벤트 내용을 응답 메시지로 전달한 다음
        다시 클라이언트 측에서 ACK 요청을 줄 때 까지 서버측 이벤트 핸들러 함수 내에서 대기합니다.
        따라서 클라이언트는 서버측 이벤트 핸들러 함수 컨텍스트 내에서 이벤트를 처리할 수 있고
        처리를 완료하면 다시 서버측으로 ACK 요청을 보내 서버측 이벤트 핸들러가 완료될 수 있도록 해야 합니다.
        """
        with KiwoomOpenApiPlusSomeBidirectionalEventHandler(
            self.control, request_iterator, context
        ) as handler:
            for response in handler:
                yield response

    # 3. rpcs for simple use cases that can be categorized into serveral distinct usage patterns

    def LoginCall(self, request, context):
        """
        키움증권 서버 연결 시나리오에 해당하는 RPC 입니다.

        CommConnect() 메소드 호출 이후 발생하는 OnEventConnect() 이벤트를 처리하고
        클라이언트에도 해당 이벤트 내용을 전달합니다.
        """
        with KiwoomOpenApiPlusLoginEventHandler(
            self.control, request, context
        ) as handler:
            for response in handler:
                yield response

    def TransactionCall(self, request, context):
        """
        TR 요청에 해당하는 RPC 입니다.

        CommRqData() 메소드 호출 이후 발생하는 OnReceiveTrData() 이벤트를 처리하고
        클라이언트에도 해당 이벤트 내용을 전달합니다.

        OnReceiveTrData() 이벤트 핸들러 함수 내부에서 요청받은 TR 에 따라 관련된 데이터를
        추가로 읽어 들인 뒤 알맞은 응답형태로 가공하여 클라이언트에 반환합니다.
        해당 과정에서 GetRepeatCnt() 및 GetCommData() 메소드를 내부적으로 호출합니다.

        경우에 따라 연속조회가 필요하다면 OnReceiveTrData() 이벤트 핸들러 함수 내부에서
        추가적인 SetInputValue() 및 CommRqData() 호출이 발생할 수 있습니다.

        일반적인 TR 이 아닌 관심종목 관련 TR 의 경우 CommRqData() 대신 CommKwRqData() 가
        내부적으로 호출됩니다.

        서버측에서 CommRqData() 혹은 CommKwRqData() 호출시 내부적으로 호출제한 회피를 위한
        대기시간이 발생할 수 있습니다.

        최초 TR 요청 이후 특정 TR 들에서는 그와 관련된 실시간 데이터가 (OpenAPI+ 레벨에서) 자동으로 등록될 수 있습니다.
        몇몇 상황에서는 해당 실시간 데이터가 유용할 수 있으나 현재 KOAPY 에서는 별도로 사용하진 않고 있으며,
        TR 에 대한 응답처리가 모두 완료된 이후에는 해당 실시간 데이터를 등록 해제하도록 처리하고 있습니다.
        """
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
        """
        주문 요청에 해당하는 RPC 입니다.

        SendOrder() 메소드 호출 이후 발생하는 OnReceiveTrData() 및 OnReceiveChejanData() 이벤트를 처리하고
        클라이언트에도 해당 이벤트 내용을 전달합니다.

        SendOrder() 메소드 호출 이후 발생하는 OnReceiveTrData() 이벤트에서
        주문번호가 확인 가능해야지만 정상주문으로 처리하고 그렇지 않다면 에러를 발생시킵니다.

        일반적으로는 OnReceiveTrData() 이벤트가 먼저 발생하고 이후 OnReceiveChejanData() 이벤트가 접수/체결/잔고확인에 각각 발생합니다.
        다만 주문건수가 폭증하는 경우 OnReceiveChejan() 이벤트가 OnReceiveTrData() 이벤트보다 앞서 수신될 수 있습니다.

        이외에 주문거부등의 케이스에서 주문거부 사유 등이 OnReceiveMsg() 이벤트로 반환됩니다.

        기본적으로 매수/매도 주문의 경우 주문받은 수량이 모두 체결될때까지 이벤트를 처리해 전달합니다.
        """
        with KiwoomOpenApiPlusOrderEventHandler(
            self.control, request, context, self.screen_manager
        ) as handler:
            for response in handler:
                yield response

    def RealCall(self, request, context):
        """
        실시간 데이터 요청에 해당하는 RPC 입니다.

        SetRealReg() 메소드 호출 이후 발생하는 OnReceiveRealData() 이벤트를 처리하고
        클라이언트에도 해당 이벤트 내용을 전달합니다.

        OnReceiveRealData() 이벤트 핸들러 함수 내부에서 앞서 요청받은 실시간 데이터 FID 목록 혹은
        직접 이벤트 핸들러 함수에서 확인 가능한 FID 목록에 따라 관련된 데이터를
        추가로 읽어 들인 뒤 알맞은 응답형태로 가공하여 클라이언트에 반환합니다.
        해당 과정에서 GetCommRealData() 메소드를 내부적으로 호출합니다.

        해당 RPC 는 별도의 이벤트 종료 상황이 존재하지 않기 때문에 더이상 사용하지 않는 경우
        클라이언트 측에서 해당 RPC 연결을 해제하는 식으로 더 이상 이벤트를 받지 않을 수 있습니다.
        이 경우 서버에서는 내부적으로 기 등록된 실시간 데이터에 대해 SetRealRemove() 가 호출됩니다.
        """
        with KiwoomOpenApiPlusRealEventHandler(
            self.control, request, context, self.screen_manager
        ) as handler:
            for response in handler:
                yield response

    def LoadConditionCall(self, request, context):
        """
        조건검색 기능 활용 이전에 먼저 조건식 목록을 불러오는데 사용할 수 있는 RPC 입니다.

        GetConditionLoad() 메소드 호출 이후 발생하는 OnReceiveConditionVer() 이벤트를 처리하고
        클라이언트에도 해당 이벤트 내용을 전달합니다.
        """
        with KiwoomOpenApiPlusLoadConditionEventHandler(
            self.control, request, context
        ) as handler:
            for response in handler:
                yield response

    def ConditionCall(self, request, context):
        """
        조건검색 기능에 해당하는 RPC 입니다.

        SendCondition() 메소드 호출 이후 발생하는 OnReceiveTrCondition() 혹은 OnReceiveRealCondition() 이벤트를
        처리하고 클라이언트에도 해당 이벤트 내용을 전달합니다.
        """
        with KiwoomOpenApiPlusConditionEventHandler(
            self.control, request, context, self.screen_manager
        ) as handler:
            for response in handler:
                yield response

    # 4. rpcs for more complex use cases based on the previously categorized simple cases above

    def BidirectionalRealCall(self, request_iterator, context):
        """
        실시간 데이터 요청에 해당하는 RPC 입니다.

        기존의 RealCall() RPC 는 최초 실시간 데이터 등록 이후 이벤트를 듣는 것만 가능했다면
        새로운 BidirectionalRealCall() 에서는 최초 설정된 이벤트 스트림을 계속 유지하면서
        신규 실시간 데이터 등록 혹은 해지를 추가로 요청해 반영할 수 있습니다.
        """
        with KiwoomOpenApiPlusBidirectionalRealEventHandler(
            self.control, request_iterator, context, self.screen_manager
        ) as handler:
            for response in handler:
                yield response

    def OrderListen(self, request, context):
        """
        주문 이벤트를 듣고 싶을때 사용할 수 있는 RPC 입니다.

        기존의 OrderCall() RPC 는 특정 주문을 수행하고 해당 주문과 관련된 이벤트들만 반환했다면
        해당 RPC 는 특정 주문 수행 없이 모든 주문관련 이벤트를 듣고 싶을때 사용할 수 있습니다.
        """
        with KiwoomOpenApiPlusAllOrderEventHandler(self.control, context) as handler:
            for response in handler:
                yield response

    # 5. rpcs for customized usage scenario (when there is no proper predefined interface to utilize)

    def CustomListen(self, request, context):
        """
        이벤트 처리와 관련해 특정 코드를 서버측에 실행시켜 그 로직에 따라 처리하도록 요청할 수 있습니다.

        해당 코드에서는 KiwoomOpenApiPlusEventHandler 클래스를 구현해야하며,
        클래스 인스턴스 생성시 control, request, context 세가지 인자를 받아 처리할 수 있어야 합니다.

        내부적으로 exec() 및 eval() 을 사용하기 때문에 실행될 코드의 보안 및 안정성에 주의가 필요합니다.
        """
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
        """
        이벤트 처리와 관련해 특정 코드를 서버측에 실행시켜 그 로직에 따라 처리하도록 요청할 수 있습니다.

        앞선 CustomListen() 과의 차이점은 요청시 특정 함수를 최초 1회 호출하고 이후 들어오는 이벤트를 처리한다는 점입니다.

        해당 코드에서는 KiwoomOpenApiPlusEventHandler 클래스를 구현해야하며,
        클래스 인스턴스 생성시 control, request, context 세가지 인자를 받아 처리할 수 있어야 합니다.

        내부적으로 exec() 및 eval() 을 사용하기 때문에 실행될 코드의 보안 및 안정성에 주의가 필요합니다.
        """
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

    # 6. rpcs for other mics scenarios

    def SetLogLevel(self, request, context):
        """
        서버에 존재하는 특정 로거의 로그레벨을 설정합니다.
        """
        level = request.level
        logger = request.logger
        logging.getLogger(logger).setLevel(level)
        response = KiwoomOpenApiPlusService_pb2.SetLogLevelResponse()
        return response
