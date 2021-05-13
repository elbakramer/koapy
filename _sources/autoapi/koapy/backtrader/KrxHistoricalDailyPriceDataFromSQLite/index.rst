:mod:`koapy.backtrader.KrxHistoricalDailyPriceDataFromSQLite`
=============================================================

.. py:module:: koapy.backtrader.KrxHistoricalDailyPriceDataFromSQLite


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backtrader.KrxHistoricalDailyPriceDataFromSQLite.KrxHistoricalDailyPriceDataFromSQLite




.. class:: KrxHistoricalDailyPriceDataFromSQLite


   Bases: :py:obj:`koapy.backtrader.SQLiteData.SQLiteData`

   .. attribute:: params
      :annotation: = [['engine', None], ['symbol', None], ['name', None], ['fromdate', None], ['todate', None],...

      

   .. attribute:: lines
      :annotation: = ['amount', 'marketcap', 'shares']

      

   .. method:: _load(self)


   .. method:: dump_from_store(cls, source_filename, dest_filename, symbols=None, fromdate=None, todate=None, progress_bar=True)
      :classmethod:


   .. method:: adddata_fromfile(cls, cerebro, filename, symbols=None, fromdate=None, todate=None, progress_bar=True)
      :classmethod:



