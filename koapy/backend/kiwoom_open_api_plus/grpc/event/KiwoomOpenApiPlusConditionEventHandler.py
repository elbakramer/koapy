from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError import (
    KiwoomOpenApiPlusError,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusTrInfo import (
    KiwoomOpenApiPlusTrInfo,
)
from koapy.backend.kiwoom_open_api_plus.grpc import KiwoomOpenApiPlusService_pb2
from koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlerForGrpc import (
    KiwoomOpenApiPlusEventHandlerForGrpc,
)
from koapy.backend.kiwoom_open_api_plus.utils.list_conversion import string_to_list
from koapy.utils.logging.Logging import Logging


class KiwoomOpenApiPlusConditionEventHandler(
    KiwoomOpenApiPlusEventHandlerForGrpc, Logging
):
    def __init__(self, control, request, context, screen_manager):
        super().__init__(control, context)
        self._request = request
        self._screen_manager = screen_manager

        self._screen_no = request.screen_no
        self._condition_name = request.condition_name
        self._condition_index = request.condition_index
        self._search_type = request.search_type

        self._request_name = request.request_name or "관심종목정보요청"
        self._with_info = request.flags.with_info
        self._is_future_option = request.flags.is_future_option
        self._type_flag = 3 if self._is_future_option else 0

        self._trcode = {0: "OPTKWFID", 3: "OPTFOFID"}[self._type_flag]
        self._trinfo = KiwoomOpenApiPlusTrInfo.get_trinfo_by_code(self._trcode)

        if self._trinfo is None:
            self.logger.error("Cannot find names for trcode %s", self._trinfo)

        self._single_names = self._trinfo.get_single_output_names()
        self._multi_names = self._trinfo.get_multi_output_names()

    def on_enter(self):
        self.control.EnsureConditionLoaded()
        condition_names = self.control.GetConditionNameListAsList()
        assert (self._condition_index, self._condition_name) in condition_names
        self._screen_no = self._screen_manager.borrow_screen(self._screen_no)
        self.add_callback(self._screen_manager.return_screen, self._screen_no)
        self.add_callback(self.control.DisconnectRealData, self._screen_no)
        self.add_callback(
            self.control.SendConditionStop,
            self._screen_no,
            self._condition_name,
            self._condition_index,
        )
        KiwoomOpenApiPlusError.try_or_raise_boolean(
            self.control.RateLimitedSendCondition.queuedCall(
                self._screen_no,
                self._condition_name,
                self._condition_index,
                self._search_type,
            ),
            "Failed to send condition",
            except_callback=self.observer.on_error,
        )

    def OnReceiveTrCondition(
        self, scrnno, codelist, condition_name, condition_index, prevnext
    ):
        if (scrnno, condition_name, condition_index) == (
            self._screen_no,
            self._condition_name,
            self._condition_index,
        ):
            response = KiwoomOpenApiPlusService_pb2.ListenResponse()
            response.name = "OnReceiveTrCondition"
            response.arguments.add().string_value = scrnno
            response.arguments.add().string_value = codelist
            response.arguments.add().string_value = condition_name
            response.arguments.add().long_value = condition_index
            response.arguments.add().long_value = prevnext

            self.observer.on_next(response)

            if self._with_info:
                if "^" in codelist:
                    items = string_to_list(codelist, sep=";")
                    items = [string_to_list(item, sep="^") for item in items]
                    items = [tuple(item) for item in items]
                    codes = [item[0] for item in items]
                else:
                    codes = string_to_list(codelist, sep=";")
                KiwoomOpenApiPlusError.try_or_raise(
                    self.control.RateLimitedCommKwRqData.queuedCall(
                        codelist,
                        0,
                        len(codes),
                        self._type_flag,
                        self._request_name,
                        self._screen_no,
                    ),
                    except_callback=self.observer.on_error,
                )

            should_continue = str(prevnext) not in ["", "0"]
            should_not_complete = (
                self._search_type == 1 or self._with_info or should_continue
            )
            should_complete = not should_not_complete

            if should_complete:
                self.observer.on_completed()
                return
            elif should_continue:
                try:
                    raise KiwoomOpenApiPlusError("Should not reach here")
                    # pylint: disable=unreachable
                    self.control.RateLimitedSendCondition.queuedCall(
                        self._screen_no,
                        self._condition_name,
                        self._condition_index,
                        int(prevnext),
                    )
                except KiwoomOpenApiPlusError as e:
                    self.observer.on_error(e)
                    return

    def OnReceiveRealCondition(
        self, code, condition_type, condition_name, condition_index
    ):
        if (condition_name, int(condition_index)) == (
            self._condition_name,
            self._condition_index,
        ):
            response = KiwoomOpenApiPlusService_pb2.ListenResponse()
            response.name = "OnReceiveRealCondition"
            response.arguments.add().string_value = code
            response.arguments.add().string_value = condition_type
            response.arguments.add().string_value = condition_name
            response.arguments.add().string_value = condition_index

            self.observer.on_next(response)

            if self._with_info:
                codelist = code
                codes = [code]
                KiwoomOpenApiPlusError.try_or_raise(
                    self.control.RateLimitedCommKwRqData.queuedCall(
                        codelist,
                        0,
                        len(codes),
                        self._type_flag,
                        self._request_name,
                        self._screen_no,
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
        _datalength,
        _errorcode,
        _message,
        _splmmsg,
    ):
        if (scrnno, rqname) == (self._screen_no, self._request_name):
            response = KiwoomOpenApiPlusService_pb2.ListenResponse()
            response.name = "OnReceiveTrData"
            response.arguments.add().string_value = scrnno
            response.arguments.add().string_value = rqname
            response.arguments.add().string_value = trcode
            response.arguments.add().string_value = recordname
            response.arguments.add().string_value = prevnext

            should_continue = str(prevnext) not in ["", "0"]
            should_not_complete = self._search_type == 1 or should_continue
            should_complete = not should_not_complete

            repeat_cnt = self.control.GetRepeatCnt(trcode, recordname)

            assert trcode.upper() == self._trcode

            if repeat_cnt > 0:
                if len(self._multi_names) == 0:
                    self.logger.warning(
                        "Repeat count greater than 0, but no multi data names available, fallback to sigle data names"
                    )
                    multi_names = self._multi_names
                    self._multi_names = self._single_names
                    self._single_names = multi_names
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
                        response.multi_data.values.add().values.extend(row)

            if len(self._single_names) > 0:
                values = [
                    self.control.GetCommData(trcode, recordname, 0, name).strip()
                    for name in self._single_names
                ]
                response.single_data.names.extend(self._single_names)
                response.single_data.values.extend(values)

            self.observer.on_next(response)

            if should_complete:
                self.observer.on_completed()
                return
            elif should_continue:
                try:
                    raise KiwoomOpenApiPlusError("Should not reach here")
                    # pylint: disable=unreachable
                    KiwoomOpenApiPlusError.try_or_raise(
                        self.control.RateLimitedCommKwRqData.queuedCall(
                            self._codelist,
                            int(prevnext),
                            len(self._codes),
                            3 if self._is_future_option else 0,
                            self._request_name,
                            self._screen_no,
                        ),
                        except_callback=self.observer.on_error,
                    )
                except KiwoomOpenApiPlusError as e:
                    self.observer.on_error(e)
                    return
