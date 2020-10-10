import datetime

def get_last_krx_datetime():
    from trading_calendars import get_calendar
    krx_calendar = get_calendar('XKRX')
    today = datetime.datetime.now()
    last = today + 0 * krx_calendar.day
    if last == today:
        last_end = datetime.datetime.combine(last.date(), datetime.time(15, 30))
        if last > last_end:
            last = last_end
    elif last > today:
        last = today - krx_calendar.day
        last_end = datetime.datetime.combine(last.date(), datetime.time(15, 30))
        last = last_end
    return last

def get_last_krx_date():
    return get_last_krx_datetime().date()

def get_holidays():
    from koapy.utils.krx.calendar.KrxBusinessDay import KrxHolidayCalendar
    today = datetime.datetime.today()
    calendar = KrxHolidayCalendar()
    start = datetime.datetime(today.year, 1, 1)
    end = datetime.datetime(today.year, 12, 31)
    holidays = calendar.holidays(start, end, return_name=True)
    return holidays

def get_holidays_as_dict():
    holidays = get_holidays()
    response = {'block1': [{
        'calnd_dd_dy': dt.strftime('%Y-%m-%d'),
        'kr_dy_tp': dt.strftime('%a'),
        'dy_tp_cd': dt.strftime('%a'),
        'holdy_nm': name,
    } for dt, name in holidays.items() if dt.weekday() < 5]}
    return response

__all__ = [
    'get_last_krx_datetime',
    'get_last_krx_date',
    'get_holidays',
    'get_holidays_as_dict',
]
