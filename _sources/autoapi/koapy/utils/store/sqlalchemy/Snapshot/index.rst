:mod:`koapy.utils.store.sqlalchemy.Snapshot`
============================================

.. py:module:: koapy.utils.store.sqlalchemy.Snapshot


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.store.sqlalchemy.Snapshot.Snapshot




.. class:: Snapshot

   Bases: :py:obj:`koapy.utils.store.sqlalchemy.Base.Base`

   .. attribute:: __tablename__
      :annotation: = snapshots

      

   .. attribute:: id
      

      

   .. attribute:: name
      

      

   .. attribute:: timestamp
      

      

   .. attribute:: library_id
      

      

   .. attribute:: library
      

      

   .. attribute:: versions
      

      

   .. attribute:: __table_args__
      

      

   .. method:: get_symbols(self)


   .. method:: get_versions(self)


   .. method:: get_version_of_symbol(self, symbol)


   .. method:: delete(self)



