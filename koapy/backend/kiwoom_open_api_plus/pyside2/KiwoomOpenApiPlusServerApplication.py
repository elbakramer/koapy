import sys

from argparse import Namespace
from contextlib import ExitStack, contextmanager
from enum import Enum
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

import grpc

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidget import (
    KiwoomOpenApiPlusQAxWidget,
)
from koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceServer import (
    KiwoomOpenApiPlusServiceServer,
)
from koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusSignalHandler import (
    KiwoomOpenApiPlusSignalHandler,
)
from koapy.backend.kiwoom_open_api_plus.utils.pyside2.QThreadPoolExecutor import (
    QThreadPoolExecutor,
)
from koapy.cli.extensions.parser import ArgumentParser
from koapy.cli.utils.grpc_options import (
    server_and_client_argument_parser,
    server_argument_parser,
)
from koapy.compat.pyside2.QtCore import QSize, QThreadPool
from koapy.compat.pyside2.QtGui import QIcon
from koapy.compat.pyside2.QtWidgets import QApplication, QMenu, QSystemTrayIcon
from koapy.config import config
from koapy.utils.logging import set_verbosity
from koapy.utils.logging.pyside2.QObjectLogging import QObjectLogging


class KiwoomOpenApiPlusServerApplicationArgumentParser(ArgumentParser):
    def __init__(self):
        self._server_argument_parser = server_argument_parser
        self._server_and_client_argument_parser = server_and_client_argument_parser

    def _merge_results(
        self,
        server_namespace,
        server_and_client_namespace,
        server_args=None,
        server_and_client_args=None,
    ):
        namespace = Namespace()

        # copy server namespace values
        for key, value in vars(server_namespace).items():
            setattr(namespace, key, value)

        # set aliases
        namespace.host = server_namespace.bind_address

        # copy fallback options to main options
        if not namespace.key_file and server_and_client_namespace.server_key_file:
            namespace.key_file = server_and_client_namespace.server_key_file
        if not namespace.cert_file and server_and_client_namespace.server_cert_file:
            namespace.cert_file = server_and_client_namespace.server_cert_file
        if (
            not namespace.root_certs_file
            and server_and_client_namespace.server_root_certs_file
        ):
            namespace.root_certs_file = (
                server_and_client_namespace.server_root_certs_file
            )

        if server_args is not None and server_and_client_args is not None:
            # filter unrecognized args
            unrecognized_args = [
                arg for arg in server_args if arg in server_and_client_args
            ]
            return namespace, unrecognized_args
        else:
            return namespace

    def parse_args(
        self,
        args: Optional[Sequence[str]] = None,
        namespace: Optional[Namespace] = None,
    ) -> Namespace:
        server_namespace = self._server_argument_parser.parse_args(args, namespace)
        server_and_client_namespace = (
            self._server_and_client_argument_parser.parse_args(args, namespace)
        )
        namespace = self._merge_results(
            server_namespace,
            server_and_client_namespace,
        )
        return namespace

    def parse_known_args(
        self,
        args: Optional[Sequence[str]] = None,
        namespace: Optional[Namespace] = None,
    ) -> Tuple[Namespace, List[str]]:
        (
            server_namespace,
            server_args,
        ) = self._server_argument_parser.parse_known_args(args, namespace)
        (
            server_and_client_namespace,
            server_and_client_args,
        ) = self._server_and_client_argument_parser.parse_known_args(args, namespace)
        namespace, unrecognized_args = self._merge_results(
            server_namespace,
            server_and_client_namespace,
            server_args,
            server_and_client_args,
        )
        return namespace, unrecognized_args


