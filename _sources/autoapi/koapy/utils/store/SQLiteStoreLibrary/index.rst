:mod:`koapy.utils.store.SQLiteStoreLibrary`
===========================================

.. py:module:: koapy.utils.store.SQLiteStoreLibrary


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.store.SQLiteStoreLibrary.SQLiteStoreLibrary




.. class:: SQLiteStoreLibrary(store, library)


   .. method:: list_symbols(self, all_symbols=False, snapshot=None)


   .. method:: has_symbol(self, symbol)


   .. method:: list_versions(self, symbol=None, snapshot=None, latest_only=False)


   .. method:: _hash_data(self, data)


   .. method:: write(self, symbol, data, metadata=None, prune_previous_version=True, **kwargs)


   .. method:: _get_version(self, symbol, as_of=None)


   .. method:: read_as_dataframe(self, symbol, as_of=None, time_column=None, start_time=None, end_time=None)


   .. method:: read_as_cursor(self, symbol, as_of=None, time_column=None, start_time=None, end_time=None)


   .. method:: read(self, *args, **kwargs)


   .. method:: _prune_previous_versions(self, symbol, keep_mins=120)


   .. method:: _delete_version(self, symbol, version)


   .. method:: delete(self, symbol)


   .. method:: list_snapshots(self)


   .. method:: snapshot(self, snapshot)


   .. method:: delete_snapshot(self, snapshot)



