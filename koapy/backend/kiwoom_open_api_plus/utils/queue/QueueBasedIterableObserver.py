from queue import Queue, Empty
from rx.core.typing import Observer
from koapy.backend.kiwoom_open_api_plus.utils.queue.QueueIterator import BufferedQueueIterator

class QueueBasedIterableObserverIterator(BufferedQueueIterator):

    def __init__(self, queue, sentinel):
        self._queue = queue
        self._sentinel = sentinel
        super().__init__(self._queue)

    def next(self, block=True, timeout=None):
        value, error = super().next(block, timeout)
        if value == self._sentinel:
            raise StopIteration
        elif error is not None and isinstance(error, Exception):
            raise error
        return value

    def head(self):
        value, error = super().head()
        if value == self._sentinel:
            raise Empty
        elif error is not None and isinstance(error, Exception):
            raise error
        return value

class QueueBasedIterableObserver(Observer):

    _default_maxsize = 0
    _queue_get_timeout = 2

    def __init__(self, queue=None, maxsize=None):
        if queue is None:
            if maxsize is None:
                maxsize = self._default_maxsize
            queue = Queue(maxsize)

        self._queue = queue
        self._maxsize = maxsize
        self._sentinel = object()

        self._iterator = QueueBasedIterableObserverIterator(self._queue, self._sentinel)

    @property
    def queue(self):
        return self._queue

    def on_next(self, value):
        self._queue.put((value, None))

    def on_error(self, error):
        self._queue.put((None, error))

    def on_completed(self):
        self._queue.put((self._sentinel, None))

    def __iter__(self):
        return self._iterator

    def stop(self):
        return self._iterator.stop()
