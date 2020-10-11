import datetime

import pytz
import tzlocal

from korean_lunar_calendar import KoreanLunarCalendar

class KoreanLunarDateTime(datetime.datetime):

    kst = pytz.timezone('Asia/Seoul')
    local_timezone = tzlocal.get_localzone()

    @classmethod
    def is_naive(cls, dt):
        return dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None

    @classmethod
    def astimezone_kst(cls, dt):
        if cls.is_naive(dt):
            dt = cls.local_timezone.localize(dt)
        return dt.astimezone(cls.kst)

    def __new__(cls, *args, **kwargs): # pylint: disable=signature-differs
        is_intercalation = kwargs.pop('is_intercalation', None)
        self = super().__new__(cls, *args, **kwargs)
        self._is_intercalation = is_intercalation
        return self

    @property
    def is_intercalation(self):
        return self._is_intercalation

    def to_solar_datetime(self, is_intercalation=None, strict=False):
        dt = self.astimezone_kst(self)
        if is_intercalation is None:
            is_intercalation = self._is_intercalation
        calendar = KoreanLunarCalendar()
        valid = calendar.setLunarDate(dt.year, dt.month, dt.day, is_intercalation)
        if not valid:
            if strict:
                raise ValueError('Invalid lunar date (%s, %s, %s, %s)' % (dt.year, dt.month, dt.day, is_intercalation))
            else:
                calendar.solarYear = dt.year
                calendar.solarMonth = dt.month
                calendar.solarDay = dt.day
        dt = datetime.datetime(
            calendar.solarYear,
            calendar.solarMonth,
            calendar.solarDay,
            dt.hour,
            dt.minute,
            dt.second,
            dt.microsecond,
            tzinfo=self.kst,
        )
        return dt

    @classmethod
    def from_solar_datetime(cls, dt):
        dt = cls.astimezone_kst(dt)
        calendar = KoreanLunarCalendar()
        valid = calendar.setSolarDate(dt.year, dt.month, dt.day)
        if not valid:
            raise ValueError('Invalid solar date')
        dt = cls(
            calendar.lunarYear,
            calendar.lunarMonth,
            calendar.lunarDay,
            dt.hour,
            dt.minute,
            dt.second,
            dt.microsecond,
            tzinfo=cls.kst,
            is_intercalation=calendar.isIntercalation,
        )
        return dt

    @classmethod
    def lunar_to_solar_datetime(cls, dt, strict=False):
        dt = cls.astimezone_kst(dt)
        if not isinstance(dt, cls):
            dt = cls(
                dt.year,
                dt.month,
                dt.day,
                getattr(dt, 'hour', 0),
                getattr(dt, 'minute', 0),
                getattr(dt, 'second', 0),
                getattr(dt, 'microsecond', 0),
                tzinfo=cls.kst,
                is_intercalation=getattr(dt, 'is_intercalation', None),
            )
        solar = dt.to_solar_datetime(strict=strict)
        return solar
