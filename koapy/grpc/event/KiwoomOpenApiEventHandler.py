import logging
import operator
import datetime

from koapy.grpc import KiwoomOpenApiService_pb2
from koapy.grpc.event.BaseKiwoomOpenApiEventHandler import BaseKiwoomOpenApiEventHandler
from koapy.openapi.KiwoomOpenApiError import KiwoomOpenApiError
from koapy.openapi.TrInfo import TrInfo
from koapy.openapi.RealType import RealType

from koapy.utils.notimplemented import isimplemented
from koapy.utils.itertools import chunk

class KiwoomOpenApiLoggingEventHandler(BaseKiwoomOpenApiEventHandler):

    def OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, _datalength, _errorcode, _message, _splmmsg):
        logging.debug('OnReceiveTrData(%r, %r, %r, %r, %r)', scrnno, rqname, trcode, recordname, prevnext)

    def OnReceiveRealData(self, code, realtype, realdata):
        logging.debug('OnReceiveRealData(%r, %r, %r)', code, realtype, realdata)
        if code == '09' and realtype == '장시작시간':
            signal_type = self.control.GetCommRealData(code, 215)
            current_time = self.control.GetCommRealData(code, 20)
            estimated_remaining_time = self.control.GetCommRealData(code, 214)
            signal_type_msg = {
                # 아래는 문서에서 확인 가능
                '0': '장시작전(동시호가시작,이후1분단위)',
                '2': '장종료전(동시호가시작,이후1분단위)',
                '3': '장시작(동시호가종료)',
                '4': '장종료(동시호가종료)',
                '8': '장종료(시간내용없음)',
                '9': '장마감(시간내용없음)',
                # 이후는 추정
                's': '선물옵션장종료전(동시호가시작)', # 17번반복
                'a': '장후시간외종가시작',
                'e': '선물옵션장종료(동시호가종료)', # 17번반복
                'b': '장후시간외종가종료',
                'c': '시간외단일가시작',
                'd': '시간외단일가종료',
            }.get(signal_type, '알수없음')
            if signal_type not in ['8', '9']:
                current_time = datetime.datetime.strptime(current_time, '%H%M%S')
            else:
                current_time = datetime.datetime.now()
            ert = datetime.datetime.strptime(estimated_remaining_time, '%H%M%S')
            estimated_remaining_time = datetime.timedelta(hours=ert.hour, minutes=ert.minute, seconds=ert.second)
            logging.debug('%s, %s remaining', signal_type_msg, estimated_remaining_time)

    def OnReceiveMsg(self, scrnno, rqname, trcode, msg):
        """
        [OnReceiveMsg()이벤트]

          OnReceiveMsg(
          BSTR sScrNo,   // 화면번호
          BSTR sRQName,  // 사용자 구분명
          BSTR sTrCode,  // TR이름
          BSTR sMsg     // 서버에서 전달하는 메시지
          )

          서버통신 후 수신한 메시지를 알려줍니다.
          메시지에는 6자리 코드번호가 포함되는데 이 코드번호는 통보없이 수시로 변경될 수 있습니다. 따라서 주문이나 오류관련처리를
          이 코드번호로 분류하시면 안됩니다.
        """
        logging.debug('OnReceiveMsg(%r, %r, %r, %r)', scrnno, rqname, trcode, msg)

        if msg == '전문 처리 실패(-22)':
            logging.warning('Server might have ended connection abruptly')

    def OnReceiveChejanData(self, gubun, itemcnt, fidlist):
        logging.debug('OnReceiveChejanData(%r, %r, %r)', gubun, itemcnt, fidlist)

    def OnEventConnect(self, errcode):
        logging.debug('OnEventConnect(%r)', errcode)

    def OnReceiveRealCondition(self, code, condition_type, condition_name, condition_index):
        logging.debug('OnReceiveRealCondition(%r, %r, %r, %r)', code, condition_type, condition_name, condition_index)

    def OnReceiveTrCondition(self, scrnno, codelist, condition_name, index, prevnext):
        logging.debug('OnReceiveTrCondition(%r, %r, %r, %r, %r)', scrnno, codelist, condition_name, index, prevnext)

    def OnReceiveConditionVer(self, ret, msg):
        logging.debug('OnReceiveConditionVer(%r, %r)', ret, msg)

