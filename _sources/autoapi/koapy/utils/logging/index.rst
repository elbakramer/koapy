:mod:`koapy.utils.logging`
==========================

.. py:module:: koapy.utils.logging


Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   Logging/index.rst


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.logging.Logging



Functions
~~~~~~~~~

.. autoapisummary::

   koapy.utils.logging.verbosity_to_loglevel
   koapy.utils.logging.loglevel_to_verbosity
   koapy.utils.logging.set_loglevel
   koapy.utils.logging.set_verbosity
   koapy.utils.logging.get_module_name
   koapy.utils.logging.get_logger



.. class:: Logging

   .. method:: logger(self)
      :property:



.. function:: verbosity_to_loglevel(verbosity=0)


.. function:: loglevel_to_verbosity(loglevel=logging.WARNING)


.. function:: set_loglevel(loglevel=logging.WARNING, logger=None)


.. function:: set_verbosity(verbosity=0, logger=None)


.. function:: get_module_name(offset=0)


.. function:: get_logger(name=None)


