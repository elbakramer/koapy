:mod:`koapy.utils.store.sqlalchemy.Version`
===========================================

.. py:module:: koapy.utils.store.sqlalchemy.Version


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.store.sqlalchemy.Version.Version




.. class:: Version

   Bases: :py:obj:`koapy.utils.store.sqlalchemy.Base.Base`

   .. attribute:: __tablename__
      :annotation: = versions

      

   .. attribute:: id
      

      

   .. attribute:: version
      

      

   .. attribute:: table_name
      

      

   .. attribute:: user_metadata
      

      

   .. attribute:: pandas_metadata
      

      

   .. attribute:: deleted
      

      

   .. attribute:: timestamp
      

      

   .. attribute:: symbol_id
      

      

   .. attribute:: symbol
      

      

   .. attribute:: snapshots
      

      

   .. attribute:: __table_args__
      

      

   .. method:: get_snapshots(self)


   .. method:: delete(self)