class KiwoomOpenApiAllEventHandler(BaseKiwoomOpenApiEventHandler):

    def OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, _datalength, _errorcode, _message, _splmmsg):
        response = KiwoomOpenApiService_pb2.CustomCallAndListenResponse()
        response.listen_response.name = 'OnReceiveTrData' # pylint: disable=no-member
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.string_value = scrnno
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.string_value = rqname
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.string_value = trcode
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.string_value = recordname
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.string_value = prevnext
        self.observer.on_next(response.listen_response) # pylint: disable=no-member

    def OnReceiveRealData(self, code, realtype, realdata):
        response = KiwoomOpenApiService_pb2.CustomCallAndListenResponse()
        response.listen_response.name = 'OnReceiveRealData' # pylint: disable=no-member
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.string_value = code
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.string_value = realtype
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.string_value = realdata
        self.observer.on_next(response.listen_response) # pylint: disable=no-member

    def OnReceiveMsg(self, scrnno, rqname, trcode, msg):
        response = KiwoomOpenApiService_pb2.CustomCallAndListenResponse()
        response.listen_response.name = 'OnReceiveMsg' # pylint: disable=no-member
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.string_value = scrnno
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.string_value = rqname
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.string_value = trcode
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.string_value = msg
        self.observer.on_next(response.listen_response) # pylint: disable=no-member

    def OnReceiveChejanData(self, gubun, itemcnt, fidlist):
        response = KiwoomOpenApiService_pb2.CustomCallAndListenResponse()
        response.listen_response.name = 'OnReceiveChejanData' # pylint: disable=no-member
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.string_value = gubun
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.long_value = itemcnt
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.string_value = fidlist
        self.observer.on_next(response.listen_response) # pylint: disable=no-member

    def OnEventConnect(self, errcode):
        response = KiwoomOpenApiService_pb2.CustomCallAndListenResponse()
        response.listen_response.name = 'OnEventConnect' # pylint: disable=no-member
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.long_value = errcode
        self.observer.on_next(response.listen_response) # pylint: disable=no-member

    def OnReceiveRealCondition(self, code, condition_type, condition_name, condition_index):
        response = KiwoomOpenApiService_pb2.CustomCallAndListenResponse()
        response.listen_response.name = 'OnReceiveRealCondition' # pylint: disable=no-member
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.string_value = code
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.string_value = condition_type
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.string_value = condition_name
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.string_value = condition_index
        self.observer.on_next(response.listen_response) # pylint: disable=no-member

    def OnReceiveTrCondition(self, scrnno, codelist, condition_name, index, prevnext):
        response = KiwoomOpenApiService_pb2.CustomCallAndListenResponse()
        response.listen_response.name = 'OnReceiveTrCondition' # pylint: disable=no-member
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.string_value = scrnno
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.string_value = codelist
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.string_value = condition_name
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.long_value = index
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.long_value = prevnext
        self.observer.on_next(response.listen_response) # pylint: disable=no-member

    def OnReceiveConditionVer(self, ret, msg):
        response = KiwoomOpenApiService_pb2.CustomCallAndListenResponse()
        response.listen_response.name = 'OnReceiveConditionVer' # pylint: disable=no-member
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.long_value = ret
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.string_value = msg
        self.observer.on_next(response.listen_response) # pylint: disable=no-member

class KiwoomOpenApiSomeEventHandler(KiwoomOpenApiAllEventHandler):

    def __init__(self, control, request):
        super().__init__(control)
        self._request = request

    def slots(self):
        names = self.names()
        slots = [getattr(self, name) for name in names]
        names_and_slots_implemented = [(name, slot) for name, slot in zip(names, slots) if isimplemented(slot) and name in self._request.slots]
        return names_and_slots_implemented

