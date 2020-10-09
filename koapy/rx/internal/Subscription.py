import threading

from abc import ABC
from abc import abstractmethod

class Disposable(ABC):
    """
    """

    @abstractmethod
    def dispose(self):
        raise NotImplementedError

class Subscription(threading.Thread, Disposable):

    def __init__(self, observable, observer):
        self._observable = observable
        self._observer = observer
        self._should_stop = False

        super().__init__(
            target=self._observable._subscribe,
            args=[
                self._observer,
                self.__should_stop,
            ], daemon=True)

        self.start()

    def __should_stop(self):
        return self._should_stop

    def unsubscribe(self):
        self._should_stop = True

    def dispose(self):
        return self.unsubscribe()
