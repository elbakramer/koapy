import math
import pandas as pd

from backtrader.feeds import PandasDirectData
from backtrader.utils.py3 import string_types

class CybosExcelData(PandasDirectData):

    params = (
        ('tz', 'Asia/Seoul'),
        ('calendar', None),
        ('date_format', '%Y%m%d'),
        ('time_format', '%H%M%S'),
        ('reverse', True),
    )

    def read_excel(self, filename):
        data = pd.read_excel(filename)

        if self.p.reverse: # pylint: disable=no-member
            data = data.iloc[::-1]

        date_format = self.p.date_format # pylint: disable=no-member
        if date_format is None:
            date_format = '%Y%m%d'

        time_format = self.p.time_format # pylint: disable=no-member
        if time_format is None:
            time_format = '%H%M%S'

        dates = data['날짜'].astype(str)
        times = data['시간'].astype(str)

        times_maxlen = times.str.len().max()
        times_maxlen = math.ceil(times_maxlen / 2) * 2

        times = times.str.zfill(times_maxlen)
        times = times.str.ljust(len(time_format), '0')

        datetimes = dates.str.cat(times)

        datetime_format = date_format + time_format
        datetimes = pd.to_datetime(datetimes, format=datetime_format)

        tz = self._gettz()
        if tz is not None:
            datetimes = datetimes.dt.tz_localize(tz)

        data = pd.DataFrame({
            'datetime': datetimes,
            'open': data['시가'],
            'high': data['고가'],
            'low': data['저가'],
            'close': data['종가'],
            'volume': data['거래량'],
            'openinterest': 0,
        })
        data.set_index('datetime', inplace=True)

        return data

    def __init__(self, *args, **kwargs): # pylint: disable=unused-argument
        if isinstance(self.p.dataname, string_types): # pylint: disable=no-member
            self.p.dataname = self.read_excel(self.p.dataname) # pylint: disable=no-member
