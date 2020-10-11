from datetime import time
from pytz import timezone

from trading_calendars.trading_calendar import TradingCalendar
from trading_calendars.exchange_calendar_xkrx import precomputed_krx_holidays
from trading_calendars import calendar_utils

from koapy.utils.krx.calendar.KrxHolidayCalendar import KrxHolidayCalendar

class XKRXExchangeCalendar(TradingCalendar):
    """
    Calendar for the Korea exchange, and the primary calendar for
    the country of South Korea.
    Open Time: 9:00 AM, KST (Korean Standard Time)
    Close Time: 3:30 PM, KST (Korean Standard Time)
    NOTE: Korea observes Standard Time year-round.
    Due to the complexity around the Korean holidays, we are hardcoding
    a list of holidays covering 1986-2019, inclusive.
    Regularly-Observed Holidays:
    - Seollal (New Year's Day)
    - Independence Movement Day
    - Labor Day
    - Buddha's Birthday
    - Memorial Day
    - Provincial Election Day
    - Liberation Day
    - Chuseok (Korean Thanksgiving)
    - National Foundation Day
    - Christmas Day
    - End of Year Holiday
    NOTE: Hangeul Day became a national holiday in 2013
    - Hangeul Proclamation Day
    """

    name_ = 'XKRX'
    tz = timezone('Asia/Seoul')

    open_times = (
        (None, time(9, 1)),
    )
    close_times = (
        (None, time(15, 30)),
    )

    def __init__(self, *args, **kwargs):
        super(XKRXExchangeCalendar, self).__init__(*args, **kwargs)

    @property
    def name(self):
        return type(self).name_

    @property
    def regular_holidays(self):
        return KrxHolidayCalendar()

    @property
    def adhoc_holidays(self):
        return precomputed_krx_holidays.tolist()

    @classmethod
    def register(cls, name=None):
        if name is None:
            name = cls.name_
        instance = calendar_utils.get_calendar(name)
        if not isinstance(instance, cls):
            calendar_utils.register_calendar_type(name, cls, force=True)
            instance = calendar_utils.get_calendar(name)
        return instance

    @classmethod
    def get_calendar(cls, name=None):
        return cls.register(name)
