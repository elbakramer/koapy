import math
import datetime

import pytz
import pandas as pd

from exchange_calendars import get_calendar

from koapy.utils.itertools import chunk
from koapy.utils.logging.Logging import Logging

class CybosPlusEntrypointMixin(Logging):

    def GetConnectState(self):
        return self.CpUtil.CpCybos.IsConnect

    def Connect(self, credential=None):
        """
        https://github.com/ippoeyeslhw/cppy/blob/master/cp_luncher.py
        """

        # https://github.com/pywinauto/pywinauto/issues/472
        import sys
        sys.coinit_flags = 2
        import warnings
        warnings.simplefilter("ignore", UserWarning)
        import pywinauto

        is_in_development = False

        if credential is None:
            from koapy.config import config
            credential = config.get('koapy.backend.daishin_cybos_plus.credential')

        userid = credential.get('user_id')
        password = credential.get('user_password')
        cert = credential.get('cert_password')

        auto_account_password = credential.get('auto_account_password')
        auto_cert_password = credential.get('auto_cert_password')
        price_check_only = credential.get('price_check_only')

        account_passwords = credential.get('account_passwords')

        _ = pywinauto.Application().start(r'C:\DAISHIN\STARTER\ncStarter.exe /prj:cp')
        desktop = pywinauto.Desktop(allow_magic_lookup=False)

        try:
            ask_stop = desktop.window(title='ncStarter')
            ask_stop.wait('ready', timeout=10)
        except pywinauto.timings.TimeoutError:
            pass
        else:
            if is_in_development:
                ask_stop.print_control_identifiers()
            if ask_stop['Static2'].window_text().endswith('종료하시겠습니까?'):
                ask_stop['Button1'].click()
                try:
                    ask_stop = desktop.window(title='ncStarter')
                    ask_stop.wait('ready', timeout=10)
                except pywinauto.timings.TimeoutError:
                    pass
                else:
                    if is_in_development:
                        ask_stop.print_control_identifiers()
                    if ask_stop['Static2'].window_text().endswith('종료할 수 없습니다.'):
                        ask_stop['Button'].click()
                        raise RuntimeError('cannot stop existing server')

        starter = desktop.window(title='CYBOS Starter')
        starter.wait('ready', timeout=30)
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
                confirm.wait('ready', timeout=5)
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
                confirm.wait('ready', timeout=5)
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
            starter.wait_not('visible', timeout=60)
        except pywinauto.timings.TimeoutError:
            pass
        else:
            notice = desktop.window(title='공지사항')
            try:
                notice.wait('ready', timeout=60)
            except pywinauto.timings.TimeoutError:
                pass
            else:
                notice.close()
                try:
                    notice.wait_not('visible', timeout=60)
                except pywinauto.timings.TimeoutError:
                    pass

    def CommConnect(self, credential=None):
        return self.Connect(credential)

    def EnsureConnected(self, credential=None):
        errcode = 0
        if self.GetConnectState() == 0:
            self.Connect(credential)
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
        codes = self.CpUtil.CpCodeMgr.GetStockListByMarket(market)
        codes = list(codes)
        return codes

    def GetKospiCodeList(self):
        codes = self.GetCodeListByMarketAsList(1)
        return codes

    def GetKosdaqCodeList(self):
        codes = self.GetCodeListByMarketAsList(2)
        return codes

    def GetGeneralCodeList(self,
            include_preferred_stock=False,
            include_etn=False,
            include_etf=False,
            include_mutual_fund=False,
            include_reits=False,
            include_kosdaq=False):

        codes = self.GetCodeListByMarketAsList(1)
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
            codes += self.GetCodeListByMarketAsList(2)

        codes = sorted(codes)

        return codes

    def GetStockDataAsDataFrame(self, code, chart_type, interval, start_date=None, end_date=None, adjusted_price=False, adjustement_only=False):
        """
        http://cybosplus.github.io/cpsysdib_rtf_1_/stockchart.htm
        """
        chart = self.CpSysDib.StockChart

        calendar = get_calendar('XKRX')
        tz = calendar.tz or pytz.timezone('Asia/Seoul')

        needs_time = chart_type in ['m', 'T']

        if len(code) == 6 and not code.startswith('A'):
            code = 'A' + code

        fids = [0]

        if needs_time:
            fids += [1]

        if not adjustement_only:
            fids += [2, 3, 4, 5, 8, 9]
        else:
            assert chart_type == 'D'
            adjusted_price = True

        if adjusted_price and chart_type == 'D':
            fids += [18, 19]

        num_fids = len(fids)
        sorted_fids = sorted(fids)
        field_indexes = [sorted_fids.index(i) for i in fids]

        maximum_value_count = 20000
        expected_count = math.floor(maximum_value_count / num_fids) - 1
        request_count = expected_count + 1

        date_format_arg = '%Y%m%d%H%M%S'
        date_format_input = '%Y%m%d'

        if start_date is None:
            start_date = calendar.previous_close(pd.Timestamp.now()).astimezone(tz).to_pydatetime()
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

        start_date = start_date.astimezone(tz)

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

            end_date = end_date.astimezone(tz)

        should_stop = False
        dataframes = []

        while not should_stop:
            chart.SetInputValue(0, code)
            chart.SetInputValue(1, ord('2'))
            chart.SetInputValue(2, int(internal_start_date.strftime(date_format_input)))
            chart.SetInputValue(4, request_count)
            chart.SetInputValue(5, fids)
            chart.SetInputValue(6, ord(chart_type))
            chart.SetInputValue(7, int(interval))
            chart.SetInputValue(9, ord('1') if adjusted_price else ord('0')) # 기본으로 수정주가 적용하지 않음

            self.logger.debug('Requesting from %s', internal_start_date)
            chart.RateLimitedBlockRequest()

            received_count = chart.GetHeaderValue(3)
            self.logger.debug('Requested %d, received %d records', request_count, received_count)

            num_fields = chart.GetHeaderValue(1)
            assert num_fields == num_fids

            names = chart.GetHeaderValue(2)
            names = [names[i] for i in field_indexes]

            records = []
            for i in range(received_count):
                record = [chart.GetDataValue(j, i) for j in field_indexes]
                records.append(record)

            df = pd.DataFrame.from_records(records, columns=names)

            if df.shape[0] != 0:
                from_date = datetime.datetime.strptime(df.iloc[0]['날짜'].astype(int).astype(str), date_format_input)
                last_date = datetime.datetime.strptime(df.iloc[-1]['날짜'].astype(int).astype(str), date_format_input)

                from_date = from_date.astimezone(tz)
                last_date = last_date.astimezone(tz)

                self.logger.debug('Received data from %s to %s for code %s', from_date, last_date, code)

            should_stop = received_count < expected_count

            if not should_stop and end_date is not None:
                should_stop = last_date <= end_date

            if not should_stop:
                self.logger.debug('More data to request remains')
                internal_start_date = last_date
                nrows_before_truncate = df.shape[0]
                datetimes = pd.to_datetime(df['날짜'].astype(int).astype(str), format='%Y%m%d')
                datetimes = datetimes.dt.tz_localize(tz)
                condition = datetimes > last_date
                df = df.loc[condition]
                nrows_after_truncate = df.shape[0]
                self.logger.debug('Trailing rows truncated: %d', nrows_before_truncate - nrows_after_truncate)
            else:
                self.logger.debug('No more data to request')
                if end_date is not None:
                    nrows_before_truncate = df.shape[0]
                    dates = df['날짜'].astype(int).astype(str)
                    if needs_time:
                        times = df['시간'].astype(int).astype(str).str.ljust(6, '0')
                        datetimes = dates.str.cat(times)
                        datetimes = pd.to_datetime(datetimes, format='%Y%m%d%H%M%S')
                    else:
                        datetimes = dates
                        datetimes = pd.to_datetime(datetimes, format='%Y%m%d')
                    datetimes = datetimes.dt.tz_localize(tz)
                    condition = datetimes > end_date
                    df = df.loc[condition]
                    nrows_after_truncate = df.shape[0]
                    self.logger.debug('Trailing rows truncated: %d', nrows_before_truncate - nrows_after_truncate)

            dataframes.append(df)

        df = pd.concat(dataframes)
        df.reset_index(drop=True, inplace=True)

        return df

    def GetDailyStockDataAsDataFrame(self, code, start_date=None, end_date=None, adjusted_price=False):
        return self.GetStockDataAsDataFrame(code, 'D', 1, start_date, end_date, adjusted_price=adjusted_price)

    def GetMinuteStockDataAsDataFrame(self, code, interval, start_date=None, end_date=None, adjusted_price=False):
        return self.GetStockDataAsDataFrame(code, 'm', interval, start_date, end_date, adjusted_price=adjusted_price)

    def GetDailyAdjustmentRatioAsDataFrame(self, code, start_date=None, end_date=None):
        return self.GetStockDataAsDataFrame(code, 'D', 1, start_date, end_date, adjustement_only=True)

    def GetCurrentStockDataAsDataFrame(self, codes):
        """
        http://cybosplus.github.io/cpdib_rtf_1_/stockmst2.htm
        """
        stock = self.DsCbo1.StockMst2

        names = [
            '종목코드',
            '종목명',
            '시간',
            '현재가',
            '전일대비',
            '상태구분',
            '시가',
            '고가',
            '저가',
            '매도호가',
            '매수호가',
            '거래량',
            '거래대금',
            '총매도잔량',
            '총매수잔량',
            '매도잔량',
            '매수잔량',
            '상장주식수',
            '외국인보유비율',
            '전일종가',
            '전일거래량',
            '체결강도',
            '순간체결량',
            '체결가비교',
            '호가비교',
            '동시호가구분',
            '예상체결가',
            '예상체결가 전일대비',
            '예상체결가 상태구분',
            '예상체결가 거래량',
        ]
        fids = list(range(len(names)))

        dataframes = []
        for code_chunk in chunk(codes, 110):
            stock.SetInputValue(0, ','.join(code_chunk))
            stock.RateLimitedBlockRequest()
            received_count = stock.GetHeaderValue(0)
            records = []
            for i in range(received_count):
                record = [stock.GetDataValue(j, i) for j in fids]
                records.append(record)

            df = pd.DataFrame.from_records(records, columns=names)
            dataframes.append(df)

        df = pd.concat(dataframes)
        df.reset_index(drop=True, inplace=True)

        return df
