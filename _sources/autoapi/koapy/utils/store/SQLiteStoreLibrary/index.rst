:py:mod:`koapy.utils.store.SQLiteStoreLibrary`
==============================================

.. py:module:: koapy.utils.store.SQLiteStoreLibrary


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.store.SQLiteStoreLibrary.SQLiteStoreLibrary




.. py:class:: SQLiteStoreLibrary(store, library)

   .. py:method:: list_symbols(self, all_symbols=False, snapshot=None)


   .. py:method:: has_symbol(self, symbol)


   .. py:method:: list_versions(self, symbol=None, snapshot=None, latest_only=False)


   .. py:method:: write(self, symbol, data, metadata=None, prune_previous_version=True, **kwargs)


   .. py:method:: read_as_dataframe(self, symbol, as_of=None, time_column=None, start_time=None, end_time=None)


   .. py:method:: read_as_cursor(self, symbol, as_of=None, time_column=None, start_time=None, end_time=None)


   .. py:method:: read(self, *args, **kwargs)


   .. py:method:: delete(self, symbol)


   .. py:method:: list_snapshots(self)


   .. py:method:: snapshot(self, snapshot)


   .. py:method:: delete_snapshot(self, snapshot)



