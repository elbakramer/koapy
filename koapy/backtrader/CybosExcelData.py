import pandas as pd

from backtrader.feeds import PandasDirectData

from koapy.backtrader.KrxTradingCalendar import KrxTradingCalendar

class CybosExcelData(PandasDirectData):

    params = (
        ('tz', 'Asia/Seoul'),
        ('calendar', KrxTradingCalendar()),
    )

    @classmethod
    def read_excel(cls, filename, tz=None):
        data = pd.read_excel(filename)
        dates = data['날짜'].astype(str)
        times = data['시간'].astype(str).str.zfill(4)
        datetimes = dates.str.cat(times)
        datetimes = pd.to_datetime(datetimes, format='%Y%m%d%H%M')
        if tz is not None:
            datetimes = datetimes.dt.tz_localize(tz)
        data = pd.DataFrame({
            'open': data['시가'],
            'high': data['고가'],
            'low': data['저가'],
            'close': data['종가'],
            'volume': data['거래량'],
            'openinterest': 0,
        }, index=datetimes)
        return data

    def __init__(self):
        self.p.dataname = self.read_excel(self.p.dataname, self._gettz()) # pylint: disable=no-member
