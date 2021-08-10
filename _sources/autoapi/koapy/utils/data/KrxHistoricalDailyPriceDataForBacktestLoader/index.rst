:py:mod:`koapy.utils.data.KrxHistoricalDailyPriceDataForBacktestLoader`
=======================================================================

.. py:module:: koapy.utils.data.KrxHistoricalDailyPriceDataForBacktestLoader


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.data.KrxHistoricalDailyPriceDataForBacktestLoader.KrxHistoricalDailyPriceDataForBacktestLoader




.. py:class:: KrxHistoricalDailyPriceDataForBacktestLoader(filename, library=None)

   .. py:method:: get_adjust_ratios(cls, data, sort=True)
      :classmethod:


   .. py:method:: adjust_data(cls, data, sort=True)
      :classmethod:


   .. py:method:: get_symbols(self)


   .. py:method:: update(self, download=False, progress_bar=False)


   .. py:method:: load(self, symbol, start_time=None, end_time=None)


   .. py:method:: load_as_cursor(self, symbol, start_time=None, end_time=None)



