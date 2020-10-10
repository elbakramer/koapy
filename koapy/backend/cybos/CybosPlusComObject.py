import math
import logging
import datetime

import pandas as pd

import win32com.client

from pywintypes import com_error as ComError # pylint: disable=no-name-in-module

from koapy.utils.rate_limiting.RateLimiter import CybosBlockRequestRateLimiter
from koapy.utils.krx.calendar import get_last_krx_datetime
from koapy.config import config

import pywinauto

class CybosPlusComObjectDispatch:

    def __init__(self, dispatch):
        self._dispatch = dispatch

    @CybosBlockRequestRateLimiter()
    def RateLimitedBlockRequest(self):
        return self._dispatch.BlockRequest()

    def __getattr__(self, name):
        return getattr(self._dispatch, name)

class CybosPlusComObjectInner:

    def __init__(self, parent, prefix):
        self._parent = parent
        self._prefix = prefix
        self._dispatches = {}

    def __getattr__(self, name):
        dispatch = self._dispatches.get(name)
        if dispatch is None:
            try:
                dispatch = win32com.client.Dispatch('%s.%s' % (self._prefix, name))
            except ComError:
                if len(self._dispatches) == 0:
                    del self._parent._inners[self._prefix]
                raise
            else:
                dispatch = CybosPlusComObjectDispatch(dispatch)
                self._dispatches[name] = dispatch
        return dispatch

is_in_development = False

