from threading import RLock
from typing import Union

from pywintypes import IID

from koapy.common import Dispatch


class CybosPlusDispatchMeta(type):
    def __new__(cls, name, bases, namespace):
        return super().__new__(cls, name, bases, namespace)

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)

        cls.INSTANCES = {}
        cls.LOCK = RLock()

    def __call__(cls, clsid: Union[IID, str]):
        if isinstance(clsid, str):
            clsid = IID(clsid)
        if clsid not in cls.INSTANCES:
            with cls.LOCK:
                if clsid not in cls.INSTANCES:
                    cls.INSTANCES[clsid] = super().__call__(clsid)
        instance = cls.INSTANCES[clsid]
        return instance


class CybosPlusDispatch(Dispatch, metaclass=CybosPlusDispatchMeta):
    pass
