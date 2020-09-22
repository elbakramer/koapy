import logging

from PyQt5.QtWidgets import QWidget
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEvent, Qt

from koapy.pyqt5.KiwoomOpenApiDynamicCallable import KiwoomOpenApiDynamicCallable
from koapy.pyqt5.KiwoomOpenApiSignalConnector import KiwoomOpenApiSignalConnector
from koapy.utils.rate_limiting.RateLimiter import SimpleRateLimiter
from koapy.openapi.KiwoomOpenApiError import KiwoomOpenApiError
from koapy.grpc.event.KiwoomOpenApiEventHandler import KiwoomOpenApiLoggingEventHandler
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
        logging.error('(%s, %s, %s, %s)', code, source, desc, help)

    def __getattr__(self, name):
        result = getattr(self._ax, name)

        if type(result).__name__ == 'pyqtMethodProxy':
            return KiwoomOpenApiDynamicCallable(self._ax, name)
        elif name.startswith('On') and name in self._signals:
            return self._signals[name]
        else:
            return result

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                event.accept()

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    @SimpleRateLimiter(period=4, calls=1) # 그냥 1초당 5회로하면 장기적으로 결국 막히기 때문에 4초당 1회로 제한 (3초당 1회부턴 제한걸림)
    def RateLimitedCommRqData(self, rqname, trcode, prevnext, scrnno, inputs=None):
        """
        [OpenAPI 게시판]
          https://bbn.kiwoom.com/bbn.openAPIQnaBbsList.do

        [조회횟수 제한 관련 가이드]
          - 1초당 5회 조회를 1번 발생시킨 경우 : 17초대기
          - 1초당 5회 조회를 5연속 발생시킨 경우 : 90초대기
          - 1초당 5회 조회를 10연속 발생시킨 경우 : 3분(180초)대기
        """
        prevnext = int(prevnext) # ensure prevnext is int
        code = self.CommRqData(rqname, trcode, prevnext, scrnno)
        spec = 'CommRqData(%r, %r, %r, %r)' % (rqname, trcode, prevnext, scrnno)

        if inputs is not None:
            spec += ' with inputs %r' % inputs

        if code == KiwoomOpenApiError.OP_ERR_NONE:
            message = 'CommRqData() was successful; ' + spec
            logging.debug(message)
        elif code == KiwoomOpenApiError.OP_ERR_SISE_OVERFLOW:
            message = 'CommRqData() was rejected due to massive request; ' + spec
            logging.error(message)
            raise KiwoomOpenApiError(code)
        elif code == KiwoomOpenApiError.OP_ERR_ORD_WRONG_INPUT:
            message = 'CommRqData() failed due to wrong input, check if input was correctly set; ' + spec
            logging.error(message)
            raise KiwoomOpenApiError(code)
        elif code in (KiwoomOpenApiError.OP_ERR_RQ_STRUCT_FAIL, KiwoomOpenApiError.OP_ERR_RQ_STRING_FAIL):
            message = 'CommRqData() request was invalid; ' + spec
            logging.error(message)
            raise KiwoomOpenApiError(code)
        else:
            message = 'Unknown error occured during CommRqData() request; ' + spec
            korean_message = KiwoomOpenApiError.get_error_message_by_code(code)
            if korean_message is not None:
                message += '; Korean error message: ' +  korean_message
            logging.error(message)
            raise KiwoomOpenApiError(code)

        return code