class KiwoomOpenApiLoginEventHandler(BaseKiwoomOpenApiEventHandler):

    def __init__(self, control, request):
        super().__init__(control)
        self._request = request

    def on_enter(self):
        KiwoomOpenApiError.try_or_raise(self.control.CommConnect())

    def OnEventConnect(self, errcode):
        if errcode < 0:
            error = KiwoomOpenApiError(errcode)
            self.observer.on_error(error)
        response = KiwoomOpenApiService_pb2.CustomCallAndListenResponse()
        response.listen_response.name = 'OnEventConnect' # pylint: disable=no-member
        response.listen_response.arguments.add().long_value = errcode # pylint: disable=no-member
        self.observer.on_next(response)
        self.observer.on_completed()

class KiwoomOpenApiTrEventHandler(BaseKiwoomOpenApiEventHandler):

    def __init__(self, control, request, screen_manager):
        super().__init__(control)
        self._request = request
        self._screen_manager = screen_manager

        self._rqname = request.request_name
        self._trcode = request.transaction_code
        self._scrnno = request.screen_no
        self._inputs = request.inputs

        self._trinfo = TrInfo.get_trinfo_by_code(self._trcode)

        if self._trinfo is None:
            logging.error('Cannot find names for trcode %s', self._trinfo)

        self._input_code = self._inputs.get('종목코드')

        self._single_names = self._trinfo.get_single_output_names()
        self._multi_names = self._trinfo.get_multi_output_names()

        stop_condition = request.stop_condition
        stop_condition_is_valid = all([
            stop_condition is not None,
            stop_condition.name is not None,
            len(stop_condition.name) > 0,
            stop_condition.name in self._multi_names])

        if stop_condition_is_valid:
            column_index_to_check = self._multi_names.index(stop_condition.name)
            comparator = {
                KiwoomOpenApiService_pb2.TransactionStopConditionCompartor.LESS_THAN_OR_EQUAL_TO: operator.le,
                KiwoomOpenApiService_pb2.TransactionStopConditionCompartor.LESS_THAN: operator.lt,
                KiwoomOpenApiService_pb2.TransactionStopConditionCompartor.GREATER_THAN_OR_EQUAL_TO: operator.ge,
                KiwoomOpenApiService_pb2.TransactionStopConditionCompartor.GREATER_THAN: operator.gt,
                KiwoomOpenApiService_pb2.TransactionStopConditionCompartor.EQUAL_TO: operator.eq,
                KiwoomOpenApiService_pb2.TransactionStopConditionCompartor.NOT_EQUAL_TO: operator.ne,
            }.get(stop_condition.comparator, operator.le)
            def is_stop_condition(row):
                return comparator(row[column_index_to_check], stop_condition.value)
        else:
            def is_stop_condition(_):
                return False

        self._is_stop_condition = is_stop_condition

    def on_enter(self):
        self._scrnno = self._screen_manager.borrow_screen(self._scrnno)
        self.add_callback(self._screen_manager.return_screen, self._scrnno)
        for k, v in self._inputs.items():
            self.control.SetInputValue(k, v)
        KiwoomOpenApiError.try_or_raise(
            self.control.RateLimitedCommRqData(self._rqname, self._trcode, 0, self._scrnno, self._inputs))

    def on_exit(self):
        self.control.DisconnectRealData(self._scrnno)

    def OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, datalength, errorcode, message, splmmsg):
        if (rqname, trcode, scrnno) == (self._rqname, self._trcode, self._scrnno):
            response = KiwoomOpenApiService_pb2.CustomCallAndListenResponse()
            response.listen_response.name = 'OnReceiveTrData' # pylint: disable=no-member
            argument = response.listen_response.arguments.add() # pylint: disable=no-member
            argument.string_value = scrnno
            argument = response.listen_response.arguments.add() # pylint: disable=no-member
            argument.string_value = rqname
            argument = response.listen_response.arguments.add() # pylint: disable=no-member
            argument.string_value = trcode
            argument = response.listen_response.arguments.add() # pylint: disable=no-member
            argument.string_value = recordname
            argument = response.listen_response.arguments.add() # pylint: disable=no-member
            argument.string_value = prevnext

            should_stop = prevnext in ['', '0']
            repeat_cnt = self.control.GetRepeatCnt(trcode, recordname)

            if len(self._single_names) > 0:
                values = [self.control.GetCommData(trcode, recordname, 0, name).strip() for name in self._single_names]
                response.listen_response.single_data.names.extend(self._single_names) # pylint: disable=no-member
                response.listen_response.single_data.values.extend(values) # pylint: disable=no-member

            if repeat_cnt > 0 and len(self._multi_names) > 0:
                rows = [[self.control.GetCommData(trcode, recordname, i, name).strip() for name in self._multi_names] for i in range(repeat_cnt)]
                response.listen_response.multi_data.names.extend(self._multi_names) # pylint: disable=no-member
                for row in rows:
                    if self._is_stop_condition(row):
                        should_stop = True
                        break
                    response.listen_response.multi_data.values.add().values.extend(row) # pylint: disable=no-member

            self.observer.on_next(response)

            if should_stop:
                self.observer.on_completed()
                return
            else:
                for k, v in self._inputs.items():
                    self.control.SetInputValue(k, v)
                try:
                    self.control.RateLimitedCommRqData(rqname, trcode, int(prevnext), scrnno, self._inputs)
                except KiwoomOpenApiError as e:
                    self.observer.on_error(e)
                    return

    def OnEventConnect(self, errcode):
        if errcode < 0:
            error = KiwoomOpenApiError(errcode)
            self.observer.on_error(error)
            return

