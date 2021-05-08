import sys
import threading

from queue import Queue

from koapy.backend.kiwoom_open_api_plus.utils.queue.QueueIterator import (
    BufferedQueueIterator,
)
from koapy.utils.logging.Logging import Logging


class QueueBasedBufferedIterator(BufferedQueueIterator, Logging):

    _check_timeout = 1
    _default_maxsize = 10

    def __init__(self, iterator, queue=None, maxsize=None):
        if queue is None:
            if maxsize is None:
                maxsize = self._default_maxsize
            queue = Queue(maxsize)

        self._iterator = iterator
        self._queue = queue
        self._maxsize = maxsize
        self._exc_info = None

        super().__init__(self._queue)

        self._thread = threading.Thread(target=self._consume_iterator, daemon=True)
        self._thread.start()

    def _consume_iterator(self):
        try:
            for item in self._iterator:
                self._queue.put(item)
        except Exception:  # pylint: disable=broad-except
            self.logger.exception("Exception raised while consuming iterator")
            self._exc_info = sys.exc_info()

    def next(self, block=True, timeout=None):
        try:
            item = super().next(block, timeout)
        except StopIteration as e:
            if self._exc_info is not None:
                raise self._exc_info[1] from e
            else:
                raise e
        else:
            if self._exc_info is not None:
                raise self._exc_info[1]
        return item
