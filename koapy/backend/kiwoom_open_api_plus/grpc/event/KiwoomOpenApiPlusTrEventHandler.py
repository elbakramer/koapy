import operator
import re

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError import (
    KiwoomOpenApiPlusError,
    KiwoomOpenApiPlusNegativeReturnCodeError,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusTrInfo import (
    KiwoomOpenApiPlusTrInfo,
)
from koapy.backend.kiwoom_open_api_plus.grpc import KiwoomOpenApiPlusService_pb2
from koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlerForGrpc import (
    KiwoomOpenApiPlusEventHandlerForGrpc,
)
from koapy.utils.logging.Logging import Logging


class KiwoomOpenApiPlusTrEventHandler(KiwoomOpenApiPlusEventHandlerForGrpc, Logging):
    def __init__(self, control, request, context, screen_manager):
        super().__init__(control, context)
        self._request = request
        self._screen_manager = screen_manager

        self._rqname = request.request_name
        self._trcode = request.transaction_code
        self._scrnno = request.screen_no
        self._inputs = request.inputs

        self._trinfo = KiwoomOpenApiPlusTrInfo.get_trinfo_by_code(self._trcode)

        if self._trinfo is None:
            self.logger.error("Cannot find names for trcode %s", self._trinfo)

        self._input_code = self._inputs.get("종목코드")

        self._single_names = self._trinfo.get_single_output_names()
        self._multi_names = self._trinfo.get_multi_output_names()

        stop_condition = request.stop_condition
        stop_condition_is_valid = (
            stop_condition is not None
            and stop_condition.name is not None
            and len(stop_condition.name) > 0
            and (
                stop_condition.name in self._multi_names
                or stop_condition.name in self._single_names
            )
        )

        if stop_condition_is_valid:
            comparator = {
                KiwoomOpenApiPlusService_pb2.TransactionStopConditionCompartor.LESS_THAN_OR_EQUAL_TO: operator.le,
                KiwoomOpenApiPlusService_pb2.TransactionStopConditionCompartor.LESS_THAN: operator.lt,
                KiwoomOpenApiPlusService_pb2.TransactionStopConditionCompartor.GREATER_THAN_OR_EQUAL_TO: operator.ge,
                KiwoomOpenApiPlusService_pb2.TransactionStopConditionCompartor.GREATER_THAN: operator.gt,
                KiwoomOpenApiPlusService_pb2.TransactionStopConditionCompartor.EQUAL_TO: operator.eq,
                KiwoomOpenApiPlusService_pb2.TransactionStopConditionCompartor.NOT_EQUAL_TO: operator.ne,
            }.get(stop_condition.comparator, operator.le)

            if stop_condition.name in self._multi_names:
                column_index_to_check = self._multi_names.index(stop_condition.name)
            else:
                # if it does not have multi_names, it may use single_names instead.
                column_index_to_check = self._single_names.index(stop_condition.name)

            def is_stop_condition(row):
                return comparator(row[column_index_to_check], stop_condition.value)

        else:

            def is_stop_condition(_):
                return False

        self._is_stop_condition = is_stop_condition

    def on_enter(self):
        self._scrnno = self._screen_manager.borrow_screen(self._scrnno)
        self.add_callback(self._screen_manager.return_screen, self._scrnno)
        self.add_callback(self.control.DisconnectRealData, self._scrnno)
        KiwoomOpenApiPlusError.try_or_raise(
            self.control.RateLimitedCommRqData.queuedCall(
                self._rqname, self._trcode, 0, self._scrnno, self._inputs
            ),
            except_callback=self.observer.on_error,
        )

    def OnReceiveTrData(
        self,
        scrnno,
        rqname,
        trcode,
        recordname,
        prevnext,
        datalength,
        errorcode,
        message,
        splmmsg,
    ):
        if (rqname, trcode, scrnno) == (self._rqname, self._trcode, self._scrnno):
            response = KiwoomOpenApiPlusService_pb2.ListenResponse()
            response.name = "OnReceiveTrData"
            response.arguments.add().string_value = scrnno
            response.arguments.add().string_value = rqname
            response.arguments.add().string_value = trcode
            response.arguments.add().string_value = recordname
            response.arguments.add().string_value = prevnext

            should_stop = prevnext in ["", "0"]
            repeat_cnt = self.control.GetRepeatCnt(trcode, recordname)

            if repeat_cnt > 0:
                if len(self._multi_names) == 0:
                    self.logger.warning(
                        "Repeat count greater than 0, but no multi data names available, fallback to sigle data names"
                    )
                    self._single_names, self._multi_names = (
                        self._multi_names,
                        self._single_names,
                    )
                if len(self._multi_names) > 0:
                    rows = [
                        [
                            self.control.GetCommData(
                                trcode, recordname, i, name
                            ).strip()
                            for name in self._multi_names
                        ]
                        for i in range(repeat_cnt)
                    ]
                    response.multi_data.names.extend(self._multi_names)
                    for row in rows:
                        if self._is_stop_condition(row):
                            should_stop = True
                            break
                        response.multi_data.values.add().values.extend(row)

            if len(self._single_names) > 0:
                values = [
                    self.control.GetCommData(trcode, recordname, 0, name).strip()
                    for name in self._single_names
                ]
                response.single_data.names.extend(self._single_names)
                response.single_data.values.extend(values)

            self.observer.on_next(response)

            if should_stop:
                self.observer.on_completed()
            else:
                KiwoomOpenApiPlusError.try_or_raise(
                    self.control.RateLimitedCommRqData.queuedCall(
                        rqname, trcode, int(prevnext), scrnno, self._inputs
                    ),
                    except_callback=self.observer.on_error,
                )

    def OnEventConnect(self, errcode):
        if errcode < 0:
            error = KiwoomOpenApiPlusNegativeReturnCodeError(errcode)
            self.observer.on_error(error)
            return

    def OnReceiveMsg(self, scrnno, rqname, trcode, msg):
        if (rqname, trcode, scrnno) == (self._rqname, self._trcode, self._scrnno):
            msg_pattern = r"^[^(]+\((-?[0-9]+)\)$"
            match = re.match(msg_pattern, msg)
            if match:
                errcode = match.group(1)
                errcode = int(errcode)
                error = KiwoomOpenApiPlusNegativeReturnCodeError(errcode, msg)
                self.observer.on_error(error)
                return
