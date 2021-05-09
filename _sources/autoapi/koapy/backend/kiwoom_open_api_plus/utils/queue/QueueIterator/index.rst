:mod:`koapy.backend.kiwoom_open_api_plus.utils.queue.QueueIterator`
===================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.utils.queue.QueueIterator


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.utils.queue.QueueIterator.QueueIterator
   koapy.backend.kiwoom_open_api_plus.utils.queue.QueueIterator.BufferedQueueIterator




.. class:: QueueIterator(queue)


   .. attribute:: _check_timeout
      :annotation: = 1

      

   .. method:: __del__(self)


   .. method:: queue(self)
      :property:


   .. method:: next(self, block=True, timeout=None)


   .. method:: next_nowait(self)


   .. method:: has_next(self)


   .. method:: __iter__(self)


   .. method:: __next__(self)


   .. method:: stop(self)


   .. method:: enable(self)



.. class:: BufferedQueueIterator(queue)


   Bases: :py:obj:`QueueIterator`

   .. method:: next(self, block=True, timeout=None)


   .. method:: has_next(self)


   .. method:: head(self)



