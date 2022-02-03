import datetime
import os
import sys

from argparse import Namespace
from contextlib import ExitStack, contextmanager
from enum import Enum
from pathlib import Path
from subprocess import TimeoutExpired
from threading import Timer
from typing import List, Optional, Sequence, Tuple

import grpc
import win32api
import win32con
import win32job
import win32process

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError import (
    KiwoomOpenApiPlusNegativeReturnCodeError,
)
from koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClient import (
    KiwoomOpenApiPlusServiceClient,
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
from koapy.cli.extensions.parser import ArgumentParser
from koapy.cli.utils.grpc_options import server_and_client_argument_parser
from koapy.compat.pyside2.QtCore import QProcess, QSize, QThreadPool, QUrl, Signal
from koapy.compat.pyside2.QtGui import QDesktopServices, QIcon
from koapy.compat.pyside2.QtWidgets import QApplication, QMenu, QSystemTrayIcon
from koapy.config import config, get_32bit_executable
from koapy.utils.logging import set_verbosity
from koapy.utils.logging.pyside2.QObjectLogging import QObjectLogging
from koapy.utils.subprocess import Popen


class KiwoomOpenApiPlusManagerApplicationArgumentParser(ArgumentParser):
    def __init__(self):
        self._parser = server_and_client_argument_parser

    def parse_args(
        self,
        args: Optional[Sequence[str]] = None,
        namespace: Optional[Namespace] = None,
    ) -> Namespace:
        return self._parser.parse_args(args, namespace)

    def parse_known_args(
        self,
        args: Optional[Sequence[str]] = None,
        namespace: Optional[Namespace] = None,
    ) -> Tuple[Namespace, List[str]]:
        return self._parser.parse_known_args(args, namespace)


class KiwoomOpenApiPlusServerApplicationProcess(QProcess):
    def __init__(self, args, parent=None):
        super().__init__(parent)

        self._args = args
        self._executable = get_32bit_executable()
        self._arguments = [
            "-m",
            KiwoomOpenApiPlusServerApplication.__module__,
        ] + self._args

        self.setProgram(self._executable)
        self.setArguments(self._arguments)
        self.setProcessChannelMode(QProcess.ForwardedChannels)

        self._hJob = None
        self._hProcess = None

        self.started.connect(self._onStarted)
        self.finished.connect(self._onFinished)

    def _onStarted(self):
        processId = self.processId()

        if processId != 0:
            # https://stackoverflow.com/questions/23434842/python-how-to-kill-child-processes-when-parent-dies/23587108#23587108s
            jobAttributes = None
            jobName = ""
            self._hJob = win32job.CreateJobObject(jobAttributes, jobName)
            extendedInfo = win32job.QueryInformationJobObject(
                self._hJob, win32job.JobObjectExtendedLimitInformation
            )
            basicLimitInformation = extendedInfo["BasicLimitInformation"]
            basicLimitInformation[
                "LimitFlags"
            ] = win32job.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
            win32job.SetInformationJobObject(
                self._hJob,
                win32job.JobObjectExtendedLimitInformation,
                extendedInfo,
            )
            desiredAccess = win32con.PROCESS_TERMINATE | win32con.PROCESS_SET_QUOTA
            inheritHandle = False
            self._hProcess = win32api.OpenProcess(
                desiredAccess,
                inheritHandle,
                processId,
            )
            win32job.AssignProcessToJobObject(self._hJob, self._hProcess)

    def _onFinished(self):
        exitCode = 0

        if self._hProcess is not None:
            try:
                exitCode = win32process.GetExitCodeProcess(self._hProcess)
            except win32process.error:
                pass

        if self._hJob is not None:
            win32job.TerminateJobObject(self._hJob, exitCode)


class KiwoomOpenApiPlusServerApplicationSubprocess:
    def __init__(self, args, parent=None):
        self._args = args
        self._executable = get_32bit_executable()
        self._cmd = [
            self._executable,
            "-m",
            KiwoomOpenApiPlusServerApplication.__module__,
        ] + self._args
        self._proc = None
        self._started = False

    def start(self):
        self._proc = Popen(self._cmd)
        self._started = True

    def waitForStarted(self, msecs: int = 30000) -> bool:
        return self._started

    def close(self):
        if self._proc is not None:
            self._proc.terminate()

    def waitForFinished(self, msecs: int = 30000) -> bool:
        if self._proc is not None:
            secs = msecs / 1000
            try:
                return_code = self._proc.wait(secs)
                return return_code == 0
            except TimeoutExpired:
                return False
        return False


class KiwoomOpenApiPlusManagerApplication(QObjectLogging):
    class ConnectionStatus(Enum):
        DISCONNECTED = 1
        CONNECTED = 2

    class ServerType(Enum):
        SIMULATION = 1
        REAL = 2
        UNKNOWN = 3

    class RestartType(Enum):
        NO_RESTART = 1
        RESTART_ONLY = 2
        RESTART_AND_RESTORE = 3
        RESTART_AND_CONNECT = 4
        RESTART_WITH_UPDATE = 5
        RESTART_WITH_UPDATE_AND_RESTORE = 6
        RESTART_WITH_UPDATE_AND_CONNECT = 7

    shouldRestart = Signal(RestartType)

    def __init__(self, args=()):
        # Parse args
        self._args = list(args)
        self._argument_parser = KiwoomOpenApiPlusManagerApplicationArgumentParser()
        (
            self._parsed_args,
            self._remaining_args,
        ) = self._argument_parser.parse_known_args(self._args[1:])

        # Set verbosity level
        self._verbose = self._parsed_args.verbose
        set_verbosity(self._verbose)

        # Attributes for gprc client
        self._host = self._parsed_args.host
        self._port = self._parsed_args.port

        # Attributes for grpc client (SSL/TLS)
        self._enable_ssl = self._parsed_args.enable_ssl
        self._key_file = self._parsed_args.client_key_file
        self._cert_file = self._parsed_args.client_cert_file
        self._root_certs_file = self._parsed_args.client_root_certs_file

        # Start creating application for real
        self.logger.debug("Creating manager application")

        # Create QApplication instance
        self._app = QApplication.instance() or QApplication(
            self._args[:1] + self._remaining_args
        )

        # Create this QObject after creating QApplication instance
        super().__init__()

        # Capture certain signals and handle them accordingly
        self._signal_handler = KiwoomOpenApiPlusSignalHandler(self, self)
        self._signal_handler.signaled.connect(self._onSignal)

        # Capture dialogs from OpenAPI and handle them accordingly
        from koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusDialogHandler import (
            KiwoomOpenApiPlusDialogHandler,
        )

        self._dialog_handler = KiwoomOpenApiPlusDialogHandler(self, self)

        # Attributes for gprc client (ThreadPoolExecutor)
        self._max_workers = config.get_int(
            "koapy.backend.kiwoom_open_api_plus.grpc.client.max_workers",
            8,
        )
        self._thread_pool = QThreadPool(self)
        self._thread_pool.setMaxThreadCount(self._max_workers)
        self._thread_pool_executor = QThreadPoolExecutor(self._thread_pool, self)

        # Prepare grpc client credentials if applicable
        if self._enable_ssl:
            root_certificates = None
            if self._root_certs_file:
                with open(self._root_certs_file, "rb") as f:
                    root_certificates = f.read()
            private_key = None
            if self._key_file:
                with open(self._key_file, "rb") as f:
                    private_key = f.read()
            certificate_chain = None
            if self._cert_file:
                with open(self._cert_file, "rb") as f:
                    certificate_chain = f.read()
            self._credentials = grpc.ssl_channel_credentials(
                root_certificates=root_certificates,
                private_key=private_key,
                certificate_chain=certificate_chain,
            )
        else:
            self._credentials = None

        # Initialize server subprocess and gprc client to the server
        self._server_process = None
        self._client = None
        self._reinitializeServerProcessAndGrpcClient()

        # Restart server application whenever restart is required
        self.shouldRestart.connect(self._onShouldRestart)

        # Create system tray icon
        self._tray = self._createSystemTrayIcon()

        # Initialize tray icon menu by invoking related event handlers
        self._onEventConnect(0)

        # Make tray icon visible
        self._tray.show()

    # ==============================================
    # Functions for server/client (re)initialization
    # ==============================================

    def _closeClient(self):
        self._client.close()

    def _closeClientIfExists(self):
        if hasattr(self, "_client") and self._client is not None:
            self._closeClient()

    def _closeServerProcess(self):
        self._server_process.close()
        self._server_process.waitForFinished()

    def _closeServerProcessIfExists(self):
        if hasattr(self, "_server_process") and self._server_process is not None:
            self._closeServerProcess()

    def _reinitializeServerProcessAndGrpcClient(self):
        self._closeClientIfExists()
        self._closeServerProcessIfExists()

        # Create server application subprocess and start that
        self._server_process = KiwoomOpenApiPlusServerApplicationProcess(
            self._args[1:], self
        )
        self._server_process.start()
        self._server_process.waitForStarted()

        # Create gRPC client
        self._client = KiwoomOpenApiPlusServiceClient(
            host=self._host,
            port=self._port,
            credentials=self._credentials,
            thread_pool=self._thread_pool_executor,
        )

        # Wait for the client to be ready
        self._client_timeout = 30
        assert self._client.is_ready(self._client_timeout), "Client is not ready"

        # Listen OnEventConnect event from OpenAPI
        # and change some application states based on that
        self._client.OnEventConnect.connect(self._onEventConnect)

    # =======================================
    # Functions for creating system tray icon
    # =======================================

    def _createIcon(self):
        icon = QIcon()
        filePath = Path(__file__)
        iconDir = (filePath.parent / "../data/icon/manager").resolve()

        def addFilesForMode(icon, iconDir, mode):
            icon.addFile(
                str(iconDir / "favicon-16x16.png"),
                QSize(16, 16),
                mode,
            )
            icon.addFile(
                str(iconDir / "favicon-32x32.png"),
                QSize(32, 32),
                mode,
            )
            icon.addFile(
                str(iconDir / "apple-touch-icon.png"),
                QSize(180, 180),
                mode,
            )
            icon.addFile(
                str(iconDir / "android-chrome-192x192.png"),
                QSize(192, 192),
                mode,
            )
            icon.addFile(
                str(iconDir / "android-chrome-512x512.png"),
                QSize(512, 512),
                mode,
            )

        # Add files for each mode
        addFilesForMode(icon, iconDir / "normal", QIcon.Normal)
        addFilesForMode(icon, iconDir / "disabled", QIcon.Disabled)
        addFilesForMode(icon, iconDir / "active", QIcon.Active)

        return icon

    def _createToolTip(self):
        toolTip = "KOAPY Manager Application"
        return toolTip

    def _createContextMenu(self):
        menu = QMenu()

        # Section for actions related to connection and login
        menu.addSection("Connection")
        connectAction = menu.addAction("Login and connect")
        connectAction.triggered.connect(self._onConnectActionTriggered)
        showAccountWindowAction = menu.addAction("Show account window")
        showAccountWindowAction.triggered.connect(
            self._onShowAccountWindowActionTriggered
        )
        enableAutoLoginAction = menu.addAction("Enable auto login")
        enableAutoLoginAction.triggered.connect(self._onEnableAutoLoginActionTriggered)
        checkForUpdateAction = menu.addAction("Check for update")
        checkForUpdateAction.triggered.connect(self._onCheckForUpdateActionTriggered)

        # Section for displaying current status, should be disabled
        menu.addSection("Status")
        text = self._getConnectionStatusText(self.ConnectionStatus.DISCONNECTED)
        self._connectionStatusAction = menu.addAction(text)
        self._connectionStatusAction.setEnabled(False)
        text = self._getServerTypeText(self.ServerType.UNKNOWN)
        self._serverStatusAction = menu.addAction(text)
        self._serverStatusAction.setEnabled(False)

        # Section for external links (koapy)
        menu.addSection("Links")
        iconDir = Path(__file__).parent / "../data/icon/external"
        iconDir = iconDir.resolve()
        icon = QIcon(str(iconDir / "readthedocs.png"))
        documentationAction = menu.addAction(icon, "Documentation")
        documentationAction.triggered.connect(self._openReadTheDocs)
        icon = QIcon(str(iconDir / "github.png"))
        githubAction = menu.addAction(icon, "Github")
        githubAction.triggered.connect(self._openGithub)

        # Section for external links (kiwoom)
        menu.addSection("Kiwoom Links")
        openApiAction = menu.addAction("Kiwoom OpenAPI+ Home")
        openApiAction.triggered.connect(self._openOpenApiHome)
        openApiAction = menu.addAction("Kiwoom OpenAPI+ Document")
        openApiAction.triggered.connect(self._openOpenApiDocument)
        qnaAction = menu.addAction("Kiwoom OpenAPI+ Qna")
        qnaAction.triggered.connect(self._openOpenApiQna)

        # Section for exit and restart
        menu.addSection("Exit")
        restartAction = menu.addAction("Restart")
        restartAction.triggered.connect(self._onRestartActionTriggered)
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(self._onExitActionTriggered)

        return menu

    def _createSystemTrayIcon(self):
        tray = QSystemTrayIcon()

        self._icon = self._createIcon()
        self._tooltip = self._createToolTip()
        self._menu = self._createContextMenu()

        tray.setIcon(self._icon)
        tray.setToolTip(self._tooltip)
        tray.setContextMenu(self._menu)

        tray.activated.connect(self._onTrayIconActivated)  # pylint: disable=no-member

        return tray

    # =========================================
    # Functions for controling tray icon states
    # =========================================

    def _updateTrayIconMode(self, mode: QIcon.Mode = QIcon.Normal):
        icon = QIcon(self._icon.pixmap(16, mode))
        self._tray.setIcon(icon)

    def _getConnectionStatusText(self, status: ConnectionStatus):
        text = {
            self.ConnectionStatus.DISCONNECTED: "Status: Disconnected",
            self.ConnectionStatus.CONNECTED: "Status: Connected",
        }[status]
        return text

    def _updateConnectionStatus(self, status: ConnectionStatus):
        text = self._getConnectionStatusText(status)
        self._connectionStatusAction.setText(text)

    def _getServerTypeText(self, server_type: ServerType):
        text = {
            self.ServerType.SIMULATION: "Server: Simulation",
            self.ServerType.REAL: "Server: Real",
            self.ServerType.UNKNOWN: "Server: Unknown",
        }[server_type]
        return text

    def _updateServerType(self, server_type: ServerType):
        text = self._getServerTypeText(server_type)
        self._serverStatusAction.setText(text)

    # =======================================
    # Functions for handling tray icon events
    # =======================================

    def _onTrayIconActivated(self, reason):
        pass

    def _onExitActionTriggered(self):
        self.exit()

    def _onRestartActionTriggered(self):
        self._emitShouldRestart(self.RestartType.RESTART_AND_RESTORE)

    def _onConnectActionTriggered(self):
        self._connect()

    def _onShowAccountWindowActionTriggered(self):
        self._showAccountWindow()

    def _onEnableAutoLoginActionTriggered(self):
        self._enableAutoLogin()

    def _onCheckForUpdateActionTriggered(self):
        self._emitShouldRestart(self.RestartType.RESTART_WITH_UPDATE_AND_RESTORE)

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

    # ==============================
    # Functions for general behavior
    # ==============================

    def _ensureConnectedAndThen(self, callback=None):
        if not self._client.IsConnected():
            self.logger.debug("Connecting to OpenAPI server")
        self._client.EnsureConnectedAndThen(callback)

    def _connect(self):
        self._ensureConnectedAndThen()

    def _showAccountWindow(self):
        self._ensureConnectedAndThen(lambda errcode: self._client.ShowAccountWindow())

    def _enableAutoLogin(self):
        self._ensureConnectedAndThen(
            lambda errcode: self._client.EnsureAutoLoginEnabled()
        )

    def _emitShouldRestart(self, restart_type: Optional[RestartType] = None):
        if restart_type is None:
            restart_type = self.RestartType.RESTART_ONLY
        self.shouldRestart.emit(restart_type)

    def _emitShouldRestartAndConnect(self):
        self._emitShouldRestart(self.RestartType.RESTART_AND_CONNECT)

    def _onShouldRestart(self, restart_type: RestartType):
        self._restart(restart_type)

    # ===================================
    # Functions for handling other events
    # ===================================

    def _onSignal(self, signal, frame):
        self.logger.debug("Received %r for manager application", signal)
        self.exit(signal)

    def _tryReconnect(self):
        now = datetime.datetime.now()
        buffer = datetime.timedelta(minutes=5)

        target = now
        timediff = datetime.timedelta()

        maintanance_start_time = now.replace(hour=5, minute=5, second=0, microsecond=0)
        maintanance_end_time = now.replace(hour=5, minute=10, second=0, microsecond=0)

        maintanance_start_time_sunday = now.replace(
            hour=4, minute=0, second=0, microsecond=0
        )
        maintanance_end_time_sunday = now.replace(
            hour=4, minute=30, second=0, microsecond=0
        )

        is_maintanance = (
            (maintanance_start_time - buffer) < now < (maintanance_end_time + buffer)
        )
        is_maintanance_sunday = (
            (maintanance_start_time_sunday - buffer)
            < now
            < (maintanance_end_time_sunday + buffer)
        )
        is_sunday = now.weekday() == 6

        if is_maintanance:
            target = maintanance_end_time + buffer
        elif is_sunday and is_maintanance_sunday:
            target = maintanance_end_time_sunday + buffer

        timediff = target - now
        total_seconds = timediff.total_seconds()

        if total_seconds > 0:
            self.logger.warning(
                "Connection lost due to maintanance, waiting until %s, then will try to reconnect",
                target,
            )
            # QTimer is not working, why?
            # QTimer.singleShot(total_seconds * 1000, self._emitShouldRestartAndConnect)
            timer = Timer(total_seconds, self._emitShouldRestartAndConnect)
            timer.start()
        else:
            self.logger.warning(
                "Connection lost unexpectedly, will try to reconnect right away"
            )
            self._emitShouldRestartAndConnect()

    def _onEventConnect(self, errcode):
        state = self._client.GetConnectState()

        if state == 1:
            self._updateTrayIconMode(QIcon.Normal)
            self._updateConnectionStatus(self.ConnectionStatus.CONNECTED)
            server = self._client.GetServerGubun()
            if server == "1":
                self._updateServerType(self.ServerType.SIMULATION)
            else:
                self._updateServerType(self.ServerType.REAL)
        else:
            self._updateTrayIconMode(QIcon.Disabled)
            self._updateConnectionStatus(self.ConnectionStatus.DISCONNECTED)
            self._updateServerType(self.ServerType.UNKNOWN)

        if errcode == KiwoomOpenApiPlusNegativeReturnCodeError.OP_ERR_SOCKET_CLOSED:
            self.logger.error("Socket closed")
            self._tryReconnect()
        elif errcode == KiwoomOpenApiPlusNegativeReturnCodeError.OP_ERR_CONNECT:
            self.logger.error("Failed to connect")

    # ================================
    # Functions for context management
    # ================================

    def _close(self):
        self._closeClient()
        self._closeServerProcess()

    def close(self):
        return self._close()

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

    # ==============================
    # Functions for public interface
    # ==============================

    def __getattr__(self, name):
        return getattr(self._app, name)

    def _exec(self):
        with self._execContext():
            self.logger.debug("Started manager application")
            return self._app.exec_()

    def _exit(self, return_code=0):
        self.logger.debug("Exiting manager application")
        return self._app.exit(return_code)

    def _isConnected(self):
        return self._client.is_ready() and self._client.IsConnected()

    def _getAPIModulePath(self):
        from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusTypeLib import (
            API_MODULE_PATH,
        )

        module_path = API_MODULE_PATH
        return module_path

    def _getAutoLoginDatPath(self):
        module_path = self._getAPIModulePath()
        autologin_dat = module_path / "system" / "Autologin.dat"
        return autologin_dat

    def _isAutoLoginEnabled(self):
        autologin_dat = self._getAutoLoginDatPath()
        return autologin_dat.exists()

    def _disableAutoLogin(self):
        self.logger.info("Disabling auto login")
        autologin_dat = self._getAutoLoginDatPath()
        if autologin_dat.exists():
            self.logger.info("Removing %s", autologin_dat)
            os.remove(autologin_dat)
            self.logger.info("Disabled auto login")
            return True
        else:
            self.logger.info("Autologin is already disabled")
            return False

    def _restart(self, restart_type: Optional[RestartType] = None):
        self.logger.debug("Restarting server application")

        if restart_type is None:
            restart_type = self.RestartType.RESTART_ONLY

        is_connected = self._isConnected()
        is_autologin_enabled = self._isAutoLoginEnabled()

        should_connect_to_restore = (
            restart_type
            in [
                self.RestartType.RESTART_AND_RESTORE,
                self.RestartType.RESTART_WITH_UPDATE_AND_RESTORE,
            ]
            and is_connected
        )
        should_connect_anyway = restart_type in [
            self.RestartType.RESTART_AND_CONNECT,
            self.RestartType.RESTART_WITH_UPDATE_AND_CONNECT,
        ]
        should_connect = should_connect_to_restore or should_connect_anyway

        should_update = restart_type in [
            self.RestartType.RESTART_WITH_UPDATE,
            self.RestartType.RESTART_WITH_UPDATE_AND_RESTORE,
            self.RestartType.RESTART_WITH_UPDATE_AND_CONNECT,
        ]

        if should_update:
            self._reinitializeServerProcessAndGrpcClient()
            if is_autologin_enabled:
                self._disableAutoLogin()
            self._client.CommConnectAndThen()
            is_updated = self._client.HandleVersionUpgradeUsingPywinauto(
                self._server_process.processId()
            )
            if is_updated:
                self._reinitializeServerProcessAndGrpcClient()
            if is_autologin_enabled:
                self.logger.info("Enabling auto login back")
                self._enableAutoLogin()
                if is_updated:
                    self.logger.info("Done update, enabled auto login")
                else:
                    self.logger.info("There was no version update, enabled auto login")
        else:
            self._reinitializeServerProcessAndGrpcClient()

        if should_connect:
            self.logger.debug("Re-establishing connection")
            self._connect()

    def exec_(self):
        return self._exec()

    def exit(self, return_code=0):
        return self._exit(return_code)

    def restart(self, restart_type: Optional[RestartType] = None):
        return self._restart(restart_type)

    def execAndExit(self):
        code = self.exec_()
        sys.exit(code)

    @classmethod
    def main(cls, args=None):
        if args is None:
            args = sys.argv
        app = cls(args)
        app.execAndExit()


if __name__ == "__main__":
    KiwoomOpenApiPlusManagerApplication.main()
