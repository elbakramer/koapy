from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusDynamicCallable import (
    KiwoomOpenApiPlusDynamicCallable,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusLoggingEventHandler import (
    KiwoomOpenApiPlusLoggingEventHandler,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin import (
    KiwoomOpenApiPlusQAxWidgetMixin,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignalConnector import (
    KiwoomOpenApiPlusSignalConnector,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignature import (
    KiwoomOpenApiPlusDispatchSignature,
    KiwoomOpenApiPlusEventHandlerSignature,
)
from koapy.compat.pyside2 import PYQT5, PYSIDE2, PythonQtError
from koapy.compat.pyside2.QtAxContainer import QAxWidget
from koapy.compat.pyside2.QtCore import QEvent, Qt
from koapy.compat.pyside2.QtWidgets import QWidget
from koapy.utils.logging.Logging import Logging
from koapy.utils.platform import is_32bit


class QWidgetWithLoggingMeta(type(Logging), type(QWidget)):
    pass


class KiwoomOpenApiPlusQAxWidget(
    QWidget, KiwoomOpenApiPlusQAxWidgetMixin, Logging, metaclass=QWidgetWithLoggingMeta
):

    CLSID = "{A1574A0D-6BFA-4BD7-9020-DED88711818D}"
    PROGID = "KHOPENAPI.KHOpenApiCtrl.1"

    METHOD_NAMES = KiwoomOpenApiPlusDispatchSignature.names()
    EVENT_NAMES = KiwoomOpenApiPlusEventHandlerSignature.names()

    def __init__(self, *args, **kwargs):
        assert is_32bit(), "Contorl object should be created in 32bit environment"

        if PYQT5:
            self.logger.debug("Using PyQt5 as Qt backend")
        elif PYSIDE2:
            self.logger.debug("Using PySide2 as Qt backend")
        else:
            raise PythonQtError("No Qt bindings could be found")

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
        KiwoomOpenApiPlusQAxWidgetMixin.__init__(self)
        Logging.__init__(self)

        self._ax = QAxWidget(clsid_or_progid, self)

        self._methods = {}
        self._signals = {}

        for method_name in self.METHOD_NAMES:
            dynamic_callable = KiwoomOpenApiPlusDynamicCallable(self._ax, method_name)
            self._methods[method_name] = dynamic_callable

        for event_name in self.EVENT_NAMES:
            signal_connector = KiwoomOpenApiPlusSignalConnector(event_name)
            self._signals[event_name] = signal_connector
            signal_connector.connect_to(self._ax)

        self._ax.exception.connect(self._onException)  # pylint: disable=no-member

        self._event_logger = KiwoomOpenApiPlusLoggingEventHandler(self)
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
            "'{}' object has no attribute '{}'".format(self.__class__.__name__, name)
        )

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                event.accept()

    def closeEvent(self, event):
        self.hide()
        event.ignore()
