import datetime
import logging
import re

import pandas as pd

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusDispatchSignature import (
    KiwoomOpenApiPlusDispatchSignature,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEventHandlerSignature import (
    KiwoomOpenApiPlusEventHandlerSignature,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin import (
    KiwoomOpenApiPlusQAxWidgetUniversalMixin,
)
from koapy.backend.kiwoom_open_api_plus.grpc import KiwoomOpenApiPlusService_pb2
from koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClientSideDynamicCallable import (
    KiwoomOpenApiPlusServiceClientSideDynamicCallable,
)
from koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClientSideSignalConnector import (
    KiwoomOpenApiPlusServiceClientSideSignalConnector,
)
from koapy.backend.kiwoom_open_api_plus.utils.grpc.PipeableMultiThreadedRendezvous import (
    PipeableMultiThreadedRendezvous,
)
from koapy.utils.logging.Logging import Logging


class KiwoomOpenApiPlusServiceClientStubCoreWrapper(
    KiwoomOpenApiPlusQAxWidgetUniversalMixin
):
    """
    KiwoomOpenApiPlusServiceServicer 에서 구현되어 이후 Stub 을 통해 제공되는
    RPC 들을 클라이언트에서 좀 더 쉽게 사용하기 위한 래퍼 함수들을 제공합니다.
    """

    METHOD_NAMES = KiwoomOpenApiPlusDispatchSignature.names()
    EVENT_NAMES = KiwoomOpenApiPlusEventHandlerSignature.names()

    def __init__(self, stub, executor):
        self._stub = stub
        self._executor = executor

        # Set methods as attributes
        for method_name in self.METHOD_NAMES:
            dynamic_callable = KiwoomOpenApiPlusServiceClientSideDynamicCallable(
                self._stub, method_name
            )
            setattr(self, method_name, dynamic_callable)

        # Set signals as attributes
        for event_name in self.EVENT_NAMES:
            signal_connector = KiwoomOpenApiPlusServiceClientSideSignalConnector(
                self._stub, event_name, self._executor
            )
            setattr(self, event_name, signal_connector)

    def __getattr__(self, name):
        return getattr(self._stub, name)

    def Call(self, name, *args):
        """
        임의의 함수 호출을 위한 RPC 입니다.

        함수의 이름과 파라미터를 요청 메시지를 통해 전달받아 서버측에서 해당 함수를 호출하고
        호출결과를 응답 메시지를 통해 전달합니다.

        함수의 파라미터와 리턴값은 문자열/숫자/불리언 등의 단순한 타입만 지원합니다.
        """
        return KiwoomOpenApiPlusServiceClientSideDynamicCallable(self._stub, name)(
            *args
        )

    def LoginCall(self, credentials=None):
        """
        키움증권 서버 연결 시나리오에 해당하는 RPC 입니다.

        CommConnect() 메소드 호출 이후 발생하는 OnEventConnect() 이벤트를 처리하고
        클라이언트에도 해당 이벤트 내용을 전달합니다.
        """
        request = KiwoomOpenApiPlusService_pb2.LoginRequest()
        if credentials is not None:
            request.credentials.user_id = credentials.get("user_id")
            request.credentials.user_password = credentials.get("user_password")
            request.credentials.cert_password = credentials.get("cert_password")
            request.credentials.is_simulation = credentials.get("is_simulation")
            account_passwords = credentials.get("account_passwords")
            for account_no, account_password in account_passwords.items():
                request.credentials.account_passwords[account_no] = account_password
        for response in self._stub.LoginCall(request):
            errcode = response.arguments[0].long_value
        return errcode

    def TransactionCall(self, rqname, trcode, scrno, inputs, stop_condition=None):
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
        request = KiwoomOpenApiPlusService_pb2.TransactionRequest()
        request.request_name = rqname
        request.transaction_code = trcode
        request.screen_no = scrno or ""
        for k, v in inputs.items():
            request.inputs[k] = v
        if stop_condition:
            request.stop_condition.name = stop_condition.get("name", "")
            request.stop_condition.value = str(stop_condition.get("value", ""))
            request.stop_condition.comparator = {
                "<=": KiwoomOpenApiPlusService_pb2.TransactionStopConditionCompartor.LESS_THAN_OR_EQUAL_TO,
                "<": KiwoomOpenApiPlusService_pb2.TransactionStopConditionCompartor.LESS_THAN,
                ">=": KiwoomOpenApiPlusService_pb2.TransactionStopConditionCompartor.GREATER_THAN_OR_EQUAL_TO,
                ">": KiwoomOpenApiPlusService_pb2.TransactionStopConditionCompartor.GREATER_THAN,
                "==": KiwoomOpenApiPlusService_pb2.TransactionStopConditionCompartor.EQUAL_TO,
                "!=": KiwoomOpenApiPlusService_pb2.TransactionStopConditionCompartor.NOT_EQUAL_TO,
            }.get(stop_condition.get("comparator", "<="))
        return self._stub.TransactionCall(request)

    def OrderCall(
        self,
        rqname,
        scrno,
        account,
        order_type,
        code,
        quantity,
        price,
        quote_type,
        original_order_no=None,
    ):
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

        거래 구분:
            - 00: 지정가
            - 03: 시장가
            - 05: 조건부지정가
            - 06: 최유리지정가
            - 07: 최우선지정가
            - 10: 지정가IOC
            - 13: 시장가IOC
            - 16: 최유리IOC
            - 20: 지정가FOK
            - 23: 시장가FOK
            - 26: 최유리FOK
            - 61: 장전시간외종가
            - 62: 시간외단일가매매
            - 81: 장후시간외종가

        ※ 모의투자에서는 지정가 주문과 시장가 주문만 가능합니다.

        주문 유형:
            - 1: 신규매수
            - 2: 신규매도
            - 3: 매수취소
            - 4: 매도취소
            - 5: 매수정정
            - 6: 매도정정

        Args:
            rqname (str): 사용자 구분 요청명
            scrno (str): 화면번호 (4자리)
            account (str): 계좌번호 (10자리)
            order_type (int): 주문유형 (1:신규매수, 2:신규매도, 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정)
            code (str): 종목코드 (6자리)
            quantity (int): 주문수량
            price (int): 주문단가
            quote_type (str): 거래구분 (혹은 호가구분)
            original_order_no (str): 원주문번호, 신규주문에는 공백 입력, 정정/취소시 입력합니다.
        """
        request = KiwoomOpenApiPlusService_pb2.OrderRequest()
        request.request_name = rqname or ""
        request.screen_no = str(scrno).zfill(4) if scrno else ""
        request.account_no = str(account) if account else ""
        request.order_type = int(order_type) if order_type else 0
        request.code = code or ""
        request.quantity = int(quantity) if quantity else 0
        request.price = int(price) if price else 0
        request.quote_type = quote_type or ""
        request.original_order_no = original_order_no or ""
        return self._stub.OrderCall(request)

    def RealCall(
        self,
        scrno,
        codes,
        fids,
        opt_type=None,
        infer_fids=False,
        readable_names=False,
        fast_parse=False,
    ):
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
        request = KiwoomOpenApiPlusService_pb2.RealRequest()
        if scrno is None:
            scrnos = []
        elif isinstance(scrno, str):
            scrnos = [scrno]
        else:
            scrnos = scrno
        fids = [int(fid) for fid in fids]
        if opt_type is None:
            opt_type = "0"
        request.screen_no.extend(scrnos)
        request.code_list.extend(codes)
        request.fid_list.extend(fids)
        request.opt_type = opt_type
        request.flags.infer_fids = infer_fids
        request.flags.readable_names = readable_names
        request.flags.fast_parse = fast_parse
        return self._stub.RealCall(request)

    def LoadConditionCall(self):
        """
        조건검색 기능 활용 이전에 먼저 조건식 목록을 불러오는데 사용할 수 있는 RPC 입니다.

        GetConditionLoad() 메소드 호출 이후 발생하는 OnReceiveConditionVer() 이벤트를 처리하고
        클라이언트에도 해당 이벤트 내용을 전달합니다.
        """
        request = KiwoomOpenApiPlusService_pb2.LoadConditionRequest()
        for response in self._stub.LoadConditionCall(request):
            ret = response.arguments[0].long_value
            msg = response.arguments[1].string_value
        return (ret, msg)

    def ConditionCall(
        self,
        scrno,
        condition_name,
        condition_index,
        search_type,
        with_info=False,
        is_future_option=False,
        request_name=None,
    ):
        """
        조건검색 기능에 해당하는 RPC 입니다.

        SendCondition() 메소드 호출 이후 발생하는 OnReceiveTrCondition() 혹은 OnReceiveRealCondition() 이벤트를
        처리하고 클라이언트에도 해당 이벤트 내용을 전달합니다.
        """
        request = request = KiwoomOpenApiPlusService_pb2.ConditionRequest()
        request.screen_no = scrno or ""
        request.condition_name = condition_name
        request.condition_index = condition_index
        request.search_type = search_type
        request.flags.with_info = with_info
        request.flags.is_future_option = is_future_option
        if request_name is not None:
            request.request_name = request_name
        return self._stub.ConditionCall(request)

    def SetLogLevel(self, level, logger=""):
        """
        서버에 존재하는 특정 로거의 로그레벨을 설정합니다.
        """
        request = KiwoomOpenApiPlusService_pb2.SetLogLevelRequest()
        request.level = level
        request.logger = logger
        return self._stub.SetLogLevel(request)

    def _LoadConditionUsingCall(self):
        return self.Call("LoadCondition")

    def LoadCondition(self):
        """
        조건검색 관련 조건식을 불러옵니다.
        """
        return self._LoadConditionUsingCall()

    def _IsConditionLoadedUsingCall(self):
        return self.Call("IsConditionLoaded")

    def IsConditionLoaded(self):
        """
        조건식이 로드 되었는지 여부를 반환합니다.
        """
        return self._IsConditionLoadedUsingCall()

    def _EnsureConditionLoadedUsingCall(self, force=False):
        return self.Call("EnsureConditionLoaded", force)

    def EnsureConditionLoaded(self, force=False):
        """
        조건식이 로드됨을 보장하도록 합니다.

        이미 조건식을 불러온 경우 별다른 처리를 하지 않습니다.
        조건식을 불러오지 않았다면 조건식을 불러오도록 처리합니다.
        """
        return self._EnsureConditionLoadedUsingCall(force)

    def _RateLimitedCommRqDataUsingCall(
        self, rqname, trcode, prevnext, scrno, inputs=None
    ):
        return self.Call(
            "RateLimitedCommRqData", rqname, trcode, prevnext, scrno, inputs
        )

    def RateLimitedCommRqData(self, rqname, trcode, prevnext, scrno, inputs=None):
        """
        CommRqData() 와 동일하지만 호출제한 회피를 위한 함수입니다.
        필요에 따라 호출제한을 회피하기 위해 실제 호출 전 대기할 수 있습니다.
        """
        self._RateLimitedCommRqDataUsingCall(rqname, trcode, prevnext, scrno, inputs)

    def _RateLimitedSendConditionUsingCall(
        self, scrno, condition_name, condition_index, search_type
    ):
        return self.Call(
            "RateLimitedSendCondition",
            scrno,
            condition_name,
            condition_index,
            search_type,
        )

    def RateLimitedSendCondition(
        self, scrno, condition_name, condition_index, search_type
    ):
        """
        SendCondition() 과 동일하지만 호출제한 회피를 위한 함수입니다.
        필요에 따라 호출제한을 회피하기 위해 실제 호출 전 대기할 수 있습니다.
        """
        return self._RateLimitedSendConditionUsingCall(
            scrno, condition_name, condition_index, search_type
        )


class KiwoomOpenApiPlusServiceClientStubExtendedWrapper(
    KiwoomOpenApiPlusServiceClientStubCoreWrapper, Logging
):
    """
    제공되는 RPC 들을 활용한 여러 사용 케이스들을 구현합니다.
    """

    def _RemoveLeadingZerosForNumber(self, value, width=0):
        remove = False
        if width is None:
            remove = False
        elif isinstance(width, int) and (width == 0 or len(value) == width):
            remove = True
        elif hasattr(width, "__contains__") and len(value) in width:
            remove = True
        if remove:
            return re.sub(r"^\s*([+-]?)[0]+([0-9]+(.[0-9]+)?)\s*$", r"\1\2", value)
        return value

    def _RemoveLeadingZerosForNumbersInValues(self, values, width=0):
        return [self._RemoveLeadingZerosForNumber(value, width) for value in values]

    def _ParseTransactionCallResponses(self, responses, remove_zeros_width=None):
        single_output = None
        columns = []
        records = []
        for response in responses:
            if single_output is None:
                single_output = dict(
                    zip(
                        response.single_data.names,
                        self._RemoveLeadingZerosForNumbersInValues(
                            response.single_data.values, remove_zeros_width
                        ),
                    )
                )
            if not columns:
                columns = response.multi_data.names
            for values in response.multi_data.values:
                records.append(
                    self._RemoveLeadingZerosForNumbersInValues(
                        values.values, remove_zeros_width
                    )
                )
        single = pd.Series(single_output, dtype=object)
        multi = pd.DataFrame.from_records(records, columns=columns)
        return single, multi

    def GetStockBasicInfoAsDict(self, code, rqname=None, scrno=None):
        """
        주식 종목의 기본정보를 딕셔너리 형태로 반환합니다.

        TR: OPT10001
        """
        if rqname is None:
            rqname = "주식기본정보요청"
        trcode = "opt10001"
        inputs = {"종목코드": code}
        for response in self.TransactionCall(rqname, trcode, scrno, inputs):
            names = response.single_data.names
            values = response.single_data.values
            result = dict(zip(names, values))
        return result

    def GetStockBasicInfoAsSeries(self, code, rqname=None, scrno=None):
        """
        주식 종목의 기본정보를 pd.Series 형태로 반환합니다.

        TR: OPT10001
        """
        dic = self.GetStockBasicInfoAsDict(code, rqname, scrno)
        series = pd.Series(dic)
        return series

    def GetStockQuoteInfoAsDataFrame(self, codes=None, rqname=None, scrno=None):
        """
        복수개의 주식 종목들의 기본정보를 pd.DataFrame 형태로 반환합니다.

        TR: OPTKWFID
        """
        if codes is None:
            codes = self.GetGeneralCodeList()
        elif isinstance(codes, str):
            codes = [codes]
        if rqname is None:
            rqname = "관심종목정보요청"
        trcode = "OPTKWFID"
        columns = []
        records = []
        inputs = {"종목코드": ";".join(codes)}
        for response in self.TransactionCall(rqname, trcode, scrno, inputs):
            if not columns:
                columns = response.multi_data.names
            for values in response.multi_data.values:
                records.append(values.values)
        df = pd.DataFrame.from_records(records, columns=columns)
        return df

    def GetTickStockDataAsDataFrame(
        self,
        code,
        interval,
        start_date=None,
        end_date=None,
        include_end=False,
        adjusted_price=False,
        rqname=None,
        scrno=None,
    ):
        """
        틱 단위 차트 데이터를 pd.DataFrame 형태로 반환합니다.

        TR: OPT10079
        """
        if interval is not None:
            interval = int(interval)
            interval = str(interval)

        date_format = "%Y%m%d%H%M%S"
        date_column_name = "체결시간"

        if isinstance(start_date, datetime.datetime):
            start_date = start_date.strftime(date_format)

        if end_date is not None:
            if isinstance(end_date, datetime.datetime):
                end_date = end_date.strftime(date_format)
            stop_condition = {
                "name": date_column_name,
                "value": end_date,
            }
            if include_end:
                stop_condition["comparator"] = "<"
        else:
            stop_condition = None

        if rqname is None:
            rqname = "주식틱차트조회요청"
        trcode = "opt10079"
        inputs = {
            "종목코드": code,
            "틱범위": interval,
            "수정주가구분": "1" if adjusted_price else "0",
        }

        columns = []
        records = []

        date_column_index = None
        should_compare_start = start_date is not None

        for response in self.TransactionCall(
            rqname, trcode, scrno, inputs, stop_condition=stop_condition
        ):
            if not columns:
                columns = list(response.multi_data.names)
                if date_column_name in columns:
                    date_column_index = columns.index(date_column_name)
            for values in response.multi_data.values:
                if should_compare_start and date_column_index is not None:
                    date = values.values[date_column_index]
                    if date > start_date:
                        # 해당 TR 은 기준일자를 INPUT 으로 설정할 수 없는 이유로
                        # 일단 가장 최근부터 차례대로 가져오고 클라이언트에서 요청보다 최근 데이터는 버림
                        # 클라이언트 말고 서버에서 미리 처리해서 데이터를 보내지조차 않아야 할지??
                        continue
                    else:
                        should_compare_start = False
                records.append(values.values)

            if self.logger.isEnabledFor(logging.DEBUG):
                nrows = len(response.multi_data.values)
                if nrows > 0:
                    from_date = response.multi_data.values[0].values[date_column_index]
                    to_date = response.multi_data.values[-1].values[date_column_index]
                    from_date = datetime.datetime.strptime(from_date, date_format)
                    to_date = datetime.datetime.strptime(to_date, date_format)
                    self.logger.debug(
                        "Received %d records from %s to %s for code %s",
                        nrows,
                        from_date,
                        to_date,
                        code,
                    )

        df = pd.DataFrame.from_records(records, columns=columns)
        return df

    def GetMinuteStockDataAsDataFrame(
        self,
        code,
        interval,
        start_date=None,
        end_date=None,
        include_end=False,
        adjusted_price=False,
        rqname=None,
        scrno=None,
    ):
        """
        분 단위 차트 데이터를 pd.DataFrame 형태로 반환합니다.

        TR: OPT10080
        """
        if interval is not None:
            interval = int(interval)
            interval = str(interval)

        date_format = "%Y%m%d%H%M%S"
        date_column_name = "체결시간"

        if isinstance(start_date, datetime.datetime):
            start_date = start_date.strftime(date_format)

        if end_date is not None:
            if isinstance(end_date, datetime.datetime):
                end_date = end_date.strftime(date_format)
            stop_condition = {
                "name": date_column_name,
                "value": end_date,
            }
            if include_end:
                stop_condition["comparator"] = "<"
        else:
            stop_condition = None

        if rqname is None:
            rqname = "주식분봉차트조회요청"
        trcode = "opt10080"
        inputs = {
            "종목코드": code,
            "틱범위": interval,
            "수정주가구분": "1" if adjusted_price else "0",
        }

        columns = []
        records = []

        date_column_index = None
        should_compare_start = start_date is not None

        for response in self.TransactionCall(
            rqname, trcode, scrno, inputs, stop_condition=stop_condition
        ):
            if not columns:
                columns = list(response.multi_data.names)
                if date_column_name in columns:
                    date_column_index = columns.index(date_column_name)
            for values in response.multi_data.values:
                if should_compare_start and date_column_index is not None:
                    date = values.values[date_column_index]
                    if date > start_date:
                        # 해당 TR 은 기준일자를 INPUT 으로 설정할 수 없는 이유로
                        # 일단 가장 최근부터 차례대로 가져오고 클라이언트에서 요청보다 최근 데이터는 버림
                        # 클라이언트 말고 서버에서 미리 처리해서 데이터를 보내지조차 않아야 할지??
                        continue
                    else:
                        should_compare_start = False
                records.append(values.values)

            if self.logger.isEnabledFor(logging.DEBUG):
                nrows = len(response.multi_data.values)
                if nrows > 0:
                    from_date = response.multi_data.values[0].values[date_column_index]
                    to_date = response.multi_data.values[-1].values[date_column_index]
                    from_date = datetime.datetime.strptime(from_date, date_format)
                    to_date = datetime.datetime.strptime(to_date, date_format)
                    self.logger.debug(
                        "Received %d records from %s to %s for code %s",
                        nrows,
                        from_date,
                        to_date,
                        code,
                    )

        df = pd.DataFrame.from_records(records, columns=columns)
        return df

    def GetDailyStockDataAsDataFrame(
        self,
        code,
        start_date=None,
        end_date=None,
        include_end=False,
        adjusted_price=False,
        rqname=None,
        scrno=None,
    ):
        """
        일 단위 차트 데이터를 pd.DataFrame 형태로 반환합니다.

        TR: OPT10081
        """
        date_format = "%Y%m%d"
        date_column_name = "일자"

        if isinstance(start_date, datetime.datetime):
            start_date = start_date.strftime(date_format)

        if end_date is not None:
            if isinstance(end_date, datetime.datetime):
                end_date = end_date.strftime(date_format)
            stop_condition = {
                "name": date_column_name,
                "value": end_date,
            }
            if include_end:
                stop_condition["comparator"] = "<"
        else:
            stop_condition = None

        if rqname is None:
            rqname = "주식일봉차트조회요청"

        trcode = "opt10081"
        inputs = {
            "종목코드": code,
            "수정주가구분": "1" if adjusted_price else "0",
        }
        if start_date is not None:
            inputs["기준일자"] = start_date

        columns = []
        records = []

        date_column_index = None

        for response in self.TransactionCall(
            rqname, trcode, scrno, inputs, stop_condition=stop_condition
        ):
            if not columns:
                columns = list(response.multi_data.names)
                if date_column_name in columns:
                    date_column_index = columns.index(date_column_name)
            for values in response.multi_data.values:
                records.append(values.values)

            if self.logger.isEnabledFor(logging.DEBUG):
                nrows = len(response.multi_data.values)
                if nrows > 0:
                    from_date = response.multi_data.values[0].values[date_column_index]
                    to_date = response.multi_data.values[-1].values[date_column_index]
                    from_date = datetime.datetime.strptime(from_date, date_format)
                    to_date = datetime.datetime.strptime(to_date, date_format)
                    self.logger.debug(
                        "Received %d records from %s to %s for code %s",
                        nrows,
                        from_date,
                        to_date,
                        code,
                    )

        df = pd.DataFrame.from_records(records, columns=columns)
        return df

    def GetWeeklyStockDataAsDataFrame(
        self,
        code,
        start_date=None,
        end_date=None,
        include_end=False,
        adjusted_price=False,
        rqname=None,
        scrno=None,
    ):
        """
        주 단위 차트 데이터를 pd.DataFrame 형태로 반환합니다.

        TR: OPT10082
        """
        date_format = "%Y%m%d"
        date_column_name = "일자"

        if isinstance(start_date, datetime.datetime):
            start_date = start_date.strftime(date_format)

        if end_date is not None:
            if isinstance(end_date, datetime.datetime):
                end_date = end_date.strftime(date_format)
            stop_condition = {
                "name": date_column_name,
                "value": end_date,
            }
            if include_end:
                stop_condition["comparator"] = "<"
        else:
            stop_condition = None

        if rqname is None:
            rqname = "주식주봉차트조회요청"

        trcode = "opt10082"
        inputs = {
            "종목코드": code,
            "수정주가구분": "1" if adjusted_price else "0",
        }
        if start_date is not None:
            inputs["기준일자"] = start_date
        if end_date is not None:
            inputs["끝일자"] = end_date  # 딱히 끝일자가 생각하는대로 안먹히는듯...

        columns = []
        records = []
        date_column_index = None

        for response in self.TransactionCall(
            rqname, trcode, scrno, inputs, stop_condition=stop_condition
        ):
            if not columns:
                columns = list(response.multi_data.names)
                if date_column_name in columns:
                    date_column_index = columns.index(date_column_name)
            for values in response.multi_data.values:
                records.append(values.values)

            if self.logger.isEnabledFor(logging.DEBUG):
                nrows = len(response.multi_data.values)
                if nrows > 0:
                    from_date = response.multi_data.values[0].values[date_column_index]
                    to_date = response.multi_data.values[-1].values[date_column_index]
                    from_date = datetime.datetime.strptime(from_date, date_format)
                    to_date = datetime.datetime.strptime(to_date, date_format)
                    self.logger.debug(
                        "Received %d records from %s to %s for code %s",
                        nrows,
                        from_date,
                        to_date,
                        code,
                    )

        df = pd.DataFrame.from_records(records, columns=columns)
        return df

    def GetMonthlyStockDataAsDataFrame(
        self,
        code,
        start_date=None,
        end_date=None,
        include_end=False,
        adjusted_price=False,
        rqname=None,
        scrno=None,
    ):
        """
        월 단위 차트 데이터를 pd.DataFrame 형태로 반환합니다.

        TR: OPT10083
        """
        date_format = "%Y%m%d"
        date_column_name = "일자"

        if isinstance(start_date, datetime.datetime):
            start_date = start_date.strftime(date_format)

        if end_date is not None:
            if isinstance(end_date, datetime.datetime):
                end_date = end_date.strftime(date_format)
            stop_condition = {
                "name": date_column_name,
                "value": end_date,
            }
            if include_end:
                stop_condition["comparator"] = "<"
        else:
            stop_condition = None

        if rqname is None:
            rqname = "주식월봉차트조회요청"

        trcode = "opt10083"
        inputs = {
            "종목코드": code,
            "수정주가구분": "1" if adjusted_price else "0",
        }
        if start_date is not None:
            inputs["기준일자"] = start_date
        if end_date is not None:
            inputs["끝일자"] = end_date  # 딱히 끝일자가 생각하는대로 안먹히는듯...

        columns = []
        records = []
        date_column_index = None

        for response in self.TransactionCall(
            rqname, trcode, scrno, inputs, stop_condition=stop_condition
        ):
            if not columns:
                columns = list(response.multi_data.names)
                if date_column_name in columns:
                    date_column_index = columns.index(date_column_name)
            for values in response.multi_data.values:
                records.append(values.values)

            if self.logger.isEnabledFor(logging.DEBUG):
                nrows = len(response.multi_data.values)
                if nrows > 0:
                    from_date = response.multi_data.values[0].values[date_column_index]
                    to_date = response.multi_data.values[-1].values[date_column_index]
                    from_date = datetime.datetime.strptime(from_date, date_format)
                    to_date = datetime.datetime.strptime(to_date, date_format)
                    self.logger.debug(
                        "Received %d records from %s to %s for code %s",
                        nrows,
                        from_date,
                        to_date,
                        code,
                    )

        df = pd.DataFrame.from_records(records, columns=columns)
        return df

    def GetYearlyStockDataAsDataFrame(
        self,
        code,
        start_date=None,
        end_date=None,
        include_end=False,
        adjusted_price=False,
        rqname=None,
        scrno=None,
    ):
        """
        년 단위 차트 데이터를 pd.DataFrame 형태로 반환합니다.

        TR: OPT10094
        """
        date_format = "%Y%m%d"
        date_column_name = "일자"

        if isinstance(start_date, datetime.datetime):
            start_date = start_date.strftime(date_format)

        if end_date is not None:
            if isinstance(end_date, datetime.datetime):
                end_date = end_date.strftime(date_format)
            stop_condition = {
                "name": date_column_name,
                "value": end_date,
            }
            if include_end:
                stop_condition["comparator"] = "<"
        else:
            stop_condition = None

        if rqname is None:
            rqname = "주식년봉차트조회요청"

        trcode = "opt10094"
        inputs = {
            "종목코드": code,
            "수정주가구분": "1" if adjusted_price else "0",
        }
        if start_date is not None:
            inputs["기준일자"] = start_date
        if end_date is not None:
            inputs["끝일자"] = end_date  # 딱히 끝일자가 생각하는대로 안먹히는듯...

        columns = []
        records = []
        date_column_index = None

        for response in self.TransactionCall(
            rqname, trcode, scrno, inputs, stop_condition=stop_condition
        ):
            if not columns:
                columns = list(response.multi_data.names)
                if date_column_name in columns:
                    date_column_index = columns.index(date_column_name)
            for values in response.multi_data.values:
                records.append(values.values)

            if self.logger.isEnabledFor(logging.DEBUG):
                nrows = len(response.multi_data.values)
                if nrows > 0:
                    from_date = response.multi_data.values[0].values[date_column_index]
                    to_date = response.multi_data.values[-1].values[date_column_index]
                    from_date = datetime.datetime.strptime(from_date, date_format)
                    to_date = datetime.datetime.strptime(to_date, date_format)
                    self.logger.debug(
                        "Received %d records from %s to %s for code %s",
                        nrows,
                        from_date,
                        to_date,
                        code,
                    )

        df = pd.DataFrame.from_records(records, columns=columns)
        return df

    def GetDepositInfo(
        self, account_no, lookup_type=None, with_multi=False, rqname=None, scrno=None
    ):
        """
        계좌의 예수금 정보를 반환합니다.

        TR: OPW00001

        조회구분 = 3:추정조회, 2:일반조회
        """
        if rqname is None:
            rqname = "예수금상세현황요청"
        trcode = "opw00001"
        inputs = {
            "계좌번호": account_no,
            "비밀번호": "",
            "비밀번호입력매체구분": "00",
            "조회구분": "2" if lookup_type is None else lookup_type,
        }
        responses = self.TransactionCall(rqname, trcode, scrno, inputs)
        single, multi = self._ParseTransactionCallResponses(responses, [12, 15])
        if with_multi:
            return single, multi
        else:
            return single

    def GetStockQuotes(self, code, rqname=None, scrno=None):
        """
        주식의 호가정보를 반환합니다.

        TR: OPT10004
        """
        if rqname is None:
            rqname = "주식호가요청"
        trcode = "opt10004"
        inputs = {
            "종목코드": code,
        }
        responses = self.TransactionCall(rqname, trcode, scrno, inputs)
        single, _multi = self._ParseTransactionCallResponses(responses, [12, 15])
        return single

    def GetOrderLogAsDataFrame1(
        self,
        account_no,
        order_type=None,
        status_type=None,
        code=None,
        rqname=None,
        scrno=None,
    ):
        """
        미체결 주문 정보를 반환합니다.

        TR: OPT10075

        계좌번호 = 전문 조회할 보유계좌번호
        전체종목구분 = 0:전체, 1:종목
        매매구분 = 0:전체, 1:매도, 2:매수
        종목코드 = 전문 조회할 종목코드
        체결구분 = 0:전체, 2:체결, 1:미체결
        """

        if rqname is None:
            rqname = "실시간미체결요청"
        trcode = "opt10075"
        inputs = {
            "계좌번호": account_no,
            "전체종목구분": "0" if code is None else "1",
            "매매구분": "0" if order_type is None else order_type,
            "종목코드": "" if code is None else code,
            "체결구분": "0" if status_type is None else status_type,
        }
        responses = self.TransactionCall(rqname, trcode, scrno, inputs)
        _single, multi = self._ParseTransactionCallResponses(responses)
        return multi

    def GetOrderLogAsDataFrame2(
        self,
        account_no,
        order_type=None,
        status_type=None,
        code=None,
        order_no=None,
        rqname=None,
        scrno=None,
    ):
        """
        주문 체결 정보를 반환합니다.

        TR: OPT10076

        종목코드 = 전문 조회할 종목코드
        조회구분 = 0:전체, 1:종목
        매도수구분 = 0:전체, 1:매도, 2:매수
        계좌번호 = 전문 조회할 보유계좌번호
        비밀번호 = 사용안함(공백)
        주문번호 = 조회할 주문번호
        체결구분 = 0:전체, 2:체결, 1:미체결
        """

        if rqname is None:
            rqname = "실시간체결요청"
        trcode = "opt10076"
        inputs = {
            "종목코드": "" if code is None else code,
            "조회구분": "0" if code is None else "1",
            "매도수구분": "0" if order_type is None else order_type,
            "계좌번호": account_no,
            "비밀번호": "",
            "주문번호": "" if order_no is None else order_no,
            "체결구분": "0" if status_type is None else status_type,
        }
        responses = self.TransactionCall(rqname, trcode, scrno, inputs)
        _single, multi = self._ParseTransactionCallResponses(responses)
        return multi

    def GetOrderLogAsDataFrame3(
        self,
        account_no,
        date=None,
        sort_type=None,
        asset_type=None,
        order_type=None,
        code=None,
        starting_order_no=None,
        rqname=None,
        scrno=None,
    ):
        """
        계좌별 주문 체결 내역을 반환합니다.

        TR: OPW00007

        주문일자 = YYYYMMDD (20170101 연도4자리, 월 2자리, 일 2자리 형식)
        계좌번호 = 전문 조회할 보유계좌번호
        비밀번호 = 사용안함(공백)
        비밀번호입력매체구분 = 00
        조회구분 = 1:주문순, 2:역순, 3:미체결, 4:체결내역만
        주식채권구분 = 0:전체, 1:주식, 2:채권
        매도수구분 = 0:전체, 1:매도, 2:매수
        종목코드
        시작주문번호
        """

        if rqname is None:
            rqname = "계좌별주문체결내역상세요청"
        trcode = "opw00007"
        if date is None:
            now = datetime.datetime.now()
            market_start_time = now.replace(hour=8, minute=20, second=0, microsecond=0)
            if now < market_start_time:
                now = now - datetime.timedelta(days=1)
            date = now.strftime("%Y%m%d")
        inputs = {
            "주문일자": date,
            "계좌번호": account_no,
            "비밀번호": "",
            "비밀번호입력매체구분": "00",
            "조회구분": "1" if sort_type is None else sort_type,
            "주식채권구분": "0" if asset_type is None else asset_type,
            "매도수구분": "0" if order_type is None else order_type,
            "종목코드": "" if code is None else code,
            "시작주문번호": "" if starting_order_no is None else starting_order_no,
        }
        responses = self.TransactionCall(rqname, trcode, scrno, inputs)
        _single, multi = self._ParseTransactionCallResponses(responses, 10)
        return multi

    def GetAccountRateOfReturnAsDataFrame(self, account_no, rqname=None, scrno=None):
        """
        계좌별 수익률 정보를 반환합니다.

        TR: OPT10085
        """
        if rqname is None:
            rqname = "계좌수익률요청"
        trcode = "opt10085"
        inputs = {
            "계좌번호": account_no,
        }
        responses = self.TransactionCall(rqname, trcode, scrno, inputs)
        _single, multi = self._ParseTransactionCallResponses(responses, 10)
        return multi

    def GetAccountEvaluationStatusAsSeriesAndDataFrame(
        self, account_no, include_delisted=True, rqname=None, scrno=None
    ):
        """
        계좌의 평가 현황 정보를 반환합니다.

        TR: OPW00004
        """
        if rqname is None:
            rqname = "계좌평가현황요청"
        trcode = "opw00004"
        inputs = {
            "계좌번호": account_no,
            "비밀번호": "",
            "상장폐지조회구분": "0" if include_delisted else "1",
            "비밀번호입력매체구분": "00",
        }
        responses = self.TransactionCall(rqname, trcode, scrno, inputs)
        single, multi = self._ParseTransactionCallResponses(responses, 12)
        return single, multi

    def GetAccountExecutionBalanceAsSeriesAndDataFrame(
        self, account_no, rqname=None, scrno=None
    ):
        """
        계좌의 체결 잔고 정보를 반환합니다.

        TR: OPW00005

        모의투자에서는 지원하지 않는 TR 입니다.
        """
        server = self.GetServerGubun()
        if server == "1":
            self.logger.warning("Not supported for simulated investment")
        if rqname is None:
            rqname = "체결잔고요청"
        if scrno is None:
            scrno = "1010"
        trcode = "opw00005"  # 모의투자에서 지원하지 않는 TR
        inputs = {
            "계좌번호": account_no,
            "비밀번호": "",
            "비밀번호입력매체구분": "00",
        }
        responses = self.TransactionCall(rqname, trcode, scrno, inputs)
        single, multi = self._ParseTransactionCallResponses(responses, 0)
        return single, multi

    def GetAccountEvaluationBalanceAsSeriesAndDataFrame(
        self, account_no, lookup_type=None, rqname=None, scrno=None
    ):
        """
        계좌의 평가 잔고 내역 정보를 반환합니다.

        TR: OPW00018

        조회구분 = 1:합산, 2:개별

        [ 주의 ]
        "수익률%" 데이터는 모의투자에서는 소숫점표현, 실거래서버에서는 소숫점으로 변환 필요 합니다.
        """
        if rqname is None:
            rqname = "계좌평가잔고내역요청"
        trcode = "opw00018"
        inputs = {
            "계좌번호": account_no,
            "비밀번호": "",
            "비밀번호입력매체구분": "00",
            "조회구분": "2" if lookup_type is None else str(lookup_type),
        }
        responses = self.TransactionCall(rqname, trcode, scrno, inputs)
        single, multi = self._ParseTransactionCallResponses(responses, [12, 15])
        return single, multi

    def GetMarketPriceInfo(self, code, rqname=None, scrno=None):
        """
        종목의 시세표성 정보를 반환합니다.

        TR: OPT10007
        """
        if rqname is None:
            rqname = "시세표성정보요청"
        trcode = "opt10007"
        inputs = {
            "종목코드": code,
        }
        responses = self.TransactionCall(rqname, trcode, scrno, inputs)
        single, _multi = self._ParseTransactionCallResponses(responses)
        return single

    def GetRealDataForCodesAsStream(
        self,
        codes,
        fids=None,
        opt_type=None,
        screen_no=None,
        infer_fids=False,
        readable_names=False,
        fast_parse=False,
    ):
        """
        실시간 데이터를 요청하고 스트림 형태로 반환받습니다.
        """
        if isinstance(codes, str):
            codes = [codes]
        if fids is None:
            from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusRealType import (
                KiwoomOpenApiPlusRealType,
            )

            fids = KiwoomOpenApiPlusRealType.get_fids_by_realtype_name("주식시세")
        if opt_type is None:
            opt_type = "0"
        assert opt_type in ["0", "1"], "opt_type should be either 0 or 1"
        responses = self.RealCall(
            screen_no, codes, fids, opt_type, infer_fids, readable_names, fast_parse
        )
        return responses

    def GetCodeListByCondition(
        self,
        condition_name,
        condition_index=None,
        with_info=False,
        is_future_option=False,
        request_name=None,
        screen_no=None,
    ):
        """
        주어진 조건식으로 조건검색을 수행하고
        검색된 종목의 종목코드를 리스트로 반환받습니다.

        파라미터 중 with_info 가 True 로 설정된 경우,
        검색된 종목들에 대한 기본 정보도 추가로 같이 반환됩니다.
        """
        search_type = 0

        if condition_index is None:
            condition_names = self.GetConditionNameListAsList()
            condition_indices = {item[1]: item[0] for item in condition_names}
            condition_index = condition_indices[condition_name]

        codes = []

        single_output = None
        columns = []
        records = []
        remove_zeros_width = None

        for response in self.ConditionCall(
            screen_no,
            condition_name,
            condition_index,
            search_type,
            with_info,
            is_future_option,
            request_name,
        ):
            if response.name == "OnReceiveTrCondition":
                code_list = response.arguments[1].string_value
                code_list = code_list.rstrip(";").split(";") if code_list else []
                codes.extend(code_list)
            elif response.name == "OnReceiveTrData":
                if single_output is None:
                    single_output = dict(
                        zip(
                            response.single_data.names,
                            self._RemoveLeadingZerosForNumbersInValues(
                                response.single_data.values, remove_zeros_width
                            ),
                        )
                    )
                if not columns:
                    columns = response.multi_data.names
                for values in response.multi_data.values:
                    records.append(
                        self._RemoveLeadingZerosForNumbersInValues(
                            values.values, remove_zeros_width
                        )
                    )
            else:
                raise ValueError("Unexpected event handler name %s" % response.name)

        _single = pd.Series(single_output, dtype=object)
        multi = pd.DataFrame.from_records(records, columns=columns)

        if with_info:
            return codes, multi
        else:
            return codes

    def _GetCodeListByConditionAsStream_GeneratorFunc(self, responses, with_info=False):
        for response in responses:
            if response.name == "OnReceiveTrCondition":
                code_list = response.arguments[1].string_value
                code_list = code_list.rstrip(";").split(";") if code_list else []
                inserted = code_list
                deleted = []
                if with_info:
                    info = None
                    yield inserted, deleted, info
                else:
                    yield inserted, deleted
            elif response.name == "OnReceiveRealCondition":
                code = response.arguments[0].string_value
                condition_type = response.arguments[1].string_value
                inserted = []
                deleted = []
                if condition_type == "I":
                    inserted.append(code)
                elif condition_type == "D":
                    deleted.append(code)
                else:
                    raise ValueError("Unexpected condition type %s" % condition_type)
                if with_info:
                    info = None
                    yield inserted, deleted, info
                else:
                    yield inserted, deleted
            elif response.name == "OnReceiveTrData":
                single_output = None
                columns = []
                records = []
                remove_zeros_width = None
                if single_output is None:
                    single_output = dict(
                        zip(
                            response.single_data.names,
                            self._RemoveLeadingZerosForNumbersInValues(
                                response.single_data.values, remove_zeros_width
                            ),
                        )
                    )
                if not columns:
                    columns = response.multi_data.names
                for values in response.multi_data.values:
                    records.append(
                        self._RemoveLeadingZerosForNumbersInValues(
                            values.values, remove_zeros_width
                        )
                    )
                _single = pd.Series(single_output, dtype=object)
                multi = pd.DataFrame.from_records(records, columns=columns)
                inserted = []
                deleted = []
                if with_info:
                    info = multi
                    yield inserted, deleted, info
                else:
                    raise RuntimeError(
                        "Unexpected, OnReceiveTrData event with with_info=False ???"
                    )
            else:
                raise ValueError("Unexpected event handler name %s" % response.name)

    def GetCodeListByConditionAsStream(
        self,
        condition_name,
        condition_index=None,
        with_info=False,
        is_future_option=False,
        request_name=None,
        screen_no=None,
        old_behavior=False,
    ):
        """
        주어진 조건식을 실시간 조건검색으로 등록합니다.
        이후 발생하는 이벤트들을 스트림 형태로 제공합니다.

        최초 검색결과는 OnReceiveTrCondition() 이벤트로 반환되며
        이후 종목의 추가/제외는 OnReceiveRealCondition() 이벤트로 반환됩니다.

        만약 with_info 가 True 로 설정된 경우,
        검색된 종목마다 추가적인 정보가 OnReceiveTrData() 이벤트를 통해 반환됩니다.
        """
        search_type = 1

        if condition_index is None:
            condition_names = self.GetConditionNameListAsList()
            condition_indices = {item[1]: item[0] for item in condition_names}
            condition_index = condition_indices[condition_name]

        responses = self.ConditionCall(
            screen_no,
            condition_name,
            condition_index,
            search_type,
            with_info,
            is_future_option,
            request_name,
        )

        if not old_behavior:
            return responses

        stream = PipeableMultiThreadedRendezvous(responses)
        stream = stream.pipe(
            lambda responses: self._GetCodeListByConditionAsStream_GeneratorFunc(
                responses, with_info=with_info
            )
        )

        return stream


class KiwoomOpenApiPlusServiceClientStubWrapper(
    KiwoomOpenApiPlusServiceClientStubExtendedWrapper
):
    """
    KiwoomOpenApiPlusServiceClientStubCoreWrapper, KiwoomOpenApiPlusServiceClientStubExtendedWrapper 의 구현 및
    KiwoomOpenApiPlusQAxWidgetUniversalMixin 의 구현들까지 최종적으로 포함된
    KiwoomOpenApiPlusServiceClientStub 객체를 위한 Mixin 래퍼 클래스 입니다.
    """
