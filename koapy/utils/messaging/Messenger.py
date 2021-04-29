from abc import ABC, abstractmethod


class Messenger(ABC):
    """ """

    @abstractmethod
    def send_message(self, content):
        raise NotImplementedError
