import re
import queue
import logging

import numpy as np

from koapy.openapi.KiwoomOpenApiError import KiwoomOpenApiError
from koapy.utils.rate_limiting.RateLimiter import KiwoomRateLimiter

class KiwoomOpenApiControlCommonWrapper:

    def __init__(self, control=None):
        self._control = control

    def __getattr__(self, name):
        return getattr(self._control, name)

    def GetServerGubun(self):
        return self.GetLoginInfo('GetServerGubun')

    def ShowAccountWindow(self):
        return self.KOA_Functions('ShowAccountWindow', '')

    def GetCodeListByMarketAsList(self, market):
        market = str(market)
        result = self.GetCodeListByMarket(market).rstrip(';')
        result = result.split(';') if result else []
        return result

    def GetNameListByMarketAsList(self, market):
        codes = self.GetCodeListByMarketAsList(market)
        names = [self.GetMasterCodeName(code) for code in codes]
        return names

    def GetAccountList(self):
        accounts = self.GetLoginInfo('ACCLIST').rstrip(';')
        accounts = accounts.split(';') if accounts else []
        return accounts

    def GetMasterStockStateAsList(self, code):
        states = self.GetMasterStockState(code).strip()
        states = states.split('|') if states else []
        return states

    def GetKospiCodeList(self):
        codes = self.GetCodeListByMarketAsList('0')
        codes = sorted(codes)
        return codes

    def GetKosdaqCodeList(self):
        codes = self.GetCodeListByMarketAsList('10')
        codes = sorted(codes)
        return codes

    def GetCommonCodeList(self,
            include_preferred_stock=True,
            include_etn=False,
            include_etf=False,
            include_mutual_fund=False,
            include_reits=False,
            include_kosdaq=False):
        """
        [시장구분값]
          0 : 장내
          10 : 코스닥
          3 : ELW
          8 : ETF
          50 : KONEX
          4 : 뮤추얼펀드
          5 : 신주인수권
          6 : 리츠
          9 : 하이얼펀드
          30 : K-OTC
        """

        codes = self.GetKospiCodeList()

        # 코드 마지막 자리가 0 이 아니면 우선주일 가능성이 있다고 보고 제외
        if not include_preferred_stock:
            codes = [code for code in codes if code.endswith('0')]

        # 장내 시장에서 ETN 이 섞여 있는데 시장구분값으로 뺄 수가 없어서 이름을 보고 대충 제외
        if not include_etn:
            names = [self.GetMasterCodeName(code) for code in codes]
            etn_suffixes = ['ETN', 'ETN(H)', 'ETN B', 'ETN(H) B']
            is_not_etn_name = [not any(name.endswith(suffix) for suffix in etn_suffixes) for name in names]
            codes = np.array(codes)[is_not_etn_name].tolist()

        # 코드값 기준 제외 준비
        codes = set(codes)

        # 나머지는 혹시나 겹치는 애들이 나올 수 있는 시장에서 코드기준 제외
        if not include_kosdaq:
            codes = codes - set(self.GetCodeListByMarketAsList('10')) # 코스닥
        if not include_etf:
            codes = codes - set(self.GetCodeListByMarketAsList('8'))  # ETF
        if not include_mutual_fund:
            codes = codes - set(self.GetCodeListByMarketAsList('4'))  # 뮤추얼펀드
        if not include_reits:
            codes = codes - set(self.GetCodeListByMarketAsList('6'))  # 리츠

        # 정렬된 리스트 형태로 제공
        codes = sorted(list(codes))

        return codes

    def IsSuspended(self, code):
        return '거래정지' in self.GetMasterStockStateAsList(code)

    def IsInSupervision(self, code):
        return '관리종목' in self.GetMasterStockStateAsList(code)

    def IsInSurveillance(self, code):
        return '감리종목' in self.GetMasterStockStateAsList(code)

    def _RemoveLeadingZerosForNumber(self, value, width=0):
        remove = False
        if width is None:
            remove = False
        elif isinstance(width, int) and width == 0 or len(value) == width:
            remove = True
        elif hasattr(width, '__iter__') and len(value) in width:
            remove = True
        if remove:
            return re.sub(r'^\s*([+-]?)[0]+([0-9]+(.[0-9]+)?)\s*$', r'\1\2', value)
        return value

    def _RemoveLeadingZerosForNumbersInValues(self, values, width=0):
        return [self._RemoveLeadingZerosForNumber(value, width) for value in values]


