:mod:`koapy.backend.kiwoom_open_api_plus.utils.queue.QueueBasedBufferedIterator`
================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.utils.queue.QueueBasedBufferedIterator


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.utils.queue.QueueBasedBufferedIterator.QueueBasedBufferedIterator




.. class:: QueueBasedBufferedIterator(iterator, queue=None, maxsize=None)


   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.utils.queue.QueueIterator.BufferedQueueIterator`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. attribute:: _check_timeout
      :annotation: = 1

      

   .. attribute:: _default_maxsize
      :annotation: = 10

      

   .. method:: _consume_iterator(self)


   .. method:: next(self, block=True, timeout=None)



