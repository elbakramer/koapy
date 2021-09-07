:py:mod:`koapy.compat.pywinauto`
================================

.. py:module:: koapy.compat.pywinauto


Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   findwindows/index.rst
   importlib/index.rst
   timings/index.rst


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.compat.pywinauto.PyWinAutoFinder




.. py:class:: PyWinAutoFinder

   Bases: :py:obj:`importlib.abc.MetaPathFinder`

   Abstract base class for import finders on sys.meta_path.

   .. py:method:: find_spec(self, fullname, path, target=None)


   .. py:method:: register(cls)
      :classmethod:


   .. py:method:: unregister(cls)
      :classmethod:



