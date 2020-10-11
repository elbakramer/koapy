def get_last_krx_close_datetime():
    from pandas import Timestamp
    from koapy.utils.krx.calendar.XKRXExchangeCalendar import XKRXExchangeCalendar
    from tzlocal import get_localzone
    local_timezone = get_localzone()
    krx_calendar = XKRXExchangeCalendar.register()
    now = Timestamp.now(tz=local_timezone)
    last_close = krx_calendar.previous_close(now)
    last_close = last_close.astimezone(local_timezone)
    last_close = last_close.to_pydatetime()
    return last_close
