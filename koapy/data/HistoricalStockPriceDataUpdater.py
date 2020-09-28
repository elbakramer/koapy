import os
import json
import hashlib
import logging
import datetime
import contextlib

from abc import ABC
from abc import abstractmethod

import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy import select, column, text, desc
from sqlalchemy.exc import OperationalError

from koapy import KiwoomOpenApiContext
from koapy.backend.cybos.CybosPlusComObject import CybosPlusComObject

from koapy.config import config
from koapy.utils.krx.holiday import get_last_krx_datetime

class BaseHistoricalStockPriceDataUpdater(ABC):
    """
    """

    def __init__(self, codes, datadir, context=None, if_exists='auto', delete_remainings=True):
        self._codes = codes
        self._datadir = datadir
        self._context = context

        """
        if_exists:
          - force  = always overwrite
          - auto   = append if exists, create if not exists, overwrite if invalid
          - append = append if exists, create if not exists, ignore if invalid
          - ignore = ignore if exists, create if not exists
        """

        self._if_exists = if_exists
        self._delete_remainings = delete_remainings

        self.context = context

        self._codes_len = len(self._codes)

        failover_hash = hashlib.md5()
        failover_hash_data = (self.__class__.__name__, sorted(self._codes), self._datadir)
        failover_hash_data = json.dumps(failover_hash_data).encode()
        failover_hash.update(failover_hash_data)
        failover_hash = failover_hash.hexdigest()

        self._failover_filename = 'koapy_failover_%s.txt' % failover_hash[:6]

    @abstractmethod
    def get_data(self, code, start_date, end_date):
        raise NotImplementedError

    @abstractmethod
    def read_data(self, filepath):
        raise NotImplementedError

    @abstractmethod
    def save_data(self, data, filepath):
        raise NotImplementedError

    @abstractmethod
    def check_last_date(self, filepath):
        raise NotImplementedError

    @abstractmethod
    def append_data(self, data, filepath):
        raise NotImplementedError

    @property
    @abstractmethod
    def extension(self):
        raise NotImplementedError

    @property
    def context(self):
        return self._context

    def set_context(self, context):
        self._context = context

    @context.setter
    def context(self, context):
        self.set_context(context)

    def check_failover_code(self):
        failover_code = None
        if os.path.exists(self._failover_filename):
            with open(self._failover_filename) as f:
                failover_code = f.read()
            if not len(failover_code) > 0:
                failover_code = None
        return failover_code

    def save_failover_code(self, code):
        with open(self._failover_filename, 'w') as f:
            f.write(code)

    def get_start_date(self):
        return get_last_krx_datetime()

    def update_only(self):
        start_date = self.get_start_date()
        end_date = None

        failover_code = self.check_failover_code()
        failover_code_found = False

        if failover_code is not None:
            logging.info('Failover file %s found with code %s', self._failover_filename, failover_code)

        with contextlib.ExitStack() as stack:
            if self.context is None:
                default_context = config.get('koapy.data.updater.default_context')
                if default_context == 'koapy.backend.cybos.CybosPlusComObject.CybosPlusComObject':
                    default_context = CybosPlusComObject()
                else:
                    if default_context != 'koapy.context.KiwoomOpenApiContext.KiwoomOpenApiContext':
                        logging.warning('Unexpected default context %s, defaults to KiwoomOpenApiContext.', default_context)
                    default_context = KiwoomOpenApiContext()
                self.context = stack.enter_context(default_context)
            self.context.EnsureConnected()

            should_try_append = self._if_exists in ['auto', 'append']

            for i, code in enumerate(self._codes):
                if failover_code is not None:
                    if not failover_code_found:
                        if code == failover_code:
                            logging.info('Found failed code %s', code)
                            failover_code_found = True
                        else:
                            logging.info('Skipping code %s (%d/%d)', code, i+1, self._codes_len)
                            continue
                try:
                    logging.info('Starting to get stock data for code: %s (%d/%d)', code, i+1, self._codes_len)
                    filename = code + self.extension
                    filepath = os.path.join(self._datadir, filename)
                    should_overwrite = True
                    if os.path.exists(filepath):
                        should_overwrite = self._if_exists in ['force', 'auto']
                        if should_try_append:
                            last_date = self.check_last_date(filepath)
                            if last_date is not None:
                                should_overwrite = False
                                if start_date > last_date:
                                    logging.info('Found existing file %s, prepending from %s until %s', os.path.basename(filepath), start_date, last_date)
                                    df = self.get_data(code, start_date, last_date)
                                    if df.shape[0] > 0:
                                        self.append_data(df, filepath)
                                        logging.info('Appended stock data for code %s to %s', code, filepath)
                                    else:
                                        logging.info('Got nothing to append for code %s', code)
                                else:
                                    logging.info('Already up to date, skipping %s...', code)
                            else:
                                if should_overwrite:
                                    logging.warning('File exists but cannot find last date, overwriting...')
                                else:
                                    logging.warning('File exists but cannot find last date, ignoring...')
                        else:
                            if should_overwrite:
                                logging.warning('File exists but forcing to overwrite...')
                            else:
                                logging.info('File exists but just ignoring...')
                    if should_overwrite:
                        df = self.get_data(code, start_date, end_date)
                        if df.shape[0] > 0:
                            self.save_data(df, filepath)
                            logging.info('Saved stock data for code %s to %s', code, filepath)
                        else:
                            logging.info('Nothing to save for code %s', code)
                except:
                    self.save_failover_code(code)
                    raise

        if os.path.exists(self._failover_filename):
            os.remove(self._failover_filename)

    def delete_remainings(self):
        for filename in os.listdir(self._datadir):
            if os.path.splitext(filename)[0] not in self._codes:
                logging.info('File %s is not included in target codes, deleting...', filename)
                os.remove(os.path.join(self._datadir, filename))

    def update(self):
        self.update_only()
        if self._delete_remainings:
            self.delete_remainings()

