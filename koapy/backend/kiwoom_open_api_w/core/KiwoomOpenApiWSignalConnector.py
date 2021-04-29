import inspect
import threading

from koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWSignature import (
    KiwoomOpenApiWEventHandlerSignature,
)
from koapy.compat.pyside2 import PYQT5, PYSIDE2, PythonQtError
from koapy.utils.logging.Logging import Logging


class KiwoomOpenApiWSignalConnector(Logging):
    def __init__(self, name=None):
        super().__init__()

        self._name = name
        self._lock = threading.RLock()
        self._slots = list()

        self._signature = KiwoomOpenApiWEventHandlerSignature.from_name(self._name)
        self._param_types = [
            (p.annotation) for p in self._signature.parameters.values()
        ]
        self._signal = self._signature.to_pyside2_event_signal()

    def is_valid_slot(self, slot):
        slot_signature = inspect.signature(slot)
        slot_types = [(p.annotation) for p in slot_signature.parameters.values()]
        condition = len(self._param_types) == len(
            slot_types
        )  # currently only check parameter length
        return condition

    def connect_to(self, control):
        if PYSIDE2:
            return control.connect(self._signal, self)
        elif PYQT5:
            return getattr(control, self._name).connect(self)
        else:
            raise PythonQtError("Unsupported Qt bindings")

    def connect(self, slot):
        if not self.is_valid_slot(slot):
            raise TypeError("Invalid slot: %s" % slot)
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
                self.logger.warning("Tried to disconnect a slot that doesn't exist")

    def call(self, *args, **kwargs):
        # make a copy in order to prevent modification during iteration problem
        with self._lock:
            slots = list(self._slots)
        # TODO: use Thread with await/join for concurrency?
        for slot in slots:
            slot(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.call(*args, **kwargs)
