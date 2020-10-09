from abc import ABC
from abc import abstractmethod

class Observer(ABC):
    """
    """

    @abstractmethod
    def on_next(self, value):
        raise NotImplementedError

    @abstractmethod
    def on_error(self, error):
        raise NotImplementedError

    @abstractmethod
    def on_completed(self):
        raise NotImplementedError

    @classmethod
    def __subclasshook__(cls, c):
        if cls is Observer:
            return all(callable(getattr(c, name, None)) for name in ['on_next', 'on_error', 'on_completed'])
        return NotImplemented

    @classmethod
    def isinstance(cls, instance):
        return isinstance(instance, cls)

    @classmethod
    def from_functions(cls, observer_or_on_next, on_error=None, on_completed=None):
        if cls.isinstance(observer_or_on_next):
            return observer_or_on_next
        elif callable(observer_or_on_next):
            return ObserverFromFunctions(observer_or_on_next, on_error, on_completed)
        else:
            raise TypeError

class ObserverFromFunctions(Observer):

    def __on_error(self, error):
        raise error

    def __on_completed(self):
        return

    def __init__(self, on_next, on_error, on_completed):
        self._on_next = on_next
        self._on_error = on_error or self.__on_error
        self._on_completed = on_completed or self.__on_completed

    def on_next(self, value):
        return self._on_next(value)

    def on_error(self, error):
        return self._on_error(error)

    def on_completed(self):
        return self._on_completed()
