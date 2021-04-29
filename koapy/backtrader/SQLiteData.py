import datetime
import sqlite3

import pandas as pd

from backtrader import date2num
from backtrader.feed import DataBase


class SQLiteData(DataBase):

    # pylint: disable=no-member

    params = (
        ("filename", None),
        ("connection", None),
        ("engine", None),
        ("tablename", None),
        ("timestampcolumn", 0),
        ("timestampcolumntimezone", None),
        ("timestampcolumnsort", False),
        ("timestampcolumnformat", None),  # '%Y-%m-%d %H:%M:%S.%f'
        ("lazy", True),
    )

    def __init__(self):
        super().__init__()

        assert self.p.tablename

        self._connection = self.p.connection
        self._should_close = False

        self._cursor = None

        if self.p.timestampcolumntimezone is None:
            self.p.timestampcolumntimezone = datetime.datetime.now().astimezone().tzinfo

        self._started_already = False

        if not self.p.lazy:
            self.start()

    def _close_connection(self):
        if self._connection is not None and self._should_close:
            self._connection.close()
            self._connection = None

    def _initialize_connection(self):
        self._close_connection()

        self._connection = self.p.connection
        self._should_close = False

        if self._connection is None:
            if self.p.engine is not None:
                self._connection = self.p.engine.raw_connection()
                self._should_close = True
            elif self.p.filename:
                self._connection = sqlite3.connect(
                    self.p.filename, check_same_thread=False
                )
                self._should_close = True

        assert self._connection is not None

    def _close_cursor(self):
        if self._cursor is not None:
            self._cursor.close()
            self._cursor = None

    def _initialize_cursor(self):
        self._close_cursor()

        self._cursor = self._connection.cursor()

        timestampcolumn = self.p.timestampcolumn

        if isinstance(timestampcolumn, int):
            self._cursor.execute("SELECT * FROM '{}' LIMIT 0".format(self.p.tablename))
            timestampcolumn = self._cursor.description[timestampcolumn][0]

        statement = "SELECT * FROM '{}'".format(self.p.tablename)

        condition_prefix = " WHERE "
        parameters = []

        if self.p.fromdate is not None:
            fromdate = pd.Timestamp(self.p.fromdate, tz=self.p.timestampcolumntimezone)
            if self.p.timestampcolumnformat:
                fromdate = fromdate.strftime(self.p.timestampcolumnformat)
            statement += condition_prefix
            statement += "'{}' >= ?".format(timestampcolumn)
            parameters.append(fromdate)
            condition_prefix = " AND "

        if self.p.todate is not None:
            todate = pd.Timestamp(self.p.todate, tz=self.p.timestampcolumntimezone)
            if self.p.timestampcolumnformat:
                todate = fromdate.strftime(self.p.timestampcolumnformat)
            statement += condition_prefix
            statement += "'{}' <= ?".format(timestampcolumn)
            parameters.append(todate)
            condition_prefix = " AND "

        if self.p.timestampcolumnsort:
            statement += " ORDER BY '{}' ASC".format(timestampcolumn)

        self._cursor.execute(statement, parameters)

    def start(self):
        if not self._started_already:
            self._initialize_connection()
            self._initialize_cursor()
            self._started_already = True

    def stop(self):
        self._close_cursor()
        self._close_connection()
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
