import pandas as pd
import pytz
from sqlalchemy import create_engine, inspect, select
from sqlalchemy.schema import DropTable, MetaData, Table

from .sqlalchemy.Timestamp import Timestamp


class SQLiteFileLibrary:
    def __init__(self, filename):
        self._engine = create_engine("sqlite:///" + filename)
        self._inspector = inspect(self._engine)

    def list_symbols(self):
        return self._inspector.get_table_names()

    def has_symbol(self, symbol):
        return self._inspector.has_table(symbol)

    def write(self, symbol, data):
        index_original_names = [name for name in data.index.names]
        index_table_names = [
            name if name is not None else "index_%d" % i
            for i, name in enumerate(data.index.names)
        ]

        datetime_columns = [
            (name, dtype)
            for name, dtype in data.dtypes.items()
            if pd.api.types.is_datetime64_any_dtype(dtype)
        ]
        column_timezones = {
            name: str(dtype.tz)
            for name, dtype in datetime_columns
            if hasattr(dtype, "tz")
        }

        index_label = index_table_names
        dtype = {
            name: Timestamp(getattr(dtype, "tz", False))
            for name, dtype in datetime_columns
        }

        index_col = index_table_names
        parse_dates = [name for name, dtype in datetime_columns]

        pandas_metadata = {
            "read_sql_table": {
                "index_col": index_col,
                "parse_dates": parse_dates,
                "index_names": index_original_names,
                "column_timezones": column_timezones,
            },
        }

        to_sql_kwargs = {
            "index_label": index_label,
            "dtype": dtype,
            "if_exists": "replace",
        }
        data.to_sql(symbol, self._engine, **to_sql_kwargs)

        return data

    def read_as_dataframe(
        self, symbol, time_column=None, start_time=None, end_time=None
    ):
        index_col = ["Date"]
        parse_dates = ["Date"]
        read_sql_table_kwargs = {
            "index_col": index_col,
            "parse_dates": parse_dates,
        }
        data = pd.read_sql_table(symbol, self._engine, **read_sql_table_kwargs)
        index_names = index_col
        index_names = tuple(index_names)
        if len(data.index.names) == 1:
            index_names = index_names[0]
        data.index.rename(index_names, inplace=True)
        column_timezones = {}
        for column_name in parse_dates:
            timezone = column_timezones.get(column_name, Timestamp.local_timezone)
            if isinstance(timezone, str):
                timezone = pytz.timezone(timezone)
            data[column_name] = (
                data[column_name].dt.tz_localize(Timestamp.utc).dt.tz_convert(timezone)
            )
            if column_name not in column_timezones:
                data[column_name] = data[column_name].dt.tz_localize(None)
        return data

    def read_as_cursor(self, symbol, time_column=None, start_time=None, end_time=None):
        records = Table(symbol, MetaData(), autoload_with=self._engine)
        statement = select(records)

        if time_column is not None:
            time_column = records.columns[
                time_column
            ]  # pylint: disable=unsubscriptable-object
            statement = statement.order_by(time_column)

        if start_time is not None:
            start_time = pd.Timestamp(start_time)
            if time_column is None:
                time_column = 0
                time_column = records.columns[
                    time_column
                ]  # pylint: disable=unsubscriptable-object
                statement = statement.order_by(time_column)
            if Timestamp.is_naive(start_time):
                start_time = start_time.tz_localize(Timestamp.local_timezone)
            start_time = start_time.astimezone(Timestamp.utc)
            statement = statement.where(
                time_column >= start_time
            )  # pylint: disable=unsubscriptable-object

        if end_time is not None:
            end_time = pd.Timestamp(end_time)
            if time_column is None:
                time_column = 0
                time_column = records.columns[
                    time_column
                ]  # pylint: disable=unsubscriptable-object
                statement = statement.order_by(time_column)
            if Timestamp.is_naive(end_time):
                end_time = end_time.tz_localize(Timestamp.local_timezone)
            end_time = end_time.astimezone(Timestamp.utc)
            statement = statement.where(
                time_column <= end_time
            )  # pylint: disable=unsubscriptable-object

        data = self._engine.execute(statement)
        return data

    def read(self, *args, **kwargs):
        return self.read_as_dataframe(*args, **kwargs)

    def delete(self, symbol):
        table = Table(symbol, MetaData(), autoload_with=self._engine)
        self._engine.execute(DropTable(table), if_exists=True)
