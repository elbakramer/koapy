import datetime
import os
import sys

from argparse import ArgumentParser
from contextlib import ExitStack, contextmanager

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError import (
    KiwoomOpenApiPlusNegativeReturnCodeError,
)
from koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClient import (
    KiwoomOpenApiPlusServiceClient,
)
from koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusDialogHandler import (
    KiwoomOpenApiPlusDialogHandler,
)
from koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusServerApplication import (
    KiwoomOpenApiPlusServerApplication,
)
from koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusSignalHandler import (
    KiwoomOpenApiPlusSignalHandler,
)
from koapy.backend.kiwoom_open_api_plus.utils.pyside2.QThreadPoolExecutor import (
    QThreadPoolExecutor,
)
from koapy.compat.pyside2.QtCore import (
    QProcess,
    QSize,
    QThreadPool,
    QTimer,
    QUrl,
    Signal,
)
from koapy.compat.pyside2.QtGui import QDesktopServices, QIcon
from koapy.compat.pyside2.QtWidgets import QApplication, QMenu, QSystemTrayIcon
from koapy.config import config, get_32bit_executable
from koapy.utils.logging import set_verbosity
from koapy.utils.logging.pyside2.QObjectLogging import QObjectLogging


class KiwoomOpenApiPlusServerApplicationProcess(QProcess):
    def __init__(self, args, parent=None):
        super().__init__(parent)

        self.setProgram(get_32bit_executable())
        self.setArguments(["-m", KiwoomOpenApiPlusServerApplication.__module__] + args)
        self.setProcessChannelMode(QProcess.ForwardedChannels)

        self._hJob = None
        self._hProcess = None

        self.started.connect(self._onStarted)
        self.finished.connect(self._onFinished)

    def _onStarted(self):
        pid = self.processId()

        if pid != 0:
            # https://stackoverflow.com/questions/23434842/python-how-to-kill-child-processes-when-parent-dies/23587108#23587108s
            import win32api
            import win32con
            import win32job

            hJob = win32job.CreateJobObject(None, "")
            extendedInfo = win32job.QueryInformationJobObject(
                hJob, win32job.JobObjectExtendedLimitInformation
            )
            extendedInfo["BasicLimitInformation"][
                "LimitFlags"
            ] = win32job.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
            win32job.SetInformationJobObject(
                hJob, win32job.JobObjectExtendedLimitInformation, extendedInfo
            )
            perms = win32con.PROCESS_TERMINATE | win32con.PROCESS_SET_QUOTA
            hProcess = win32api.OpenProcess(perms, False, pid)
            win32job.AssignProcessToJobObject(hJob, hProcess)

            self._hJob = hJob
            self._hProcess = hProcess

    def _onFinished(self):
        if self._hJob is not None and self._hProcess is not None:
            import win32job

            win32job.TerminateJobObject(self._hJob, self._hProcess)


