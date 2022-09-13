from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError import (
    KiwoomOpenApiPlusError,
    KiwoomOpenApiPlusNegativeReturnCodeError,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusRealType import (
    KiwoomOpenApiPlusRealType,
)
from koapy.backend.kiwoom_open_api_plus.grpc import KiwoomOpenApiPlusService_pb2
from koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlerForGrpc import (
    KiwoomOpenApiPlusEventHandlerForGrpc,
)
from koapy.utils.logging.Logging import Logging


class KiwoomOpenApiPlusBaseOrderEventHandler(
    KiwoomOpenApiPlusEventHandlerForGrpc, Logging
):
    def __init__(self, control, context):
        super().__init__(control, context)

        self._single_names = ["주문번호"]
        self._multi_names = []

        self._is_stop_condition = lambda row: False
        self._inputs = {}

        self._listen_msg = True

    def ResponseForOnReceiveMsg(self, scrnno, rqname, trcode, msg):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveMsg"
        response.arguments.add().string_value = scrnno
        response.arguments.add().string_value = rqname
        response.arguments.add().string_value = trcode
        response.arguments.add().string_value = msg

        return response

    def OnReceiveMsg(self, scrnno, rqname, trcode, msg):
        if self._listen_msg:
            response = self.ResponseForOnReceiveMsg(scrnno, rqname, trcode, msg)
            self.observer.on_next(response)

        # 아래는 개발과정에서 확인 용도
        # 키움에서도 경고하지만 메시지의 코드로 판단하는건 위험함 (게다가 모의투자만 해당)
        if trcode == "KOA_NORMAL_BUY_KP_ORD":
            if msg == "[00Z218] 모의투자 장종료 상태입니다":
                self.logger.warning("Market is closed")
            elif msg == "[00Z217] 모의투자 장시작전입니다":
                self.logger.warning("Market is before opening")
            elif msg == "[00Z237] 모의투자 단가를 입력하지 않는 호가입니다.":
                self.logger.warning("Price is given but should not")
            elif msg == "[00Z112] 모의투자 정상처리 되었습니다":
                self.logger.debug("Order processed successfully")
        elif trcode == "KOA_NORMAL_KP_CANCEL":
            if msg == "[00Z924] 모의투자 취소수량이 취소가능수량을 초과합니다":
                self.logger.warning("Not enough amount to cancel")

    def ResponseForOnReceiveTrData(
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
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveTrData"
        response.arguments.add().string_value = scrnno
        response.arguments.add().string_value = rqname
        response.arguments.add().string_value = trcode
        response.arguments.add().string_value = recordname
        response.arguments.add().string_value = prevnext

        should_stop = prevnext in ["", "0"]  # pylint: disable=unused-variable
        repeat_cnt = self.control.GetRepeatCnt(trcode, recordname)

        if len(self._single_names) > 0:
            values = [
                self.control.GetCommData(trcode, recordname, 0, name).strip()
                for name in self._single_names
            ]
            response.single_data.names.extend(self._single_names)
            response.single_data.values.extend(values)

        if repeat_cnt > 0 and len(self._multi_names) > 0:
            rows = [
                [
                    self.control.GetCommData(trcode, recordname, i, name).strip()
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

        return response

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
        order_no = self.control.GetCommData(trcode, recordname, 0, "주문번호").strip()
        if order_no:
            response = self.ResponseForOnReceiveTrData(
                scrnno,
                rqname,
                trcode,
                recordname,
                prevnext,
                datalength,
                errorcode,
                message,
                splmmsg,
            )
            self.observer.on_next(response)

            should_stop = prevnext in ["", "0"]
            if not should_stop:
                self.logger.warning("Unexpected to have prevnext for order tr data.")

    def ResponseForOnReceiveChejanData(self, gubun, itemcnt, fidlist):
        fids = fidlist.rstrip(";")
        fids = fids.split(";") if fids else []
        fids = [int(fid) for fid in fids]

        assert itemcnt == len(fids)

        names = [
            KiwoomOpenApiPlusRealType.Fid.get_name_by_fid(fid, str(fid)) for fid in fids
        ]
        values = [self.control.GetChejanData(fid).strip() for fid in fids]

        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveChejanData"
        response.arguments.add().string_value = gubun
        response.arguments.add().long_value = itemcnt
        response.arguments.add().string_value = fidlist

        response.single_data.names.extend(names)
        response.single_data.values.extend(values)

        return response

    def OnReceiveChejanData(self, gubun, itemcnt, fidlist):
        response = self.ResponseForOnReceiveChejanData(gubun, itemcnt, fidlist)
        self.observer.on_next(response)

    def OnEventConnect(self, errcode):
        if errcode < 0:
            error = KiwoomOpenApiPlusNegativeReturnCodeError(errcode)
            self.observer.on_error(error)
            return


class KiwoomOpenApiPlusAllOrderEventHandler(KiwoomOpenApiPlusBaseOrderEventHandler):

    pass


class KiwoomOpenApiPlusOrderEventHandler(
    KiwoomOpenApiPlusBaseOrderEventHandler, Logging
):
    def __init__(self, control, request, context, screen_manager):
        super().__init__(control, context)

        self._request = request
        self._screen_manager = screen_manager

        self._rqname = request.request_name
        self._scrnno = request.screen_no
        self._accno = request.account_no
        self._ordertype = request.order_type
        self._code = request.code
        self._qty = request.quantity
        self._price = request.price
        self._hogagb = request.quote_type
        self._orgorderno = request.original_order_no

        self._order_no = None
        self._should_stop = False

    def on_enter(self):
        self._scrnno = self._screen_manager.borrow_screen(self._scrnno)
        self.add_callback(self._screen_manager.return_screen, self._scrnno)
        self.add_callback(self.control.DisconnectRealData, self._scrnno)
        KiwoomOpenApiPlusError.try_or_raise(
            self.control.RateLimitedSendOrder.queuedCall(
                self._rqname,
                self._scrnno,
                self._accno,
                self._ordertype,
                self._code,
                self._qty,
                self._price,
                self._hogagb,
                self._orgorderno,
            ),
            except_callback=self.observer.on_error,
        )

    def OnReceiveMsg(self, scrnno, rqname, trcode, msg):
        if (rqname, scrnno) == (self._rqname, self._scrnno):
            response = self.ResponseForOnReceiveMsg(scrnno, rqname, trcode, msg)
            self.observer.on_next(response)

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
        if (rqname, scrnno) == (self._rqname, self._scrnno):
            response = self.ResponseForOnReceiveTrData(
                scrnno,
                rqname,
                trcode,
                recordname,
                prevnext,
                datalength,
                errorcode,
                message,
                splmmsg,
            )
            self.observer.on_next(response)

            self._order_no = self.control.GetCommData(
                trcode, recordname, 0, "주문번호"
            ).strip()
            if not self._order_no:
                e = KiwoomOpenApiPlusError("Cannot specify order no")
                self.observer.on_error(e)
                return

            should_stop = prevnext in ["", "0"]
            if not should_stop:
                self.logger.warning("Unexpected to have prevnext for order tr data.")

    def OnReceiveChejanData(self, gubun, itemcnt, fidlist):
        # TODO: 정정 케이스에 대해 테스트 해보지 않음
        # TODO: 취소를 취소하는 케이스 같은건 고려하지 않음
        # TODO: 서로 같은 원주문을 정정 혹은 취소하는 케이스 사이에는 이벤트 전파가 필요할지 모르겠음
        accno = self.control.GetChejanData(9201).strip()
        code = self.control.GetChejanData(9001).strip()
        if accno == self._accno and code.endswith(
            self._code
        ):  # code 비교시에 앞에 prefix 가 붙어오기 때문에 endswith 으로 비교해야됨
            if gubun == "0":  # 접수와 체결시 (+ 취소 확인)
                order_no = self.control.GetChejanData(9203).strip()
                original_order_no = self.control.GetChejanData(904).strip()
                status = self.control.GetChejanData(913).strip()
                scrnno = self.control.GetChejanData(920).strip()
                is_last = self.control.GetChejanData(819).strip() == "1"
                if order_no in [self._order_no, self._orgorderno] or self._order_no in [
                    order_no,
                    original_order_no,
                ]:
                    response = self.ResponseForOnReceiveChejanData(
                        gubun, itemcnt, fidlist
                    )
                    self.observer.on_next(response)
                if (
                    order_no == self._order_no
                ):  # 자기 주문 처리하는 입장 OR 취소 및 정정 당한 뒤 원주문 정보를 받는 입장
                    if is_last and self._should_stop:  # 취소 확인 이후 원주문 정보 받고 종료 (타)
                        self.observer.on_completed()
                        return
                    elif status == "접수":
                        pass
                    elif status == "체결":
                        orders_left = self.control.GetChejanData(902).strip()
                        orders_left = int(orders_left) if orders_left.isdigit() else 0
                        if orders_left == 0:
                            self._should_stop = True  # 미체결수량이 더 이상 없다면 이후 잔고 이벤트 후 종료
                    elif status == "확인":
                        self._should_stop = True  # 취소 확인 이후 원주문 정보 받고 종료 (자)
                    else:
                        e = KiwoomOpenApiPlusError(
                            "Unexpected order status: %s" % status
                        )
                        self.observer.on_error(e)
                        return
                elif order_no == self._orgorderno:  # 취소하는 입장에서 원주문 정보 받는 케이스
                    if is_last and self._should_stop:  # 취소 확인 이후 원주문 정보 받고 종료 (자)
                        self.observer.on_completed()
                        return
                    elif status in ["접수", "체결"]:
                        pass
                    else:
                        e = KiwoomOpenApiPlusError(
                            "Unexpected order status: %s" % status
                        )
                        self.observer.on_error(e)
                        return
                elif self._order_no == original_order_no:  # 취소 혹은 정정 당하는 케이스
                    if status == "접수":
                        pass
                    elif status == "확인":
                        self._should_stop = True  # 취소 확인 이후 원주문 정보 받고 종료 (타)
                    else:
                        e = KiwoomOpenApiPlusError(
                            "Unexpected order status: %s" % status
                        )
                        self.observer.on_error(e)
                        return
            elif gubun == "1":  # 국내주식 잔고전달
                response = self.ResponseForOnReceiveChejanData(gubun, itemcnt, fidlist)
                self.observer.on_next(response)
                if self._should_stop:  # 미체결수량이 더 이상 없다면 잔고 이벤트 후 종료
                    self.observer.on_completed()
                    return
            elif gubun == "4":  # 파생 잔고전달
                response = self.ResponseForOnReceiveChejanData(gubun, itemcnt, fidlist)
                self.observer.on_next(response)
                if self._should_stop:  # 미체결수량이 더 이상 없다면 잔고 이벤트 후 종료
                    self.observer.on_completed()
                    return
            else:
                e = KiwoomOpenApiPlusError("Unexpected gubun value: %s" % gubun)
                self.observer.on_error(e)
                return
