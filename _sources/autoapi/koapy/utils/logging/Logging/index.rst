:mod:`koapy.utils.logging.Logging`
==================================

.. py:module:: koapy.utils.logging.Logging


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.logging.Logging.LoggingMeta
   koapy.utils.logging.Logging.Logging




.. class:: LoggingMeta(cls, clsname, bases, dct)


   Bases: :py:obj:`type`

   .. attribute:: __default_config
      

      

   .. attribute:: __config_key
      :annotation: = koapy.utils.logging.config

      

   .. attribute:: __initialized
      :annotation: = False

      

   .. attribute:: __init_lock
      

      

   .. method:: __initialize_if_necessary(cls)


   .. method:: __initialize(cls)


   .. method:: __get_name_from_module(cls, module)


   .. method:: __module_name(cls)


   .. method:: __class_name(cls)


   .. method:: __logger_name(cls)


   .. method:: _get_logger(cls)


   .. method:: logger(cls)
      :property:


   .. method:: get_logger(cls, name=None)


   .. method:: verbosity_to_loglevel(cls, verbosity=0)


   .. method:: loglevel_to_verbosity(cls, loglevel=logging.WARNING)


   .. method:: set_loglevel(cls, loglevel=logging.WARNING, logger=None)


   .. method:: set_verbosity(cls, verbosity=0, logger=None)



.. class:: Logging

   .. method:: logger(self)
      :property:



