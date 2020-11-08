import os
import json
import hashlib
import logging
import datetime
import contextlib

import pandas as pd
import pytz

from sqlalchemy import create_engine
from sqlalchemy import select, column, text, desc
from sqlalchemy.exc import OperationalError

from koapy import KiwoomOpenApiContext
from koapy.backend.cybos.CybosPlusComObject import CybosPlusComObject

from koapy.config import config
from koapy.utils.krx.calendar import get_last_krx_close_datetime

from send2trash import send2trash

# TODO: 수정주가로 받으면서 append 하는 경우 과거 데이터에 대한 추가보정이 별도로 필요함
# TODO: InfluxDB 지원 추가 검토
# TODO: 1일봉, 15분봉 이외는 테스트 해본 적 없음

class ChartType:

    TICK = 1
    MINUTE = 2
    DAY = 3
    WEEK = 4
    MONTH = 5

    DAY_STRINGS = ['day', 'daily', 'date', 'd', 'D']
    WEEK_STRINGS = ['week', 'weekly', 'w', 'W']
    MONTH_STRINGS = ['month', 'monthly', 'mon', 'M']
    MINUTE_STRINGS = ['minute', 'min', 'm']
    TICK_STRINGS = ['tick', 't', 'T']

    FROM_STRING_DICT = {}
    TO_STRING_DICT = {}

    for enum, strings in zip(
        [DAY, WEEK, MONTH, MINUTE, TICK],
        [DAY_STRINGS, WEEK_STRINGS, MONTH_STRINGS, MINUTE_STRINGS, TICK_STRINGS]):
        TO_STRING_DICT[enum] = strings[0]
        for string in strings:
            FROM_STRING_DICT[string] = enum

    @classmethod
    def from_string(cls, value):
        if value not in cls.FROM_STRING_DICT:
            raise ValueError('unsupported chart type %s' % value)
        return cls.FROM_STRING_DICT[value]

    @classmethod
    def to_string(cls, value):
        if value not in cls.TO_STRING_DICT:
            raise ValueError('unsupported chart type %s' % value)
        return cls.TO_STRING_DICT[value]

class FileFormat:

    XLSX = 1
    SQLITE = 2

    XLSX_STRINGS = ['xlsx', 'excel']
    SQLITE_STRINGS = ['sqlite3', 'sqlite']

    FROM_STRING_DICT = {}
    TO_STRING_DICT = {}

    for enum, strings in zip(
        [XLSX, SQLITE],
        [XLSX_STRINGS, SQLITE_STRINGS]):
        TO_STRING_DICT[enum] = strings[0]
        for string in strings:
            FROM_STRING_DICT[string] = enum

    @classmethod
    def from_string(cls, value):
        if value not in cls.FROM_STRING_DICT:
            raise ValueError('unsupported file format %s' % value)
        return cls.FROM_STRING_DICT[value]

    @classmethod
    def to_string(cls, value):
        if value not in cls.TO_STRING_DICT:
            raise ValueError('unsupported file format %s' % value)
        return cls.TO_STRING_DICT[value]

class IfExists:

    """
    if_exists:
        - force  = always overwrite
        - auto   = append if exists, create if not exists, overwrite if invalid
        - append = append if exists, create if not exists, ignore if invalid
        - ignore = ignore if exists, create if not exists
    """

    AUTO = 1
    APPEND = 2
    IGNORE = 3
    FORCE = 4

    AUTO_STRINGS = ['auto']
    APPEND_STRINGS = ['append']
    IGNORE_STRINGS = ['ignore']
    FORCE_STRINGS = ['force']

    FROM_STRING_DICT = {}
    TO_STRING_DICT = {}

    for enum, strings in zip(
        [AUTO, APPEND, IGNORE, FORCE],
        [AUTO_STRINGS, APPEND_STRINGS, IGNORE_STRINGS, FORCE_STRINGS]):
        TO_STRING_DICT[enum] = strings[0]
        for string in strings:
            FROM_STRING_DICT[string] = enum

    @classmethod
    def from_string(cls, value):
        if value not in cls.FROM_STRING_DICT:
            raise ValueError('unsupported if exists %s' % value)
        return cls.FROM_STRING_DICT[value]

    @classmethod
    def to_string(cls, value):
        if value not in cls.TO_STRING_DICT:
            raise ValueError('unsupported if exists %s' % value)
        return cls.TO_STRING_DICT[value]

