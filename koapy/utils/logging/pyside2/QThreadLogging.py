from koapy.compat.pyside2.QtCore import QThread
from koapy.utils.logging.Logging import Logging


class QThreadLoggingMeta(type(Logging), type(QThread)):
    pass


class QThreadLogging(QThread, Logging, metaclass=QThreadLoggingMeta):
    def __init__(self, *args, **kwargs):
        QThread.__init__(self, *args, **kwargs)
        Logging.__init__(self)
