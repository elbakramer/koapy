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
