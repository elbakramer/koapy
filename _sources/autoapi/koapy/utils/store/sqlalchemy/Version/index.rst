:py:mod:`koapy.utils.store.sqlalchemy.Version`
==============================================

.. py:module:: koapy.utils.store.sqlalchemy.Version


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.store.sqlalchemy.Version.Version




.. py:class:: Version

   Bases: :py:obj:`koapy.utils.store.sqlalchemy.Base.Base`

   .. py:attribute:: __tablename__
      :annotation: = versions

      

   .. py:attribute:: id
      

      

   .. py:attribute:: version
      

      

   .. py:attribute:: table_name
      

      

   .. py:attribute:: user_metadata
      

      

   .. py:attribute:: pandas_metadata
      

      

   .. py:attribute:: deleted
      

      

   .. py:attribute:: timestamp
      

      

   .. py:attribute:: symbol_id
      

      

   .. py:attribute:: symbol
      

      

   .. py:attribute:: snapshots
      

      

   .. py:attribute:: __table_args__
      

      

   .. py:method:: get_snapshots(self)


   .. py:method:: delete(self)



