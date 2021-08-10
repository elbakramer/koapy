from exchange_calendars import get_calendar
from pandas import Timestamp

name = "XKRX"
calendar = get_calendar(name)
day = calendar.day


def is_currently_in_session():
    now = Timestamp.now(calendar.tz)
    previous_open = calendar.previous_open(now).astimezone(calendar.tz)
    next_close = calendar.next_close(previous_open).astimezone(calendar.tz)
    return previous_open <= now <= next_close


def last_session_date():
    now = Timestamp.now(calendar.tz)
    previous_close = calendar.previous_close(now).astimezone(calendar.tz)
    previous_open = calendar.previous_open(previous_close).astimezone(calendar.tz)
    return previous_open.normalize()
