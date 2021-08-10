:py:mod:`koapy.utils.logging.Logging`
=====================================

.. py:module:: koapy.utils.logging.Logging


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.logging.Logging.LoggingMeta
   koapy.utils.logging.Logging.Logging




.. py:class:: LoggingMeta(cls, clsname, bases, dct)

   Bases: :py:obj:`type`

   .. py:attribute:: __default_config
      

      

   .. py:attribute:: __config_key
      :annotation: = koapy.utils.logging.config

      

   .. py:attribute:: __initialized
      :annotation: = False

      

   .. py:attribute:: __init_lock
      

      

   .. py:method:: __initialize_if_necessary(cls)


   .. py:method:: __initialize(cls)


   .. py:method:: get_logger(cls, name=None)


   .. py:method:: __module_name(cls)


   .. py:method:: __class_name(cls)


   .. py:method:: __logger_name(cls)


   .. py:method:: get_class_logger(cls)


   .. py:method:: get_module_logger(cls)


   .. py:method:: get_package_logger(cls)


   .. py:method:: _logger(cls)


   .. py:method:: logger(cls)
      :property:


   .. py:method:: verbosity_to_loglevel(cls, verbosity)


   .. py:method:: loglevel_to_verbosity(cls, loglevel)


   .. py:method:: set_loglevel(cls, loglevel=logging.WARNING)


   .. py:method:: set_verbosity(cls, verbosity=0)



.. py:class:: Logging

   .. py:method:: logger(self)
      :property:



