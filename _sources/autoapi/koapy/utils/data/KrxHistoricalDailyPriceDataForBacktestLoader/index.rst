:mod:`koapy.utils.data.KrxHistoricalDailyPriceDataForBacktestLoader`
====================================================================

.. py:module:: koapy.utils.data.KrxHistoricalDailyPriceDataForBacktestLoader


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.data.KrxHistoricalDailyPriceDataForBacktestLoader.KrxHistoricalDailyPriceDataForBacktestLoader




.. class:: KrxHistoricalDailyPriceDataForBacktestLoader(filename, library=None)


   .. method:: get_adjust_ratios(cls, data, sort=True)
      :classmethod:


   .. method:: adjust_data(cls, data, sort=True)
      :classmethod:


   .. method:: get_symbols(self)


   .. method:: update(self, download=False, progress_bar=False)


   .. method:: load(self, symbol, start_time=None, end_time=None)


   .. method:: load_as_cursor(self, symbol, start_time=None, end_time=None)



