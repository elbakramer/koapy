import datetime

from koapy.utils.krx.holiday.KoreanLunarCalendar import KoreanLunarCalendar
from koapy.utils.krx.holiday.LunarHoliday import LunarHoliday
from koapy.utils.krx.holiday.KrxBusinessDay import KrxBusinessDay, KrxHolidayCalendar

from koapy.utils.krx.marketdata.holiday import *

def get_last_krx_datetime():
    """
    별도 덤프파일을 사용하지 않는 경우 아래 사항들 주의필요
      - 선거일은 반영되지 않음
      - 임시공휴일은 반영되지 않음
      - 대학수학능력 시험일에 한시간씩 늦춰지는건 고려하지 않음
    """
    today = datetime.datetime.now()
    last = today + KrxBusinessDay(0)
    if last == today:
        last_end = datetime.datetime.combine(last.date(), datetime.time(15, 30))
        if last > last_end:
            last = last_end
    elif last > today:
        last = today - KrxBusinessDay(1)
        last_end = datetime.datetime.combine(last.date(), datetime.time(15, 30))
        last = last_end
    return last

def get_last_krx_date():
    return get_last_krx_datetime().date()

def get_holidays():
    today = datetime.datetime.today()
    calendar = KrxHolidayCalendar()
    start = datetime.datetime(today.year, 1, 1)
    end = datetime.datetime(today.year, 12, 31)
    return calendar.holidays(start, end, return_name=True)

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
