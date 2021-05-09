:mod:`koapy.utils.store.sqlalchemy.Library`
===========================================

.. py:module:: koapy.utils.store.sqlalchemy.Library


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.store.sqlalchemy.Library.Library




.. class:: Library

   Bases: :py:obj:`koapy.utils.store.sqlalchemy.Base.Base`

   .. attribute:: __tablename__
      :annotation: = libraries

      

   .. attribute:: id
      

      

   .. attribute:: name
      

      

   .. attribute:: symbols
      

      

   .. attribute:: snapshots
      

      

   .. method:: get_symbol(self, symbol, deleted=False)


   .. method:: get_or_create_symbol(self, symbol)


   .. method:: get_symbols(self, deleted=False)


   .. method:: get_versions(self, deleted=False)


   .. method:: get_latest_versions(self, deleted=False)


   .. method:: get_snapshot(self, snapshot)


   .. method:: create_snapshot(self, snapshot)


   .. method:: delete(self)



