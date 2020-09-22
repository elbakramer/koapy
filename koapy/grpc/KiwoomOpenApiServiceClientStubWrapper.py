import re
import logging
import datetime

import numpy as np
import pandas as pd

from koapy.grpc import KiwoomOpenApiService_pb2
from koapy.grpc.KiwoomOpenApiServiceClientSideDynamicCallable import KiwoomOpenApiServiceClientSideDynamicCallable
from koapy.openapi.KiwoomOpenApiError import KiwoomOpenApiError
from koapy.openapi.RealType import RealType

class KiwoomOpenApiServiceClientStubCoreWrapper:

    def __init__(self, stub):
        self._stub = stub

    def __getattr__(self, name):
        return KiwoomOpenApiServiceClientSideDynamicCallable(self._stub, name)

    def Call(self, name, *args):
        return KiwoomOpenApiServiceClientSideDynamicCallable(self._stub, name)(*args)

    def LoginCall(self):
        request = KiwoomOpenApiService_pb2.LoginRequest()
        for response in self._stub.LoginCall(request):
            errcode = response.listen_response.arguments[0].long_value
        return errcode

    def TransactionCall(self, rqname, trcode, scrnno, inputs, stop_condition=None):
        request = KiwoomOpenApiService_pb2.TransactionRequest()
        request.request_name = rqname
        request.transaction_code = trcode
        request.screen_no = scrnno
        for k, v in inputs.items():
            request.inputs[k] = v # pylint: disable=no-member
        if stop_condition:
            request.stop_condition.name = stop_condition.get('name') # pylint: disable=no-member
            request.stop_condition.value = str(stop_condition.get('value')) # pylint: disable=no-member
            request.stop_condition.comparator = { # pylint: disable=no-member
                '<=': KiwoomOpenApiService_pb2.TransactionStopConditionCompartor.LESS_THAN_OR_EQUAL_TO,
                '<': KiwoomOpenApiService_pb2.TransactionStopConditionCompartor.LESS_THAN,
                '>=': KiwoomOpenApiService_pb2.TransactionStopConditionCompartor.GREATER_THAN_OR_EQUAL_TO,
                '>': KiwoomOpenApiService_pb2.TransactionStopConditionCompartor.GREATER_THAN,
                '==': KiwoomOpenApiService_pb2.TransactionStopConditionCompartor.EQUAL_TO,
                '!=': KiwoomOpenApiService_pb2.TransactionStopConditionCompartor.NOT_EQUAL_TO,
            }.get(stop_condition.get('comparator', '<='))
        return self._stub.TransactionCall(request)

    def OrderCall(self, rqname, scrnno, account, order_type, code, quantity, price, quote_type, original_order_no=None):
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
        request = KiwoomOpenApiService_pb2.OrderRequest()
        request.request_name = rqname
        request.screen_no = scrnno
        request.account_no = account
        request.order_type = int(order_type) if order_type else 0
        request.code = code
        request.quantity = int(quantity) if quantity else 0
        request.price = int(price) if price else 0
        request.quote_type = quote_type
        request.original_order_no = '' if original_order_no is None else original_order_no
        return self._stub.OrderCall(request)

    def RealCall(self, scrnno, codes, fids, realtype=None, infer_fids=False, readable_names=False, fast_parse=False):
        request = KiwoomOpenApiService_pb2.RealRequest()
        fids = [int(fid) for fid in fids]
        if realtype is None:
            realtype = '0'
        request.screen_no = scrnno
        request.code_list.extend(codes) # pylint: disable=no-member
        request.fid_list.extend(fids) # pylint: disable=no-member
        request.real_type = realtype
        request.flags.infer_fids = infer_fids # pylint: disable=no-member
        request.flags.readable_names = readable_names # pylint: disable=no-member
        request.flags.fast_parse = fast_parse # pylint: disable=no-member
        return self._stub.RealCall(request)
    
    def SetLogLevel(self, level, logger=''):
        request = KiwoomOpenApiService_pb2.SetLogLevelRequest()
        request.level = level
        request.logger = logger
        return self._stub.SetLogLevel(request)


