:mod:`koapy.utils.store.sqlalchemy.Symbol`
==========================================

.. py:module:: koapy.utils.store.sqlalchemy.Symbol


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.store.sqlalchemy.Symbol.Symbol




.. class:: Symbol

   Bases: :py:obj:`koapy.utils.store.sqlalchemy.Base.Base`

   .. attribute:: __tablename__
      :annotation: = symbols

      

   .. attribute:: id
      

      

   .. attribute:: name
      

      

   .. attribute:: library_id
      

      

   .. attribute:: library
      

      

   .. attribute:: versions
      

      

   .. attribute:: __table_args__
      

      

   .. method:: get_versions(self, deleted=False)

      versions = self.versions
      if not deleted:
          versions = [version for version in versions if not version.deleted]


   .. method:: get_latest_version(self, deleted=False)

      versions = self.versions
      if len(versions) == 0:
          raise NoResultFound
      latest_version = self.versions[-1]
      if not deleted and latest_version.deleted:
          raise NoResultFound


   .. method:: create_new_version(self, table_name=None, user_metadata=None, pandas_metadata=None, deleted=None)


   .. method:: get_version_by_number(self, version_number, deleted=False)


   .. method:: get_prunable_versions(self, keep_mins=120)



