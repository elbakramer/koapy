import pandas as pd

from backtrader import TimeFrame, date2num
from sqlalchemy import create_engine, inspect
from tqdm import tqdm

from koapy.backtrader.SQLiteData import SQLiteData
from koapy.utils.data.KrxHistoricalDailyPriceDataForBacktestLoader import (
    KrxHistoricalDailyPriceDataForBacktestLoader,
)


class KrxHistoricalDailyPriceDataFromSQLite(SQLiteData):

    # pylint: disable=no-member

    params = (
        ("engine", None),
        ("symbol", None),
        ("name", None),
        ("fromdate", None),
        ("todate", None),
        ("compression", 1),
        ("timeframe", TimeFrame.Days),
        ("calendar", None),
        ("timestampcolumn", 0),
        ("timestampcolumntimezone", None),
        ("lazy", False),
    )

    lines = (
        "amount",
        "marketcap",
        "shares",
    )

    def __init__(self):
        assert self.p.timeframe == TimeFrame.Days
        assert self.p.compression == 1

        self.p.tablename = self.p.tablename or self.p.symbol or None
        self.p.name = self.p.name or self.p.symbol or self.p.tablename or ""

        super().__init__()

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
    def dump_from_store(
        cls,
        source_filename,
        dest_filename,
        symbols=None,
        fromdate=None,
        todate=None,
        progress_bar=True,
    ):
        loader = KrxHistoricalDailyPriceDataForBacktestLoader(source_filename)
        if symbols is None:
            symbols = loader.get_symbols()
        engine = create_engine("sqlite:///" + dest_filename)
        progress = tqdm(symbols, disable=not progress_bar)
        for symbol in progress:
            progress.set_description("Dumping Symbol [%s]" % symbol)
            data = loader.load(symbol, start_time=fromdate, end_time=todate)
            data.to_sql(symbol, engine, if_exists="replace")

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
        engine = create_engine("sqlite:///" + filename)
        inspector = inspect(engine)
        if symbols is None:
            symbols = inspector.get_table_names()
        progress = tqdm(symbols, disable=not progress_bar)
        for symbol in progress:
            progress.set_description("Adding Symbol [%s]" % symbol)
            # pylint: disable=unexpected-keyword-arg
            data = cls(
                engine=engine,
                tablename=symbol,
                fromdate=fromdate,
                todate=todate,
                symbol=symbol,
                name=symbol,
            )
            cerebro.adddata(data, name=data.p.name)