class CybosPlusComObject:

    """
    http://cybosplus.github.io/
    """

    def __init__(self):
        self._inners = {}

    def __getattr__(self, name):
        if name.startswith('Cp'):
            return self._inners.setdefault(name, CybosPlusComObjectInner(self, name))
        raise AttributeError

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return

    def GetConnectState(self):
        return self.CpUtil.CpCybos.IsConnect

    def CommConnect(self):
        """
        https://github.com/ippoeyeslhw/cppy/blob/master/cp_luncher.py
        """

        login_config = config.get('koapy.backend.cybos.login')

        userid = login_config.get('id')
        password = login_config.get('password')
        cert = login_config.get('cert')

        auto_account_password = login_config.get('auto_account_password')
        auto_cert_password = login_config.get('auto_cert_password')
        price_check_only = login_config.get('price_check_only')

        account_passwords = login_config.get('account_passwords')

        app = pywinauto.Application().start(r'C:\DAISHIN\STARTER\ncStarter.exe /prj:cp')
        desktop = pywinauto.Desktop(allow_magic_lookup=False)

        try:
            ask_stop = desktop.window(title='ncStarter')
            ask_stop.wait('ready', timeout=8)
        except pywinauto.timings.TimeoutError:
            pass
        else:
            if is_in_development:
                ask_stop.print_control_identifiers()
            if ask_stop['Static2'].window_text().endswith('종료하시겠습니까?'):
                ask_stop['Button1'].click()
                try:
                    ask_stop = desktop.window(title='ncStarter')
                    ask_stop.wait('ready', timeout=5)
                except pywinauto.timings.TimeoutError:
                    pass
                else:
                    if is_in_development:
                        ask_stop.print_control_identifiers()
                    if ask_stop['Static2'].window_text().endswith('종료할 수 없습니다.'):
                        ask_stop['Button'].click()
                        raise RuntimeError('cannot stop existing server')

        starter = desktop.window(title='CYBOS Starter')
        starter.wait('ready', timeout=10)
        if is_in_development:
            starter.print_control_identifiers()

        if userid:
            starter['Edit1'].set_text(userid)
        if password:
            starter['Edit2'].set_text(password)
        else:
            raise RuntimeError('no password given')
        if not price_check_only:
            if cert:
                starter['Edit3'].set_text(cert)
            else:
                raise RuntimeError('no cert password given')

        if auto_account_password:
            starter['Button4'].check()
            try:
                confirm = desktop.window(title='대신증권')
                confirm.wait('ready', timeout=1)
            except pywinauto.timings.TimeoutError:
                pass
            else:
                if is_in_development:
                    confirm.print_control_identifiers()
                confirm['Button'].click()
        if auto_cert_password:
            starter['Button5'].check()
            try:
                confirm = desktop.window(title='대신증권')
                confirm.wait('ready', timeout=1)
            except pywinauto.timings.TimeoutError:
                pass
            else:
                if is_in_development:
                    confirm.print_control_identifiers()
                confirm['Button'].click()
        if price_check_only:
            starter['Button6'].check()

        starter['Button1'].click()

        should_stop = False
        while not should_stop:
            try:
                account_password = desktop.window(title='종합계좌 비밀번호 확인 입력')
                account_password.wait('ready', timeout=5)
            except pywinauto.timings.TimeoutError:
                should_stop = True
            else:
                if is_in_development:
                    account_password.print_control_identifiers()
                account_no = account_password['Static'].window_text().split(':')[-1].strip()
                if account_no in account_passwords:
                    account_password['Edit'].set_text(account_passwords[account_no])
                else:
                    raise RuntimeError('no account password given for account %s' % account_no)
                account_password['Button1'].click()

        try:
            starter.wait_not('visible', timeout=10)
        except pywinauto.timings.TimeoutError:
            pass

    def EnsureConnected(self):
        errcode = 0
        if self.GetConnectState() == 0:
            self.CommConnect()
        if self.GetConnectState() == 0:
            raise RuntimeError('Cybos Plus is not running, please start Cybos Plus.')
        return errcode

    def GetCodeListByMarketAsList(self, market):
        """
        0: 구분없음
        1: 거래소
        2: 코스닥
        3: 프리보드
        4: KRX
        """
        return self.CpUtil.CpCodeMgr.GetStockListByMarket(market)

    def GetKospiCodeList(self):
        codes = self.GetCodeListByMarketAsList(1)
        codes = sorted(codes)
        return codes

    def GetKosdaqCodeList(self):
        codes = self.GetCodeListByMarketAsList(2)
        codes = sorted(codes)
        return codes

    def GetCommonCodeList(self,
            include_preferred_stock=True,
            include_etn=False,
            include_etf=False,
            include_mutual_fund=False,
            include_reits=False,
            include_kosdaq=False):

        codes = self.GetKospiCodeList()
        codemgr = self.CpUtil.CpCodeMgr

        if not include_preferred_stock:
            codes = [code for code in codes if code.endswith('0')]
        if not include_etn:
            codes = [code for code in codes if not code.startswith('Q')]
        if not include_etf:
            codes = [code for code in codes if codemgr.GetStockSectionKind(code) not in [10, 12]]
        if not include_mutual_fund:
            codes = [code for code in codes if codemgr.GetStockSectionKind(code) not in [2]]
        if not include_reits:
            codes = [code for code in codes if codemgr.GetStockSectionKind(code) not in [3]]

        if include_kosdaq:
            codes += self.GetKosdaqCodeList()

        codes = sorted(codes)

        return codes

    def GetStockDataAsDataFrame(self, code, chart_type, interval, start_date=None, end_date=None):
        """
        http://cybosplus.github.io/cpsysdib_rtf_1_/stockchart.htm
        """
        chart = self.CpSysDib.StockChart

        if len(code) == 6 and not code.startswith('A'):
            code = 'A' + code

        fids = [5, 8, 0, 1, 2, 3, 4, 18, 19]
        num_fids = len(fids)
        sorted_fids = sorted(fids)
        field_indexes = [sorted_fids.index(i) for i in fids]

        maximum_value_count = 20000
        expected_count = math.floor(maximum_value_count / num_fids) - 1
        request_count = expected_count + 1

        date_format_arg = '%Y%m%d%H%M%S'
        date_format_input = '%Y%m%d'

        if start_date is None:
            start_date = get_last_krx_datetime()
        if isinstance(start_date, str):
            start_date_len = len(start_date)
            if start_date_len == 14:
                start_date = datetime.datetime.strptime(start_date, date_format_arg)
            elif start_date_len == 8:
                start_date = datetime.datetime.strptime(start_date, date_format_input)
            else:
                raise ValueError
        if not isinstance(start_date, datetime.datetime):
            raise ValueError

        internal_start_date = start_date

        if end_date is not None:
            if isinstance(end_date, str):
                end_date_len = len(end_date)
                if end_date_len == 14:
                    end_date = datetime.datetime.strptime(end_date, date_format_arg)
                elif end_date_len == 8:
                    end_date = datetime.datetime.strptime(end_date, date_format_input)
                else:
                    raise ValueError
            if not isinstance(end_date, datetime.datetime):
                raise ValueError

        should_stop = False
        dataframes = []

        while not should_stop:
            chart.SetInputValue(0, code)
            chart.SetInputValue(1, ord('2'))
            chart.SetInputValue(2, int(internal_start_date.strftime(date_format_input)))
            chart.SetInputValue(4, request_count)
            chart.SetInputvalue(5, fids)
            chart.SetInputValue(6, ord(chart_type))
            chart.SetInputValue(7, int(interval))
            chart.SetInputValue(9, ord('1')) # TODO: 수정주가로 받으면서 append 하는 경우 과거 데이터에 대한 추가보정이 별도로 필요함

            logging.debug('Requesting from %s', internal_start_date)
            err = chart.RateLimitedBlockRequest()
            if err < 0:
                logging.warning('BlockRequest returned non-zero code %d', err)

            received_count = chart.GetHeaderValue(3)
            logging.debug('Requested %d, received %d records', request_count, received_count)

            num_fields = chart.GetHeaderValue(1)
            assert num_fields == num_fids

            names = chart.GetHeaderValue(2)
            names = [names[i] for i in field_indexes]

            records = []
            for i in range(received_count):
                record = [chart.GetDataValue(j, i) for j in field_indexes]
                records.append(record)

            df = pd.DataFrame.from_records(records, columns=names)

            from_date = datetime.datetime.strptime(df.iloc[0]['날짜'].astype(int).astype(str), date_format_input)
            last_date = datetime.datetime.strptime(df.iloc[-1]['날짜'].astype(int).astype(str), date_format_input)
            logging.debug('Received data from %s to %s for code %s', from_date, last_date, code)

            if end_date is None:
                should_stop = received_count < expected_count
            else:
                should_stop = last_date <= end_date

            if not should_stop:
                logging.debug('More data to request remains')
                internal_start_date = last_date
                nrows_before_truncate = df.shape[0]
                condition = pd.to_datetime(df['날짜'].astype(int).astype(str), format='%Y%m%d') > last_date
                df = df.loc[condition]
                nrows_after_truncate = df.shape[0]
                logging.debug('Trailing rows truncated: %d', nrows_before_truncate - nrows_after_truncate)
            else:
                logging.debug('No more data to request')
                if end_date is not None:
                    nrows_before_truncate = df.shape[0]
                    datetimes = pd.to_datetime(df['날짜'].astype(int).astype(str).str.cat(df['시간'].astype(int).astype(str).str.zfill(6)), format='%Y%m%d%H%M%S')
                    condition = datetimes > end_date
                    df = df.loc[condition]
                    nrows_after_truncate = df.shape[0]
                    logging.debug('Trailing rows truncated: %d', nrows_before_truncate - nrows_after_truncate)

            dataframes.append(df)

        return pd.concat(dataframes)

    def GetDailyStockDataAsDataFrame(self, code, start_date=None, end_date=None):
        return self.GetStockDataAsDataFrame(code, 'D', 1, start_date, end_date)

    def GetMinuteStockDataAsDataFrame(self, code, interval, start_date=None, end_date=None):
        return self.GetStockDataAsDataFrame(code, 'm', interval, start_date, end_date)

if __name__ == '__main__':
    CybosPlusComObject().CommConnect()
