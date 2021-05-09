:mod:`koapy.compat.pywinauto`
=============================

.. py:module:: koapy.compat.pywinauto


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.compat.pywinauto.PyWinAutoFinder
   koapy.compat.pywinauto.PyWinAutoLoader




.. class:: PyWinAutoFinder

   Bases: :py:obj:`importlib.abc.MetaPathFinder`

   Abstract base class for import finders on sys.meta_path.

   .. method:: find_spec(self, fullname, path, target=None)


   .. method:: register(cls)
      :classmethod:


   .. method:: unregister(cls)
      :classmethod:



.. class:: PyWinAutoLoader


   Bases: :py:obj:`importlib.abc.Loader`

   Abstract base class for import loaders.

   .. method:: set_sys_coinit_flags(self)


   .. method:: reset_sys_coinit_flags(self)


   .. method:: create_module(self, spec)

      Return a module to initialize and into which to load.

      This method should raise ImportError if anything prevents it
      from creating a new module.  It may return None to indicate
      that the spec should create the new module.


   .. method:: exec_module(self, module)



