:mod:`koapy.utils.calendar.exchange_calendar_xkrx`
==================================================

.. py:module:: koapy.utils.calendar.exchange_calendar_xkrx


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.calendar.exchange_calendar_xkrx.XKRXExchangeCalendar
   koapy.utils.calendar.exchange_calendar_xkrx.PrecomputedXKRXExchangeCalendar




Attributes
~~~~~~~~~~

.. autoapisummary::

   koapy.utils.calendar.exchange_calendar_xkrx.start_krx
   koapy.utils.calendar.exchange_calendar_xkrx.start_default


.. data:: start_krx
   

   

.. data:: start_default
   

   

.. class:: XKRXExchangeCalendar(start=start_default, end=end_default)


   Bases: :py:obj:`exchange_calendars.exchange_calendar.ExchangeCalendar`

   Calendar for the Korea exchange, and the primary calendar for
   the country of South Korea.

   Open Time: 9:00 AM, KST (Korean Standard Time)
   Close Time: 3:30 PM, KST (Korean Standard Time)

   NOTE: Korea observes Standard Time year-round.

   Due to the complexity around the Korean holidays, we are hardcoding
   a list of holidays covering 1986-2019, inclusive.

   Regularly-Observed Holidays:
   - Seollal (New Year's Day)
   - Independence Movement Day
   - Labor Day
   - Buddha's Birthday
   - Memorial Day
   - Provincial Election Day
   - Liberation Day
   - Chuseok (Korean Thanksgiving)
   - National Foundation Day
   - Christmas Day
   - End of Year Holiday

   NOTE: Hangeul Day became a national holiday in 2013
   - Hangeul Proclamation Day

   .. attribute:: name
      :annotation: = XKRX

      

   .. attribute:: tz
      

      

   .. attribute:: open_times
      :annotation: = [None, None, None, None, None]

      

   .. attribute:: break_start_times
      :annotation: = [None, None, None, None, None, None]

      

   .. attribute:: break_end_times
      :annotation: = [None, None, None, None]

      

   .. attribute:: close_times
      :annotation: = [None, None, None, None]

      

   .. attribute:: weekmask
      :annotation: = 1111100

      

   .. method:: special_weekmasks(self)
      :property:


   .. method:: regular_holidays(self)
      :property:

      :returns: * **pd.AbstractHolidayCalendar** (*a calendar containing the regular holidays*)
      * *for this calendar*


   .. method:: adhoc_holidays(self)
      :property:

      :returns: **list**
      :rtype: A list of timestamps representing unplanned closes.


   .. method:: special_offsets(self)
      :property:


   .. method:: special_offsets_adhoc(self)
      :property:



.. class:: PrecomputedXKRXExchangeCalendar(start=None, end=None)


   Bases: :py:obj:`exchange_calendars.precomputed_exchange_calendar.PrecomputedExchangeCalendar`

   Calendar for the Korea exchange, and the primary calendar for
   the country of South Korea.

   Open Time: 9:00 AM, KST (Korean Standard Time)
   Close Time: 3:30 PM, KST (Korean Standard Time)

   NOTE: Korea observes Standard Time year-round.

   Due to the complexity around the Korean holidays, we are hardcoding
   a list of holidays covering 1986-2019, inclusive.

   Regularly-Observed Holidays:
   - Seollal (New Year's Day)
   - Independence Movement Day
   - Labor Day
   - Buddha's Birthday
   - Memorial Day
   - Provincial Election Day
   - Liberation Day
   - Chuseok (Korean Thanksgiving)
   - National Foundation Day
   - Christmas Day
   - End of Year Holiday

   NOTE: Hangeul Day became a national holiday in 2013
   - Hangeul Proclamation Day

   .. attribute:: name
      :annotation: = XKRX

      

   .. attribute:: tz
      

      

   .. attribute:: open_times
      :annotation: = [None]

      

   .. attribute:: close_times
      :annotation: = [None]

      

   .. method:: precomputed_holidays(self)
      :property:



