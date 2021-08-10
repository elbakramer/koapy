:py:mod:`koapy.backtrader.KrxHistoricalDailyPriceDataFromSQLite`
================================================================

.. py:module:: koapy.backtrader.KrxHistoricalDailyPriceDataFromSQLite


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backtrader.KrxHistoricalDailyPriceDataFromSQLite.KrxHistoricalDailyPriceDataFromSQLite




.. py:class:: KrxHistoricalDailyPriceDataFromSQLite

   Bases: :py:obj:`koapy.backtrader.SQLiteData.SQLiteData`

   .. py:attribute:: params
      :annotation: = [['engine', None], ['symbol', None], ['name', None], ['fromdate', None], ['todate', None],...

      

   .. py:attribute:: lines
      :annotation: = ['amount', 'marketcap', 'shares']

      

   .. py:method:: _load(self)


   .. py:method:: dump_from_store(cls, source_filename, dest_filename, symbols=None, fromdate=None, todate=None, progress_bar=True)
      :classmethod:


   .. py:method:: adddata_fromfile(cls, cerebro, filename, symbols=None, fromdate=None, todate=None, progress_bar=True)
      :classmethod:



