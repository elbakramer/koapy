:py:mod:`koapy.backtrader.KrxTradingCalendar`
=============================================

.. py:module:: koapy.backtrader.KrxTradingCalendar


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backtrader.KrxTradingCalendar.ExchangeCalendarsTradingCalendar
   koapy.backtrader.KrxTradingCalendar.KrxTradingCalendar




.. py:class:: ExchangeCalendarsTradingCalendar

   Bases: :py:obj:`backtrader.tradingcal.TradingCalendarBase`

   .. py:attribute:: params
      :annotation: = [['calendar', None], ['cachesize', 365]]

      

   .. py:method:: schedule(self, day, tz=None)

      day: expecting naive datetime.datetime day in utc timezone
      tz: treat/localize internal naive datetimes to this timezone
      returns: (opening, closing) naive datetime.datetime pair in utc timezone



.. py:class:: KrxTradingCalendar

   Bases: :py:obj:`ExchangeCalendarsTradingCalendar`

   .. py:attribute:: params
      :annotation: = [['calendar', 'XKRX'], ['cachesize', 365]]

      


