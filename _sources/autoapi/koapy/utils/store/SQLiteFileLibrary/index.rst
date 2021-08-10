:py:mod:`koapy.utils.store.SQLiteFileLibrary`
=============================================

.. py:module:: koapy.utils.store.SQLiteFileLibrary


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.store.SQLiteFileLibrary.SQLiteFileLibrary




.. py:class:: SQLiteFileLibrary(filename)

   .. py:method:: list_symbols(self)


   .. py:method:: has_symbol(self, symbol)


   .. py:method:: write(self, symbol, data)


   .. py:method:: read_as_dataframe(self, symbol, time_column=None, start_time=None, end_time=None)


   .. py:method:: read_as_cursor(self, symbol, time_column=None, start_time=None, end_time=None)


   .. py:method:: read(self, *args, **kwargs)


   .. py:method:: delete(self, symbol)