class KiwoomOpenApiPlusManagerApplication(QObjectLogging):

    shouldRestart = Signal(int)

    def __init__(self, args=()):
        self.logger.debug("Creating manager application")

        self._args = args
        self._parser = ArgumentParser()
        self._parser.add_argument("-p", "--port")
        self._parser.add_argument("-v", "--verbose", action="count", default=0)
        self._parsed_args, self._remaining_args = self._parser.parse_known_args(args)

        self._port = self._parsed_args.port
        self._verbose = self._parsed_args.verbose

        set_verbosity(self._verbose)

        self._app = QApplication.instance()

        if not self._app:
            self._app = QApplication(self._remaining_args)

        super().__init__()

        self._signal_handler = KiwoomOpenApiPlusSignalHandler(self, self)
        self._signal_handler.signaled.connect(self._onSignal)

        self._dialog_handler = KiwoomOpenApiPlusDialogHandler(self, self)

        self._server_process = KiwoomOpenApiPlusServerApplicationProcess(
            self._args, self
        )
        self._server_process.start()
        self._server_process.waitForStarted()

        self._max_workers = config.get_int(
            "koapy.backend.kiwoom_open_api_plus.grpc.client.max_workers",
            8,
        )
        self._thread_pool = QThreadPool(self)
        self._thread_pool.setMaxThreadCount(self._max_workers)
        self._thread_pool_executor = QThreadPoolExecutor(self._thread_pool, self)

        self._client = KiwoomOpenApiPlusServiceClient(
            port=self._port, thread_pool=self._thread_pool_executor
        )
        assert self._client.is_ready(), "Client is not ready"
        self._client.OnEventConnect.connect(self._onEventConnect)

        self.shouldRestart.connect(self._restart)

        self._tray = self._createSystemTrayIcon()
        self._tray.show()

    def _createSystemTrayIcon(self):
        tray = QSystemTrayIcon()
        tray.activated.connect(self._activate)  # pylint: disable=no-member

        self._icon = self._createIcon()
        self._tooltip = self._createTooltip()
        self._menu = self._createContextMenu()

        tray.setIcon(self._icon)
        tray.setToolTip(self._tooltip)
        tray.setContextMenu(self._menu)

        return tray

    def _activate(self, reason):
        pass

    def _createIcon(self):
        icon = QIcon()
        iconDir = os.path.join(os.path.dirname(__file__), "../data/icon/manager")

        def addFiles(iconDir, mode):
            icon.addFile(
                os.path.join(iconDir, "favicon-16x16.png"), QSize(16, 16), mode
            )
            icon.addFile(
                os.path.join(iconDir, "favicon-32x32.png"), QSize(32, 32), mode
            )
            icon.addFile(
                os.path.join(iconDir, "apple-touch-icon.png"), QSize(180, 180), mode
            )
            icon.addFile(
                os.path.join(iconDir, "android-chrome-192x192.png"),
                QSize(192, 192),
                mode,
            )
            icon.addFile(
                os.path.join(iconDir, "android-chrome-512x512.png"),
                QSize(512, 512),
                mode,
            )

        addFiles(os.path.join(iconDir, "normal"), QIcon.Normal)
        addFiles(os.path.join(iconDir, "disabled"), QIcon.Disabled)
        addFiles(os.path.join(iconDir, "active"), QIcon.Active)

        return icon

    def _createTooltip(self):
        tooltip = "KOAPY Manager Application"
        return tooltip

    def _createContextMenu(self):
        menu = QMenu()
        iconDir = os.path.join(os.path.dirname(__file__), "../data/icon/external")
        menu.addSection("Connection")
        connectAction = menu.addAction("Login and Connect")
        connectAction.triggered.connect(self._connect)
        showAccountWindowAction = menu.addAction("Show Account Window")
        showAccountWindowAction.triggered.connect(self._showAccountWindow)
        menu.addSection("Status")
        self._connectionStatusAction = menu.addAction("Status: Disconnected")
        self._connectionStatusAction.setEnabled(False)
        self._serverStatusAction = menu.addAction("Server: Unknown")
        self._serverStatusAction.setEnabled(False)
        menu.addSection("Links")
        icon = QIcon(os.path.join(iconDir, "readthedocs.png"))
        documentationAction = menu.addAction(icon, "Documentation")
        documentationAction.triggered.connect(self._openReadTheDocs)
        icon = QIcon(os.path.join(iconDir, "github.png"))
        githubAction = menu.addAction(icon, "Github")
        githubAction.triggered.connect(self._openGithub)
        menu.addSection("Kiwoom Links")
        openApiAction = menu.addAction("Kiwoom OpenAPI+ Home")
        openApiAction.triggered.connect(self._openOpenApiHome)
        openApiAction = menu.addAction("Kiwoom OpenAPI+ Document")
        openApiAction.triggered.connect(self._openOpenApiDocument)
        qnaAction = menu.addAction("Kiwoom OpenAPI+ Qna")
        qnaAction.triggered.connect(self._openOpenApiQna)
        menu.addSection("Exit")
        restartAction = menu.addAction("Restart")
        restartAction.triggered.connect(self._emitShouldRestart)
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(self._exit)
        return menu

    def _ensureConnectedAndThen(self, callback=None):
        self._client.EnsureConnectedAndThen(callback)

    def _connect(self):
        self._ensureConnectedAndThen()

    def _showAccountWindow(self):
        self._ensureConnectedAndThen(self._client.ShowAccountWindow)

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

    def _emitShouldRestart(self):
        self.shouldRestart.emit(0)

    def _closeClient(self):
        self._client.close()

    def _closeServerProcess(self):
        self._server_process.close()
        self._server_process.waitForFinished()

    def _close(self):
        self._closeClient()
        self._closeServerProcess()

    def close(self):
        return self._close()

    def __del__(self):
        try:
            self.close()
        except RuntimeError:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    @contextmanager
    def _execContext(self):
        with ExitStack() as stack:
            stack.enter_context(self._signal_handler)
            stack.enter_context(self._dialog_handler)
            stack.enter_context(self._thread_pool_executor)
            stack.enter_context(self)
            yield

    def _exec(self):
        self.logger.debug("Starting manager application")
        with self._execContext():
            self.logger.debug("Started manager application")
            return self._app.exec_()

    def _exit(self, return_code=0):
        self.logger.debug("Exiting manager application")
        return self._app.exit(return_code)

    def _restart(self, code):
        self.logger.debug("Restarting server application")
        self._client.close()
        self._server_process.close()
        self._server_process.waitForFinished()

        self._server_process = KiwoomOpenApiPlusServerApplicationProcess(
            self._args, self
        )
        self._server_process.start()
        self._server_process.waitForStarted()

        self._client = KiwoomOpenApiPlusServiceClient(
            port=self._port, thread_pool=self._thread_pool_executor
        )
        assert self._client.is_ready(), "Client is not ready"
        self._client.OnEventConnect.connect(self._onEventConnect)

        if code > 0:
            self._connect()

    def exec_(self):
        return self._exec()

    def exit(self, return_code=0):
        return self._exit(return_code)

    def restart(self):
        return self._restart(1)

    def execAndExit(self):
        code = self._exec()
        sys.exit(code)

    def __getattr__(self, name):
        return getattr(self._app, name)

    @classmethod
    def main(cls, args=None):
        if args is None:
            args = sys.argv
        app = cls(args)
        app.execAndExit()

    def _onSignal(self, signal, frame):
        self.logger.debug("Received %r for manager application", signal)
        self.exit(signal)

    def _tryReconnect(self):
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

        buffer = datetime.timedelta(minutes=1)

        def reconnect():
            self.logger.warning("Trying to reconnect")
            self.shouldRestart.emit(1)

        if (maintanance_start_time - buffer) < now < (maintanance_end_time + buffer):
            target = maintanance_end_time + buffer
            self.logger.warning(
                "Connection lost due to maintanance, waiting until %s, then will try to reconnect",
                target,
            )
            timediff = target - now
        else:
            self.logger.warning(
                "Connection lost unexpectedly, will try to reconnect right away"
            )
            timediff = datetime.timedelta()

        QTimer.singleShot(timediff.total_seconds() * 1000, reconnect)

    def _onEventConnect(self, errcode):
        if errcode == 0:
            state = self._client.GetConnectState()
            if state == 1:
                self._connectionStatusAction.setText("Status: Connected")
                server = self._client.GetLoginInfo("GetServerGubun")
                if server == "1":
                    self.logger.debug("Connected to Simulation server")
                    self._serverStatusAction.setText("Server: Simulation")
                else:
                    self.logger.debug("Connected to Real server")
                    self._serverStatusAction.setText("Server: Real")
            else:
                raise RuntimeError("Unexpected case")
        elif errcode == KiwoomOpenApiPlusNegativeReturnCodeError.OP_ERR_SOCKET_CLOSED:
            self.logger.error("Socket closed")
            state = self._client.GetConnectState()
            if state == 0:
                self._connectionStatusAction.setText("Status: Disconnected")
            self._tryReconnect()
        elif errcode == KiwoomOpenApiPlusNegativeReturnCodeError.OP_ERR_CONNECT:
            self.logger.error("Failed to connect")
            state = self._client.GetConnectState()
            if state == 0:
                self._connectionStatusAction.setText("Status: Disconnected")


if __name__ == "__main__":
    KiwoomOpenApiPlusManagerApplication.main()
