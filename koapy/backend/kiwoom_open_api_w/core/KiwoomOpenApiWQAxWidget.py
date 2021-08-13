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
from koapy.compat.pyside2 import PYQT5, PYSIDE2, PythonQtError
from koapy.compat.pyside2.QtAxContainer import QAxWidget
from koapy.compat.pyside2.QtCore import QEvent, Qt
from koapy.compat.pyside2.QtWidgets import QWidget
from koapy.utils.logging.pyside2.QWidgetLogging import QWidgetLogging
from koapy.utils.platform import is_32bit


class KiwoomOpenApiWQAxWidget(QWidgetLogging, KiwoomOpenApiWQAxWidgetMixin):

    CLSID = "{D1ACAB7D-A3AF-49E4-9004-C9E98344E17A}"

    METHOD_NAMES = KiwoomOpenApiWDispatchSignature.names()
    EVENT_NAMES = KiwoomOpenApiWEventHandlerSignature.names()

    def __init__(self, *args, **kwargs):
        # Check 32bit requirement
        assert is_32bit(), "Control object should be created in 32bit environment"

        # Check Qt backend
        if PYQT5:
            self.logger.debug("Using PyQt5 as Qt backend")
        elif PYSIDE2:
            self.logger.debug("Using PySide2 as Qt backend")
        else:
            raise PythonQtError("No Qt bindings could be found")

        # Process arguments
        control = None
        parent = None
        window_flags = None

        args = list(args)
        kwargs = dict(kwargs)

        if len(args) > 0 and isinstance(args[0], str):
            control = args.pop(0)
        elif "c" in kwargs:
            control = kwargs.pop("c")

        if len(args) > 0 and (args[0] is None or isinstance(args[0], QWidget)):
            parent = args[0]
        elif "parent" in kwargs:
            parent = kwargs["parent"]

        if len(args) > 1:
            window_flags = args[1]
        elif "f" in kwargs:
            window_flags = kwargs["f"]

        if control is None:
            control = self.CLSID

        # Call super inits
        QWidgetLogging.__init__(self, *args, **kwargs)
        KiwoomOpenApiWQAxWidgetMixin.__init__(self)

        # Create QAxWidget
        self._control = control
        self._ax = QAxWidget(self._control, self)

        # Check if instantiation of the QAxWidget was successful
        successful = not self._ax.isNull()
        if not successful:
            raise RuntimeError(
                "Requested control {} could not be instantiated".format(self._control)
            )

        # Set methods as attributes
        for method_name in self.METHOD_NAMES:
            dynamic_callable = KiwoomOpenApiWDynamicCallable(self._ax, method_name)
            setattr(self, method_name, dynamic_callable)

        # Set signals as attributes
        for event_name in self.EVENT_NAMES:
            signal_connector = KiwoomOpenApiWSignalConnector(event_name)
            signal_connector.connect_to(self._ax)
            setattr(self, event_name, signal_connector)

        # Enable logging for QAxWidget exceptions
        self._ax.exception.connect(self._onException)  # pylint: disable=no-member

        # Enable logging for OpenAPI events
        self._event_logger = KiwoomOpenApiWLoggingEventHandler(self)
        self._event_logger.connect()

    def _onException(
        self, code, source, desc, help
    ):  # pylint: disable=redefined-builtin
        self.logger.error("QAxBaseException(%r, %r, %r, %r)", code, source, desc, help)

    def __getattr__(self, name):
        try:
            return getattr(self._ax, name)
        except AttributeError as e:
            raise AttributeError(
                "'{}' object has no attribute '{}'".format(
                    self.__class__.__name__, name
                )
            ) from e

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                event.accept()

    def closeEvent(self, event):
        self.hide()
        event.ignore()
