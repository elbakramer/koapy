:py:mod:`koapy.utils.store`
===========================

.. py:module:: koapy.utils.store


Subpackages
-----------
.. toctree::
   :titlesonly:
   :maxdepth: 3

   misc/index.rst
   sqlalchemy/index.rst


Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   SQLiteFileLibrary/index.rst
   SQLiteStore/index.rst
   SQLiteStoreLibrary/index.rst


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.store.SQLiteStore




.. py:class:: SQLiteStore(filename)

   .. py:method:: list_libraries(self)


   .. py:method:: library_exists(self, library)


   .. py:method:: initialize_library(self, library)


   .. py:method:: get_library(self, library)


   .. py:method:: get_or_create_library(self, library)


   .. py:method:: delete_library(self, library)



