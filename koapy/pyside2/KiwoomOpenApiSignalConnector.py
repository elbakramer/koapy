import logging
import threading
import inspect

from PySide2.QtCore import SIGNAL
from PySide2.QtAxContainer import QAxWidget

from koapy.openapi.KiwoomOpenApiSignature import get_event_signature_by_name, qt_function_spec_from_signature

class KiwoomOpenApiSignalConnector:

    def __init__(self, name=None):
        self._name = name
        self._lock = threading.RLock()
        self._slots = list()

        self._signature = get_event_signature_by_name(self._name)
        self._param_types = [(p.annotation) for p in self._signature.parameters.values()]
        self._signal = qt_function_spec_from_signature(self._name, self._signature)

    def is_valid_slot(self, slot):
        slot_signature = inspect.signature(slot)
        slot_types = [(p.annotation) for p in slot_signature.parameters.values()]
        condition = len(self._param_types) == len(slot_types)
        return condition

    def connect_to(self, control):
        if isinstance(control, QAxWidget):
            return control.connect(SIGNAL(self._signal), self)
        else:
            return getattr(control, self._name).connect(self)

    def connect(self, slot):
        if not self.is_valid_slot(slot):
            raise TypeError('Invalid slot: %s' % slot)
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
        # TODO: use Thread with await/join for concurrency?
        for slot in self.get_slots():
            slot(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.call(*args, **kwargs)