class BaseHistoricalStockPriceDataToSqliteUpdater(BaseHistoricalStockPriceDataUpdater):

    @property
    def extension(self):
        return '.sqlite3'

    @property
    def tablename(self):
        return 'history'

    def read_data(self, filepath):
        engine = create_engine('sqlite:///' + filepath)
        with engine.connect() as con:
            data = pd.read_sql_table(self.tablename, con)
        engine.dispose()
        return data

class HistoricalDailyStockPriceDataToSqliteUpdater(BaseHistoricalStockPriceDataToSqliteUpdater):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._date_column_name = '일자'
        self._date_format = '%Y%m%d'

    def get_start_date(self):
        return datetime.datetime.combine(get_last_krx_datetime().date(), datetime.time())

    def get_data(self, code, start_date, end_date):
        return self.context.GetDailyStockDataAsDataFrame(code, start_date, end_date)

    def set_context(self, context):
        super().set_context(context)
        if isinstance(self.context, CybosPlusComObject):
            self._date_column_name = '날짜'
        else:
            self._date_column_name = '일자'

    def write_data(self, data, filepath, if_exists='replace'):
        engine = create_engine('sqlite:///' + filepath)
        with engine.connect() as con:
            dates = pd.to_datetime(data[self._date_column_name].astype(str), format=self._date_format).dt.date
            data = data.assign(**{self._date_column_name: dates})
            data = data.set_index(self._date_column_name)
            data.to_sql(self.tablename, con, if_exists=if_exists)
        engine.dispose()

    def save_data(self, data, filepath):
        return self.write_data(data, filepath, if_exists='replace')

    def append_data(self, data, filepath):
        return self.write_data(data, filepath, if_exists='append')

    def check_last_date_kiwoom(self, filepath):
        engine = create_engine('sqlite:///' + filepath)
        with engine.connect() as con:
            sql = select([column(self._date_column_name)])
            sql = sql.select_from(text(self.tablename))
            sql = sql.order_by(desc(self._date_column_name))
            sql = sql.limit(1)
            data = pd.read_sql_query(sql, con)
            result = data.iloc[0, 0]
        engine.dispose()
        return result

