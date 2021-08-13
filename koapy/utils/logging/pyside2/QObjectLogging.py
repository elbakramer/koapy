from koapy.compat.pyside2.QtCore import QObject
from koapy.utils.logging.Logging import Logging


class QObjectLoggingMeta(type(Logging), type(QObject)):
    pass


class QObjectLogging(QObject, Logging, metaclass=QObjectLoggingMeta):
    def __init__(self, *args, **kwargs):
        QObject.__init__(self, *args, **kwargs)
        Logging.__init__(self)
