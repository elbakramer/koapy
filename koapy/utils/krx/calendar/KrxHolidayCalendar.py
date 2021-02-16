import os
import json
import datetime
import itertools

from pandas.tseries.offsets import CustomBusinessDay
from pandas.tseries.offsets import Day

from koapy.utils.krx.calendar.AbstractHolidayCalendar import AbstractHolidayCalendar
from koapy.utils.krx.calendar.LunarHoliday import LunarHoliday, SolarHoliday as Holiday
from koapy.utils.krx.marketdata.holiday import download_entire_holidays_as_dicts

original_korean_holiday_datetimes = {}

def is_sunday(dt):
    return dt.weekday() == 6

def is_saterday_and_childrens_day(dt):
    return dt.month == 5 and dt.day == 5 and dt.weekday() == 5

def prepare_original_holidays_for_year(dt):
    if dt.year not in original_korean_holiday_datetimes:
        original_korean_holiday_datetimes[dt.year] = {}
        for rule in korean_non_alternate_regular_holiday_rules:
            date = rule.to_datetime(dt.year, apply_observance=rule.observance is not alternate_holiday)
            original_korean_holiday_datetimes[dt.year].setdefault(date, []).append(rule)
        for rule in korean_alternate_regular_holiday_rules:
            date = rule.to_datetime(dt.year, apply_observance=rule.observance is not alternate_holiday)
            original_korean_holiday_datetimes[dt.year].setdefault(date, []).append(rule)

def is_already_holiday(dt, offset=0):
    prepare_original_holidays_for_year(dt)
    return dt in original_korean_holiday_datetimes[dt.year] and len(original_korean_holiday_datetimes[dt.year][dt]) > (1 if offset == 0 else 0)

def alternate_holiday(dt):
    offset = 0
    while is_sunday(dt) or is_saterday_and_childrens_day(dt) or is_already_holiday(dt, offset):
        dt += datetime.timedelta(days=1)
        offset += 1
    return dt

# 국가법령정보센터 : 관공서의 공휴일에 관한 규정
# http://www.law.go.kr/LSW/lsSc.do?section=&menuId=1&subMenuId=15&tabMenuId=81&eventGubun=060101&query=%EA%B4%80%EA%B3%B5%EC%84%9C%EC%9D%98+%EA%B3%B5%ED%9C%B4%EC%9D%BC%EC%97%90+%EA%B4%80%ED%95%9C+%EA%B7%9C%EC%A0%95

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
HangulProclamationDay = Holiday("Hangul Proclamation Day", month=10, day=9, start_date=datetime.datetime(2013, 1, 1))
Christmas = Holiday("Christmas", month=12, day=25)
YearEndHoliday = Holiday("Year End Holiday", month=12, day=31)

korean_regular_holiday_rules = [
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
]

korean_non_alternate_regular_holiday_rules = [
    NewYearsDay,
    IndependenceMovementDay,
    BuddhasBirthday,
    LoborDay,
    MemorialDay,
    NationalLiberationDay,
    KoreanNationalFoundationDay,
    HangulProclamationDay,
    Christmas,
]

korean_alternate_regular_holiday_rules = [
    KoreanNewYearsDayBefore,
    KoreanNewYearsDay,
    KoreanNewYearsDayAfter,
    ChildrensDay,
    KoreanThanksgivingDayBefore,
    KoreanThanksgivingDay,
    KoreanThanksgivingDayAfter,
]

korean_holiday_rules = korean_regular_holiday_rules

krx_additional_holiday_rules = [
    YearEndHoliday,
]

krx_holiday_rules = [
    krx_additional_holiday_rules,
    korean_regular_holiday_rules,
]
krx_holiday_rules = itertools.chain.from_iterable(krx_holiday_rules)
krx_holiday_rules = list(krx_holiday_rules)


class KoreanHolidayCalendar(AbstractHolidayCalendar):
    """
    정규 휴일 이외에 임시공휴일과 선거일 등은 대응하지 못함
    """

    rules = korean_holiday_rules

class KrxHolidayCalendar(AbstractHolidayCalendar):
    """
    정규 휴일 이외는 각종 외부 데이터들로 최대한 대응
    """

    rules = krx_holiday_rules

class KoreanBusinessDay(CustomBusinessDay):
    """
    정규 휴일 이외에 임시공휴일과 선거일 등은 대응하지 못함
    """

    def __init__(self, *args, **kwargs):
        if 'calendar' not in kwargs:
            kwargs['calendar'] = KoreanHolidayCalendar()
        super().__init__(*args, **kwargs)

class KrxBusinessDay(CustomBusinessDay):
    """
    정규 휴일 이외는 각종 외부 데이터들로 최대한 대응
    """

    def __init__(self, *args, **kwargs):
        if 'calendar' not in kwargs:
            kwargs['calendar'] = KrxHolidayCalendar()
        super().__init__(*args, **kwargs)


file_directory = os.path.dirname(os.path.realpath(__file__))
dumpfile_directory = os.path.join(file_directory, '..', 'data')
dumpfile_name = 'holiday.json'
dumpfile_path = os.path.join(dumpfile_directory, dumpfile_name)

def dump_holidays(dump=None):
    if dump is None:
        dump = download_entire_holidays_as_dicts()
    with open(dumpfile_path, 'w', encoding='utf-8') as f:
        for d in dump:
            json.dump(d, f)
            f.write('\n')

def load_holidays():
    if os.path.exists(dumpfile_path):
        with open(dumpfile_path, encoding='utf-8') as f:
            for line in f:
                dump = json.loads(line.rstrip())
                for holiday in dump['block1']:
                    dt = datetime.datetime.strptime(holiday['calnd_dd'][:10], '%Y-%m-%d')
                    name = holiday['holdy_eng_nm'].strip() or 'Loaded %s' % dt.strftime('%Y-%m-%d')
                    new_holiday_rule = Holiday(name, year=dt.year, month=dt.month, day=dt.day)
                    krx_holiday_rules.insert(0, new_holiday_rule)

load_holidays()
