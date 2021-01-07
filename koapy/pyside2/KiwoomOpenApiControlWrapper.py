import os
import re
import queue
import logging

from wrapt import synchronized

from koapy.openapi.KiwoomOpenApiError import KiwoomOpenApiError
from koapy.utils.rate_limiting.RateLimiter import KiwoomCommRqDataRateLimiter, KiwoomSendConditionRateLimiter

class KiwoomOpenApiControlCommonWrapper:

    def __init__(self, control=None):
        self._control = control

    def __getattr__(self, name):
        return getattr(self._control, name)

    def _RemoveLeadingZerosForNumber(self, value, width=0):
        remove = False
        if width is None:
            remove = False
        elif isinstance(width, int) and (width == 0 or len(value) == width):
            remove = True
        elif hasattr(width, '__iter__') and len(value) in width:
            remove = True
        if remove:
            return re.sub(r'^\s*([+-]?)[0]+([0-9]+(.[0-9]+)?)\s*$', r'\1\2', value)
        return value

    def _RemoveLeadingZerosForNumbersInValues(self, values, width=0):
        return [self._RemoveLeadingZerosForNumber(value, width) for value in values]

    def GetServerGubun(self):
        return self.GetLoginInfo('GetServerGubun')

    def ShowAccountWindow(self):
        return self.KOA_Functions('ShowAccountWindow', '')

    def GetCodeListByMarketAsList(self, market=None):
        if market is None:
            market = ''
        market = str(market)
        result = self.GetCodeListByMarket(market).rstrip(';')
        result = result.split(';') if result else []
        return result

    def GetNameListByMarketAsList(self, market):
        codes = self.GetCodeListByMarketAsList(market)
        names = [self.GetMasterCodeName(code) for code in codes]
        return names

    def GetUserId(self):
        userid = self.GetLoginInfo('USER_ID')
        return userid

    def GetAccountList(self):
        accounts = self.GetLoginInfo('ACCLIST').rstrip(';')
        accounts = accounts.split(';') if accounts else []
        return accounts

    def GetFirstAvailableAccount(self):
        account = None
        accounts = self.GetAccountList()
        if len(accounts) > 0:
            account = accounts[0]
        return account

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
            include_preferred_stock=False,
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
            codes = [code for code, cond in zip(codes, is_not_etn_name) if cond]

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

    def GetConditionFilePath(self):
        modulepath = self.GetAPIModulePath()
        userid = self.GetUserId()
        condition_filepath = os.path.join(modulepath, 'system', '%s_NewSaveIndex.dat' % userid)
        return condition_filepath

    def GetConditionNameListAsList(self):
        self.EnsureConditionLoaded()
        conditions = self.GetConditionNameList()
        conditions = conditions.rstrip(';').split(';') if conditions else []
        conditions = [cond.split('^') for cond in conditions]
        conditions = [(int(cond[0]), cond[1]) for cond in conditions]
        return conditions

commratelimited = KiwoomCommRqDataRateLimiter()
condratelimited = KiwoomSendConditionRateLimiter()