class KiwoomOpenApiOrderEventHandler(BaseKiwoomOpenApiEventHandler):

    def __init__(self, control, request, screen_manager):
        super().__init__(control)
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

        self._single_names = ['주문번호']
        self._multi_names = []

        self._is_stop_condition = lambda row: False
        self._inputs = {}

    def on_enter(self):
        self._scrnno = self._screen_manager.borrow_screen(self._scrnno)
        self.add_callback(self._screen_manager.return_screen, self._scrnno)
        KiwoomOpenApiError.try_or_raise(
            self.control.SendOrder(
                self._rqname,
                self._scrnno,
                self._accno,
                self._ordertype,
                self._code,
                self._qty,
                self._price,
                self._hogagb,
                self._orgorderno))

    def OnReceiveMsg(self, scrnno, rqname, trcode, msg):
        if (rqname, scrnno) == (self._rqname, self._scrnno):
            response = KiwoomOpenApiService_pb2.CustomCallAndListenResponse()
            response.listen_response.name = 'OnReceiveMsg' # pylint: disable=no-member
            argument = response.listen_response.arguments.add() # pylint: disable=no-member
            argument.string_value = rqname
            argument = response.listen_response.arguments.add() # pylint: disable=no-member
            argument.string_value = trcode
            argument = response.listen_response.arguments.add() # pylint: disable=no-member
            argument.string_value = msg

            self.observer.on_next(response)

            # 아래는 개발과정에서 확인용도
            if trcode == 'KOA_NORMAL_BUY_KP_ORD':
                if msg == '[00Z218] 모의투자 장종료 상태입니다': # 메시지의 코드로 판단하는건 위험함 (게다가 모의투자만 해당)
                    logging.warning('Market is closed')
                elif msg == '[00Z217] 모의투자 장시작전입니다':
                    logging.warning('Market is before opening')
                elif msg == '[00Z237] 모의투자 단가를 입력하지 않는 호가입니다.':
                    logging.warning('Price is given but should not')
                elif msg == '[00Z112] 모의투자 정상처리 되었습니다':
                    logging.debug('Processed successfully')
            elif trcode == 'KOA_NORMAL_KP_CANCEL':
                if msg == '[00Z924] 모의투자 취소수량이 취소가능수량을 초과합니다':
                    logging.warning('Not enough amount to cancel')

    def OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, datalength, errorcode, message, splmmsg):
        if (rqname, scrnno) == (self._rqname, self._scrnno):
            response = KiwoomOpenApiService_pb2.CustomCallAndListenResponse()
            response.listen_response.name = 'OnReceiveTrData' # pylint: disable=no-member
            argument = response.listen_response.arguments.add() # pylint: disable=no-member
            argument.string_value = scrnno
            argument = response.listen_response.arguments.add() # pylint: disable=no-member
            argument.string_value = rqname
            argument = response.listen_response.arguments.add() # pylint: disable=no-member
            argument.string_value = trcode
            argument = response.listen_response.arguments.add() # pylint: disable=no-member
            argument.string_value = recordname
            argument = response.listen_response.arguments.add() # pylint: disable=no-member
            argument.string_value = prevnext

            self._order_no = self.control.GetCommData(trcode, recordname, 0, '주문번호').strip()

            should_stop = prevnext in ['', '0']
            repeat_cnt = self.control.GetRepeatCnt(trcode, recordname)

            if len(self._single_names) > 0:
                values = [self.control.GetCommData(trcode, recordname, 0, name).strip() for name in self._single_names]
                response.listen_response.single_data.names.extend(self._single_names) # pylint: disable=no-member
                response.listen_response.single_data.values.extend(values) # pylint: disable=no-member

            if repeat_cnt > 0 and len(self._multi_names) > 0:
                rows = [[self.control.GetCommData(trcode, recordname, i, name).strip() for name in self._multi_names] for i in range(repeat_cnt)]
                response.listen_response.multi_data.names.extend(self._multi_names) # pylint: disable=no-member
                for row in rows:
                    if self._is_stop_condition(row):
                        should_stop = True
                        break
                    response.listen_response.multi_data.values.add().values.extend(row) # pylint: disable=no-member

            self.observer.on_next(response)

            if not self._order_no:
                self.observer.on_completed()
                return
            elif not should_stop:
                for k, v in self._inputs.items():
                    self.control.SetInputValue(k, v)
                try:
                    self.control.CommRqDataAndCheck(rqname, trcode, int(prevnext), scrnno, self._inputs)
                except KiwoomOpenApiError as e:
                    self.observer.on_error(e)
                    return

    def OnReceiveChejanData(self, gubun, itemcnt, fidlist):
        fids = fidlist.rstrip(';')
        fids = fids.split(';') if fids else []
        fids = [int(fid) for fid in fids]

        assert itemcnt == len(fids)

        names = [RealType.Fid.get_name_by_fid(fid, str(fid)) for fid in fids]
        values = [self.control.GetChejanData(fid).strip() for fid in fids]

        response = KiwoomOpenApiService_pb2.CustomCallAndListenResponse()
        response.listen_response.name = 'OnReceiveChejanData' # pylint: disable=no-member
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.string_value = gubun
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.long_value = itemcnt
        argument = response.listen_response.arguments.add() # pylint: disable=no-member
        argument.string_value = fidlist

        response.listen_response.single_data.names.extend(names) # pylint: disable=no-member
        response.listen_response.single_data.values.extend(values) # pylint: disable=no-member

        if gubun == '0': # 접수와 체결시 (+ 취소 확인)
            accno = self.control.GetChejanData(9201).strip()
            scrnno = self.control.GetChejanData(920).strip()
            order_no = self.control.GetChejanData(9203).strip()
            if (scrnno, accno, order_no) == (self._scrnno, self._accno, self._order_no):
                self.observer.on_next(response)
                status = self.control.GetChejanData(913).strip()
                if status == '접수':
                    pass
                elif status == '체결':
                    orders_left = self.control.GetChejanData(902).strip()
                    orders_left = int(orders_left) if orders_left.isdigit() else 0
                    if orders_left == 0:
                        self._should_stop = True # 미체결수량이 더이상 없다면 이후 잔고 이벤트 후 종료
                elif status == '확인':
                    self.observer.on_completed()
                    return
        elif gubun == '1': # 국내주식 잔고전달
            accno = self.control.GetChejanData(9201).strip()
            code = self.control.GetChejanData(9001).strip()
            if accno == self._accno and code.endswith(self._code): # code 비교시에 앞에 prefix 가 붙어오기 때문에 endswith 으로 비교해야됨
                self.observer.on_next(response)
                if self._should_stop: # 미체결수량이 더이상 없다면 이후 잔고 이벤트 후 종료
                    self.observer.on_completed()
                    return
        elif gubun == '4': # 파생 잔고전달
            accno = self.control.GetChejanData(9201).strip()
            code = self.control.GetChejanData(9001).strip()
            if accno == self._accno and code.endswith(self._code):
                self.observer.on_next(response)
                if self._should_stop: # 미체결수량이 더이상 없다면 이후 잔고 이벤트 후 종료
                    self.observer.on_completed()
                    return
        else:
            logging.error('Unexpected gubun value: %r', gubun)
            e = ValueError('Unexpected gubun value: %r' % gubun)
            self.observer.on_error(e)
            return

    def OnEventConnect(self, errcode):
        if errcode < 0:
            error = KiwoomOpenApiError(errcode)
            self.observer.on_error(error)
            return

