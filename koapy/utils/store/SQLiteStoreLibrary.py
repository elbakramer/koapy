import hashlib

import pandas as pd
import pytz

from sqlalchemy import select
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.schema import MetaData, Table

from .misc.VersionedItem import VersionedItem
from .sqlalchemy.Timestamp import Timestamp


class SQLiteStoreLibrary:
    def __init__(self, store, library):
        self._store = store
        self._library = library

        self._engine = self._store._engine
        self._session = self._store._session

    def list_symbols(self, all_symbols=False, snapshot=None):
        if snapshot is not None:
            snapshot = self._library.get_snapshot(snapshot)
            symbols = snapshot.get_symbols()
        else:
            symbols = self._library.get_symbols(deleted=all_symbols)
        symbols = [symbol.name for symbol in symbols]
        return symbols

    def has_symbol(self, symbol):
        try:
            _symbol = self._library.get_symbol(symbol)
            return True
        except NoResultFound:
            return False

    def list_versions(self, symbol=None, snapshot=None, latest_only=False):
        if symbol is not None:
            symbol = self._library.get_symbol(symbol)
            versions = symbol.get_versions()
        elif snapshot is not None:
            snapshot = self._library.get_snapshot(snapshot)
            versions = snapshot.get_versions()
        elif latest_only:
            versions = self._library.get_latest_versions()
        else:
            versions = self._library.get_versions()
        versions = [
            {
                "symbol": version.symbol.name,
                "version": version.version,
                "deleted": version.deleted,
                "timestamp": version.timestamp,
                "snapshots": [snapshot.name for snapshot in version.get_snapshots()],
            }
            for version in versions
        ]
        return versions

    def _hash_data(self, data):
        return hashlib.sha256(
            pd.util.hash_pandas_object(data).values.tobytes()
        ).hexdigest()

    def write(self, symbol, data, metadata=None, prune_previous_version=True, **kwargs):
        symbol_name = symbol
        try:
            symbol = self._library.get_or_create_symbol(symbol_name)

            if data is None:
                _version = symbol.create_new_version(
                    user_metadata=metadata, deleted=metadata and metadata.get("deleted")
                )
                self._session.commit()
            else:
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

                table_name = self._hash_data(data)
                _version = symbol.create_new_version(
                    table_name=table_name,
                    user_metadata=metadata,
                    pandas_metadata=pandas_metadata,
                    deleted=metadata and metadata.get("deleted"),
                )
                self._session.commit()

                to_sql_kwargs = {
                    "index_label": index_label,
                    "dtype": dtype,
                    "if_exists": "replace",
                }
                data.to_sql(table_name, self._engine, **to_sql_kwargs)
        except:
            self._session.rollback()
            raise

        if prune_previous_version:
            self._prune_previous_versions(symbol_name, **kwargs)

        return self.read(symbol_name)

    def _get_version(self, symbol, as_of=None):
        symbol_name = symbol
        symbol = self._library.get_symbol(symbol_name)

        if as_of is None:
            version = symbol.get_latest_version()
        elif isinstance(as_of, int):
            version = symbol.get_version_by_number(as_of)
        elif isinstance(as_of, str):
            snapshot = self._library.get_snapshot(as_of)
            version = snapshot.get_version_of_symbol(symbol)
        else:
            raise ValueError("Invalid as_of argument")

        return version

    def read_as_dataframe(
        self, symbol, as_of=None, time_column=None, start_time=None, end_time=None
    ):
        symbol_name = symbol
        version = self._get_version(symbol_name, as_of)

        data = None

        if version.table_name is not None:
            read_sql_table_kwargs = {
                "index_col": version.pandas_metadata["read_sql_table"]["index_col"],
                "parse_dates": version.pandas_metadata["read_sql_table"]["parse_dates"],
            }
            data = pd.read_sql_table(
                version.table_name, self._engine, **read_sql_table_kwargs
            )
            index_names = version.pandas_metadata["read_sql_table"]["index_names"]
            index_names = tuple(index_names)
            if len(data.index.names) == 1:
                index_names = index_names[0]
            data.index.rename(index_names, inplace=True)  # pylint: disable=no-member
            column_timezones = version.pandas_metadata["read_sql_table"][
                "column_timezones"
            ]
            for column_name in version.pandas_metadata["read_sql_table"]["parse_dates"]:
                timezone = column_timezones.get(column_name, Timestamp.local_timezone)
                if isinstance(timezone, str):
                    timezone = pytz.timezone(timezone)
                data[column_name] = (
                    data[column_name]
                    .dt.tz_localize(Timestamp.utc)
                    .dt.tz_convert(timezone)
                )
                if column_name not in column_timezones:
                    data[column_name] = data[column_name].dt.tz_localize(None)

        return VersionedItem(
            self._library.name,
            symbol_name,
            version.version,
            version.timestamp,
            data,
            version.user_metadata,
        )

    def read_as_cursor(
        self, symbol, as_of=None, time_column=None, start_time=None, end_time=None
    ):
        symbol_name = symbol
        version = self._get_version(symbol_name, as_of)

        cursor = None

        if version.table_name is not None:
            records = Table(version.table_name, MetaData(), autoload_with=self._engine)
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

            statement = statement.execution_options(stream_results=True)

            cursor = self._session.execute(statement)

        return VersionedItem(
            self._library.name,
            symbol_name,
            version.version,
            version.timestamp,
            cursor,
            version.user_metadata,
        )

    def read(self, *args, **kwargs):
        return self.read_as_dataframe(*args, **kwargs)

    def _prune_previous_versions(self, symbol, keep_mins=120):
        symbol_name = symbol
        symbol = self._library.get_symbol(symbol_name)
        prunable_verions = symbol.get_prunable_versions(keep_mins)
        try:
            for version in prunable_verions:
                version.delete()
            self._session.commit()
        except:
            self._session.rollback()
            raise

    def _delete_version(self, symbol, version):
        symbol = self._library.get_symbol(symbol)
        version = symbol.get_version_by_number(version, deleted=True)
        try:
            version.delete()
            self._session.commit()
        except:
            self._session.rollback()
            raise

    def delete(self, symbol):
        symbol_name = symbol
        symbol = self._library.get_symbol(symbol_name)
        _sentinel = self.write(
            symbol_name, None, prune_previous_version=False, metadata={"deleted": True}
        )
        self._prune_previous_versions(symbol_name, 0)
        assert not self.has_symbol(symbol_name)

    def list_snapshots(self):
        snapshots = self._library.snapshots
        snapshots = [snapshot.name for snapshot in snapshots]
        return snapshots

    def snapshot(self, snapshot):
        try:
            self._library.create_snapshot(snapshot)
            self._session.commit()
        except:
            self._session.rollback()
            raise

    def delete_snapshot(self, snapshot):
        snapshot = self._library.get_snapshot(snapshot)
        try:
            snapshot.delete()
            self._session.commit()
        except:
            self._session.rollback()
            raise