class KiwoomOpenApiControlWrapper(KiwoomOpenApiControlCommonWrapper):

    def Connect(self):
        q = queue.Queue()
        def OnEventConnect(errcode):
            q.put(errcode)
        self.OnEventConnect.connect(OnEventConnect)
        try:
            errcode = KiwoomOpenApiError.try_or_raise(self.CommConnect())
            errcode = KiwoomOpenApiError.try_or_raise(q.get())
        finally:
            self.OnEventConnect.disconnect(OnEventConnect)
        return errcode

    def EnsureConnected(self):
        errcode = 0
        if self.GetConnectState() == 0:
            errcode = self.Connect()
        return errcode

    def LoadCondition(self):
        q = queue.Queue()
        def OnReceiveConditionVer(ret, msg):
            if not ret:
                q.put(KiwoomOpenApiError(msg))
            else:
                q.put((ret, msg))
        self.OnReceiveConditionVer.connect(OnReceiveConditionVer)
        try:
            return_code = KiwoomOpenApiError.try_or_raise_boolean(
                self.GetConditionLoad(), 'Failed to load condition')
            res = q.get()
            if isinstance(res, KiwoomOpenApiError):
                raise res
        finally:
            self.OnReceiveConditionVer.disconnect(OnReceiveConditionVer)
        return return_code

    def EnsureConditionLoaded(self, force=False):
        return_code = 1
        condition_filepath = self.GetConditionFilePath()
        if not os.path.exists(condition_filepath) or force:
            return_code = self.LoadCondition()
        return return_code

    @synchronized
    def AtomicCommRqData(self, rqname, trcode, prevnext, scrnno, inputs=None):
        if inputs:
            for k, v in inputs.items():
                self.SetInputValue(k, v)
        prevnext = int(prevnext) # ensure prevnext is int
        code = self.CommRqData(rqname, trcode, prevnext, scrnno)
        return code

    @commratelimited
    def RateLimitedCommRqData(self, rqname, trcode, prevnext, scrnno, inputs=None):
        """
        [OpenAPI 게시판]
          https://bbn.kiwoom.com/bbn.openAPIQnaBbsList.do

        [조회횟수 제한 관련 가이드]
          - 1초당 5회 조회를 1번 발생시킨 경우 : 17초대기
          - 1초당 5회 조회를 5연속 발생시킨 경우 : 90초대기
          - 1초당 5회 조회를 10연속 발생시킨 경우 : 3분(180초)대기
        """
        return self.AtomicCommRqData(rqname, trcode, prevnext, scrnno, inputs)

    @commratelimited
    def RateLimitedCommKwRqData(self, codes, prevnext, codecnt, typeflag, rqname, scrnno):
        """
        [조회제한]
          OpenAPI 조회는 1초당 5회로 제한되며 복수종목 조회와 조건검색 조회 횟수가 합산됩니다.
          가령 1초 동안 시세조회2회 관심종목 1회 조건검색 2회 순서로 조회를 했다면 모두 합쳐서 5회이므로 모두 조회성공하겠지만
          조건검색을 3회 조회하면 맨 마지막 조건검색 조회는 실패하게 됩니다.

        [조건검색 제한]
          조건검색(실시간 조건검색 포함)은 시세조회와 관심종목조회와 합산해서 1초에 5회만 요청 가능하며 1분에 1회로 조건검색 제한됩니다.
        """
        return self.CommKwRqData(codes, prevnext, codecnt, typeflag, rqname, scrnno)

    def RateLimitedCommRqDataAndCheck(self, rqname, trcode, prevnext, scrnno, inputs=None):
        code = self.RateLimitedCommRqData(rqname, trcode, prevnext, scrnno)

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

    @commratelimited
    def RatedLimitedSendOrder(self, rqname, scrnno, accno, ordertype, code, qty, price, hogagb, orgorderno):
        return self.SendOrder(rqname, scrnno, accno, ordertype, code, qty, price, hogagb, orgorderno)

    @condratelimited
    @commratelimited
    def RateLimitedSendCondition(self, scrnno, condition_name, condition_index, search_type):
        """
        [조회제한]
          OpenAPI 조회는 1초당 5회로 제한되며 복수종목 조회와 조건검색 조회 횟수가 합산됩니다.
          가령 1초 동안 시세조회2회 관심종목 1회 조건검색 2회 순서로 조회를 했다면 모두 합쳐서 5회이므로 모두 조회성공하겠지만
          조건검색을 3회 조회하면 맨 마지막 조건검색 조회는 실패하게 됩니다.

        [조건검색 제한]
          조건검색(실시간 조건검색 포함)은 시세조회와 관심종목조회와 합산해서 1초에 5회만 요청 가능하며 1분에 1회로 조건검색 제한됩니다.
        """
        return self.SendCondition(scrnno, condition_name, condition_index, search_type)
