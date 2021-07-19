import argparse
import contextlib
import datetime
import signal
import sys

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError import (
    KiwoomOpenApiPlusNegativeReturnCodeError,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidget import (
    KiwoomOpenApiPlusQAxWidget,
)
from koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceServer import (
    KiwoomOpenApiPlusServiceServer,
)
from koapy.backend.kiwoom_open_api_plus.utils.pyside2.QSignalHandler import (
    QSignalHandler,
)
from koapy.compat.pyside2.QtCore import QObject, QTimer, QUrl, Signal
from koapy.compat.pyside2.QtGui import QDesktopServices
from koapy.compat.pyside2.QtWidgets import QApplication, QMenu, QStyle, QSystemTrayIcon
from koapy.utils.logging.Logging import Logging


class QObjectWithLoggingMeta(type(Logging), type(QObject)):
    pass


class KiwoomOpenApiPlusTrayApplication(
    QObject, Logging, metaclass=QObjectWithLoggingMeta
):

    _should_restart = Signal(int)
    _should_restart_exit_code = 1

    def __init__(self, args=()):
        super().__init__()

        self._parser = argparse.ArgumentParser()
        self._parser.add_argument("-p", "--port")
        self._parser.add_argument("--verbose", "-v", action="count", default=0)
        self._parsed_args, remaining_args = self._parser.parse_known_args(args)

        self._port = self._parsed_args.port
        self._verbose = self._parsed_args.verbose

        self._app = QApplication.instance()
        if not self._app:
            self._app = QApplication(remaining_args)
        self._control = KiwoomOpenApiPlusQAxWidget()
        self._server = KiwoomOpenApiPlusServiceServer(self._control)

        self._should_restart.connect(self._exit)
        self._startRestartNotifier()

        self._signal_handler = QSignalHandler(self._app)

        self._tray = QSystemTrayIcon()
        self._tray.activated.connect(self._activate)  # pylint: disable=no-member

        icon = self._app.style().standardIcon(QStyle.SP_TitleBarMenuButton)

        menu = QMenu()
        menu.addSection("Connection")
        connectAction = menu.addAction("Login and Connect")
        connectAction.triggered.connect(self._connect)
        autoLoginAction = menu.addAction("Congifure Auto Login")
        autoLoginAction.triggered.connect(self._configureAutoLogin)
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

        self._control.OnEventConnect.connect(self._onEventConnect)

    def _checkAndWaitForMaintananceAndThen(self, callback=None, args=None, kwargs=None):

        """
        # 시스템 점검 안내

        안녕하세요. 키움증권 입니다.
        시스템의 안정적인 운영을 위하여
        매일 시스템 점검을 하고 있습니다.
        점검시간은 월~토요일 (05:05 ~ 05:10)
                  일요일    (04:00 ~ 04:30) 까지 입니다.
        따라서 해당 시간대에는 접속단절이 될 수 있습니다.
        참고하시기 바랍니다.
        """

        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}

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
            if callback is not None and callable(callback):
                QTimer.singleShot(
                    timediff.total_seconds() * 1000, lambda: callback(*args, **kwargs)
                )

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
                self._ensureConnectedAndThen()  # 재연결 시도

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

    def _ensureConnectedAndThen(self, callback=None, args=None, kwargs=None):
        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}
        if self._control.GetConnectState() == 1:
            if callback is not None:
                if not callable(callback):
                    raise TypeError("Function is not callable")
                callback(*args, **kwargs)
        else:
            if callback is not None:
                if not callable(callback):
                    raise TypeError("Function is not callable")

                def callbackAndDisconnect(errcode):
                    self._control.OnEventConnect.disconnect(callbackAndDisconnect)
                    if errcode == 0:
                        callback(*args, **kwargs)

                self._control.OnEventConnect.connect(callbackAndDisconnect)
            self._control.CommConnect()

    def _connect(self):
        self._ensureConnectedAndThen()

    def _showAccountWindow(self):
        self._control.ShowAccountWindow()

    def _configureAutoLogin(self):
        self._ensureConnectedAndThen(self._showAccountWindow)

    def _openOpenApiHome(self):
        openApiHomeUrl = "https://www3.kiwoom.com/nkw.templateFrameSet.do?m=m1408000000"
        url = QUrl(openApiHomeUrl)
        QDesktopServices.openUrl(url)

    def _openOpenApiDocument(self):
        openApiHomeUrl = "https://download.kiwoom.com/web/openapi/kiwoom_openapi_plus_devguide_ver_1.5.pdf"
        url = QUrl(openApiHomeUrl)
        QDesktopServices.openUrl(url)

    def _openOpenApiQna(self):
        openApiQnaUrl = "https://bbn.kiwoom.com/bbn.openAPIQnaBbsList.do"
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
        self._exit(signum + 100)

    def _exec(self):
        self.logger.debug("Starting app")
        with contextlib.ExitStack() as stack:
            for signal_ in [signal.SIGINT, signal.SIGTERM]:
                self._signal_handler.setHandler(signal_, self._onSignal)
                stack.callback(self._signal_handler.restoreHandler, signal_)
            self._server.start()
            return self._app.exec_()

    def _exit(self, return_code=0):
        self.logger.debug("Exiting app")
        self._server.stop()
        self._server.wait_for_termination()
        self._app.exit(return_code)

    def _nextRestartTime(self):
        now = datetime.datetime.now()
        target = now.replace(hour=6, minute=50, second=0, microsecond=0)
        if now >= target:
            target += datetime.timedelta(days=1)
        return target

    def _startRestartNotifier(self):
        def notify_and_wait_for_next():
            self._should_restart.emit(self._should_restart_exit_code)
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

    def _exitForRestart(self):
        return self._exit(self._should_restart_exit_code)

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

    def execAndExitWithAutomaticRestart(self):
        should_restart = True
        while should_restart:
            code = self._exec()
            self.logger.debug("App exitted with return code: %d", code)
            should_restart = code == self._should_restart_exit_code
            if should_restart:
                self.logger.warning("Exitted app for restart")
                self.logger.warning("Restarting app")
        sys.exit(code)

    @classmethod
    def main(cls, args):
        app = cls(args)
        app.execAndExitWithAutomaticRestart()
