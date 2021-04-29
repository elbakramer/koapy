import numpy as np
import pandas as pd
from exchange_calendars import get_calendar
from tqdm import tqdm

from ..store import SQLiteStore
from .KrxHistoricalDailyPriceDataLoader import KrxHistoricalDailyPriceDataLoader


class KrxHistoricalDailyPriceDataForBacktestLoader:
    def __init__(self, filename, library=None):
        self._loader = KrxHistoricalDailyPriceDataLoader(filename)
        self._store = SQLiteStore(filename)
        self._calendar = get_calendar("XKRX")

        if library is None:
            library = "XKRX-ALL-BACKTEST"

        self._library = self._store.get_or_create_library(library)

    @classmethod
    def get_adjust_ratios(cls, data, sort=True):
        if sort:
            data = data.sort_index(ascending=False)
        adjust_ratios = []
        last_close = data["Close"].iloc[0]
        last_adjust_ratio = 1.0
        adjust_ratios.append(last_adjust_ratio)
        eleven_days = pd.Timedelta(11, unit="D")
        for i in range(data.shape[0] - 1):
            if data.index[i] - data.index[i + 1] > eleven_days:
                last_close = data["Close"].iloc[i + 1]
                last_adjust_ratio = 1.0
            else:
                last_close = last_close - data["Change"].iloc[i] * last_adjust_ratio
                last_adjust_ratio = last_close / data["Close"].iloc[i + 1]
            adjust_ratios.append(last_adjust_ratio)
        adjust_ratios = np.array(adjust_ratios)
        return adjust_ratios

    @classmethod
    def adjust_data(cls, data, sort=True):
        if sort:
            data = data.sort_index(ascending=False)
        adjust_ratios = cls.get_adjust_ratios(data, sort=False)
        data["Open"] = data["Open"] * adjust_ratios
        data["High"] = data["High"] * adjust_ratios
        data["Low"] = data["Low"] * adjust_ratios
        data["Close"] = data["Close"] * adjust_ratios
        data["Volume"] = data["Volume"] / adjust_ratios
        return data

    def get_symbols(self):
        return self._library.list_symbols()

    def update(self, download=False, progress_bar=False):
        now = pd.Timestamp.now(self._calendar.tz)
        end_date = (
            self._calendar.previous_close(now).astimezone(self._calendar.tz).normalize()
        )

        symbols_with_delisted = {}

        for symbol in self._loader.symbols:
            symbols_with_delisted.setdefault(symbol, False)
        for symbol in self._loader.symbols_delisted:
            symbols_with_delisted.setdefault(symbol, True)

        entire_index = pd.DatetimeIndex([], name="Date")

        entire_data = {}
        entire_data_converted = {}

        progress = tqdm(symbols_with_delisted.items(), disable=not progress_bar)
        for symbol, is_delisted in progress:
            progress.set_description("Loading Symbol [%s]" % symbol)
            if download:
                versioned_item = self._loader.load_or_download(
                    symbol, is_delisted=is_delisted, end_date=end_date
                )
            else:
                versioned_item = self._loader.load_from_database(
                    symbol, is_delisted=is_delisted
                )
            if versioned_item is not None:
                entire_data[symbol] = versioned_item.data

        progress = tqdm(entire_data.items(), disable=not progress_bar)
        for symbol, data in progress:
            progress.set_description("Adjusting Symbol [%s]" % symbol)
            entire_index = entire_index.union(data.index)
            data = data[data["Close"] > 0]
            if data.shape[0] > 0:
                data = self.adjust_data(data)
                data = data.sort_index()
                columns = [
                    "Open",
                    "High",
                    "Low",
                    "Close",
                    "Volume",
                    "Amount",
                    "MarCap",
                    "Shares",
                ]
                data = data[columns]
                entire_data_converted[symbol] = data

        progress = tqdm(entire_data_converted.items(), disable=not progress_bar)
        for symbol, data in progress:
            progress.set_description("Saving Symbol [%s]" % symbol)
            data = data.reindex(entire_index)
            data = data.fillna(0)
            self._library.write(symbol, data)

    def load(self, symbol, start_time=None, end_time=None):
        if self._library.has_symbol(symbol):
            versioned_item = self._library.read(
                symbol, start_time=start_time, end_time=end_time
            )
            if (
                versioned_item is not None
                and versioned_item.data is not None
                and versioned_item.data.shape[0] > 0
            ):
                return versioned_item.data

    def load_as_cursor(self, symbol, start_time=None, end_time=None):
        if self._library.has_symbol(symbol):
            versioned_item = self._library.read_as_cursor(
                symbol, start_time=start_time, end_time=end_time
            )
            if versioned_item is not None and versioned_item.data is not None:
                return versioned_item.data
