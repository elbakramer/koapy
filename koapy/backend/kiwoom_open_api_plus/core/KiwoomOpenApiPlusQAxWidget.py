from typing import Optional, overload

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusDispatchSignature import (
    KiwoomOpenApiPlusDispatchSignature,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusDynamicCallable import (
    KiwoomOpenApiPlusDynamicCallable,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEventHandlerSignature import (
    KiwoomOpenApiPlusEventHandlerSignature,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusLoggingEventHandler import (
    KiwoomOpenApiPlusLoggingEventHandler,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin import (
    KiwoomOpenApiPlusQAxWidgetServerSideMixin,
    KiwoomOpenApiPlusQAxWidgetUniversalMixin,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignalConnector import (
    KiwoomOpenApiPlusSignalConnector,
)
from koapy.backend.kiwoom_open_api_plus.utils.pyside2.QSlotLikeExecutor import (
    QSlotLikeExecutor,
)
from koapy.compat.pyside2.QtAxContainer import QAxWidget
from koapy.compat.pyside2.QtCore import QEvent, Qt
from koapy.compat.pyside2.QtWidgets import QWidget
from koapy.utils.logging.pyside2.QWidgetLogging import QWidgetLogging
from koapy.utils.platform import is_32bit


class KiwoomOpenApiPlusQAxWidget(
    QWidgetLogging,
    KiwoomOpenApiPlusQAxWidgetUniversalMixin,
    KiwoomOpenApiPlusQAxWidgetServerSideMixin,
):

    CLSID = "{A1574A0D-6BFA-4BD7-9020-DED88711818D}"
    PROGID = "KHOPENAPI.KHOpenApiCtrl.1"

    METHOD_NAMES = KiwoomOpenApiPlusDispatchSignature.names()
    EVENT_NAMES = KiwoomOpenApiPlusEventHandlerSignature.names()

    @overload
    def __init__(
        self,
        c: Optional[str] = None,
        parent: Optional[QWidget] = None,
        f: Qt.WindowFlags = Qt.WindowFlags(),
    ):
        ...

    @overload
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        f: Qt.WindowFlags = Qt.WindowFlags(),
    ):
        ...

    def __init__(self, *args, **kwargs):
        # Check 32bit requirement
        assert is_32bit(), "Control object should be created in 32bit environment"

        # Process arguments
        control: Optional[str] = None
        parent: Optional[QWidget] = None  # pylint: disable=unused-variable
        window_flags: Optional[Qt.WindowFlags] = None  # pylint: disable=unused-variable

        # Copy args before modification
        args = list(args)
        kwargs = dict(kwargs)

        # Pop control argument for QWidget init
        if len(args) > 0 and isinstance(args[0], str):
            control = args.pop(0)
        elif "c" in kwargs:
            control = kwargs.pop("c")

        # Preserve others
        if len(args) > 0 and (args[0] is None or isinstance(args[0], QWidget)):
            parent = args[0]
        elif "parent" in kwargs:
            parent = kwargs["parent"]

        if len(args) > 1:
            window_flags = args[1]
        elif "f" in kwargs:
            window_flags = kwargs["f"]

        # Use default control if not set
        if control is None:
            control = self.CLSID

        # Call super init
        QWidgetLogging.__init__(self, *args, **kwargs)

        # Create QAxWidget
        self._control = control
        self._ax = QAxWidget(self._control, self)

        # Check if instantiation of the QAxWidget was successful
        successful = not self._ax.isNull()
        if not successful:
            raise RuntimeError(
                "Requested control {} could not be instantiated".format(self._control)
            )

        # Initialize slot-like executor (for ensuring thread safety)
        self._slot_like_executor = QSlotLikeExecutor(self)

        # Set methods as attributes
        for method_name in self.METHOD_NAMES:
            dynamic_callable = KiwoomOpenApiPlusDynamicCallable(self._ax, method_name)
            dynamic_callable = self._slot_like_executor.wrapCallable(dynamic_callable)
            setattr(self, method_name, dynamic_callable)

        # Set signals as attributes
        for event_name in self.EVENT_NAMES:
            signal_connector = KiwoomOpenApiPlusSignalConnector(event_name)
            signal_connector.connect_to(self._ax)
            setattr(self, event_name, signal_connector)

        # Call mixin init here, after method attributes are set
        KiwoomOpenApiPlusQAxWidgetUniversalMixin.__init__(self)

        # Wrap additional mixin functions
        self.CommRqDataWithInputs = self._slot_like_executor.wrapCallable(
            self.CommRqDataWithInputs
        )

        # Call mixin init here, after method attributes are set
        KiwoomOpenApiPlusQAxWidgetServerSideMixin.__init__(self)

        # Enable logging for QAxWidget exceptions
        self._ax.exception.connect(self._onException)  # pylint: disable=no-member

        # Enable logging for OpenAPI events
        self._event_logger = KiwoomOpenApiPlusLoggingEventHandler(self)
        self._event_logger.connect()

        # Other misc flags
        self.hideOnMinimize = True
        self.hideOnClose = True

    def _onException(
        self, code, source, desc, help
    ):  # pylint: disable=redefined-builtin
        self.logger.error("QAxBaseException(%r, %r, %r, %r)", code, source, desc, help)

    def __getattr__(self, name):
        try:
            # Fallback to AxObject for attrs such as 'self.dynamicCall(...)'
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
                if self.hideOnMinimize:
                    self.hide()
                    return event.ignore()
        return event.accept()

    def closeEvent(self, event):
        if self.hideOnClose:
            self.hide()
            return event.ignore()
        return event.accept()
