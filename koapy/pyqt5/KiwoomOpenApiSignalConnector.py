import logging
import threading

class KiwoomOpenApiSignalConnector:

    def __init__(self, name=None):
        self._name = name
        self._lock = threading.RLock()
        self._slots = list()

    def connect(self, slot):
        with self._lock:
            if slot not in self._slots:
                self._slots.append(slot)

    def disconnect(self, slot=None):
        with self._lock:
            if slot is None:
                self._slots.clear()
            elif slot in self._slots:
                self._slots.remove(slot)
            else:
                logging.warning("Tried to disconnect a slot that doesn't exist")

    def get_slots(self):
        with self._lock:
            # make a copy in order to prevent modification during iteration
            # problem
            return list(self._slots)

    def call(self, *args, **kwargs):
        # TODO: use ThreadPoolExecutor with await/join for concurrency?
        for slot in self.get_slots():
            slot(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        self.call(*args, **kwargs)
