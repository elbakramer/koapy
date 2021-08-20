from koapy.compat.pyside2.QtNetwork import QAbstractSocket
from koapy.utils.logging.Logging import Logging


class QAbstractSocketLoggingMeta(type(Logging), type(QAbstractSocket)):
    pass


class QAbstractSocketLogging(
    QAbstractSocket, Logging, metaclass=QAbstractSocketLoggingMeta
):
    def __init__(self, *args, **kwargs):
        QAbstractSocket.__init__(self, *args, **kwargs)
        Logging.__init__(self)
