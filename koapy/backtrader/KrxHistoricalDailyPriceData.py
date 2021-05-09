import pandas as pd

from backtrader import TimeFrame, date2num
from backtrader.feed import DataBase
from tqdm import tqdm

from koapy.utils.data.KrxHistoricalDailyPriceDataForBacktestLoader import (
    KrxHistoricalDailyPriceDataForBacktestLoader,
)


class KrxHistoricalDailyPriceData(DataBase):

    # pylint: disable=no-member

    params = (
        ("loader", None),
        ("symbol", None),
        ("name", None),
        ("fromdate", None),
        ("todate", None),
        ("compression", 1),
        ("timeframe", TimeFrame.Days),
        ("calendar", None),
        ("lazy", False),
    )

    lines = (
        "amount",
        "marketcap",
        "shares",
    )

    def __init__(self):
        super().__init__()

        assert self.p.loader
        assert self.p.symbol

        assert self.p.timeframe == TimeFrame.Days
        assert self.p.compression == 1

        self.p.name = self.p.name or self.p.symbol or ""

        self._cursor = None
        self._started_already = False

        if not self.p.lazy:
            self.start()

    def _close_cursor(self):
        if self._cursor is not None:
            self._cursor.close()
            self._cursor = None

    def _initialize_cursor(self):
        self._close_cursor()
        self._cursor = self.p.loader.load_as_cursor(
            self.p.symbol, start_time=self.p.fromdate, end_time=self.p.todate
        )

    def start(self):
        if not self._started_already:
            self._initialize_cursor()
            self._started_already = True

    def stop(self):
        self._close_cursor()
        self._started_already = False

    def _load(self):
        if self._cursor is None:
            return False

        try:
            date, open_, high, low, close, volume, amount, marcap, shares = next(
                self._cursor
            )
        except StopIteration:
            return False
        else:
            dt = pd.Timestamp(date)

            self.lines.datetime[0] = date2num(dt)
            self.lines.open[0] = open_
            self.lines.high[0] = high
            self.lines.low[0] = low
            self.lines.close[0] = close
            self.lines.volume[0] = volume
            self.lines.openinterest[0] = 0.0

            self.lines.amount[0] = amount
            self.lines.marketcap[0] = marcap
            self.lines.shares[0] = shares

            return True

    @classmethod
    def adddata_fromfile(
        cls,
        cerebro,
        filename,
        symbols=None,
        fromdate=None,
        todate=None,
        progress_bar=True,
    ):
        loader = KrxHistoricalDailyPriceDataForBacktestLoader(filename)
        if symbols is None:
            symbols = loader.get_symbols()
        progress = tqdm(symbols, disable=not progress_bar)
        for symbol in progress:
            progress.set_description("Adding Symbol [%s]" % symbol)
            data = cls(
                loader=loader,
                symbol=symbol,
                fromdate=fromdate,
                todate=todate,
                name=symbol,
            )  # pylint: disable=unexpected-keyword-arg
            cerebro.adddata(data, name=data.p.name)
