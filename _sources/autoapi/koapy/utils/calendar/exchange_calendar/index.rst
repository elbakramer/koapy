:mod:`koapy.utils.calendar.exchange_calendar`
=============================================

.. py:module:: koapy.utils.calendar.exchange_calendar


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.calendar.exchange_calendar.ExchangeCalendar



Functions
~~~~~~~~~

.. autoapisummary::

   koapy.utils.calendar.exchange_calendar.selection
   koapy.utils.calendar.exchange_calendar.days_at_time
   koapy.utils.calendar.exchange_calendar._group_times



.. function:: selection(arr, start, end)


.. function:: days_at_time(days, t, tz, day_offset=0)


.. function:: _group_times(all_days, times, tz, offset=0)


.. class:: ExchangeCalendar(start=start_default, end=end_default)


   Bases: :py:obj:`exchange_calendars.exchange_calendar.ExchangeCalendar`

   An ExchangeCalendar represents the timing information of a single market
   exchange.

   The timing information is made up of two parts: sessions, and opens/closes.

   A session represents a contiguous set of minutes, and has a label that is
   midnight UTC. It is important to note that a session label should not be
   considered a specific point in time, and that midnight UTC is just being
   used for convenience.

   For each session, we store the open and close time in UTC time.

   .. method:: day(self)


   .. method:: special_weekmasks(self)
      :property:

      :returns: **list** -- weekmasks that applies between dates.
      :rtype: List of (date, date, str) tuples that represent special


   .. method:: special_offsets(self)
      :property:

      :returns: **list** -- that represent special open, break_start, break_end, close offsets
                and corresponding HolidayCalendars.
      :rtype: List of (timedelta, timedelta, timedelta, timedelta, AbstractHolidayCalendar) tuples


   .. method:: special_offsets_adhoc(self)
      :property:

      :returns: **list** -- that represent special open, break_start, break_end, close offsets
                and corresponding DatetimeIndexes.
      :rtype: List of (timedelta, timedelta, timedelta, timedelta, DatetimeIndex) tuples


   .. method:: _overwrite_special_offsets(self, session_labels, opens_or_closes, calendars, ad_hoc_dates, start_date, end_date, strict=False)


   .. method:: _calculate_and_overwrite_special_offsets(self, session_labels, start, end)



