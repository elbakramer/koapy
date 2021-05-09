:mod:`koapy.backend.kiwoom_open_api_plus.utils.queue.QueueBasedIterableObserver`
================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.utils.queue.QueueBasedIterableObserver


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.utils.queue.QueueBasedIterableObserver.QueueBasedIterableObserverIterator
   koapy.backend.kiwoom_open_api_plus.utils.queue.QueueBasedIterableObserver.QueueBasedIterableObserver




.. class:: QueueBasedIterableObserverIterator(queue, sentinel)


   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.utils.queue.QueueIterator.BufferedQueueIterator`

   .. method:: next(self, block=True, timeout=None)


   .. method:: head(self)



.. class:: QueueBasedIterableObserver(queue=None, maxsize=None)


   Bases: :py:obj:`rx.core.typing.Observer`

   Observer abstract base class

   An Observer is the entity that receives all emissions of a subscribed
   Observable.

   .. attribute:: _default_maxsize
      :annotation: = 0

      

   .. attribute:: _queue_get_timeout
      :annotation: = 2

      

   .. method:: queue(self)
      :property:


   .. method:: on_next(self, value)

      Notifies the observer of a new element in the sequence.

      :param value: The received element.


   .. method:: on_error(self, error)

      Notifies the observer that an exception has occurred.

      :param error: The error that has occurred.


   .. method:: on_completed(self)

      Notifies the observer of the end of the sequence.


   .. method:: __iter__(self)


   .. method:: stop(self)



