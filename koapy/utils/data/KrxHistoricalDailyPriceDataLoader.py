import pandas as pd

from exchange_calendars import get_calendar
from tqdm import tqdm

from ..store import SQLiteStore
from .KrxHistoricalDailyPriceDataDownloader import KrxHistoricalDailyPriceDataDownloader


class KrxHistoricalDailyPriceDataLoader:
    def __init__(self, filename, library=None, library_delisted=None):
        self._downloader = KrxHistoricalDailyPriceDataDownloader()
        self._store = SQLiteStore(filename)
        self._calendar = get_calendar("XKRX")

        if library is None:
            library = "XKRX"
        if library_delisted is None:
            library_delisted = "XKRX-DELISTED"

        self._library = self._store.get_or_create_library(library)
        self._library_delisted = self._store.get_or_create_library(library_delisted)

    @property
    def symbols(self):
        return self._downloader.stocks.index

    @property
    def symbols_delisted(self):
        return self._downloader.stocks_delisted.index

    def load_from_database(self, symbol, is_delisted=None):
        if is_delisted is None:
            is_delisted = symbol not in self.symbols

        library = self._library if not is_delisted else self._library_delisted

        if library.has_symbol(symbol):
            versioned_item = library.read(symbol)
            if versioned_item.data is not None and versioned_item.data.shape[0] > 0:
                return versioned_item

    def load_or_download(
        self, symbol, is_delisted=None, start_date=None, end_date=None
    ):
        if is_delisted is None:
            is_delisted = symbol not in self.symbols

        library = self._library
        now = pd.Timestamp.now(self._calendar.tz)

        if is_delisted:
            library = self._library_delisted

        if library.has_symbol(symbol):
            versioned_item = self.load_from_database(symbol, is_delisted=is_delisted)
            if not is_delisted and versioned_item is not None:
                if start_date is None:
                    start_date = (
                        versioned_item.data.index.max().tz_localize(self._calendar.tz)
                        + self._calendar.day
                    )
                if end_date is None:
                    end_date = (
                        self._calendar.previous_close(now)
                        .astimezone(self._calendar.tz)
                        .normalize()
                    )
                if start_date <= end_date:
                    recent_data = self._downloader.download(
                        symbol, start_date=start_date
                    )
                    if recent_data is not None and recent_data.shape[0] > 0:
                        data = versioned_item.data
                        data = data.combine_first(recent_data)[data.columns]
                        data = data.convert_dtypes(convert_floating=False)
                        data = data.sort_index()
                        versioned_item = library.write(symbol, data)
            return versioned_item
        else:
            data = self._downloader.download(
                symbol, start_date=start_date, end_date=end_date
            )
            if data is not None and data.shape[0] > 0:
                data = data.convert_dtypes(convert_floating=False)
                data = data.sort_index()
                versioned_item = library.write(symbol, data)
                return versioned_item

    def load(
        self, symbol, is_delisted=None, start_date=None, end_date=None, download=True
    ):
        if download:
            return self.load_or_download(
                symbol,
                is_delisted=is_delisted,
                start_date=start_date,
                end_date=end_date,
            )
        else:
            return self.load_from_database(symbol, is_delisted=is_delisted)

    def update(self, progress_bar=False):
        now = pd.Timestamp.now(self._calendar.tz)
        end_date = (
            self._calendar.previous_close(now).astimezone(self._calendar.tz).normalize()
        )

        symbols_with_delisted = {}

        for symbol in self.symbols:
            symbols_with_delisted.setdefault(symbol, False)
        for symbol in self.symbols_delisted:
            symbols_with_delisted.setdefault(symbol, True)

        progress = tqdm(symbols_with_delisted.items(), disable=not progress_bar)
        for symbol, is_delisted in progress:
            progress.set_description("Updating Symbol [%s]" % symbol)
            _versioned_item = self.load_or_download(
                symbol, is_delisted=is_delisted, end_date=end_date
            )
