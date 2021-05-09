:mod:`koapy.utils.calendar.pandas_extensions.holiday`
=====================================================

.. py:module:: koapy.utils.calendar.pandas_extensions.holiday


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.calendar.pandas_extensions.holiday.Holiday
   koapy.utils.calendar.pandas_extensions.holiday.AbstractHolidayCalendar



Functions
~~~~~~~~~

.. autoapisummary::

   koapy.utils.calendar.pandas_extensions.holiday.combine



.. class:: Holiday(name, year=None, month=None, day=None, offset=None, observance=None, start_date=None, end_date=None, days_of_week=None, tz=None)


   Bases: :py:obj:`pandas.tseries.holiday.Holiday`

   This extension allows to have both offset and observance while the original
   Holiday does not. The order of application is offset => observance.

   .. method:: __repr__(self) -> str

      Return repr(self).


   .. method:: dates(self, start_date, end_date, return_name=False)

      Calculate holidays observed between start date and end date

      :param start_date:
      :type start_date: starting date, datetime-like, optional
      :param end_date:
      :type end_date: ending date, datetime-like, optional
      :param return_name: If True, return a series that has dates and holiday names.
                          False will only return dates.
      :type return_name: bool, optional, default=False


   .. method:: _apply_offset(self, dates)


   .. method:: _apply_observance(self, dates)


   .. method:: _apply_rule(self, dates, apply_offset=True, apply_observance=True)

      Apply the given offset/observance to a DatetimeIndex of dates.

      :param dates: Dates to apply the given offset/observance rule
      :type dates: DatetimeIndex

      :returns:
      :rtype: Dates with rules applied



.. function:: combine(pre_holidays)


.. class:: AbstractHolidayCalendar(name=None, rules=None)


   Bases: :py:obj:`pandas.tseries.holiday.AbstractHolidayCalendar`

   This extension allows to have overlaps between calculated holidays while
   the original AbstractHolidayCalendar does not.

   .. method:: holidays(self, start=None, end=None, return_name=False)

      Returns a curve with holidays between start_date and end_date
      :param start:
      :type start: starting date, datetime-like, optional
      :param end:
      :type end: ending date, datetime-like, optional
      :param return_name: If True, return a series that has dates and holiday names.
                          False will only return a DatetimeIndex of dates.
      :type return_name: bool, optional

      :returns:
      :rtype: DatetimeIndex of holidays