class KiwoomOpenApiRealEventHandler(BaseKiwoomOpenApiEventHandler):

    _num_codes_per_screen = 100
    _default_real_type = '0'

    def __init__(self, control, request, screen_manager):
        super().__init__(control)
        self._request = request
        self._screen_manager = screen_manager

        self._screen_no = request.screen_no
        self._code_list = request.code_list
        self._fid_list = request.fid_list
        self._real_type = request.real_type

        self._infer_fids = request.flags.infer_fids
        self._readable_names = request.flags.readable_names
        self._fast_parse = request.flags.fast_parse

        self._code_lists = [';'.join(codes) for codes in chunk(self._code_list, self._num_codes_per_screen)]
        if len(self._screen_no) == 0:
            self._screen_nos = [None for i in range(len(self._code_lists))]
        elif len(self._screen_no) < len(self._code_lists):
            logging.warning('Given screen nos are not sufficient.')
            self._screen_nos = list(self._screen_nos) + [None for i in range(len(self._code_lists) - len(self.screen_nos))]
        else:
            self._screen_nos = self._screen_no
        self._fid_list_joined = ';'.join([str(fid) for fid in self._fid_list])
        self._real_type_explicit = self._real_type or self._default_real_type

    def on_enter(self):
        for screen_no, code_list in zip(self._screen_nos, self._code_lists):
            screen_no = self._screen_manager.borrow_screen(screen_no)
            self.add_callback(self._screen_manager.return_screen, screen_no)
            self.add_callback(self.control.DisconnectRealData, screen_no)
            self.add_callback(self.control.SetRealRemove, screen_no, code_list)

            KiwoomOpenApiError.try_or_raise(
                self.control.SetRealReg(screen_no, code_list, self._fid_list_joined, self._real_type_explicit))

    def OnReceiveRealData(self, code, realtype, realdata):
        if code in self._code_list:
            response = KiwoomOpenApiService_pb2.CustomCallAndListenResponse()
            response.listen_response.name = 'OnReceiveRealData' # pylint: disable=no-member
            argument = response.listen_response.arguments.add() # pylint: disable=no-member
            argument.string_value = code
            argument = response.listen_response.arguments.add() # pylint: disable=no-member
            argument.string_value = realtype
            argument = response.listen_response.arguments.add() # pylint: disable=no-member
            argument.string_value = realdata

            if self._infer_fids:
                fids = RealType.get_fids_by_realtype(realtype)
            else:
                fids = self._fid_list

            if self._readable_names:
                names = [RealType.Fid.get_name_by_fid(fid, str(fid)) for fid in fids]
            else:
                names = [str(fid) for fid in fids]

            if self._infer_fids and self._fast_parse:
                values = realdata.split('\t')
            else:
                values = [self.control.GetCommRealData(code, fid) for fid in fids]

            assert len(names) == len(values)

            response.listen_response.single_data.names.extend(names) # pylint: disable=no-member
            response.listen_response.single_data.values.extend(values) # pylint: disable=no-member

            self.observer.on_next(response)

    def OnEventConnect(self, errcode):
        if errcode < 0:
            error = KiwoomOpenApiError(errcode)
            self.observer.on_error(error)
            return
