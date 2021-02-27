import datetime
import pytz

from pandas import Timestamp, DatetimeIndex, DataFrame

from backtrader.tradingcal import TradingCalendarBase
from backtrader.utils.py3 import string_types

class ExchangeCalendarsTradingCalendar(TradingCalendarBase):

    params = (
        ('calendar', None),
        ('cachesize', 365),
    )

    def __init__(self): # pylint: disable=super-init-not-called
        self._calendar = self.p.calendar # pylint: disable=no-member

        if isinstance(self._calendar, string_types):
            from exchange_calendars import get_calendar
            self._calendar = get_calendar(self._calendar)

        self.dcache = DatetimeIndex([0.0])
        self.idcache = DataFrame(index=DatetimeIndex([0.0]))
        self.csize = datetime.timedelta(days=self.p.cachesize) # pylint: disable=no-member

    def _nextday(self, day):
        d = day + self._calendar.day
        return d, d.isocalendar()

    def schedule(self, day, tz=None): # pylint: disable=arguments-differ,unused-argument
        """
        day: expecting naive datetime.datetime day in utc timezone
        tz: treat/localize internal naive datetimes to this timezone
        returns: (opening, closing) naive datetime.datetime pair in utc timezone
        """
        session = Timestamp(day, tz=pytz.UTC).normalize()
        opening, closing = self._calendar.open_and_close_for_session(session)
        opening = opening.tz.localize(None).to_pydatetime()
        closing = closing.tz.localize(None).to_pydatetime()
        return opening, closing

class KrxTradingCalendar(ExchangeCalendarsTradingCalendar):

    params = (
        ('calendar', 'XKRX'),
        ('cachesize', 365),
    )