class HistoricalMinuteStockPriceDataToSqliteUpdater(BaseHistoricalStockPriceDataToSqliteUpdater):

    def __init__(self, codes, datadir, interval, context=None, if_exists='auto', delete_remainings=True):
        super().__init__(codes, datadir, context, if_exists, delete_remainings)
        self._interval = interval
        self._date_column_name = '체결시간'
        self._date_format = '%Y%m%d%H%M%S'
        self._time_column_name = '시간'
        self._time_format = '%H%M'

    def get_data(self, code, start_date, end_date):
        return self.context.GetMinuteStockDataAsDataFrame(code, self._interval, start_date, end_date)

    def set_context(self, context):
        super().set_context(context)
        if isinstance(self.context, CybosPlusComObject):
            self._date_column_name = '날짜'
            self._date_format = '%Y%m%d'
            self._time_column_name = '시간'
            self._time_format = '%H%M'
            self.write_data = self.write_data_cybos
            self.check_last_date = self.check_last_date_cybos
        else:
            self._date_column_name = '체결시간'
            self._date_format = '%Y%m%d%H%M%S'
            self.write_data = self.write_data_kiwoom
            self.check_last_date = self.check_last_date_kiwoom

    def write_data_kiwoom(self, data, filepath, if_exists='replace'):
        engine = create_engine('sqlite:///' + filepath)
        with engine.connect() as con:
            dates = pd.to_datetime(data[self._date_column_name].astype(str), format=self._date_format).dt.date
            data = data.assign(**{self._date_column_name: dates})
            data = data.set_index(self._date_column_name)
            data.to_sql(self.tablename, con, if_exists=if_exists)
        engine.dispose()

    def write_data_cybos(self, data, filepath, if_exists='replace'):
        engine = create_engine('sqlite:///' + filepath)
        with engine.connect() as con:
            datetimes = data[self._date_column_name].astype(str).str.cat(data[self._time_column_name].astype(str).str.zfill(4))
            datetimes = pd.to_datetime(datetimes, format=self._date_format + self._time_format)
            data = data.assign(**{
                self._date_column_name: datetimes.dt.date,
                self._time_column_name: datetimes.dt.time,
            })
            data = data.set_index([self._date_column_name, self._time_column_name])
            data.to_sql(self.tablename, con, if_exists=if_exists)
        engine.dispose()

    def write_data(self, data, filepath, if_exists='replace'): # pylint: disable=method-hidden
        self.write_data_kiwoom(data, filepath, if_exists=if_exists)

    def save_data(self, data, filepath):
        return self.write_data(data, filepath, if_exists='replace')

    def append_data(self, data, filepath):
        return self.write_data(data, filepath, if_exists='append')

    def check_last_date_kiwoom(self, filepath):
        engine = create_engine('sqlite:///' + filepath)
        with engine.connect() as con:
            sql = select([column(self._date_column_name)])
            sql = sql.select_from(text(self.tablename))
            sql = sql.order_by(desc(self._date_column_name))
            sql = sql.limit(1)
            data = pd.read_sql_query(sql, con)
            result = data.iloc[0, 0]
        engine.dispose()
        return result

    def check_last_date_cybos(self, filepath):
        engine = create_engine('sqlite:///' + filepath)
        with engine.connect() as con:
            sql = select([column(self._date_column_name), column(self._time_column_name)])
            sql = sql.select_from(text(self.tablename))
            sql = sql.order_by(desc(self._date_column_name), desc(self._time_column_name))
            sql = sql.limit(1)
            try:
                data = pd.read_sql_query(sql, con, parse_dates=[self._date_column_name, self._time_column_name])
                data[self._date_column_name] = data[self._date_column_name].dt.date
                data[self._time_column_name] = data[self._time_column_name].dt.time
            except OperationalError:
                result = None
            else:
                date, time = data.iloc[0]
                result = datetime.datetime.combine(date, time)
        engine.dispose()
        return result

    def check_last_date(self, filepath):
        return self.check_last_date_kiwoom(filepath)

