:py:mod:`koapy.backtrader.KrxHistoricalDailyPriceData`
======================================================

.. py:module:: koapy.backtrader.KrxHistoricalDailyPriceData


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backtrader.KrxHistoricalDailyPriceData.KrxHistoricalDailyPriceData




.. py:class:: KrxHistoricalDailyPriceData

   Bases: :py:obj:`backtrader.feed.DataBase`

   .. py:attribute:: params
      :annotation: = [['loader', None], ['symbol', None], ['name', None], ['fromdate', None], ['todate', None],...

      

   .. py:attribute:: lines
      :annotation: = ['amount', 'marketcap', 'shares']

      

   .. py:method:: _close_cursor(self)


   .. py:method:: _initialize_cursor(self)


   .. py:method:: start(self)


   .. py:method:: stop(self)


   .. py:method:: _load(self)


   .. py:method:: adddata_fromfile(cls, cerebro, filename, symbols=None, fromdate=None, todate=None, progress_bar=True)
      :classmethod:



