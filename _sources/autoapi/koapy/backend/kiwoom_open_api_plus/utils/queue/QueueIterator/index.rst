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

   .. py:method:: queue(self)
      :property:


   .. py:method:: next(self, block=True, timeout=None)


   .. py:method:: next_nowait(self)


   .. py:method:: has_next(self)


   .. py:method:: stop(self)


   .. py:method:: enable(self)



.. py:class:: BufferedQueueIterator(queue)

   Bases: :py:obj:`QueueIterator`

   .. py:method:: next(self, block=True, timeout=None)


   .. py:method:: has_next(self)


   .. py:method:: head(self)