class KiwoomOpenApiPlusServerApplication(QObjectLogging):
    class ConnectionStatus(Enum):
        DISCONNECTED = 1
        CONNECTED = 2

    class ServerType(Enum):
        SIMULATION = 1
        REAL = 2
        UNKNOWN = 3

    def __init__(self, args=()):
        # Parse args
        self._args = list(args)
        self._argument_parser = KiwoomOpenApiPlusServerApplicationArgumentParser()
        (
            self._parsed_args,
            self._remaining_args,
        ) = self._argument_parser.parse_known_args(self._args[1:])

        # Set verbosity level
        self._verbose = self._parsed_args.verbose
        set_verbosity(self._verbose)

        # Attributes for gprc server
        self._bind_address = self._parsed_args.bind_address
        self._port = self._parsed_args.port

        # Attributes for grpc server (SSL/TLS)
        self._key_file = self._parsed_args.key_file
        self._cert_file = self._parsed_args.cert_file
        self._root_certs_file = self._parsed_args.root_certs_file
        self._require_client_auth = self._parsed_args.require_client_auth

        # Start creating application for real
        self.logger.debug("Creating server application")

        # Create QApplication instance
        self._app = QApplication.instance() or QApplication(
            self._args[:1] + self._remaining_args
        )

        # Create this QObject after creating QApplication instance
        super().__init__()

        # Capture certain signals and handle them accordingly
        self._signal_handler = KiwoomOpenApiPlusSignalHandler(self, self)
        self._signal_handler.signaled.connect(self._onSignal)

        # Attributes for gprc server (ThreadPoolExecutor)
        self._max_workers = config.get_int(
            "koapy.backend.kiwoom_open_api_plus.grpc.server.max_workers",
            8,
        )
        self._thread_pool = QThreadPool(self)
        self._thread_pool.setMaxThreadCount(self._max_workers)
        self._thread_pool_executor = QThreadPoolExecutor(self._thread_pool, self)

        # Prepare grpc server credentials if applicable
        if (self._key_file and self._cert_file) or self._root_certs_file:
            private_key_certificate_chain_pairs = None
            server_key = None
            server_cert = None
            if self._key_file:
                with open(self._key_file, "rb") as f:
                    server_key = f.read()
            if self._cert_file:
                with open(self._cert_file, "rb") as f:
                    server_cert = f.read()
            if server_key and server_cert:
                private_key_certificate_chain_pairs = [
                    (server_key, server_cert),
                ]
            root_certificates = None
            if self._root_certs_file:
                with open(self._root_certs_file, "rb") as f:
                    root_certificates = f.read()
            require_client_auth = self._require_client_auth
            self._credentials = grpc.ssl_server_credentials(
                private_key_certificate_chain_pairs=private_key_certificate_chain_pairs,
                root_certificates=root_certificates,
                require_client_auth=require_client_auth,
            )
        else:
            self._credentials = None

        # Create OpenAPI control object
        self._control = KiwoomOpenApiPlusQAxWidget()

        # Create gRPC server
        self._server = KiwoomOpenApiPlusServiceServer(
            control=self._control,
            host=self._bind_address,
            port=self._port,
            credentials=self._credentials,
            thread_pool=self._thread_pool_executor,
        )

        # Listen OnEventConnect event from OpenAPI
        # and change some application states based on that
        self._control.OnEventConnect.connect(self._onEventConnect)

        # Create system tray icon
        self._tray = self._createSystemTrayIcon()

        # Initialize tray icon menu by invoking related event handlers
        self._onEventConnect(0)

        # Make tray icon visible
        self._tray.show()

    # =======================================
    # Functions for creating system tray icon
    # =======================================

    def _createIcon(self):
        icon = QIcon()
        filePath = Path(__file__)
        iconDir = (filePath.parent / "../data/icon/server").resolve()

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
        toolTip = "KOAPY Server Application"
        return toolTip

    def _createContextMenu(self):
        menu = QMenu()

        # Section for displaying current status, should be disabled
        menu.addSection("Status")
        text = self._getConnectionStatusText(self.ConnectionStatus.DISCONNECTED)
        self._connectionStatusAction = menu.addAction(text)
        self._connectionStatusAction.setEnabled(False)
        text = self._getServerTypeText(self.ServerType.UNKNOWN)
        self._serverStatusAction = menu.addAction(text)
        self._serverStatusAction.setEnabled(False)

        # Exit button
        menu.addSection("Exit")
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(self._onExitButtonClicked)

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
        if reason == QSystemTrayIcon.DoubleClick:
            self._control.showNormal()
            self._control.activateWindow()

    def _onExitButtonClicked(self):
        self.exit()

    # ===================================
    # Functions for handling other events
    # ===================================

    def _onSignal(self, signal, frame):
        self.logger.debug("Received %r for server application ", signal)
        self.exit(signal)

    def _onEventConnect(self, errcode):
        state = self._control.GetConnectState()
        if state == 1:
            self._updateTrayIconMode(QIcon.Normal)
            self._updateConnectionStatus(self.ConnectionStatus.CONNECTED)
            server = self._control.GetServerGubun()
            if server == "1":
                self._updateServerType(self.ServerType.SIMULATION)
            else:
                self._updateServerType(self.ServerType.REAL)
        else:
            self._updateTrayIconMode(QIcon.Disabled)
            self._updateConnectionStatus(self.ConnectionStatus.DISCONNECTED)
            self._updateServerType(self.ServerType.UNKNOWN)

    # ================================
    # Functions for context management
    # ================================

    @contextmanager
    def _execContext(self):
        with ExitStack() as stack:
            stack.enter_context(self._signal_handler)
            stack.enter_context(self._thread_pool_executor)
            stack.enter_context(self._server)
            yield

    # ==============================
    # Functions for public interface
    # ==============================

    def __getattr__(self, name):
        return getattr(self._app, name)

    def _exec(self):
        with self._execContext():
            self.logger.debug("Started server application")
            return self._app.exec_()

    def _exit(self, return_code=0):
        self.logger.debug("Exiting server application")
        return self._app.exit(return_code)

    def exec_(self):
        return self._exec()

    def exit(self, return_code=0):
        return self._exit(return_code)

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
    KiwoomOpenApiPlusServerApplication.main()
