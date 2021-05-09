:mod:`koapy.utils.calendar.pandas_extensions.korean_holiday`
============================================================

.. py:module:: koapy.utils.calendar.pandas_extensions.korean_holiday


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.calendar.pandas_extensions.korean_holiday.KoreanHoliday
   koapy.utils.calendar.pandas_extensions.korean_holiday.KoreanSolarHoliday
   koapy.utils.calendar.pandas_extensions.korean_holiday.KoreanLunarHoliday



Functions
~~~~~~~~~

.. autoapisummary::

   koapy.utils.calendar.pandas_extensions.korean_holiday.is_naive
   koapy.utils.calendar.pandas_extensions.korean_holiday.to_korean_datetime
   koapy.utils.calendar.pandas_extensions.korean_holiday.is_saturday
   koapy.utils.calendar.pandas_extensions.korean_holiday.is_holiday_saturday
   koapy.utils.calendar.pandas_extensions.korean_holiday.is_sunday
   koapy.utils.calendar.pandas_extensions.korean_holiday.is_already_korean_holiday
   koapy.utils.calendar.pandas_extensions.korean_holiday.alternative_holiday_func
   koapy.utils.calendar.pandas_extensions.korean_holiday.is_already_holiday_for_alternative_holiday
   koapy.utils.calendar.pandas_extensions.korean_holiday.is_already_holiday_for_childrens_day_alternative_holiday
   koapy.utils.calendar.pandas_extensions.korean_holiday.is_already_holiday
   koapy.utils.calendar.pandas_extensions.korean_holiday.alternative_holiday
   koapy.utils.calendar.pandas_extensions.korean_holiday.childrens_day_alternative_holiday
   koapy.utils.calendar.pandas_extensions.korean_holiday.next_business_day
   koapy.utils.calendar.pandas_extensions.korean_holiday.last_business_day
   koapy.utils.calendar.pandas_extensions.korean_holiday.korean_lunar_to_solar
   koapy.utils.calendar.pandas_extensions.korean_holiday.korean_lunar_to_solar_datetime
   koapy.utils.calendar.pandas_extensions.korean_holiday.korean_solar_to_lunar
   koapy.utils.calendar.pandas_extensions.korean_holiday.korean_solar_to_lunar_datetime



.. function:: is_naive(dt)


.. class:: KoreanHoliday(name, year=None, month=None, day=None, offset=None, observance=None, start_date=None, end_date=None, days_of_week=None, tz=None)


   Bases: :py:obj:`koapy.utils.calendar.pandas_extensions.holiday.Holiday`

   This extension allows to have both offset and observance while the original
   Holiday does not. The order of application is offset => observance.

   .. attribute:: _timezone
      

      

   .. attribute:: _local_timezone
      

      

   .. attribute:: _computed_holidays
      

      

   .. attribute:: _alternate_holidays_cache
      

      

   .. method:: _apply_rule(self, dates, apply_offset=True, apply_observance=True, register_holidays=True)

      Apply the given offset/observance to a DatetimeIndex of dates.

      :param dates: Dates to apply the given offset/observance rule
      :type dates: DatetimeIndex

      :returns:
      :rtype: Dates with rules applied



.. function:: to_korean_datetime(dt)


.. function:: is_saturday(dt)


.. function:: is_holiday_saturday(dt)


.. function:: is_sunday(dt)


.. function:: is_already_korean_holiday(dt)


.. function:: alternative_holiday_func(dt, is_already_holiday)


.. function:: is_already_holiday_for_alternative_holiday(dt)


.. function:: is_already_holiday_for_childrens_day_alternative_holiday(dt)


.. function:: is_already_holiday(dt)


.. function:: alternative_holiday(dt)


.. function:: childrens_day_alternative_holiday(dt)


.. function:: next_business_day(dt)


.. function:: last_business_day(dt)


.. class:: KoreanSolarHoliday(name, year=None, month=None, day=None, offset=None, observance=None, start_date=None, end_date=None, days_of_week=None, tz=None)


   Bases: :py:obj:`KoreanHoliday`

   This extension allows to have both offset and observance while the original
   Holiday does not. The order of application is offset => observance.


.. function:: korean_lunar_to_solar(year, month, day, is_intercalation=False)


.. function:: korean_lunar_to_solar_datetime(dt, is_intercalation=False)


.. function:: korean_solar_to_lunar(year, month, day)


.. function:: korean_solar_to_lunar_datetime(dt)


.. class:: KoreanLunarHoliday(name, year=None, month=None, day=None, offset=None, observance=None, start_date=None, end_date=None, days_of_week=None, tz=None)


   Bases: :py:obj:`KoreanHoliday`

   This extension allows to have both offset and observance while the original
   Holiday does not. The order of application is offset => observance.

   .. attribute:: _max_solar_end_date
      

      

   .. attribute:: _max_lunar_end_date
      

      

   .. method:: _reference_dates(self, start_date, end_date, strict=False)

      Get reference dates for the holiday.

      Return reference dates for the holiday also returning the year
      prior to the start_date and year following the end_date.  This ensures
      that any offsets to be applied will yield the holidays within
      the passed in dates.