class KiwoomOpenApiServiceClientStubWrapper(KiwoomOpenApiServiceClientStubCoreWrapper):

    def EnsureConnected(self):
        errcode = 0
        if self.GetConnectState() == 0:
            errcode = self.LoginCall()
        if errcode < 0:
            message = 'Failed to connect'
            korean_message = KiwoomOpenApiError.get_error_message_by_code(errcode)
            if korean_message is not None:
                message += ', Korean error message: %s' % korean_message
            logging.warning(message)
        return errcode

    def GetCodeListByMarketAsList(self, market):
        market = str(market)
        result = self.GetCodeListByMarket(market).rstrip(';')
        result = result.split(';') if result else []
        return result

    def GetNameListByMarketAsList(self, market):
        codes = self.GetCodeListByMarketAsList(market)
        names = [self.GetMasterCodeName(code) for code in codes]
        return names

    def GetAccountListAsList(self):
        accounts = self.GetLoginInfo('ACCLIST').rstrip(';')
        accounts = accounts.split(';') if accounts else []
        return accounts

    def GetMasterStockStateAsList(self, code):
        states = self.GetMasterStockState(code).strip()
        states = states.split('|') if states else []
        return states

    def _RemoveLeadingZerosForNumber(self, value, width=None):
        remove = False
        if width is None:
            remove = True
        elif isinstance(width, int) and len(value) == width:
            remove = True
        elif hasattr(width, '__iter__') and len(value) in width:
            remove = True
        if remove:
            return re.sub(r'^\s*([+-]?)[0]+([0-9]+(.[0-9]+)?)\s*$', r'\1\2', value)
        return value

    def _RemoveLeadingZerosForNumbersInValues(self, values, width=None):
        return [self._RemoveLeadingZerosForNumber(value, width) for value in values]

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

    def GetStockInfoAsDataFrame(self, codes=None, rqname=None, scrnno=None):
        """
        [화면번호]
         화면번호는 서버에 조회나 주문등 필요한 기능을 요청할때 이를 구별하기 위한 키값으로 이해하시면 됩니다.
         0000(혹은 0)을 제외한 임의의 숫자를 사용하시면 되는데 갯수가 200개로 한정되어 있기 때문에 이 갯수를 넘지 않도록 관리하셔야 합니다.
         만약 사용하는 화면번호가 200개를 넘는 경우 조회결과나 주문결과에 다른 데이터가 섞이거나 원하지 않는 결과를 나타날 수 있습니다.
        """
        if codes is None:
            codes = self.GetCommonCodeList()
        if rqname is None:
            rqname = '주식기본정보요청'
        if scrnno is None:
            scrnno = '0291'
        trcode = 'opt10001'
        codes_len = len(codes)
        columns = []
        records = []
        for i, code in enumerate(codes):
            logging.debug('Getting basic info for code: %s (%d/%d)', code, i+1, codes_len)
            inputs = {'종목코드': code}
            for response in self.TransactionCall(rqname, trcode, scrnno, inputs):
                if not columns:
                    columns = response.listen_response.single_data.names
                records.append(response.listen_response.single_data.values)
        df = pd.DataFrame.from_records(records, columns=columns)
        return df

    def GetDailyStockDataAsDataFrame(self, code, start_date=None, end_date=None, rqname=None, scrnno=None):
        """
        [수정주가구분] 1:유상증자, 2:무상증자, 4:배당락, 8:액면분할, 16:액면병합, 32:기업합병, 64:감자, 256:권리락
        """
        if start_date is None:
            now = datetime.datetime.now()
            start_date = now
            if now < now.replace(hour=15, minute=30):
                start_date -= datetime.timedelta(days=1)
        date_format = '%Y%m%d'
        if isinstance(start_date, datetime.datetime):
            start_date = start_date.strftime(date_format)
        if end_date is not None:
            if isinstance(end_date, datetime.datetime):
                end_date = end_date.strftime(date_format)
            stop_condition = {
                'name': '일자',
                'value': end_date,
            }
        else:
            stop_condition = None
        if rqname is None:
            rqname = '주식일봉차트조회요청'
        if scrnno is None:
            scrnno = '0613'
        trcode = 'opt10081'
        inputs = {
            '종목코드': code,
            '기준일자': start_date,
            '수정주가구분': '1',
        }
        columns = []
        records = []
        for response in self.TransactionCall(rqname, trcode, scrnno, inputs, stop_condition=stop_condition):
            if not columns:
                columns = list(response.listen_response.multi_data.names)
            for values in response.listen_response.multi_data.values:
                records.append(values.values)
            date_index = columns.index('일자')
            if len(response.listen_response.multi_data.values) > 0:
                from_date = response.listen_response.multi_data.values[0].values[date_index]
                to_date = response.listen_response.multi_data.values[-1].values[date_index]
                from_date = datetime.datetime.strptime(from_date, date_format)
                to_date = datetime.datetime.strptime(to_date, date_format)
                logging.debug('Received data from %s to %s for code %s', from_date, to_date, code)
        df = pd.DataFrame.from_records(records, columns=columns)
        return df

    def GetMinuteStockDataAsDataFrame(self, code, interval=None, start_date=None, end_date=None, rqname=None, scrnno=None):
        """
        [수정주가구분] 1:유상증자, 2:무상증자, 4:배당락, 8:액면분할, 16:액면병합, 32:기업합병, 64:감자, 256:권리락
        """
        if interval is None:
            interval = 15
        if interval is not None:
            interval = str(interval)
        if start_date is None:
            now = datetime.datetime.now()
            start_date = now
            if now < now.replace(hour=15, minute=30):
                start_date -= datetime.timedelta(days=1)
        date_format = '%Y%m%d%H%M%S'
        if isinstance(start_date, datetime.datetime):
            start_date = start_date.strftime(date_format)
        if end_date is not None:
            if isinstance(end_date, datetime.datetime):
                end_date = end_date.strftime(date_format)
            stop_condition = {
                'name': '체결시간',
                'value': end_date,
            }
        else:
            stop_condition = None
        if rqname is None:
            rqname = '주식분봉차트조회요청'
        if scrnno is None:
            scrnno = '0613'
        trcode = 'opt10080'
        inputs = {
            '종목코드': code,
            '틱범위': interval,
            '수정주가구분': '1',
        }
        columns = []
        records = []
        for response in self.TransactionCall(rqname, trcode, scrnno, inputs, stop_condition=stop_condition):
            if not columns:
                columns = list(response.listen_response.multi_data.names)
            for values in response.listen_response.multi_data.values:
                records.append(values.values)
            date_index = columns.index('체결시간')
            if len(response.listen_response.multi_data.values) > 0:
                from_date = response.listen_response.multi_data.values[0].values[date_index]
                to_date = response.listen_response.multi_data.values[-1].values[date_index]
                from_date = datetime.datetime.strptime(from_date, date_format)
                to_date = datetime.datetime.strptime(to_date, date_format)
                logging.debug('Received data from %s to %s for code %s', from_date, to_date, code)
        df = pd.DataFrame.from_records(records, columns=columns)
        return df

    def GetAccounts(self):
        return self.GetLoginInfo('ACCLIST').rstrip(';').split(';')

    def GetDepositInfo(self, account_no, lookup_type=None, rqname=None, scrnno=None):
        """
        조회구분 = 1:추정조회, 2:일반조회
        """
        if rqname is None:
            rqname = '예수금상세현황요청'
        if scrnno is None:
            scrnno = '0362'
        trcode = 'opw00001'
        inputs = {
            '계좌번호': account_no,
            '비밀번호': '',
            '비밀번호입력매체구분': '00',
            '조회구분': '2' if lookup_type is None else lookup_type,
        }
        single_output = None
        columns = []
        records = []
        for response in self.TransactionCall(rqname, trcode, scrnno, inputs):
            if single_output is None:
                single_output = dict(zip(
                    response.listen_response.single_data.names,
                    self._RemoveLeadingZerosForNumbersInValues(response.listen_response.single_data.values, [12, 15])))
            if not columns:
                columns = response.listen_response.multi_data.names
            for values in response.listen_response.multi_data.values:
                records.append(self._RemoveLeadingZerosForNumbersInValues(values.values, [12, 15]))
        _df = pd.DataFrame.from_records(records, columns=columns)
        return single_output

    def GetStockQuotes(self, code, rqname=None, scrnno=None):
        if rqname is None:
            rqname = '주식호가요청'
        if scrnno is None:
            scrnno = '4989'
        trcode = 'opt10004'
        inputs = {
            '종목코드': code,
        }
        single_output = None
        columns = []
        records = []
        for response in self.TransactionCall(rqname, trcode, scrnno, inputs):
            if single_output is None:
                single_output = dict(zip(
                    response.listen_response.single_data.names,
                    self._RemoveLeadingZerosForNumbersInValues(response.listen_response.single_data.values, [12, 15])))
            if not columns:
                columns = response.listen_response.multi_data.names
            for values in response.listen_response.multi_data.values:
                records.append(self._RemoveLeadingZerosForNumbersInValues(values.values, [12, 15]))
        _df = pd.DataFrame.from_records(records, columns=columns)
        return single_output

    def GetOrderLogAsDataFrame1(self, account_no, order_type=None, status_type=None, code=None, rqname=None, scrnno=None):
        """
       	계좌번호 = 전문 조회할 보유계좌번호
        전체종목구분 = 0:전체, 1:종목
        매매구분 = 0:전체, 1:매도, 2:매수
        종목코드 = 전문 조회할 종목코드
        체결구분 = 0:전체, 2:체결, 1:미체결
        """

        if rqname is None:
            rqname = '실시간미체결요청'
        if scrnno is None:
            scrnno = '1010'
        trcode = 'opt10075'
        inputs = {
            '계좌번호': account_no,
            '전체종목구분': '0' if code is None else '1',
            '매매구분': '0' if order_type is None else order_type,
            '종목코드': '' if code is None else code,
            '체결구분': '0' if status_type is None else status_type,
        }
        columns = []
        records = []
        for response in self.TransactionCall(rqname, trcode, scrnno, inputs):
            if not columns:
                columns = response.listen_response.multi_data.names
            for values in response.listen_response.multi_data.values:
                records.append(values.values)
        df = pd.DataFrame.from_records(records, columns=columns)
        return df

    def GetOrderLogAsDataFrame2(self, account_no, order_type=None, status_type=None, code=None, order_no=None, rqname=None, scrnno=None):
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
            rqname = '실시간체결요청'
        if scrnno is None:
            scrnno = '1010'
        trcode = 'opt10076'
        inputs = {
            '종목코드': '' if code is None else code,
            '조회구분': '0' if code is None else '1',
            '매도수구분': '0' if order_type is None else order_type,
            '계좌번호': account_no,
            '비밀번호': '',
            '주문번호': '' if order_no is None else order_no,
            '체결구분': '0' if status_type is None else status_type,
        }
        columns = []
        records = []
        for response in self.TransactionCall(rqname, trcode, scrnno, inputs):
            if not columns:
                columns = response.listen_response.multi_data.names
            for values in response.listen_response.multi_data.values:
                records.append(values.values)
        df = pd.DataFrame.from_records(records, columns=columns)
        return df

    def GetOrderLogAsDataFrame3(self, account_no, date=None, sort_type=None, asset_type=None, order_type=None, code=None, starting_order_no=None, rqname=None, scrnno=None):
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
            rqname = '계좌별주문체결내역상세요청'
        if scrnno is None:
            scrnno = '1010'
        trcode = 'opw00007'
        if date is None:
            now = datetime.datetime.now()
            market_start_time = now.replace(hour=8, minute=20, second=0, microsecond=0)
            if now < market_start_time:
                now = now - datetime.timedelta(days=1)
            date = now.strftime('%Y%m%d')
        inputs = {
            '주문일자': date,
            '계좌번호': account_no,
            '비밀번호': '',
            '비밀번호입력매체구분': '00',
            '조회구분': '1' if sort_type is None else sort_type,
            '주식채권구분': '0' if asset_type is None else asset_type,
            '매도수구분': '0' if order_type is None else order_type,
            '종목코드': '' if code is None else code,
            '시작주문번호': '' if starting_order_no is None else starting_order_no,
        }
        columns = []
        records = []
        for response in self.TransactionCall(rqname, trcode, scrnno, inputs):
            if not columns:
                columns = response.listen_response.multi_data.names
            for values in response.listen_response.multi_data.values:
                records.append(self._RemoveLeadingZerosForNumbersInValues(values.values, 10))
        df = pd.DataFrame.from_records(records, columns=columns)
        return df

    def GetAccountRateOfReturnAsDataFrame(self, account_no, rqname=None, scrnno=None):
        if rqname is None:
            rqname = '계좌수익률요청'
        if scrnno is None:
            scrnno = '1010'
        trcode = 'opt10085'
        inputs = {
            '계좌번호': account_no,
        }
        single_output = None
        columns = []
        records = []
        for response in self.TransactionCall(rqname, trcode, scrnno, inputs):
            print(response)
            if single_output is None:
                single_output = dict(zip(
                    response.listen_response.single_data.names,
                    self._RemoveLeadingZerosForNumbersInValues(response.listen_response.single_data.values, [10])))
            if not columns:
                columns = response.listen_response.multi_data.names
            for values in response.listen_response.multi_data.values:
                records.append(self._RemoveLeadingZerosForNumbersInValues(values.values, [10]))
        df = pd.DataFrame.from_records(records, columns=columns)
        return df

    def GetAccountEvaluationStatusAsSeriesAndDataFrame(self, account_no, include_delisted=True, rqname=None, scrnno=None):
        if rqname is None:
            rqname = '계좌평가현황요청'
        if scrnno is None:
            scrnno = '1010'
        trcode = 'opw00004'
        inputs = {
            '계좌번호': account_no,
            '비밀번호': '',
            '상장폐지조회구분': '0' if include_delisted else '1',
            '비밀번호입력매체구분': '00',
        }
        single_output = None
        columns = []
        records = []
        for response in self.TransactionCall(rqname, trcode, scrnno, inputs):
            if single_output is None:
                single_output = dict(zip(
                    response.listen_response.single_data.names,
                    self._RemoveLeadingZerosForNumbersInValues(response.listen_response.single_data.values, 12)))
            if not columns:
                columns = response.listen_response.multi_data.names
            for values in response.listen_response.multi_data.values:
                records.append(self._RemoveLeadingZerosForNumbersInValues(values.values, 12))
        single = pd.Series(single_output)
        multi = pd.DataFrame.from_records(records, columns=columns)
        return single, multi

    def GetAccountExecutionBalanceAsSeriesAndDataFrame(self, account_no, rqname=None, scrnno=None):
        server = self.GetLoginInfo('GetServerGubun')
        if server == '1':
            logging.warning('Not supported for simulated investment')
        if rqname is None:
            rqname = '체결잔고요청'
        if scrnno is None:
            scrnno = '1010'
        trcode = 'opw00005' # 모의투자에서 지원하지 않는 TR
        inputs = {
            '계좌번호': account_no,
            '비밀번호': '',
            '비밀번호입력매체구분': '00',
        }
        single_output = None
        columns = []
        records = []
        for response in self.TransactionCall(rqname, trcode, scrnno, inputs):
            if single_output is None:
                single_output = dict(zip(
                    response.listen_response.single_data.names,
                    self._RemoveLeadingZerosForNumbersInValues(response.listen_response.single_data.values)))
            if not columns:
                columns = response.listen_response.multi_data.names
            for values in response.listen_response.multi_data.values:
                records.append(self._RemoveLeadingZerosForNumbersInValues(values.values))
        single = pd.Series(single_output)
        multi = pd.DataFrame.from_records(records, columns=columns)
        return single, multi

    def GetAccountEvaluationBalanceAsSeriesAndDataFrame(self, account_no, lookup_type=None, rqname=None, scrnno=None):
        """
        조회구분 = 1:합산, 2:개별

        [ 주의 ]
        "수익률%" 데이터는 모의투자에서는 소숫점표현, 실거래서버에서는 소숫점으로 변환 필요 합니다.
        """
        if rqname is None:
            rqname = '계좌평가잔고내역요청'
        if scrnno is None:
            scrnno = '1010'
        trcode = 'opw00018'
        inputs = {
            '계좌번호': account_no,
            '비밀번호': '',
            '비밀번호입력매체구분': '00',
            '조회구분': '2' if lookup_type is None else lookup_type,
        }
        single_output = None
        columns = []
        records = []
        for response in self.TransactionCall(rqname, trcode, scrnno, inputs):
            if single_output is None:
                single_output = dict(zip(
                    response.listen_response.single_data.names,
                    self._RemoveLeadingZerosForNumbersInValues(response.listen_response.single_data.values, [12, 15])))
            if not columns:
                columns = response.listen_response.multi_data.names
            for values in response.listen_response.multi_data.values:
                records.append(self._RemoveLeadingZerosForNumbersInValues(values.values, [12, 15]))
        single = pd.Series(single_output)
        multi = pd.DataFrame.from_records(records, columns=columns)
        return single, multi

    def GetMarketPriceInfo(self, code, rqname=None, scrnno=None):
        if rqname is None:
            rqname = '시세표성정보요청'
        if scrnno is None:
            scrnno = '1010'
        trcode = 'opt10007'
        inputs = {
            '종목코드': code,
        }
        single_output = None
        columns = []
        records = []
        for response in self.TransactionCall(rqname, trcode, scrnno, inputs):
            if single_output is None:
                single_output = dict(zip(
                    response.listen_response.single_data.names,
                    response.listen_response.single_data.values))
            if not columns:
                columns = response.listen_response.multi_data.names
            for values in response.listen_response.multi_data.values:
                records.append(values.values)
        _df = pd.DataFrame.from_records(records, columns=columns)
        return single_output

    def WatchRealDataForCodesAsStream(self, codes=None, fids=None, scrnno=None, realtype=None, infer_fids=False, readable_names=False, fast_parse=False):
        if codes is None:
            codes = self.GetCommonCodeList() + self.GetKosdaqCodeList()
        if fids is None:
            fids = RealType.get_fids_by_realtype('주식시세')
        if scrnno is None:
            scrnno = '0001'
        if realtype is None:
            realtype = '0'
        for response in self.RealCall(scrnno, codes, fids, realtype, infer_fids, readable_names, fast_parse):
            yield response
