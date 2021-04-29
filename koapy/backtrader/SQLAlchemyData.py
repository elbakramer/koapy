import datetime

import pandas as pd
from sqlalchemy import MetaData, Table, create_engine, select

from backtrader import date2num
from backtrader.feed import DataBase


class SQLAlchemyData(DataBase):

    # pylint: disable=no-member

    params = (
        ("url", None),
        ("engine", None),
        ("connection", None),
        ("tablename", None),
        ("timestampcolumn", 0),
        ("timestampcolumntimezone", None),
        ("timestampcolumnsort", False),
        ("lazy", True),
    )

    def __init__(self):
        super().__init__()

        assert self.p.url
        assert self.p.tablename

        self._engine = self.p.engine
        self._should_dispose = False

        self._cursor = None

        if self.p.timestampcolumntimezone is None:
            self.p.timestampcolumntimezone = datetime.datetime.now().astimezone().tzinfo

        self._started_already = False

        if not self.p.lazy:
            self.start()

    def _dispose_engine(self):
        if self._engine is not None and self._should_dispose:
            self._engine.dispose()
            self._engine = None

    def _initialize_engine(self):
        self._dispose_engine()

        self._engine = self.p.engine
        self._should_dispose = False

        if self._engine is None:
            if self.p.connection is not None:
                self._engine = create_engine(
                    self.p.url, creator=lambda: self.p.connection
                )
                self._should_dispose = False
            else:
                self._engine = create_engine(self.p.url)
                self._should_dispose = True

        assert self._engine is not None

    def _close_cursor(self):
        if self._cursor is not None:
            self._cursor.close()
            self._cursor = None

    def _initialize_cursor(self):
        self._close_cursor()

        metadata = MetaData()
        table = Table(self.p.tablename, metadata, autoload_with=self._engine)
        timestampcolumn = table.columns[
            self.p.timestampcolumn
        ]  # pylint: disable=unsubscriptable-object
        statement = select(table)

        if self.p.timestampcolumnsort:
            statement = statement.order_by(timestampcolumn)

        if self.p.fromdate is not None:
            fromdate = pd.Timestamp(self.p.fromdate, tz=self.p.timestampcolumntimezone)
            statement = statement.where(timestampcolumn >= fromdate)

        if self.p.todate is not None:
            todate = pd.Timestamp(self.p.todate, tz=self.p.timestampcolumntimezone)
            statement = statement.where(timestampcolumn <= todate)

        statement = statement.execution_options(stream_results=True)

        self._cursor = self._engine.execute(statement)

    def start(self):
        if not self._started_already:
            self._initialize_engine()
            self._initialize_cursor()
            self._started_already = True

    def stop(self):
        self._close_cursor()
        self._dispose_engine()
        self._started_already = False

    def _load(self):
        if self._cursor is None:
            return False

        try:
            date, open_, high, low, close, volume, openinterest = next(self._cursor)
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
            self.lines.openinterest[0] = openinterest

            return True