class HistoricalStockPriceDataUpdater:

    def __init__(self, codes, datadir, chart_type='daily', interval=1, file_format='xlsx',
            if_exists='auto', delete_remainings=True, timezone='Asia/Seoul', context=None):

        if isinstance(timezone, str):
            timezone = pytz.timezone(timezone)

        self._codes = codes
        self._datadir = datadir
        self._chart_type = ChartType.from_string(chart_type)
        self._interval = interval
        self._format = FileFormat.from_string(file_format)
        self._extension = '.' + FileFormat.to_string(self._format)
        self._if_exists = IfExists.from_string(if_exists)
        self._delete_remainings = delete_remainings
        self._timezone = timezone
        self._context = context

        self._codes_len = len(self._codes)

        failover_hash = hashlib.md5()
        failover_hash_data = (self.__class__.__name__, sorted(self._codes), self._datadir)
        failover_hash_data = json.dumps(failover_hash_data).encode()
        failover_hash.update(failover_hash_data)
        failover_hash = failover_hash.hexdigest()

        self._failover_filename = 'koapy_failover_%s.txt' % failover_hash[:6]

        self._date_column_name = '일자'
        self._date_format = '%Y%m%d'
        self._time_column_name = '시간'
        self._time_format = '%H%M'

    def get_start_date(self):
        dt = get_last_krx_close_datetime()
        if self._chart_type >= ChartType.DAY:
            dt = datetime.datetime.combine(dt.date(), datetime.time())
            dt = self._timezone.localize(dt)
        return dt

    def check_failover_code(self):
        failover_code = None
        if os.path.exists(self._failover_filename):
            logging.debug('Failover file found: %s', self._failover_filename)
            with open(self._failover_filename) as f:
                failover_code = f.read()
            if not len(failover_code) > 0:
                failover_code = None
            if failover_code:
                logging.debug('Failover code found: %s', failover_code)
        return failover_code

    def save_failover_code(self, code):
        with open(self._failover_filename, 'w') as f:
            f.write(code)

    @contextlib.contextmanager
    def get_or_create_context(self):
        with contextlib.ExitStack() as stack:
            if self._context is None:
                default_context = config.get('koapy.data.updater.default_context')
                if default_context == 'koapy.backend.cybos.CybosPlusComObject.CybosPlusComObject':
                    logging.debug('Using CybosPlus backend')
                    default_context = CybosPlusComObject()
                else:
                    if default_context != 'koapy.context.KiwoomOpenApiContext.KiwoomOpenApiContext':
                        logging.warning('Unexpected default context %s, defaults to KiwoomOpenApiContext.', default_context)
                    logging.debug('Using Kiwoom OpenAPI backend')
                    default_context = KiwoomOpenApiContext()
                self._context = stack.enter_context(default_context)
                def unset_context():
                    self._context = None
                stack.callback(unset_context)
            else:
                logging.debug('Using existing given context of type %s', type(self._context))
            if isinstance(self._context, KiwoomOpenApiContext):
                if self._chart_type == ChartType.DAY:
                    self._date_column_name = '일자'
                    self._date_format = '%Y%m%d'
                elif self._chart_type == ChartType.MINUTE:
                    self._date_column_name = '체결시간'
                    self._date_format = '%Y%m%d%H%M%S'
                else:
                    raise ValueError
            elif isinstance(self._context, CybosPlusComObject):
                if self._chart_type == ChartType.DAY:
                    self._date_column_name = '날짜'
                    self._date_format = '%Y%m%d'
                elif self._chart_type == ChartType.MINUTE:
                    self._date_column_name = '날짜'
                    self._date_format = '%Y%m%d'
                    self._time_column_name = '시간'
                    self._time_format = '%H%M'
                else:
                    raise ValueError
            else:
                raise TypeError
            self._context.EnsureConnected()
            yield self._context

    def get_filepath_for_code(self, code):
        if self._format == FileFormat.XLSX:
            filename = code + self._extension
            filepath = os.path.join(self._datadir, filename)
            return filepath
        elif self._format == FileFormat.SQLITE:
            if os.path.exists(self._datadir) and os.path.isdir(self._datadir):
                filename = code + self._extension
                filepath = os.path.join(self._datadir, filename)
                return filepath
            else:
                filepath = self._datadir
                if not filepath.endswith(self._extension):
                    filepath += self._extension
                return filepath
        else:
            raise ValueError('Unsupported file format')

    def remove_file(self, filepath):
        return send2trash(filepath)

    def _read_data_excel(self, filepath, tablename):
        return pd.read_excel(filepath, sheet_name=tablename, dtype=str)

    def _check_last_date_day_excel(self, filepath, tablename):
        last_date = None
        df = self._read_data_excel(filepath, tablename)
        if df.shape[0] > 0 and self._date_column_name in df.columns:
            last_date = df.loc[0, self._date_column_name]
            last_date = datetime.datetime.strptime(last_date, self._date_format)
            last_date = self._timezone.localize(last_date)
        return last_date

    def _check_last_date_minute_excel_kiwoom(self, filepath, tablename):
        last_date = None
        df = self._read_data_excel(filepath, tablename)
        if df.shape[0] > 0 and self._date_column_name in df.columns:
            last_date = df.loc[0, self._date_column_name]
            last_date = datetime.datetime.strptime(last_date, self._date_format)
            last_date = self._timezone.localize(last_date)
        return last_date

    def _check_last_date_minute_excel_cybos(self, filepath, tablename):
        last_date = None
        df = self._read_data_excel(filepath, tablename)
        if df.shape[0] > 0 and self._date_column_name in df.columns and self._time_column_name in df.columns:
            last_record = df.loc[0]
            last_date = last_record[self._date_column_name]
            last_time = last_record[self._time_column_name]
            last_date = datetime.datetime.strptime(last_date + last_time, self._date_format + self._time_format)
            last_date = self._timezone.localize(last_date)
        return last_date

    def _check_last_date_day_sql(self, filepath, tablename):
        engine = create_engine('sqlite:///' + filepath)
        with engine.connect() as con:
            sql = select([column(self._date_column_name)])
            sql = sql.select_from(text(tablename))
            sql = sql.order_by(desc(self._date_column_name))
            sql = sql.limit(1)
            try:
                data = pd.read_sql_query(sql, con)
            except OperationalError:
                last_date = None
            else:
                last_date = data.iloc[0, 0]
                last_date = datetime.datetime.strptime(last_date, '%Y-%m-%d')
                last_date = self._timezone.localize(last_date)
        engine.dispose()
        return last_date

    def _check_last_date_minute_sql_kiwoom(self, filepath, tablename):
        engine = create_engine('sqlite:///' + filepath)
        with engine.connect() as con:
            sql = select([column(self._date_column_name)])
            sql = sql.select_from(text(tablename))
            sql = sql.order_by(desc(self._date_column_name))
            sql = sql.limit(1)
            try:
                data = pd.read_sql_query(sql, con)
            except OperationalError:
                last_date = None
            else:
                last_date = data.iloc[0, 0]
                last_date = self._timezone.localize(last_date)
        engine.dispose()
        return last_date

    def _check_last_date_minute_sql_cybos(self, filepath, tablename):
        engine = create_engine('sqlite:///' + filepath)
        with engine.connect() as con:
            sql = select([column(self._date_column_name), column(self._time_column_name)])
            sql = sql.select_from(text(tablename))
            sql = sql.order_by(desc(self._date_column_name), desc(self._time_column_name))
            sql = sql.limit(1)
            try:
                data = pd.read_sql_query(sql, con, parse_dates=[self._date_column_name, self._time_column_name])
            except OperationalError:
                last_date = None
            else:
                data[self._date_column_name] = data[self._date_column_name].dt.date
                data[self._time_column_name] = data[self._time_column_name].dt.time
                date, time = data.iloc[0]
                last_date = datetime.datetime.combine(date, time)
                last_date = self._timezone.localize(last_date)
        engine.dispose()
        return last_date

    def check_last_date(self, filepath, tablename):
        if isinstance(self._context, KiwoomOpenApiContext):
            if self._chart_type == ChartType.DAY:
                self._date_column_name = '일자'
                self._date_format = '%Y%m%d'
                if self._format == FileFormat.XLSX:
                    return self._check_last_date_day_excel(filepath, tablename)
                elif self._format == FileFormat.SQLITE:
                    return self._check_last_date_day_sql(filepath, tablename)
                else:
                    raise ValueError
            elif self._chart_type == ChartType.MINUTE:
                self._date_column_name = '체결시간'
                self._date_format = '%Y%m%d%H%M%S'
                if self._format == FileFormat.XLSX:
                    return self._check_last_date_minute_excel_kiwoom(filepath, tablename)
                elif self._format == FileFormat.SQLITE:
                    return self._check_last_date_minute_sql_kiwoom(filepath, tablename)
                else:
                    raise ValueError
            else:
                raise ValueError
        elif isinstance(self._context, CybosPlusComObject):
            if self._chart_type == ChartType.DAY:
                self._date_column_name = '날짜'
                self._date_format = '%Y%m%d'
                if self._format == FileFormat.XLSX:
                    return self._check_last_date_day_excel(filepath, tablename)
                elif self._format == FileFormat.SQLITE:
                    return self._check_last_date_day_sql(filepath, tablename)
                else:
                    raise ValueError
            elif self._chart_type == ChartType.MINUTE:
                self._date_column_name = '날짜'
                self._date_format = '%Y%m%d'
                self._time_column_name = '시간'
                self._time_format = '%H%M'
                if self._format == FileFormat.XLSX:
                    return self._check_last_date_minute_excel_cybos(filepath, tablename)
                elif self._format == FileFormat.SQLITE:
                    return self._check_last_date_minute_sql_cybos(filepath, tablename)
                else:
                    raise ValueError
            else:
                raise ValueError
        else:
            raise TypeError

    def get_data(self, code, start_date, end_date):
        if isinstance(self._context, KiwoomOpenApiContext):
            if self._chart_type == ChartType.DAY:
                assert self._interval == 1
                return self._context.GetDailyStockDataAsDataFrame(code, start_date, end_date)
            elif self._chart_type == ChartType.MINUTE:
                return self._context.GetMinuteStockDataAsDataFrame(code, self._interval, start_date, end_date)
            else:
                raise ValueError
        elif isinstance(self._context, CybosPlusComObject):
            if self._chart_type == ChartType.DAY:
                chart_type = 'D'
            elif self._chart_type == ChartType.MINUTE:
                chart_type = 'm'
            else:
                raise ValueError
            return self._context.GetStockDataAsDataFrame(code, chart_type, self._interval, start_date, end_date)
        else:
            raise TypeError

    def _save_data_excel(self, data, filepath, tablename):
        filepathparts = os.path.splitext(filepath)
        tempfilepath = filepathparts[0] + '.tmp' + filepathparts[1]
        data.to_excel(tempfilepath, index=False, sheet_name=tablename)
        os.replace(tempfilepath, filepath)

    def _append_data_excel(self, data, filepath, tablename):
        original = self._read_data_excel(filepath, tablename)
        appended = pd.concat([data, original])
        self._save_data_excel(appended, filepath, tablename)

    def _write_data_day_sql(self, data, filepath, tablename, if_exists='replace'):
        engine = create_engine('sqlite:///' + filepath)
        with engine.connect() as con:
            dates = pd.to_datetime(data[self._date_column_name].astype(str), format=self._date_format).dt.date
            data = data.assign(**{self._date_column_name: dates})
            data = data.set_index(self._date_column_name)
            data.to_sql(tablename, con, if_exists=if_exists)
        engine.dispose()

    def _save_data_day_sql(self, data, filepath, tablename):
        return self._write_data_day_sql(data, filepath, tablename, if_exists='replace')

    def _append_data_day_sql(self, data, filepath, tablename):
        return self._write_data_day_sql(data, filepath, tablename, if_exists='append')

    def _write_data_minute_sql_kiwoom(self, data, filepath, tablename, if_exists='replace'):
        engine = create_engine('sqlite:///' + filepath)
        with engine.connect() as con:
            dates = pd.to_datetime(data[self._date_column_name].astype(str), format=self._date_format).dt.date
            data = data.assign(**{self._date_column_name: dates})
            data = data.set_index(self._date_column_name)
            data.to_sql(tablename, con, if_exists=if_exists)
        engine.dispose()

    def _write_data_minute_sql_cybos(self, data, filepath, tablename, if_exists='replace'):
        engine = create_engine('sqlite:///' + filepath)
        with engine.connect() as con:
            datetimes = data[self._date_column_name].astype(str).str.cat(data[self._time_column_name].astype(str).str.zfill(4))
            datetimes = pd.to_datetime(datetimes, format=self._date_format + self._time_format)
            data = data.assign(**{
                self._date_column_name: datetimes.dt.date,
                self._time_column_name: datetimes.dt.time,
            })
            data = data.set_index([self._date_column_name, self._time_column_name])
            data.to_sql(tablename, con, if_exists=if_exists)
        engine.dispose()

    def _write_data_minute_sql(self, data, filepath, tablename, if_exists='replace'): # pylint: disable=method-hidden
        if isinstance(self._context, KiwoomOpenApiContext):
            return self._write_data_minute_sql_kiwoom(data, filepath, tablename, if_exists)
        elif isinstance(self._context, CybosPlusComObject):
            return self._write_data_minute_sql_cybos(data, filepath, tablename, if_exists)
        else:
            raise TypeError

    def _save_data_minute_sql(self, data, filepath, tablename):
        return self._write_data_minute_sql(data, filepath, tablename, if_exists='replace')

    def _append_data_minute_sql(self, data, filepath, tablename):
        return self._write_data_minute_sql(data, filepath, tablename, if_exists='append')

    def append_data(self, data, filepath, tablename):
        if self._format == FileFormat.XLSX:
            return self._append_data_excel(data, filepath, tablename)
        elif self._format == FileFormat.SQLITE:
            if self._chart_type == ChartType.DAY:
                return self._append_data_day_sql(data, filepath, tablename)
            elif self._chart_type == ChartType.MINUTE:
                return self._append_data_minute_sql(data, filepath, tablename)
            else:
                raise ValueError
        else:
            raise ValueError

    def save_data(self, data, filepath, tablename):
        if self._format == FileFormat.XLSX:
            return self._save_data_excel(data, filepath, tablename)
        elif self._format == FileFormat.SQLITE:
            if self._chart_type == ChartType.DAY:
                return self._save_data_day_sql(data, filepath, tablename)
            elif self._chart_type == ChartType.MINUTE:
                return self._save_data_minute_sql(data, filepath, tablename)
            else:
                raise ValueError
        else:
            raise ValueError

    def update_with_progress(self):
        start_date = self.get_start_date()
        end_date = None

        failover_code = self.check_failover_code()
        failover_code_reached = False

        if failover_code is not None:
            logging.info('Failover file %s found with code %s', self._failover_filename, failover_code)

        should_try_append = self._if_exists in [IfExists.AUTO, IfExists.APPEND]
        should_overwrite_invalid = self._if_exists in [IfExists.FORCE, IfExists.AUTO]
        should_overwrite_anyway = self._if_exists in [IfExists.FORCE]

        with self.get_or_create_context():
            for i, code in enumerate(self._codes):
                yield (0, code, i, self._codes_len)
                if failover_code is not None:
                    if not failover_code_reached:
                        if code == failover_code:
                            logging.info('Found failed code %s', code)
                            failover_code_reached = True
                        else:
                            logging.info('Skipping code %s (%d/%d)', code, i+1, self._codes_len)
                            continue
                try:
                    logging.info('Starting to get stock data for code: %s (%d/%d)', code, i+1, self._codes_len)
                    filepath = self.get_filepath_for_code(code)
                    tablename = code
                    if not tablename[0].isalpha():
                        tablename = 'A' + tablename
                    should_overwrite = False
                    if os.path.exists(filepath):
                        if should_try_append:
                            last_date = self.check_last_date(filepath, tablename)
                            if last_date is not None:
                                if start_date > last_date:
                                    logging.info('Found existing file %s, prepending from %s until %s', os.path.basename(filepath), start_date, last_date)
                                    df = self.get_data(code, start_date, last_date)
                                    if df is not None and df.shape[0] > 0:
                                        self.append_data(df, filepath, tablename)
                                        logging.info('Appended stock data for code %s to %s', code, filepath)
                                    else:
                                        logging.info('Got nothing to append for code %s', code)
                                else:
                                    logging.info('Already up to date, skipping %s...', code)
                            else:
                                if should_overwrite_invalid:
                                    should_overwrite = True
                                    logging.warning('File exists but cannot find last date, overwriting...')
                                else:
                                    should_overwrite = False
                                    logging.warning('File exists but cannot find last date, ignoring...')
                        else:
                            if should_overwrite_anyway:
                                should_overwrite = True
                                logging.warning('File exists but forcing to overwrite...')
                            else:
                                should_overwrite = False
                                logging.info('File exists but just ignoring...')
                    if not os.path.exists(filepath) or should_overwrite:
                        df = self.get_data(code, start_date, end_date)
                        if df is not None and df.shape[0] > 0:
                            self.save_data(df, filepath, tablename)
                            logging.info('Saved stock data for code %s to %s', code, filepath)
                        else:
                            logging.info('Nothing to save for code %s', code)
                except:
                    self.save_failover_code(code)
                    raise
                yield (1, code, i, self._codes_len)

        # update finished successfully, delete possibly existing failover file
        if os.path.exists(self._failover_filename):
            self.remove_file(self._failover_filename)

        # delete untracked data if want to
        if os.path.isdir(self._datadir) and self._delete_remainings:
            for filename in os.listdir(self._datadir):
                basefilename, ext = os.path.splitext(filename)
                if ext == self._extension and basefilename not in self._codes:
                    logging.info('File %s is not included in target codes, deleting...', filename)
                    self.remove_file(os.path.join(self._datadir, filename))

    def update(self):
        for event in self.update_with_progress():
            pass
        return self
