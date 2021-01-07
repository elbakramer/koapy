import datetime

from pandas import Timestamp
from tzlocal import get_localzone
from trading_calendars import get_calendar

def get_last_krx_close_datetime():
    krx_calendar = get_calendar('XKRX')
    local_timezone = get_localzone()
    now = Timestamp.now(tz=local_timezone)
    last_close = krx_calendar.previous_close(now)
    last_close = last_close.astimezone(local_timezone)
    last_close = last_close.to_pydatetime()
    return last_close

def is_currently_in_session():
    krx_calendar = get_calendar('XKRX')
    local_timezone = get_localzone()
    now = Timestamp.now(tz=local_timezone)
    previous_open = krx_calendar.previous_open(now)
    # https://github.com/quantopian/trading_calendars#why-are-open-times-one-minute-late
    if previous_open.minute % 5 == 1:
        previous_open -= datetime.timedelta(minutes=1)
    next_close = krx_calendar.next_close(previous_open)
    return previous_open <= now <= next_close

def get_krx_timezone():
    krx_calendar = get_calendar('XKRX')
    return krx_calendar.tz
