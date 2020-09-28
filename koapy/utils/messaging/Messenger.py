from abc import ABC
from abc import abstractmethod

class Messenger(ABC):
    """
    """

    @abstractmethod
    def send_message(self, content):
        raise NotImplementedError
