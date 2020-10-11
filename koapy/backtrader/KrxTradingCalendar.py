import datetime

from pandas import Timestamp, DatetimeIndex, DataFrame

from backtrader.tradingcal import TradingCalendarBase
from backtrader.utils import tzparse
from backtrader.utils.py3 import string_types

class TradingCalendarsTradingCalendar(TradingCalendarBase):

    params = (
        ('calendar', None),
        ('cachesize', 365),
        ('tz', None),
    )

    def __init__(self): # pylint: disable=super-init-not-called
        self._calendar = self.p.calendar # pylint: disable=no-member

        if isinstance(self._calendar, string_types):
            from trading_calendars import get_calendar
            self._calendar = get_calendar(self._calendar)

        self.dcache = DatetimeIndex([0.0])
        self.idcache = DataFrame(index=DatetimeIndex([0.0]))
        self.csize = datetime.timedelta(days=self.p.cachesize) # pylint: disable=no-member

        self._tz = self.p.tz # pylint: disable=no-member

        if self._tz is None:
            self._tz = self._calendar.tz
        elif isinstance(self._tz, string_types):
            self._tz = tzparse(self._tz)

    def _nextday(self, day):
        d = day + self._calendar.day
        return d, d.isocalendar()

    def schedule(self, day, tz=None): # pylint: disable=arguments-differ
        session = Timestamp(year=day.year, month=day.month, day=day.day)
        opening, closing = self._calendar.open_and_close_for_session(session)
        if tz is None:
            tz = self._tz
        if tz is not None:
            opening = opening.astimezone(tz)
            closing = closing.astimezone(tz)
        opening = opening.to_pydatetime()
        closing = closing.to_pydatetime()
        return opening, closing

class KrxTradingCalendar(TradingCalendarsTradingCalendar):

    params = (
        ('calendar', 'XKRX'),
        ('cachesize', 365),
        ('tz', 'Asia/Seoul'),
    )
