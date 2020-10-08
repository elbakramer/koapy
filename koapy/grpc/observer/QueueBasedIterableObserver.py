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
        self._should_stop = False

        atexit.register(self.stop)

    def __del__(self):
        atexit.unregister(self.stop)

    def on_next(self, item):
        self._queue.put((item, None))

    def on_error(self, error):
        self._queue.put((None, error))

    def on_completed(self):
        self._queue.put((self._sentinel, None))

    def stop(self):
        self._should_stop = True

    def enable(self):
        self._should_stop = False

    def __iter__(self):
        while not self._should_stop:
            try:
                item, err = self._queue.get(True, self._queue_get_timeout)
            except Empty:
                pass
            else:
                if item == self._sentinel:
                    self._queue.task_done()
                    break
                if err is not None and isinstance(err, Exception):
                    self._queue.task_done()
                    raise err
                yield item
                self._queue.task_done()
