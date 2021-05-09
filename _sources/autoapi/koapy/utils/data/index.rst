:mod:`koapy.utils.data`
=======================

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




.. class:: KrxHistoricalDailyPriceDataDownloader


   .. method:: get_stocks(self)


   .. method:: get_stocks_delisted(self)


   .. method:: stocks(self)
      :property:


   .. method:: stocks_delisted(self)
      :property:


   .. method:: get_full_code(self, symbol)


   .. method:: download(self, symbol, start_date=None, end_date=None)



.. class:: KrxHistoricalDailyPriceDataForBacktestLoader(filename, library=None)


   .. method:: get_adjust_ratios(cls, data, sort=True)
      :classmethod:


   .. method:: adjust_data(cls, data, sort=True)
      :classmethod:


   .. method:: get_symbols(self)


   .. method:: update(self, download=False, progress_bar=False)


   .. method:: load(self, symbol, start_time=None, end_time=None)


   .. method:: load_as_cursor(self, symbol, start_time=None, end_time=None)



.. class:: KrxHistoricalDailyPriceDataLoader(filename, library=None, library_delisted=None)


   .. method:: symbols(self)
      :property:


   .. method:: symbols_delisted(self)
      :property:


   .. method:: load_from_database(self, symbol, is_delisted=None)


   .. method:: load_or_download(self, symbol, is_delisted=None, start_date=None, end_date=None)


   .. method:: load(self, symbol, is_delisted=None, start_date=None, end_date=None, download=True)


   .. method:: update(self, progress_bar=False)



