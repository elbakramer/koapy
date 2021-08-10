:py:mod:`koapy.utils.store.sqlalchemy.Snapshot`
===============================================

.. py:module:: koapy.utils.store.sqlalchemy.Snapshot


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.store.sqlalchemy.Snapshot.Snapshot




.. py:class:: Snapshot

   Bases: :py:obj:`koapy.utils.store.sqlalchemy.Base.Base`

   .. py:attribute:: __tablename__
      :annotation: = snapshots

      

   .. py:attribute:: id
      

      

   .. py:attribute:: name
      

      

   .. py:attribute:: timestamp
      

      

   .. py:attribute:: library_id
      

      

   .. py:attribute:: library
      

      

   .. py:attribute:: versions
      

      

   .. py:attribute:: __table_args__
      

      

   .. py:method:: get_symbols(self)


   .. py:method:: get_versions(self)


   .. py:method:: get_version_of_symbol(self, symbol)


   .. py:method:: delete(self)



