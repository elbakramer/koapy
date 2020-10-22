import pandas as pd

from backtrader.feeds import PandasDirectData

class KiwoomExcelData(PandasDirectData):

    params = (
        ('tz', 'Asia/Seoul'),
        ('calendar', None),
        ('date_format', '%Y%m%d'),
        ('datetime_format', '%Y%m%d%H%M%S'),
        ('reverse', True),
    )

    def read_excel(self, filename):
        data = pd.read_excel(filename)

        if self.p.reverse: # pylint: disable=no-member
            data = data.iloc[::-1]

        if '일자' in data.columns:
            datetimes = data['일자'].astype(str)
            date_format = self.p.date_format # pylint: disable=no-member
            if date_format is None:
                date_format = '%Y%m%d'
            datetimes = pd.to_datetime(datetimes, format=date_format)
        elif '체결시간' in data.columns:
            datetimes = data['체결시간'].astype(str)
            datetime_format = self.p.datetime_format # pylint: disable=no-member
            if datetime_format is None:
                datetime_format = '%Y%m%d%H%M%S'
            datetimes = pd.to_datetime(datetimes, format=datetime_format)
        else:
            raise ValueError('Cannot find datetime column in file %s' % filename)

        tz = self._gettz()

        if tz is not None:
            datetimes = datetimes.dt.tz_localize(tz)

        data = pd.DataFrame({
            'datetime': datetimes,
            'open': data['시가'].abs(),
            'high': data['고가'].abs(),
            'low': data['저가'].abs(),
            'close': data['현재가'].abs(),
            'volume': data['거래량'].abs(),
            'openinterest': 0,
        })
        data.set_index('datetime', inplace=True)

        return data

    def __init__(self, *args, **kwargs):
        self.p.dataname = self.read_excel(self.p.dataname) # pylint: disable=no-member
        super().__init__(*args, **kwargs)
