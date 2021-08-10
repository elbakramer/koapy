:py:mod:`koapy.utils.store.sqlalchemy.Symbol`
=============================================

.. py:module:: koapy.utils.store.sqlalchemy.Symbol


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.store.sqlalchemy.Symbol.Symbol




.. py:class:: Symbol

   Bases: :py:obj:`koapy.utils.store.sqlalchemy.Base.Base`

   .. py:attribute:: __tablename__
      :annotation: = symbols

      

   .. py:attribute:: id
      

      

   .. py:attribute:: name
      

      

   .. py:attribute:: library_id
      

      

   .. py:attribute:: library
      

      

   .. py:attribute:: versions
      

      

   .. py:attribute:: __table_args__
      

      

   .. py:method:: get_versions(self, deleted=False)

      versions = self.versions
      if not deleted:
          versions = [version for version in versions if not version.deleted]


   .. py:method:: get_latest_version(self, deleted=False)

      versions = self.versions
      if len(versions) == 0:
          raise NoResultFound
      latest_version = self.versions[-1]
      if not deleted and latest_version.deleted:
          raise NoResultFound


   .. py:method:: create_new_version(self, table_name=None, user_metadata=None, pandas_metadata=None, deleted=None)


   .. py:method:: get_version_by_number(self, version_number, deleted=False)


   .. py:method:: get_prunable_versions(self, keep_mins=120)



