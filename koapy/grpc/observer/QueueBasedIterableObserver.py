import atexit

from queue import Queue, Empty
from koapy.grpc.observer.Observer import Observer

class QueueBasedIterableObserver(Observer):

    _queue_get_timeout = 2

    def __init__(self, queue=None):
        if queue is None:
            queue = Queue()

        self._queue = queue
        self._sentinel = object()

        atexit.register(self._queue.put, self._sentinel)

    def __del__(self):
        atexit.unregister(self._queue.put)

    def on_next(self, value):
        self._queue.put(value)

    def on_error(self, error):
        self._queue.put(error)

    def on_completed(self):
        self._queue.put(self._sentinel)

    def __iter__(self):
        while True:
            try:
                value = self._queue.get(True, self._queue_get_timeout)
            except Empty:
                pass
            else:
                if value == self._sentinel:
                    self._queue.task_done()
                    break
                if isinstance(value, Exception):
                    self._queue.task_done()
                    raise value
                yield value
                self._queue.task_done()