class KiwoomOpenApiControlWrapper(KiwoomOpenApiControlCommonWrapper):

    def EnsureConnected(self):
        errcode = 0
        if self.GetConnectState() == 0:
            q = queue.Queue()
            def OnEventConnect(errcode):
                q.put(errcode)
                self.OnEventConnect.disconnect(OnEventConnect)
            self.OnEventConnect.connect(OnEventConnect)
            errcode = KiwoomOpenApiError.try_or_raise(self.CommConnect())
            errcode = KiwoomOpenApiError.try_or_raise(q.get())
        return errcode

    # 그냥 1초당 5회로하면 장기적으로 결국 막히기 때문에 원래 4초당 1회로 제한했었음 (3초당 1회부턴 제한걸림)
    # @SimpleRateLimiter(period=4, calls=1)

    # 1시간에 1000회로 제한한다는 추측이 있는데 일리 있어 보임 (http://blog.quantylab.com/htsapi.html)
    # 1초당 1회로 계산했을때 1시간이면 3600 회, 주기를 1초씩 늘려보면
    # 2초당 1회 => 1800 > 1000, 3초당 1회 => 1200 > 1000, 4초당 1회 => 900 < 1000

    @KiwoomRateLimiter()
    def RateLimitedCommRqData(self, rqname, trcode, prevnext, scrnno, inputs=None):
        """
        [OpenAPI 게시판]
          https://bbn.kiwoom.com/bbn.openAPIQnaBbsList.do

        [조회횟수 제한 관련 가이드]
          - 1초당 5회 조회를 1번 발생시킨 경우 : 17초대기
          - 1초당 5회 조회를 5연속 발생시킨 경우 : 90초대기
          - 1초당 5회 조회를 10연속 발생시킨 경우 : 3분(180초)대기
        """
        prevnext = int(prevnext) # ensure prevnext is int
        code = self.CommRqData(rqname, trcode, prevnext, scrnno)
        spec = 'CommRqData(%r, %r, %r, %r)' % (rqname, trcode, prevnext, scrnno)

        if inputs is not None:
            spec += ' with inputs %r' % inputs

        if code == KiwoomOpenApiError.OP_ERR_NONE:
            message = 'CommRqData() was successful; ' + spec
            logging.debug(message)
        elif code == KiwoomOpenApiError.OP_ERR_SISE_OVERFLOW:
            message = 'CommRqData() was rejected due to massive request; ' + spec
            logging.error(message)
            raise KiwoomOpenApiError(code)
        elif code == KiwoomOpenApiError.OP_ERR_ORD_WRONG_INPUT:
            message = 'CommRqData() failed due to wrong input, check if input was correctly set; ' + spec
            logging.error(message)
            raise KiwoomOpenApiError(code)
        elif code in (KiwoomOpenApiError.OP_ERR_RQ_STRUCT_FAIL, KiwoomOpenApiError.OP_ERR_RQ_STRING_FAIL):
            message = 'CommRqData() request was invalid; ' + spec
            logging.error(message)
            raise KiwoomOpenApiError(code)
        else:
            message = 'Unknown error occured during CommRqData() request; ' + spec
            korean_message = KiwoomOpenApiError.get_error_message_by_code(code)
            if korean_message is not None:
                message += '; Korean error message: ' +  korean_message
            logging.error(message)
            raise KiwoomOpenApiError(code)

        return code
