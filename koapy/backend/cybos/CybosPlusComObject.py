import math
import logging
import datetime

import pandas as pd

import win32com.client
from pywintypes import com_error as ComError # pylint: disable=no-name-in-module

from koapy.utils.rate_limiting.RateLimiter import CybosRateLimiter
from koapy.utils.krx.holiday import get_last_krx_datetime

class CybosPlusComObjectDispatch:

    def __init__(self, dispatch):
        self._dispatch = dispatch

    @CybosRateLimiter()
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

    def EnsureConnected(self):
        errcode = 0
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

    def GetKospiCodeList(self, include_preferred_stocks=False, include_reits=True):
        return self.GetCodeListByMarketAsList(1)

    def GetKosdaqCodeList(self):
        return self.GetCodeListByMarketAsList(2)

    def GetStockDataAsDataFrame(self, code, type, interval, start_date=None, end_date=None):
        chart = self.CpSysDib.StockChart

        if len(code) == 6 and not code.startswith('A'):
            code = 'A' + code

        fids = [5, 8, 0, 1, 2, 3, 4]
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
            chart.SetInputValue(6, ord(type))
            chart.SetInputValue(7, int(interval))
            chart.SetInputValue(9, ord('1'))

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

            from_date = datetime.datetime.strptime(str(df.iloc[0]['날짜']), date_format_input)
            last_date = datetime.datetime.strptime(str(df.iloc[-1]['날짜']), date_format_input)
            logging.debug('Received data from %s to %s for code %s', from_date, last_date, code)

            if end_date is None:
                should_stop = received_count < expected_count
            else:
                should_stop = last_date <= end_date

            if not should_stop:
                logging.debug('More data to request remains')
                internal_start_date = last_date
                nrows_before_truncate = df.shape[0]
                condition = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d') > last_date
                df = df.loc[condition]
                nrows_after_truncate = df.shape[0]
                logging.debug('Trailing rows truncated: %d', nrows_before_truncate - nrows_after_truncate)
            else:
                logging.debug('No more data to request')
                if end_date is not None:
                    nrows_before_truncate = df.shape[0]
                    datetimes = pd.to_datetime(df['날짜'].astype(str).str.cat(df['시간'].astype(str).str.zfill(6)), format='%Y%m%d%H%M%S')
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
