from koapy.compat.pyside2.QtWidgets import QWidget
from koapy.utils.logging.Logging import Logging


class QWidgetLoggingMeta(type(Logging), type(QWidget)):
    pass


class QWidgetLogging(QWidget, Logging, metaclass=QWidgetLoggingMeta):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        Logging.__init__(self)
