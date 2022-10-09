import warnings

from threading import RLock
from typing import Any, Callable, Generic, List, Optional

try:
    from typing import ParamSpec
except ImportError:
    from typing_extensions import ParamSpec

P = ParamSpec("P")


class EventInstance(Generic[P]):
    def __init__(self):
        self._lock = RLock()
        self._slots: List[Callable[P, Any]] = []

    def connect(self, slot: Callable[P, Any]):
        with self._lock:
            if slot not in self._slots:
                self._slots.append(slot)

    def disconnect(self, slot: Optional[Callable[P, Any]] = None):
        with self._lock:
            if slot is None:
                self._slots.clear()
            elif slot in self._slots:
                self._slots.remove(slot)
            else:
                warnings.warn("Tried to disconnect a slot that doesn't exist")

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> None:
        with self._lock:
            slots = list(self._slots)
        for slot in slots:
            slot(*args, **kwargs)
