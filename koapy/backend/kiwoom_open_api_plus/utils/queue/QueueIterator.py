import atexit

from queue import Empty

class QueueIterator:

    _check_timeout = 1

    def __init__(self, queue):
        self._queue = queue
        self._should_stop = False

        atexit.register(self.stop)

    def __del__(self):
        atexit.unregister(self.stop)

    @property
    def queue(self):
        return self._queue

    def next(self, block=True, timeout=None):
        if block and timeout is None:
            timeout = self._check_timeout
            while not self._should_stop:
                try:
                    item = self._queue.get(block=block, timeout=timeout)
                except Empty:
                    pass
                else:
                    self._queue.task_done()
                    return item
            raise StopIteration
        else:
            item = self._queue.get(block=block, timeout=timeout)
            self._queue.task_done()
            return item

    def next_nowait(self):
        return self.next(block=False)

    def has_next(self):
        return not self._queue.empty()

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def stop(self):
        self._should_stop = True

    def enable(self):
        self._should_stop = False

class BufferedQueueIterator(QueueIterator):

    def __init__(self, queue):
        super().__init__(queue)

        self._none = object()
        self._head = self._none

    def next(self, block=True, timeout=None):
        if self._head is not self._none:
            item = self._head
            self._head = self._none
            return item
        else:
            return super().next(block, timeout)

    def has_next(self):
        return self._head is not self._none or super().has_next()

    def head(self):
        if self._head is not self._none:
            return self._head
        else:
            item = self.next_nowait() # raises queue.Empty if queue is empty
            self._head = item
            return self._head
