:mod:`koapy.backtrader.KrxHistoricalDailyPriceData`
===================================================

.. py:module:: koapy.backtrader.KrxHistoricalDailyPriceData


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backtrader.KrxHistoricalDailyPriceData.KrxHistoricalDailyPriceData




.. class:: KrxHistoricalDailyPriceData


   Bases: :py:obj:`backtrader.feed.DataBase`

   .. attribute:: params
      :annotation: = [['loader', None], ['symbol', None], ['name', None], ['fromdate', None], ['todate', None],...

      

   .. attribute:: lines
      :annotation: = ['amount', 'marketcap', 'shares']

      

   .. method:: _close_cursor(self)


   .. method:: _initialize_cursor(self)


   .. method:: start(self)


   .. method:: stop(self)


   .. method:: _load(self)


   .. method:: adddata_fromfile(cls, cerebro, filename, symbols=None, fromdate=None, todate=None, progress_bar=True)
      :classmethod:



