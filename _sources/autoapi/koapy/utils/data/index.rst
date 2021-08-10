:py:mod:`koapy.utils.data`
==========================

.. py:module:: koapy.utils.data


Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   KrxHistoricalDailyPriceDataDownloader/index.rst
   KrxHistoricalDailyPriceDataForBacktestLoader/index.rst
   KrxHistoricalDailyPriceDataLoader/index.rst
   YahooFinanceKrxHistoricalDailyPriceDataDownloader/index.rst


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.data.KrxHistoricalDailyPriceDataDownloader
   koapy.utils.data.KrxHistoricalDailyPriceDataForBacktestLoader
   koapy.utils.data.KrxHistoricalDailyPriceDataLoader




.. py:class:: KrxHistoricalDailyPriceDataDownloader

   .. py:method:: get_stocks(self)


   .. py:method:: get_stocks_delisted(self)


   .. py:method:: stocks(self)
      :property:


   .. py:method:: stocks_delisted(self)
      :property:


   .. py:method:: get_full_code(self, symbol)


   .. py:method:: get_name(self, symbol)


   .. py:method:: download(self, symbol, start_date=None, end_date=None)



.. py:class:: KrxHistoricalDailyPriceDataForBacktestLoader(filename, library=None)

   .. py:method:: get_adjust_ratios(cls, data, sort=True)
      :classmethod:


   .. py:method:: adjust_data(cls, data, sort=True)
      :classmethod:


   .. py:method:: get_symbols(self)


   .. py:method:: update(self, download=False, progress_bar=False)


   .. py:method:: load(self, symbol, start_time=None, end_time=None)


   .. py:method:: load_as_cursor(self, symbol, start_time=None, end_time=None)



.. py:class:: KrxHistoricalDailyPriceDataLoader(filename, library=None, library_delisted=None)

   .. py:method:: symbols(self)
      :property:


   .. py:method:: symbols_delisted(self)
      :property:


   .. py:method:: load_from_database(self, symbol, is_delisted=None)


   .. py:method:: load_or_download(self, symbol, is_delisted=None, start_date=None, end_date=None)


   .. py:method:: load(self, symbol, is_delisted=None, start_date=None, end_date=None, download=True)


   .. py:method:: update(self, progress_bar=False)



