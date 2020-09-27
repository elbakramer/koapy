import datetime

from pandas.tseries.holiday import Holiday, AbstractHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay
from pandas.tseries.offsets import Day

from koapy.utils.krx.holiday.LunarHoliday import LunarHoliday

korean_holiday_rules = []

def alternate_holiday(dt):
    is_sunday = lambda dt: dt.weekday() == 6
    is_saterday_and_childrens_day = lambda dt: dt.month == 5 and dt.day == 5 and dt.weekday() == 5
    is_holiday = lambda dt: any(len(rule.dates(dt, dt)) > 0 for rule in korean_holiday_rules)
    while is_sunday(dt) or is_saterday_and_childrens_day(dt) or is_holiday(dt):
        dt += datetime.datetime.timedelta(1)
    return dt

NewYearsDay = Holiday("New Years Day", month=1, day=1)

KoreanNewYearsDayBefore = LunarHoliday("Korean New Years Day", month=1, day=1, offset=Day(-1), observance=alternate_holiday)
KoreanNewYearsDay = LunarHoliday("Korean New Years Day", month=1, day=1, observance=alternate_holiday)
KoreanNewYearsDayAfter = LunarHoliday("Korean New Years Day", month=1, day=1, offset=Day(1), observance=alternate_holiday)

IndependenceMovementDay = Holiday("Independence Movement Day", month=3, day=1)

BuddhasBirthday = LunarHoliday("Buddha's Birthday", month=4, day=8)

ChildrensDay = Holiday("Children's Day", month=5, day=5, observance=alternate_holiday)

MemorialDay = Holiday("Memorial Day", month=6, day=6)
NationalLiberationDay = Holiday("National Liberation Day", month=8, day=15)

KoreanThanksgivingDayBefore = LunarHoliday("Korean Thanksgiving Day", month=8, day=15, offset=Day(-1), observance=alternate_holiday)
KoreanThanksgivingDay = LunarHoliday("Korean Thanksgiving Day", month=8, day=15, observance=alternate_holiday)
KoreanThanksgivingDayAfter = LunarHoliday("Korean Thanksgiving Day", month=8, day=15, offset=Day(1), observance=alternate_holiday)

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

krx_holiday_rules = korean_holiday_rules + [YearEndHoliday]

class KoreanHolidayCalendar(AbstractHolidayCalendar):
    """
    주의: 선거일이 빠져있습니다.
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
