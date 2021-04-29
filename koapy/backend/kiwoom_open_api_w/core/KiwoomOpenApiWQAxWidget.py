import platform

from koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWDynamicCallable import (
    KiwoomOpenApiWDynamicCallable,
)
from koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWLoggingEventHandler import (
    KiwoomOpenApiWLoggingEventHandler,
)
from koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWQAxWidgetMixin import (
    KiwoomOpenApiWQAxWidgetMixin,
)
from koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWSignalConnector import (
    KiwoomOpenApiWSignalConnector,
)
from koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWSignature import (
    KiwoomOpenApiWDispatchSignature,
    KiwoomOpenApiWEventHandlerSignature,
)
from koapy.compat.pyside2.QtAxContainer import QAxWidget
from koapy.compat.pyside2.QtCore import QEvent, Qt
from koapy.compat.pyside2.QtWidgets import QWidget
from koapy.utils.logging.Logging import Logging


class QWidgetWithLoggingMeta(type(Logging), type(QWidget)):
    pass


class KiwoomOpenApiWQAxWidget(
    QWidget, KiwoomOpenApiWQAxWidgetMixin, Logging, metaclass=QWidgetWithLoggingMeta
):

    CLSID = "{D1ACAB7D-A3AF-49E4-9004-C9E98344E17A}"

    METHOD_NAMES = KiwoomOpenApiWDispatchSignature.names()
    EVENT_NAMES = KiwoomOpenApiWEventHandlerSignature.names()

    def __init__(self, *args, **kwargs):
        assert (
            platform.architecture()[0] == "32bit"
        ), "Contorl object should be created in 32bit environment"

        super_args = args
        super_kwargs = kwargs

        clsid_or_progid = self.CLSID

        if len(args) > 0 and isinstance(args[0], str):
            super_args = args[1:]
            clsid_or_progid = args[0]
        elif "c" in kwargs:
            super_kwargs = {k: v for k, v in kwargs if k != "c"}
            clsid_or_progid = kwargs["c"]

        QWidget.__init__(self, *super_args, **super_kwargs)
        KiwoomOpenApiWQAxWidgetMixin.__init__(self)
        Logging.__init__(self)

        self._ax = QAxWidget(clsid_or_progid, self)

        self._methods = {}
        self._signals = {}

        for method_name in self.METHOD_NAMES:
            dynamic_callable = KiwoomOpenApiWDynamicCallable(self._ax, method_name)
            self._methods[method_name] = dynamic_callable

        for event_name in self.EVENT_NAMES:
            signal_connector = KiwoomOpenApiWSignalConnector(event_name)
            self._signals[event_name] = signal_connector
            signal_connector.connect_to(self._ax)

        self._ax.exception.connect(self._onException)  # pylint: disable=no-member

        self._event_logger = KiwoomOpenApiWLoggingEventHandler(self)
        self._event_logger.connect()

    def _onException(
        self, code, source, desc, help
    ):  # pylint: disable=redefined-builtin
        self.logger.exception(
            "QAxBaseException(%r, %r, %r, %r)", code, source, desc, help
        )

    def __getattr__(self, name):
        if name in self._methods:
            return self._methods[name]
        if name in self._signals:
            return self._signals[name]
        try:
            return getattr(self._ax, name)
        except AttributeError:
            pass
        raise AttributeError(
            "'%s' object has not attribute '%s'" % (self.__class__.__name__, name)
        )

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                event.accept()

    def closeEvent(self, event):
        self.hide()
        event.ignore()
