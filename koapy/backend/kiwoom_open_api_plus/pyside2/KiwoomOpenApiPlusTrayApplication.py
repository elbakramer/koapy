import argparse
import contextlib
import datetime
import signal
import sys

from typing import Optional

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError import (
    KiwoomOpenApiPlusNegativeReturnCodeError,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidget import (
    KiwoomOpenApiPlusQAxWidget,
)
from koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceServer import (
    KiwoomOpenApiPlusServiceServer,
)
from koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusDialogHandler import (
    KiwoomOpenApiPlusDialogHandler,
)
from koapy.backend.kiwoom_open_api_plus.utils.pyside2.QSignalHandler import (
    QSignalHandler,
)
from koapy.backend.kiwoom_open_api_plus.utils.pyside2.QThreadPoolExecutor import (
    QThreadPoolExecutor,
)
from koapy.compat.pyside2.QtCore import QThreadPool, QTimer, QUrl, Signal
from koapy.compat.pyside2.QtGui import QDesktopServices
from koapy.compat.pyside2.QtWidgets import QApplication, QMenu, QStyle, QSystemTrayIcon
from koapy.utils.logging import set_verbosity
from koapy.utils.logging.pyside2.QObjectLogging import QObjectLogging


class KiwoomOpenApiPlusTrayApplication(QObjectLogging):

    shouldRestart = Signal(int)

    def __init__(self, args=()):
        self._parser = argparse.ArgumentParser()
        self._parser.add_argument("-p", "--port")
        self._parser.add_argument("-v", "--verbose", action="count", default=0)
        self._parser.add_argument("-c", "--ensure-connected", action="store_true")
        self._parsed_args, self._remaining_args = self._parser.parse_known_args(args)

        self._port = self._parsed_args.port
        self._verbose = self._parsed_args.verbose
        self._ensure_connected = self._parsed_args.ensure_connected

        set_verbosity(self._verbose)

        self._app = QApplication.instance()

        if not self._app:
            self._app = QApplication(self._remaining_args)

        super().__init__()

        self._thread_pool = QThreadPool(self)
        self._thread_pool_executor = QThreadPoolExecutor(self._thread_pool, self)

        self._control: Optional[KiwoomOpenApiPlusQAxWidget] = None
        self._server: Optional[KiwoomOpenApiPlusServiceServer] = None
        self._initializeGrpcServer()

        self.shouldRestart.connect(self._onShouldRestart)
        self._startRestartNotifier()

        self._signal_handler = QSignalHandler(self)
        self._dialog_handler = KiwoomOpenApiPlusDialogHandler(self)

        self._tray = QSystemTrayIcon()
        self._tray.activated.connect(self._activate)  # pylint: disable=no-member

        icon = self._app.style().standardIcon(QStyle.SP_TitleBarMenuButton)

        menu = QMenu()
        menu.addSection("Connection")
        connectAction = menu.addAction("Login and Connect")
        connectAction.triggered.connect(self._ensureConnectedAndThen)
        showAccountWindowAction = menu.addAction("Show Account Window")
        showAccountWindowAction.triggered.connect(self._showAccountWindow)
        menu.addSection("Status")
        self._connectionStatusAction = menu.addAction("Status: Disconnected")
        self._connectionStatusAction.setEnabled(False)
        self._serverStatusAction = menu.addAction("Server: Unknown")
        self._serverStatusAction.setEnabled(False)
        menu.addSection("Links")
        documentationAction = menu.addAction("Documentation")
        documentationAction.triggered.connect(self._openReadTheDocs)
        githubAction = menu.addAction("Github")
        githubAction.triggered.connect(self._openGithub)
        menu.addSection("Kiwoom Links")
        openApiAction = menu.addAction("Kiwoom OpenAPI+ Home")
        openApiAction.triggered.connect(self._openOpenApiHome)
        openApiAction = menu.addAction("Kiwoom OpenAPI+ Document")
        openApiAction.triggered.connect(self._openOpenApiDocument)
        qnaAction = menu.addAction("Kiwoom OpenAPI+ Qna")
        qnaAction.triggered.connect(self._openOpenApiQna)
        menu.addSection("Exit")
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(self._exit)

        tooltip = "KOAPY Tray Application"

        self._tray.setIcon(icon)
        self._tray.setContextMenu(menu)
        self._tray.setToolTip(tooltip)

        self._tray.show()

    def _initializeGrpcServer(self):
        self._control = KiwoomOpenApiPlusQAxWidget()
        self._server = KiwoomOpenApiPlusServiceServer(
            self._control,
            port=self._port,
            thread_pool=self._thread_pool_executor,
        )
        self._control.OnEventConnect.connect(self._onEventConnect)

    def _startServer(self, ensure_connected=None):
        if ensure_connected is None:
            ensure_connected = self._ensure_connected
        self._server.start()
        if ensure_connected:
            self._ensureConnectedAndThen()

    def _stopServer(self):
        self._server.stop()
        self._server.wait_for_termination()

    def _deleteControl(self):
        self._control.setParent(None)
        self._control.deleteLater()

    def _stopAndTearDownGrpcServer(self):
        if self._server is not None:
            self._stopServer()
            self._server = None
        if self._control is not None:
            self._deleteControl()
            self._control = None

    def _reinitializeGrpcServer(self):
        self._stopAndTearDownGrpcServer()
        self._initializeGrpcServer()

    def _reinitializeAndStartGrpcServer(self, ensure_connected=None):
        self._reinitializeGrpcServer()
        self._startServer(ensure_connected)

    def _checkAndWaitForMaintananceAndThen(self, callback=None):

        """
        TITLE: 안녕하세요. 키움증권 입니다.
        TIME: 04:45
        BODY:
        안녕하세요. 키움증권 입니다.
        시스템의 안정적인 운영을 위하여
        매일 시스템 점검을 하고 있습니다.
        점검시간은 월~토요일 (05:05 ~ 05:10)
                  일요일    (04:00 ~ 04:30) 까지 입니다.
        따라서 해당 시간대에는 접속단절이 될 수 있습니다.
        참고하시기 바랍니다.
        """

        """
        TITLE: KHOpenAPI
        TIME: 05:05
        BODY:
        통신 연결이 끊겼습니다. 프로그램 종료후 재접속 해주시기 바랍니다.
        """

        now = datetime.datetime.now()

        if now.weekday() < 6:
            maintanance_start_time = now.replace(
                hour=5, minute=5, second=0, microsecond=0
            )
            maintanance_end_time = now.replace(
                hour=5, minute=10, second=0, microsecond=0
            )
        else:
            maintanance_start_time = now.replace(
                hour=4, minute=0, second=0, microsecond=0
            )
            maintanance_end_time = now.replace(
                hour=4, minute=30, second=0, microsecond=0
            )

        if maintanance_start_time < now < maintanance_end_time:
            target = maintanance_end_time + datetime.timedelta(minutes=5)
            self.logger.warning(
                "Connection lost due to maintanance, waiting until %s (then will try to reconnect)",
                target,
            )
            timediff = target - now
            if callable(callback):
                QTimer.singleShot(timediff.total_seconds() * 1000, callback)

    def _onEventConnect(self, errcode):
        if errcode == 0:
            self.logger.debug("Connected to server")
            state = self._control.GetConnectState()
            if state == 1:
                self._connectionStatusAction.setText("Status: Connected")
                server = self._control.GetLoginInfo("GetServerGubun")
                if server == "1":
                    self._serverStatusAction.setText("Server: Simulation")
                else:
                    self._serverStatusAction.setText("Server: Real")
            else:
                raise RuntimeError("Unexpected case")
        elif errcode == KiwoomOpenApiPlusNegativeReturnCodeError.OP_ERR_SOCKET_CLOSED:
            self.logger.error("Socket closed")
            state = self._control.GetConnectState()
            if state == 0:
                self._connectionStatusAction.setText("Status: Disconnected")

            def callback():
                self.logger.warning("Trying to reconnect")
                # TODO: 기존 구현에서 프로그램 전체 재시작 없이 이미 생성된 control/server 객체로 다시 접속을 시도하는 경우 접속이 실패함
                self.shouldRestart.emit(1)

            self._checkAndWaitForMaintananceAndThen(callback)
        elif errcode == KiwoomOpenApiPlusNegativeReturnCodeError.OP_ERR_CONNECT:
            self.logger.error("Failed to connect")
            state = self._control.GetConnectState()
            if state == 0:
                self._connectionStatusAction.setText("Status: Disconnected")

    def _activate(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self._control.showNormal()
            self._control.activateWindow()

    def _ensureConnectedAndThen(self, callback=None):
        self._control.EnsureConnectedAndThen(callback)

    def _showAccountWindow(self):
        self._ensureConnectedAndThen(self._control.ShowAccountWindow)

    def _openOpenApiHome(self):
        openApiHomeUrl = "https://www.kiwoom.com/h/customer/download/VOpenApiInfoView"
        url = QUrl(openApiHomeUrl)
        QDesktopServices.openUrl(url)

    def _openOpenApiDocument(self):
        openApiHomeUrl = "https://download.kiwoom.com/web/openapi/kiwoom_openapi_plus_devguide_ver_1.5.pdf"
        url = QUrl(openApiHomeUrl)
        QDesktopServices.openUrl(url)

    def _openOpenApiQna(self):
        openApiQnaUrl = "https://www.kiwoom.com/h/common/bbs/VBbsBoardBWOAZView"
        url = QUrl(openApiQnaUrl)
        QDesktopServices.openUrl(url)

    def _openGithub(self):
        githubUrl = "https://github.com/elbakramer/koapy"
        url = QUrl(githubUrl)
        QDesktopServices.openUrl(url)

    def _openReadTheDocs(self):
        docUrl = "https://koapy.readthedocs.io/en/latest/"
        url = QUrl(docUrl)
        QDesktopServices.openUrl(url)

    def _onSignal(self, signum, _frame):
        if signum == signal.SIGTERM:
            self.logger.warning("Received SIGTERM")
        if signum == signal.SIGINT:
            self.logger.warning("Received SIGINT")
        self._exit(signum)

    def _setSignalHandlers(self):
        for signal_ in [signal.SIGINT, signal.SIGTERM]:
            self._signal_handler.setHandler(signal_, self._onSignal)

    def _restoreSignalHandlers(self):
        for signal_ in [signal.SIGINT, signal.SIGTERM]:
            self._signal_handler.restoreHandler(signal_)

    @contextlib.contextmanager
    def _signalHandlersSet(self):
        with contextlib.ExitStack() as stack:
            self._setSignalHandlers()
            stack.callback(self._restoreSignalHandlers)
            yield

    @contextlib.contextmanager
    def _serverStarted(self):
        with contextlib.ExitStack() as stack:
            self._startServer()
            stack.callback(self._stopServer)
            yield

    def _exec(self):
        self.logger.debug("Starting app")
        with self._signalHandlersSet():
            self._server.start()
            return self._app.exec_()

    def _exit(self, return_code=0):
        self.logger.debug("Exiting app")

        self._app.exit(return_code)

    def _nextRestartTime(self):
        """
        TITLE: [HTS 재접속 안내]
        TIME: 06:50
        BODY:
        안녕하세요. 키움증권입니다.

        오전 6시 50분 이전에 접속하신 고객님께서는
        영웅문을 재접속하여 주시기 바랍니다.
        재접속을 하지 않을 경우 거래종목 정보, 전일 거래에
        대한 결제분 등이 반영되지 않아 실제 잔고와 차이가
        발생할 수 있습니다.
                               -키움증권-
        """
        # TODO: 팝업창을 닫아주지 않을 경우 행이 걸리는 것으로 보임
        now = datetime.datetime.now()
        target = now.replace(hour=6, minute=50, second=0, microsecond=0)
        if now >= target:
            target += datetime.timedelta(days=1)
        return target

    def _startRestartNotifier(self):
        def notify_and_wait_for_next():
            self.shouldRestart.emit(0)
            now = datetime.datetime.now()
            next_restart_time = self._nextRestartTime()
            timediff = next_restart_time - now
            QTimer.singleShot(
                (timediff.total_seconds() + 1) * 1000, notify_and_wait_for_next
            )

        now = datetime.datetime.now()
        next_restart_time = self._nextRestartTime()
        timediff = next_restart_time - now
        QTimer.singleShot(
            (timediff.total_seconds() + 1) * 1000, notify_and_wait_for_next
        )

    def _onShouldRestart(self, code):
        ensure_connected = None
        if code > 0:
            ensure_connected = True
        elif code < 0:
            ensure_connected = False
        self._reinitializeAndStartGrpcServer(ensure_connected)

    def __getattr__(self, name):
        return getattr(self._app, name)

    @property
    def control(self):
        return self._control

    def exec_(self):
        return self._exec()

    def exit(self, return_code=0):
        return self._exit(return_code)

    def execAndExit(self):
        code = self._exec()
        sys.exit(code)

    @classmethod
    def main(cls, args):
        app = cls(args)
        app.execAndExit()
