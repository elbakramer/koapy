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


   .. py:method:: _hash_data(self, data)


   .. py:method:: write(self, symbol, data, metadata=None, prune_previous_version=True, **kwargs)


   .. py:method:: _get_version(self, symbol, as_of=None)


   .. py:method:: read_as_dataframe(self, symbol, as_of=None, time_column=None, start_time=None, end_time=None)


   .. py:method:: read_as_cursor(self, symbol, as_of=None, time_column=None, start_time=None, end_time=None)


   .. py:method:: read(self, *args, **kwargs)


   .. py:method:: _prune_previous_versions(self, symbol, keep_mins=120)


   .. py:method:: _delete_version(self, symbol, version)


   .. py:method:: delete(self, symbol)


   .. py:method:: list_snapshots(self)


   .. py:method:: snapshot(self, snapshot)


   .. py:method:: delete_snapshot(self, snapshot)



