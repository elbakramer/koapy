from abc import ABC
from abc import abstractmethod

from koapy.rx.internal.Observer import Observer
from koapy.rx.internal.Subscription import Subscription

class Observable(ABC):
    """
    """

    @abstractmethod
    def _subscribe(self, observer, should_stop):
        raise NotImplementedError

    @abstractmethod
    def subscribe(self, observer_or_on_next, on_error=None, on_completed=None):
        raise NotImplementedError

    @classmethod
    def from_iterable(cls, iterable):
        return ObservableFromIterable(iterable)

class ObservableFromIterable(Observable):

    def __init__(self, iterable):
        self._iterable = iterable

    def _subscribe(self, observer, should_stop):
        iterator = iter(self._iterable)
        while not should_stop():
            try:
                item = next(iterator)
            except StopIteration:
                observer.on_completed()
                break
            except Exception as e: # pylint: disable=broad-except
                observer.on_error(e)
            else:
                observer.on_next(item)

    def subscribe(self, observer_or_on_next, on_error=None, on_completed=None):
        observer = Observer.from_functions(observer_or_on_next, on_error, on_completed)
        return Subscription(self, observer)
