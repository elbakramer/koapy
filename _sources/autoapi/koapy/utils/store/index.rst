:mod:`koapy.utils.store`
========================

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




.. class:: SQLiteStore(filename)


   .. method:: list_libraries(self)


   .. method:: _get_library(self, library)


   .. method:: library_exists(self, library)


   .. method:: initialize_library(self, library)


   .. method:: get_library(self, library)


   .. method:: get_or_create_library(self, library)


   .. method:: delete_library(self, library)


   .. method:: __getitem__(self, library)



