:py:mod:`koapy.utils.store.sqlalchemy.Library`
==============================================

.. py:module:: koapy.utils.store.sqlalchemy.Library


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.store.sqlalchemy.Library.Library




.. py:class:: Library

   Bases: :py:obj:`koapy.utils.store.sqlalchemy.Base.Base`

   .. py:attribute:: __tablename__
      :annotation: = libraries

      

   .. py:attribute:: id
      

      

   .. py:attribute:: name
      

      

   .. py:attribute:: symbols
      

      

   .. py:attribute:: snapshots
      

      

   .. py:method:: get_symbol(self, symbol, deleted=False)


   .. py:method:: get_or_create_symbol(self, symbol)


   .. py:method:: get_symbols(self, deleted=False)


   .. py:method:: get_versions(self, deleted=False)


   .. py:method:: get_latest_versions(self, deleted=False)


   .. py:method:: get_snapshot(self, snapshot)


   .. py:method:: create_snapshot(self, snapshot)


   .. py:method:: delete(self)



