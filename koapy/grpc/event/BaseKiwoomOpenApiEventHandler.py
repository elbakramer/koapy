from abc import ABC
from contextlib import ExitStack
from threading import RLock

from koapy.grpc.event.KiwoomOpenApiEventHandlerFunctions import KiwoomOpenApiEventHandlerFunctions
from koapy.grpc.observer.QueueBasedIterableObserver import QueueBasedIterableObserver

from koapy.utils.notimplemented import isimplemented

class BaseKiwoomOpenApiEventHandler(KiwoomOpenApiEventHandlerFunctions, ABC):
    """
    """

    def __init__(self, control):
        self._control = control
        self._observer = QueueBasedIterableObserver()
        self._enter_count = 0
        self._stack = ExitStack()
        self._lock = RLock()

    @property
    def control(self):
        return self._control

    @property
    def observer(self):
        return self._observer

    def on_next(self, value):
        self.observer.on_next(value)

    def on_error(self, error):
        self.observer.on_error(error)

    def on_completed(self):
        self.observer.on_completed()

    def __getattr__(self, name):
        return getattr(self.control, name)

    @classmethod
    def names(cls):
        names = [name for name in dir(KiwoomOpenApiEventHandlerFunctions) if name.startswith('On')]
        return names

    def slots(self):
        names = self.names()
        slots = [getattr(self, name) for name in names]
        names_and_slots_implemented = [(name, slot) for name, slot in zip(names, slots) if isimplemented(slot)]
        return names_and_slots_implemented

    def connect(self):
        for name, slot in self.slots():
            getattr(self.control, name).connect(slot)

    def disconnect(self):
        for name, slot in self.slots():
            getattr(self.control, name).disconnect(slot)

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def add_callback(self, callback, *args, **kwargs):
        self._stack.callback(callback, *args, **kwargs)

    def __enter__(self):
        with self._lock:
            if self._enter_count == 0:
                self.connect()
                self.on_enter()
            self._enter_count += 1
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        with self._lock:
            if self._enter_count > 0:
                self._enter_count -= 1
            if self._enter_count == 0:
                self.disconnect()
                self.on_exit()
                self._stack.__exit__(exc_type, exc_value, traceback)

    def __iter__(self):
        with self:
            return iter(self.observer)
