import re
import queue

import numpy as np

from koapy.openapi.KiwoomOpenApiError import KiwoomOpenApiError

class KiwoomOpenApiControlWrapper:

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

    def GetCommonCodeList(self):
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

        # 기본 코드 리스트
        codes = self.GetCodeListByMarketAsList('0')

        # 장내 시장에서 ETN 이 섞여 있는데 시장구분값으로 뺄 수가 없어서 이름을 보고 대충 제외
        names = [self.GetMasterCodeName(code) for code in codes]
        etn_suffixes = ['ETN', 'ETN(H)', 'ETN B', 'ETN(H) B']
        is_not_etn_name = [not any(name.endswith(suffix) for suffix in etn_suffixes) for name in names]
        codes = np.array(codes)[is_not_etn_name].tolist()

        # 코드값 기준 제외 준비
        codes = set(codes)

        # 우선주 구분은 기본정보에서 유통주식 수량이 확인되지 않는 주식들
        # 그 중에 ~3호 등 배 관련 종목은 우선주가 아니고 PER 같은 값이 있음
        # 종목코드의 마지막 자리가 숫자가 아닌 K,L 등 인 것으로 구분할 수도 있는데 모두 그런건 아님
        # 당장은 미리  구분해놓은 값들을 참고해 제외하는 식으로
        preferred_stock_codes = []
        codes = codes - set(preferred_stock_codes)

        # 나머지는 혹시나 겹치는 애들이 나올 수 있는 시장에서 코드기준 제외
        codes = codes - set(self.GetCodeListByMarketAsList('10'))
        codes = codes - set(self.GetCodeListByMarketAsList('8'))
        codes = codes - set(self.GetCodeListByMarketAsList('4'))
        codes = codes - set(self.GetCodeListByMarketAsList('6'))

        # 정렬된 리스트 형태로 제공
        codes = sorted(list(codes))

        return codes

    def GetKosdaqCodeList(self):
        codes = self.GetCodeListByMarketAsList('10')
        codes = sorted(codes)
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

    def EnsureConnected(self):
        errcode = 0
        if self.GetConnectState() == 0:
            errcode = KiwoomOpenApiError.try_or_raise(self.control.CommConnect())
            q = queue.Queue()
            def OnEventConnect(errcode):
                q.put(errcode)
                self.OnEventConnect.disconnect(OnEventConnect)
            self.OnEventConnect.connect(OnEventConnect)
            errcode = q.get()
        return errcode
