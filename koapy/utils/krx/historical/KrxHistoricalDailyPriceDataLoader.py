import pandas as pd

from sqlalchemy import create_engine, inspect
from sqlalchemy import Table, MetaData

from exchange_calendars import get_calendar
from tqdm import tqdm

from koapy.utils.krx.historical.KrxHistoricalDailyPriceDataDownloader import KrxHistoricalDailyPriceDataDownloader

class KrxHistoricalDailyPriceDataLoader:

    def __init__(self, filename):
        self._downloader = KrxHistoricalDailyPriceDataDownloader()
        self._engine = create_engine('sqlite:///' + filename)
        self._inspector = inspect(self._engine)
        self._calendar = get_calendar('XKRX')

    def load_naive(self, symbol):
        data = pd.read_sql_table(symbol, self._engine, index_col='Date', parse_dates=['Date'])
        return data

    def load_if_exists(self, symbol):
        if self._inspector.has_table(symbol):
            data = self.load_naive(symbol)
            if data.shape[0] > 0:
                return data

    def load_or_download(self, symbol, start_date=None, end_date=None, save=True):
        if end_date is None:
            now = pd.Timestamp.now(self._calendar.tz)
            end_date = self._calendar.previous_close(now).normalize()
        if self._inspector.has_table(symbol):
            data = self.load_naive(symbol)
            data = data.sort_index()
            if data.shape[0] > 0:
                start_date = data.index.max().tz_localize(self._calendar.tz) + self._calendar.day
                if start_date < end_date:
                    recent_data = self._downloader.download(symbol, start_date, end_date)
                    if recent_data.shape[0] > 0:
                        data = data.combine_first(recent_data)[data.columns]
                        data = data.convert_dtypes(convert_floating=False)
                        data = data.sort_index()
                        if save:
                            data.to_sql(symbol, self._engine, if_exists='replace')
                return data
            else:
                Table(symbol, MetaData()).drop(self._engine)
        if not self._inspector.has_table(symbol):
            if start_date is None:
                start_date = pd.Timestamp(1990, 1, 1)
            data = self._downloader.download(symbol, start_date, end_date)
            data = data.convert_dtypes(convert_floating=False)
            data = data.sort_index()
            if data.shape[0] > 0:
                if save:
                    data.to_sql(symbol, self._engine, if_exists='replace')
                return data

    def load(self, symbol):
        return self.load_or_download(symbol)

    def load_all(self, include_delisted=False, progress_bar=False):
        symbols_with_delisted = {}
        result = {}

        symbols = self._downloader.stocks.index.tolist()
        for symbol in symbols:
            symbols_with_delisted.setdefault(symbol, False)

        if include_delisted:
            symbols = self._downloader.stocks_delisted.index.tolist()
            for symbol in symbols:
                symbols_with_delisted.setdefault(symbol, True)

        now = pd.Timestamp.now(self._calendar.tz)
        end_date = self._calendar.previous_close(now).normalize()

        disable = not progress_bar

        for symbol, _delisted in tqdm(symbols_with_delisted.items(), disable=disable):
            data = self.load_or_download(symbol, end_date=end_date)
            result[symbol] = data

        return result
