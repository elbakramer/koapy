import os
import logging

if os.environ.get('QT_API', 'pyside2') == 'pyside2' and False:
    import PySide2
    if hasattr(PySide2, '__file__') and 'QT_QPA_PLATFORM_PLUGIN_PATH' not in os.environ:
        qt_qpa_platform_plugin_path = os.path.join(os.path.dirname(PySide2.__file__), 'plugins', 'platforms')
        os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qt_qpa_platform_plugin_path
    from PySide2.QtWidgets import QWidget
    from PySide2.QtAxContainer import QAxWidget
    from PySide2.QtCore import QEvent, Qt
else:
    from PyQt5.QtWidgets import QWidget
    from PyQt5.QAxContainer import QAxWidget
    from PyQt5.QtCore import QEvent, Qt

from koapy.pyside2.KiwoomOpenApiDynamicCallable import KiwoomOpenApiDynamicCallable
from koapy.pyside2.KiwoomOpenApiSignalConnector import KiwoomOpenApiSignalConnector
from koapy.pyside2.KiwoomOpenApiControlWrapper import KiwoomOpenApiControlWrapper
from koapy.grpc.event.KiwoomOpenApiEventHandlers import KiwoomOpenApiLoggingEventHandler
from koapy.openapi.KiwoomOpenApiSignature import dispatch_signatures_by_name, event_signatures_by_name

class KiwoomOpenApiQAxWidget(QWidget):

    CLSID = '{A1574A0D-6BFA-4BD7-9020-DED88711818D}'
    PROGID = 'KHOPENAPI.KHOpenApiCtrl.1'

    try:
        import pythoncom
        from pywintypes import com_error as ComError
    except ImportError:
        pass
    else:
        try:
            PROGID = pythoncom.ProgIDFromCLSID(CLSID) or PROGID
        except ComError:
            pass
        finally:
            del pythoncom
            del ComError

    CONTROL_NAME_KWARG_KEY = 'c'

    METHOD_NAMES = list(dispatch_signatures_by_name.keys())
    EVENT_NAMES = list(event_signatures_by_name.keys())

    def __init__(self, *args, **kwargs):
        super_args = args
        super_kwargs = kwargs

        clsid_or_progid = self.CLSID

        if len(args) > 0 and isinstance(args[0], str):
            super_args = args[1:]
            clsid_or_progid = args[0]
        elif self.CONTROL_NAME_KWARG_KEY in kwargs:
            super_kwargs = {k:v for k, v in kwargs if k != self.CONTROL_NAME_KWARG_KEY}
            clsid_or_progid = kwargs[self.CONTROL_NAME_KWARG_KEY]

        super().__init__(*super_args, **super_kwargs)

        self._ax = QAxWidget(clsid_or_progid, self)
        self._ax_wrapped = KiwoomOpenApiControlWrapper(self)

        self._methods = {}
        self._signals = {}

        self._event_logger = KiwoomOpenApiLoggingEventHandler(self)

        for method_name in self.METHOD_NAMES:
            dynamic_callable = KiwoomOpenApiDynamicCallable(self._ax, method_name)
            self._methods[method_name] = dynamic_callable

        for event_name in self.EVENT_NAMES:
            signal_connector = KiwoomOpenApiSignalConnector(event_name)
            if hasattr(self._event_logger, event_name):
                signal_connector.connect(getattr(self._event_logger, event_name))
            self._signals[event_name] = signal_connector
            signal_connector.connect_to(self._ax)

        self._ax.exception.connect(self._onException)

    def _onException(self, code, source, desc, help): # pylint: disable=redefined-builtin
        logging.exception('QAxBaseException(%r, %r, %r, %r)', code, source, desc, help)

    def __getattr__(self, name):
        if name in self._methods:
            return self._methods[name]
        if name in self._signals:
            return self._signals[name]
        try:
            return getattr(self._ax, name)
        except AttributeError:
            pass
        try:
            return self._ax_wrapped.__getattribute__(name)
        except AttributeError:
            pass
        raise AttributeError("'%s' object has not attribute '%s'" % (self.__class__.__name__, name))

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                event.accept()

    def closeEvent(self, event):
        self.hide()
        event.ignore()
