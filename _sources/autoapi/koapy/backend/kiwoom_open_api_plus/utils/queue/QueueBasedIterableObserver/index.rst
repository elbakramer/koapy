:py:mod:`koapy.backend.kiwoom_open_api_plus.utils.queue.QueueBasedIterableObserver`
===================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.utils.queue.QueueBasedIterableObserver


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.utils.queue.QueueBasedIterableObserver.QueueBasedIterableObserverIterator
   koapy.backend.kiwoom_open_api_plus.utils.queue.QueueBasedIterableObserver.QueueBasedIterableObserver




.. py:class:: QueueBasedIterableObserverIterator(queue, sentinel)

   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.utils.queue.QueueIterator.BufferedQueueIterator`

   .. py:method:: next(self, block=True, timeout=None)


   .. py:method:: head(self)



.. py:class:: QueueBasedIterableObserver(queue=None, maxsize=None)

   Bases: :py:obj:`rx.core.typing.Observer`

   Observer abstract base class

   An Observer is the entity that receives all emissions of a subscribed
   Observable.

   .. py:method:: queue(self)
      :property:


   .. py:method:: on_next(self, value)

      Notifies the observer of a new element in the sequence.

      :param value: The received element.


   .. py:method:: on_error(self, error)

      Notifies the observer that an exception has occurred.

      :param error: The error that has occurred.


   .. py:method:: on_completed(self)

      Notifies the observer of the end of the sequence.


   .. py:method:: stop(self)



