import datetime
import logging
import queue
import re

import pandas as pd

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError import (
    KiwoomOpenApiPlusNegativeReturnCodeError,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEventHandlerFunctions import (
    KiwoomOpenApiPlusEventHandlerFunctions,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin import (
    KiwoomOpenApiPlusSimpleQAxWidgetMixin,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignature import (
    KiwoomOpenApiPlusDispatchSignature,
    KiwoomOpenApiPlusEventHandlerSignature,
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
    KiwoomOpenApiPlusSimpleQAxWidgetMixin
):
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
        return KiwoomOpenApiPlusServiceClientSideDynamicCallable(self._stub, name)(
            *args
        )

    def LoginCall(self, credential=None):
        # pylint: disable=no-member
        request = KiwoomOpenApiPlusService_pb2.LoginRequest()
        if credential is not None:
            request.credential.user_id = credential.get(
                "user_id"
            )  # pylint: disable=no-member
            request.credential.user_password = credential.get(
                "user_password"
            )  # pylint: disable=no-member
            request.credential.cert_password = credential.get(
                "cert_password"
            )  # pylint: disable=no-member
            request.credential.is_simulation = credential.get(
                "is_simulation"
            )  # pylint: disable=no-member
            account_passwords = credential.get(
                "account_passwords"
            )  # pylint: disable=no-member
            for account_no, account_password in account_passwords.items():
                request.credential.account_passwords[
                    account_no
                ] = account_password  # pylint: disable=no-member
        for response in self._stub.LoginCall(request):
            errcode = response.arguments[0].long_value
        return errcode

    def TransactionCall(self, rqname, trcode, scrno, inputs, stop_condition=None):
        # pylint: disable=no-member
        request = KiwoomOpenApiPlusService_pb2.TransactionRequest()
        request.request_name = rqname
        request.transaction_code = trcode
        request.screen_no = scrno or ""
        for k, v in inputs.items():
            request.inputs[k] = v  # pylint: disable=no-member
        if stop_condition:
            request.stop_condition.name = stop_condition.get(
                "name", ""
            )  # pylint: disable=no-member
            request.stop_condition.value = str(
                stop_condition.get("value", "")
            )  # pylint: disable=no-member
            request.stop_condition.comparator = {  # pylint: disable=no-member
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
        [거래구분]
          모의투자에서는 지정가 주문과 시장가 주문만 가능합니다.

          00 : 지정가
          03 : 시장가
          05 : 조건부지정가
          06 : 최유리지정가
          07 : 최우선지정가
          10 : 지정가IOC
          13 : 시장가IOC
          16 : 최유리IOC
          20 : 지정가FOK
          23 : 시장가FOK
          26 : 최유리FOK
          61 : 장전시간외종가
          62 : 시간외단일가매매
          81 : 장후시간외종가

        [주문유형]
          1:신규매수, 2:신규매도 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정
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
        request.screen_no.extend(scrnos)  # pylint: disable=no-member
        request.code_list.extend(codes)  # pylint: disable=no-member
        request.fid_list.extend(fids)  # pylint: disable=no-member
        request.opt_type = opt_type
        request.flags.infer_fids = infer_fids  # pylint: disable=no-member
        request.flags.readable_names = readable_names  # pylint: disable=no-member
        request.flags.fast_parse = fast_parse  # pylint: disable=no-member
        return self._stub.RealCall(request)

    def LoadConditionCall(self):
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
        request = request = KiwoomOpenApiPlusService_pb2.ConditionRequest()
        request.screen_no = scrno or ""
        request.condition_name = condition_name
        request.condition_index = condition_index
        request.search_type = search_type
        request.flags.with_info = with_info  # pylint: disable=no-member
        request.flags.is_future_option = is_future_option  # pylint: disable=no-member
        if request_name is not None:
            request.request_name = request_name
        return self._stub.ConditionCall(request)

    def SetLogLevel(self, level, logger=""):
        request = KiwoomOpenApiPlusService_pb2.SetLogLevelRequest()
        request.level = level
        request.logger = logger
        return self._stub.SetLogLevel(request)

    def _LoadConditionUsingCall(self):
        return self.Call("LoadCondition")

    def LoadCondition(self):
        return self._LoadConditionUsingCall()

    def _EnsureConditionLoadedUsingCall(self, force=False):
        return self.Call("EnsureConditionLoaded", force)

    def EnsureConditionLoaded(self, force=False):
        return self._EnsureConditionLoadedUsingCall(force)

    def _RateLimitedCommRqDataUsingCall(
        self, rqname, trcode, prevnext, scrno, inputs=None
    ):
        return self.Call(
            "RateLimitedCommRqData", rqname, trcode, prevnext, scrno, inputs
        )

    def RateLimitedCommRqData(self, rqname, trcode, prevnext, scrno, inputs=None):
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
        return self._RateLimitedSendConditionUsingCall(
            scrno, condition_name, condition_index, search_type
        )


class KiwoomOpenApiPlusServiceClientStubWrapper(
    KiwoomOpenApiPlusServiceClientStubCoreWrapper, Logging
):
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
        dic = self.GetStockBasicInfoAsDict(code, rqname, scrno)
        series = pd.Series(dic)
        return series

    def GetStockQuoteInfoAsDataFrame(self, codes=None, rqname=None, scrno=None):
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

            if self.logger.getEffectiveLevel() <= logging.DEBUG:
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

            if self.logger.getEffectiveLevel() <= logging.DEBUG:
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

            if self.logger.getEffectiveLevel() <= logging.DEBUG:
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

            if self.logger.getEffectiveLevel() <= logging.DEBUG:
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

            if self.logger.getEffectiveLevel() <= logging.DEBUG:
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

            if self.logger.getEffectiveLevel() <= logging.DEBUG:
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
