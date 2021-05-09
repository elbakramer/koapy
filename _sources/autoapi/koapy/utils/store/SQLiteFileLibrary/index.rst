:mod:`koapy.utils.store.SQLiteFileLibrary`
==========================================

.. py:module:: koapy.utils.store.SQLiteFileLibrary


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.store.SQLiteFileLibrary.SQLiteFileLibrary




.. class:: SQLiteFileLibrary(filename)


   .. method:: list_symbols(self)


   .. method:: has_symbol(self, symbol)


   .. method:: write(self, symbol, data)


   .. method:: read_as_dataframe(self, symbol, time_column=None, start_time=None, end_time=None)


   .. method:: read_as_cursor(self, symbol, time_column=None, start_time=None, end_time=None)


   .. method:: read(self, *args, **kwargs)


   .. method:: delete(self, symbol)



