:py:mod:`koapy.backend.kiwoom_open_api_plus.utils.queue.QueueIterator`
======================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.utils.queue.QueueIterator


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.utils.queue.QueueIterator.QueueIterator
   koapy.backend.kiwoom_open_api_plus.utils.queue.QueueIterator.BufferedQueueIterator




.. py:class:: QueueIterator(queue)

   .. py:attribute:: _check_timeout
      :annotation: = 1

      

   .. py:method:: __del__(self)


   .. py:method:: queue(self)
      :property:


   .. py:method:: next(self, block=True, timeout=None)


   .. py:method:: next_nowait(self)


   .. py:method:: has_next(self)


   .. py:method:: __iter__(self)


   .. py:method:: __next__(self)


   .. py:method:: stop(self)


   .. py:method:: enable(self)



.. py:class:: BufferedQueueIterator(queue)

   Bases: :py:obj:`QueueIterator`

   .. py:method:: next(self, block=True, timeout=None)


   .. py:method:: has_next(self)


   .. py:method:: head(self)