class Historical15MinuteStockPriceDataToSqliteUpdater(HistoricalMinuteStockPriceDataToSqliteUpdater):

    def __init__(self, codes, datadir, context=None, if_exists='auto', delete_remainings=True):
        super().__init__(codes, datadir, 15, context, if_exists, delete_remainings)

class BaseHistoricalStockPriceDataToExcelUpdater(BaseHistoricalStockPriceDataUpdater):

    @property
    def extension(self):
        return '.xlsx'

    def read_data(self, filepath):
        return pd.read_excel(filepath, dtype=str)

    def save_data(self, data, filepath):
        filepathparts = os.path.splitext(filepath)
        tempfilepath = filepathparts[0] + '.tmp' + filepathparts[1]
        data.to_excel(tempfilepath, index=False)
        os.replace(tempfilepath, filepath)

    def append_data(self, data, filepath):
        original = self.read_data(filepath)
        appended = pd.concat([data, original])
        self.save_data(appended, filepath)

class HistoricalDailyStockPriceDataToExcelUpdater(BaseHistoricalStockPriceDataToExcelUpdater):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._date_column_name = '일자'
        self._date_format = '%Y%m%d'

    def get_start_date(self):
        return datetime.datetime.combine(get_last_krx_datetime().date(), datetime.time())

    def get_data(self, code, start_date, end_date):
        return self.context.GetDailyStockDataAsDataFrame(code, start_date, end_date)

    def set_context(self, context):
        super().set_context(context)
        if isinstance(self.context, CybosPlusComObject):
            self._date_column_name = '날짜'
        else:
            self._date_column_name = '일자'

    def check_last_date(self, filepath):
        last_date = None
        df = self.read_data(filepath)
        if df.shape[0] > 0 and self._date_column_name in df.columns:
            last_date = df.loc[0, self._date_column_name]
            last_date = datetime.datetime.strptime(last_date, self._date_format)
        return last_date

class HistoricalMinuteStockPriceDataToExcelUpdater(BaseHistoricalStockPriceDataToExcelUpdater):

    def __init__(self, codes, datadir, interval, context=None, if_exists='auto', delete_remainings=True):
        super().__init__(codes, datadir, context, if_exists, delete_remainings)
        self._interval = interval
        self._date_column_name = '체결시간'
        self._date_format = '%Y%m%d%H%M%S'
        self._time_column_name = '시간'
        self._time_format = '%H%M'

    def get_data(self, code, start_date, end_date):
        return self.context.GetMinuteStockDataAsDataFrame(code, self._interval, start_date, end_date)

    def set_context(self, context):
        super().set_context(context)
        if isinstance(self.context, CybosPlusComObject):
            self._date_column_name = '날짜'
            self._date_format = '%Y%m%d'
            self._time_column_name = '시간'
            self._time_format = '%H%M'
            self.check_last_date = self.check_last_date_cybos
        else:
            self._date_column_name = '체결시간'
            self._date_format = '%Y%m%d%H%M%S'
            self.check_last_date = self.check_last_date_kiwoom

    def check_last_date_kiwoom(self, filepath):
        last_date = None
        df = self.read_data(filepath)
        if df.shape[0] > 0 and self._date_column_name in df.columns:
            last_date = df.loc[0, self._date_column_name]
            last_date = datetime.datetime.strptime(last_date, self._date_format)
        return last_date

    def check_last_date_cybos(self, filepath):
        last_date = None
        df = self.read_data(filepath)
        if df.shape[0] > 0 and self._date_column_name in df.columns and self._time_column_name in df.columns:
            last_record = df.loc[0]
            last_date = last_record[self._date_column_name]
            last_time = last_record[self._time_column_name]
            last_date = datetime.datetime.strptime(last_date + last_time, self._date_format + self._time_format)
        return last_date

    def check_last_date(self, filepath):
        return self.check_last_date_kiwoom(filepath)

class Historical15MinuteStockPriceDataToExcelUpdater(HistoricalMinuteStockPriceDataToExcelUpdater):

    def __init__(self, codes, datadir, context=None, if_exists='auto', delete_remainings=True):
        super().__init__(codes, datadir, 15, context, if_exists, delete_remainings)
