def get_last_krx_close_datetime():
    from pandas import Timestamp
    from koapy.utils.krx.calendar.XKRXExchangeCalendar import XKRXExchangeCalendar
    from tzlocal import get_localzone
    krx_calendar = XKRXExchangeCalendar.get_calendar()
    local_timezone = get_localzone()
    now = Timestamp.now(tz=krx_calendar.tz)
    last_close = krx_calendar.previous_close(now)
    last_close = last_close.astimezone(local_timezone)
    last_close = last_close.to_pydatetime()
    return last_close

def is_currently_in_session():
    from pandas import Timestamp
    from koapy.utils.krx.calendar.XKRXExchangeCalendar import XKRXExchangeCalendar
    krx_calendar = XKRXExchangeCalendar.get_calendar()
    now = Timestamp.now(tz=krx_calendar.tz)
    is_in_session = False
    today_session = now.normalize()
    if krx_calendar.is_session(today_session):
        opening, closing = krx_calendar.open_and_close_for_session(today_session)
        is_in_session = opening <= now <= closing
    return is_in_session

def get_krx_timezone():
    from trading_calendars import get_calendar
    krx_calendar = get_calendar('XKRX')
    return krx_calendar.tz
