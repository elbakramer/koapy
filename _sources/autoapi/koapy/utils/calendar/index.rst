:mod:`koapy.utils.calendar`
===========================

.. py:module:: koapy.utils.calendar


Subpackages
-----------
.. toctree::
   :titlesonly:
   :maxdepth: 3

   etc/index.rst
   pandas_extensions/index.rst


Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   exchange_calendar/index.rst
   exchange_calendar_xkrx/index.rst
   xkrx_holidays/index.rst


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.calendar.XKRXExchangeCalendar




Attributes
~~~~~~~~~~

.. autoapisummary::

   koapy.utils.calendar._default_calendar_factories
   koapy.utils.calendar._default_calendar_aliases
   koapy.utils.calendar.global_calendar_dispatcher
   koapy.utils.calendar.get_calendar
   koapy.utils.calendar.get_calendar_names
   koapy.utils.calendar.clear_calendars
   koapy.utils.calendar.deregister_calendar
   koapy.utils.calendar.register_calendar
   koapy.utils.calendar.register_calendar_type
   koapy.utils.calendar.register_calendar_alias
   koapy.utils.calendar.resolve_alias


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



.. data:: _default_calendar_factories
   

   

.. data:: _default_calendar_aliases
   

   

.. data:: global_calendar_dispatcher
   

   

.. data:: get_calendar
   

   

.. data:: get_calendar_names
   

   

.. data:: clear_calendars
   

   

.. data:: deregister_calendar
   

   

.. data:: register_calendar
   

   

.. data:: register_calendar_type
   

   

.. data:: register_calendar_alias
   

   

.. data:: resolve_alias
   

   

