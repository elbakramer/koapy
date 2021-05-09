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

   .. attribute:: __config
      

      

   .. attribute:: __initialized
      :annotation: = False

      

   .. attribute:: __init_lock
      

      

   .. method:: __initialize_if_necessary(cls)


   .. method:: __initialize(cls)


   .. method:: __class_name(cls)


   .. method:: __logger_name(cls)


   .. method:: logger(cls)
      :property:


   .. method:: get_logger(cls, name=None)



.. class:: Logging

   .. method:: logger(self)
      :property:



