import os
import json
import datetime

from pandas.tseries.holiday import Holiday, AbstractHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay
from pandas.tseries.offsets import Day

from koapy.utils.krx.holiday.KoreanLunarCalendar import KoreanLunarCalendar
from koapy.utils.krx.holiday.LunarHoliday import LunarHoliday
from koapy.utils.krx.marketdata.holiday import download_holidays_as_dict

from koapy.utils import recursion

korean_holiday_rules = []

def is_sunday(dt):
    return dt.weekday() == 6

def is_saterday_and_childrens_day(dt):
    return dt.month == 5 and dt.day == 5 and dt.weekday() == 5

def holiday_to_datetime(rule, reference_dt=None): # pylint: disable=redefined-outer-name
    if reference_dt is None:
        reference_dt = datetime.datetime.today()
    if isinstance(rule, LunarHoliday):
        holiday_dt = KoreanLunarCalendar.lunar_to_solar_datetime(rule.year or reference_dt.year, rule.month, rule.day)
    else:
        holiday_dt = datetime.datetime(rule.year or reference_dt.year, rule.month, rule.day)
    if rule.offset:
        holiday_dt += rule.offset
    if rule.observance:
        holiday_dt = rule.observance(holiday_dt)
    return holiday_dt

def is_holiday(dt):
    for rule in korean_holiday_rules: # pylint: disable=redefined-outer-name
        holiday_dt = holiday_to_datetime(rule, dt)
        if dt == holiday_dt:
            return True
    return False

def alternate_holiday(dt):
    depth = recursion.depth()
    if depth > 2:
        return dt
    original_dt = dt
    while is_sunday(dt) or is_saterday_and_childrens_day(dt) or (dt != original_dt and is_holiday(dt)):
        dt += datetime.timedelta(1)
    return dt

NewYearsDay = Holiday("New Years Day", month=1, day=1)
KoreanNewYearsDayBefore = LunarHoliday("Korean New Years Day (-1)", month=1, day=1, offset=Day(-1), observance=alternate_holiday)
KoreanNewYearsDay = LunarHoliday("Korean New Years Day", month=1, day=1, observance=alternate_holiday)
KoreanNewYearsDayAfter = LunarHoliday("Korean New Years Day (+1)", month=1, day=1, offset=Day(1), observance=alternate_holiday)
IndependenceMovementDay = Holiday("Independence Movement Day", month=3, day=1)
BuddhasBirthday = LunarHoliday("Buddha's Birthday", month=4, day=8)
LoborDay = Holiday("Labor Day", month=5, day=1)
ChildrensDay = Holiday("Children's Day", month=5, day=5, observance=alternate_holiday)
MemorialDay = Holiday("Memorial Day", month=6, day=6)
NationalLiberationDay = Holiday("National Liberation Day", month=8, day=15)
KoreanThanksgivingDayBefore = LunarHoliday("Korean Thanksgiving Day (-1)", month=8, day=15, offset=Day(-1), observance=alternate_holiday)
KoreanThanksgivingDay = LunarHoliday("Korean Thanksgiving Day", month=8, day=15, observance=alternate_holiday)
KoreanThanksgivingDayAfter = LunarHoliday("Korean Thanksgiving Day (+1)", month=8, day=15, offset=Day(1), observance=alternate_holiday)
KoreanNationalFoundationDay = Holiday("Korean National Foundation Day", month=10, day=3)
HangulProclamationDay = Holiday("Hangul Proclamation Day", month=10, day=9)
Christmas = Holiday("Christmas", month=12, day=25)
YearEndHoliday = Holiday("Year End Holiday", month=12, day=31)

for rule in  [
    NewYearsDay,
    KoreanNewYearsDayBefore,
    KoreanNewYearsDay,
    KoreanNewYearsDayAfter,
    IndependenceMovementDay,
    BuddhasBirthday,
    LoborDay,
    ChildrensDay,
    MemorialDay,
    NationalLiberationDay,
    KoreanThanksgivingDayBefore,
    KoreanThanksgivingDay,
    KoreanThanksgivingDayAfter,
    KoreanNationalFoundationDay,
    HangulProclamationDay,
    Christmas,
]:
    korean_holiday_rules.append(rule)

file_directory = os.path.dirname(os.path.realpath(__file__))
dumpfile_directory = os.path.join(file_directory, '..', 'data')
dumpfile_name = 'holiday.json'
dumpfile_path = os.path.join(dumpfile_directory, dumpfile_name)

def dump_holidays(dump=None):
    if dump is None:
        dump = download_holidays_as_dict()
    with open(dumpfile_path, 'w', encoding='utf-8') as f:
        json.dump(dump, f)

def load_holidays():
    if os.path.exists(dumpfile_path):
        holiday_datetimes = [holiday_to_datetime(rule) for rule in korean_holiday_rules]
        yearend_datetime = holiday_to_datetime(YearEndHoliday)
        holiday_datetimes.append(yearend_datetime)
        with open(dumpfile_path, encoding='utf-8') as f:
            dump = json.load(f)
        for holiday in dump['block1']:
            dt = datetime.datetime.strptime(holiday['calnd_dd_dy'], '%Y-%m-%d')
            if dt not in holiday_datetimes:
                name = holiday['holdy_nm']
                new_holiday = Holiday(name, year=dt.year, month=dt.month, day=dt.day)
                for i, h in enumerate(holiday_datetimes):
                    if h >= dt:
                        holiday_datetimes.insert(i, dt)
                        korean_holiday_rules.insert(i, new_holiday)
                        break

load_holidays()

krx_holiday_rules = korean_holiday_rules + [YearEndHoliday]

class KoreanHolidayCalendar(AbstractHolidayCalendar):
    """
    별도 덤프파일을 사용하지 않는 경우 아래 사항들 주의필요
      - 선거일은 반영되지 않음
      - 임시공휴일은 반영되지 않음
    """

    rules = korean_holiday_rules

class KrxHolidayCalendar(KoreanHolidayCalendar):

    rules = krx_holiday_rules

class KoreanBusinessDay(CustomBusinessDay):

    def __init__(self, *args, **kwargs):
        if 'calendar' not in kwargs:
            kwargs['calendar'] = KoreanHolidayCalendar()
        super().__init__(*args, **kwargs)

class KrxBusinessDay(CustomBusinessDay):

    def __init__(self, *args, **kwargs):
        if 'calendar' not in kwargs:
            kwargs['calendar'] = KrxHolidayCalendar()
        super().__init__(*args, **kwargs)

if __name__ == '__main__':
    dump_holidays()
