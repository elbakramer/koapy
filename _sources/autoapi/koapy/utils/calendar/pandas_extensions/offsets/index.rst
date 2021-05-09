:mod:`koapy.utils.calendar.pandas_extensions.offsets`
=====================================================

.. py:module:: koapy.utils.calendar.pandas_extensions.offsets


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.calendar.pandas_extensions.offsets.CompositeCustomBusinessDay
   koapy.utils.calendar.pandas_extensions.offsets.MultipleWeekmaskCustomBusinessDay



Functions
~~~~~~~~~

.. autoapisummary::

   koapy.utils.calendar.pandas_extensions.offsets._is_normalized
   koapy.utils.calendar.pandas_extensions.offsets._to_dt64D
   koapy.utils.calendar.pandas_extensions.offsets._get_calendar



.. class:: CompositeCustomBusinessDay(n=1, normalize=False, weekmask='Mon Tue Wed Thu Fri', holidays=None, calendar=None, offset=timedelta(0), business_days=None)


   Bases: :py:obj:`pandas.tseries.offsets.CustomBusinessDay`

   .. attribute:: _prefix
      :annotation: = C

      

   .. attribute:: _attributes
      

      

   .. method:: __setstate__(self, state)


   .. method:: business_days(self)
      :property:

      Returns list of tuples of (start_date, end_date, custom_business_day)
      which overrides default behavior for the given interval, which starts
      from start_date to end_date, inclusive in both sides.


   .. method:: _as_custom_business_day(self)


   .. method:: _custom_business_day_for(self, other, n=None, is_edge=False, with_interval=False)


   .. method:: _moved(self, from_date, to_date, bday)


   .. method:: apply(self, other)


   .. method:: is_on_offset(self, dt)



.. function:: _is_normalized(dt)


.. function:: _to_dt64D(dt)


.. function:: _get_calendar(weekmask, holidays, calendar)

   Generate busdaycalendar


.. class:: MultipleWeekmaskCustomBusinessDay(n=1, normalize=False, weekmask='Mon Tue Wed Thu Fri', holidays=None, calendar=None, offset=timedelta(0), business_days=None, weekmasks=None)


   Bases: :py:obj:`CompositeCustomBusinessDay`

   .. attribute:: _prefix
      :annotation: = C

      

   .. attribute:: _attributes
      

      

   .. method:: __setstate__(self, state)


   .. method:: weekmasks(self)
      :property:



