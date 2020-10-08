import logging

from PyQt5.QtWidgets import QWidget
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEvent, Qt

from koapy.pyqt5.KiwoomOpenApiDynamicCallable import KiwoomOpenApiDynamicCallable
from koapy.pyqt5.KiwoomOpenApiSignalConnector import KiwoomOpenApiSignalConnector
from koapy.pyqt5.KiwoomOpenApiControlWrapper import KiwoomOpenApiControlWrapper
from koapy.grpc.event.KiwoomOpenApiEventHandlers import KiwoomOpenApiLoggingEventHandler
from koapy.grpc.event.KiwoomOpenApiEventHandlerFunctions import KiwoomOpenApiEventHandlerFunctions

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
        self._signals = {}
        self._event_logger = KiwoomOpenApiLoggingEventHandler(self)

        for event_name in [name for name in dir(KiwoomOpenApiEventHandlerFunctions) if name.startswith('On')]:
            # 아래처럼 중간의 프록시 객체 (KiwoomOpenApiSignalConnector) 를 넣지
            # 않으면 외부에서 동적으로 connect 를 할 수가 없어보임 (하더라도
            # 제대로 이벤트를 받지 못함)
            connector = KiwoomOpenApiSignalConnector()
            connector.connect(getattr(self._event_logger, event_name))
            getattr(self._ax, event_name).connect(connector)
            self._signals[event_name] = connector
            # 아래는 기존에 시도해서 실패한 구현 (제대로 이벤트를 받지 못함)
            """
            connector = getattr(self._ax, event_name)
            connector.connect(getattr(self._event_logger, event_name))
            self._signals[event_name] = connector
            """

        self._ax.exception.connect(self._onException)

    def _onException(self, code, source, desc, help):
        logging.exception('QAxBaseException(%r, %r, %r, %r)', code, source, desc, help)

    def __getattr__(self, name):
        try:
            result = getattr(self._ax, name)
        except AttributeError:
            result = self._ax_wrapped.__getattribute__(name)
        else:
            if type(result).__name__ == 'pyqtMethodProxy':
                result = KiwoomOpenApiDynamicCallable(self._ax, name)
            elif name.startswith('On') and name in self._signals:
                result = self._signals[name]
        return result

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                event.accept()

    def closeEvent(self, event):
        self.hide()
        event.ignore()
