:py:mod:`koapy.compat.pywinauto.importlib`
==========================================

.. py:module:: koapy.compat.pywinauto.importlib


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.compat.pywinauto.importlib.PyWinAutoFinder
   koapy.compat.pywinauto.importlib.PyWinAutoLoader




.. py:class:: PyWinAutoFinder

   Bases: :py:obj:`importlib.abc.MetaPathFinder`

   Abstract base class for import finders on sys.meta_path.

   .. py:method:: find_spec(self, fullname, path, target=None)


   .. py:method:: register(cls)
      :classmethod:


   .. py:method:: unregister(cls)
      :classmethod:



.. py:class:: PyWinAutoLoader

   Bases: :py:obj:`importlib.abc.Loader`

   Abstract base class for import loaders.

   .. py:method:: set_sys_coinit_flags(self)


   .. py:method:: reset_sys_coinit_flags(self)


   .. py:method:: create_module(self, spec)

      Return a module to initialize and into which to load.

      This method should raise ImportError if anything prevents it
      from creating a new module.  It may return None to indicate
      that the spec should create the new module.


   .. py:method:: exec_module(self, module)



