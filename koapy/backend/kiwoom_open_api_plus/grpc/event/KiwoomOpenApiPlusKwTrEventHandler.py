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
from koapy.utils.itertools import chunk
from koapy.utils.logging.Logging import Logging


class KiwoomOpenApiPlusKwTrEventHandler(KiwoomOpenApiPlusEventHandlerForGrpc, Logging):

    _num_codes_per_request = 100

    def __init__(self, control, request, context, screen_manager):
        super().__init__(control, context)
        self._request = request
        self._screen_manager = screen_manager

        self._rqname = request.request_name
        self._trcode = request.transaction_code.upper()
        self._scrnno = request.screen_no
        self._inputs = request.inputs

        assert self._trcode in ["OPTKWFID", "OPTFOFID"]

        self._type_flag = {"OPTKWFID": 0, "OPTFOFID": 3}[self._trcode]

        self._trinfo = KiwoomOpenApiPlusTrInfo.get_trinfo_by_code(self._trcode)

        if self._trinfo is None:
            self.logger.error("Cannot find names for trcode %s", self._trinfo)

        self._input_code = self._inputs.get("종목코드")

        self._code_list = self._input_code.rstrip(";").split(";")
        self._code_lists = [
            codes for codes in chunk(self._code_list, self._num_codes_per_request)
        ]
        self._scrnnos = [None for _ in range(len(self._code_lists))]
        self._scrnnos[0] = self._scrnno
        self._scrnnos_completed = {}

        self._single_names = self._trinfo.get_single_output_names()
        self._multi_names = self._trinfo.get_multi_output_names()

        stop_condition = request.stop_condition
        stop_condition_is_valid = all(
            [
                stop_condition is not None,
                stop_condition.name is not None,
                len(stop_condition.name) > 0,
                stop_condition.name in self._multi_names,
            ]
        )

        if stop_condition_is_valid:
            column_index_to_check = self._multi_names.index(stop_condition.name)
            comparator = {
                KiwoomOpenApiPlusService_pb2.TransactionStopConditionCompartor.LESS_THAN_OR_EQUAL_TO: operator.le,
                KiwoomOpenApiPlusService_pb2.TransactionStopConditionCompartor.LESS_THAN: operator.lt,
                KiwoomOpenApiPlusService_pb2.TransactionStopConditionCompartor.GREATER_THAN_OR_EQUAL_TO: operator.ge,
                KiwoomOpenApiPlusService_pb2.TransactionStopConditionCompartor.GREATER_THAN: operator.gt,
                KiwoomOpenApiPlusService_pb2.TransactionStopConditionCompartor.EQUAL_TO: operator.eq,
                KiwoomOpenApiPlusService_pb2.TransactionStopConditionCompartor.NOT_EQUAL_TO: operator.ne,
            }.get(stop_condition.comparator, operator.le)

            def is_stop_condition(row):
                return comparator(row[column_index_to_check], stop_condition.value)

        else:

            def is_stop_condition(_):
                return False

        self._is_stop_condition = is_stop_condition

    def on_enter(self):
        for i, scrnno in enumerate(self._scrnnos):
            scrnno = self._screen_manager.borrow_screen(scrnno)
            self._scrnnos[i] = scrnno
            self._scrnnos_completed[scrnno] = False
        for codes, scrnno in zip(self._code_lists, self._scrnnos):
            self.add_callback(self._screen_manager.return_screen, scrnno)
            self.add_callback(self.control.DisconnectRealData, scrnno)
            KiwoomOpenApiPlusError.try_or_raise(
                self.control.RateLimitedCommKwRqData.async_call(
                    ";".join(codes),
                    0,
                    len(codes),
                    self._type_flag,
                    self._rqname,
                    scrnno,
                ),
                except_callback=lambda e: self.observer.on_error(e)
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
        if (rqname, trcode) == (self._rqname, self._trcode) and scrnno in self._scrnnos:
            response = KiwoomOpenApiPlusService_pb2.ListenResponse()
            response.name = "OnReceiveTrData"  # pylint: disable=no-member
            response.arguments.add().string_value = scrnno  # pylint: disable=no-member
            response.arguments.add().string_value = rqname  # pylint: disable=no-member
            response.arguments.add().string_value = trcode  # pylint: disable=no-member
            response.arguments.add().string_value = (
                recordname  # pylint: disable=no-member
            )
            response.arguments.add().string_value = (
                prevnext  # pylint: disable=no-member
            )

            should_stop = prevnext in ["", "0"]
            repeat_cnt = self.control.GetRepeatCnt(trcode, recordname)

            if repeat_cnt > 0:
                if len(self._multi_names) == 0:
                    self.logger.warning(
                        "Repeat count greater than 0, but no multi data names available, fallback to sigle data names"
                    )
                    multi_names = self._multi_names
                    self._multi_names = self._single_names
                    self._single_name = multi_names
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
                    response.multi_data.names.extend(
                        self._multi_names
                    )  # pylint: disable=no-member
                    for row in rows:
                        if self._is_stop_condition(row):
                            should_stop = True
                            break
                        response.multi_data.values.add().values.extend(
                            row
                        )  # pylint: disable=no-member

            if len(self._single_names) > 0:
                values = [
                    self.control.GetCommData(trcode, recordname, 0, name).strip()
                    for name in self._single_names
                ]
                response.single_data.names.extend(
                    self._single_names
                )  # pylint: disable=no-member
                response.single_data.values.extend(values)  # pylint: disable=no-member

            self.observer.on_next(response)

            if should_stop:
                self._scrnnos_completed[scrnno] = True
                if all(self._scrnnos_completed.values()):
                    self.observer.on_completed()
                    return
            else:
                try:
                    raise KiwoomOpenApiPlusError("Should not reach here")
                except KiwoomOpenApiPlusError as e:
                    self.observer.on_error(e)
                    return

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
