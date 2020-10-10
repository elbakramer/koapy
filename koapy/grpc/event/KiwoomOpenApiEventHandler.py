from contextlib import ExitStack
from threading import RLock

from koapy.grpc.event.KiwoomOpenApiEventHandlerFunctions import KiwoomOpenApiEventHandlerFunctions
from koapy.grpc.utils.QueueBasedIterableObserver import QueueBasedIterableObserver

from koapy.utils.notimplemented import isimplemented

class KiwoomOpenApiEventHandler(KiwoomOpenApiEventHandlerFunctions):

    def __init__(self, control):
        self._control = control
        self._observer = QueueBasedIterableObserver()
        self._enter_count = 0
        self._should_exit = False
        self._stack = ExitStack()
        self._lock = RLock()

    @property
    def control(self):
        return self._control

    @property
    def observer(self):
        return self._observer

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

    def on_exit(self, exc_type=None, exc_value=None, traceback=None):
        pass

    def add_callback(self, callback, *args, **kwargs):
        self._stack.callback(callback, *args, **kwargs)

    def enter(self):
        with self._lock:
            self.connect()
            self.on_enter()
            self._should_exit = True

    def exit(self, exc_type=None, exc_value=None, traceback=None):
        with self._lock:
            if self._should_exit:
                self.disconnect()
                self.on_exit(exc_type, exc_value, traceback)
                self._stack.__exit__(exc_type, exc_value, traceback)
                self._should_exit = False

    def stop(self):
        return self.observer.stop()

    def close(self):
        self.exit()
        self.stop()

    def __enter__(self):
        with self._lock:
            if self._enter_count == 0:
                self.enter()
            self._enter_count += 1
            return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            return self.exit(exc_type, exc_value, traceback)
        with self._lock:
            if self._enter_count > 0:
                self._enter_count -= 1
            if self._enter_count == 0:
                return self.exit(exc_type, exc_value, traceback)
        return

    def __iter__(self):
        with self:
            return iter(self.observer)

class KiwoomOpenApiEventHandlerForGrpc(KiwoomOpenApiEventHandler):

    def __init__(self, control, context):
        super().__init__(control)

        self._context = context
        self._context.add_callback(self.stop)

    @property
    def context(self):
        return self._context
