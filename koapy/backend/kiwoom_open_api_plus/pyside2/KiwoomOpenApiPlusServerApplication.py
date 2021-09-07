import os
import sys

from argparse import ArgumentParser
from contextlib import ExitStack, contextmanager

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
from koapy.compat.pyside2.QtCore import QSize, QThreadPool
from koapy.compat.pyside2.QtGui import QIcon
from koapy.compat.pyside2.QtWidgets import QApplication, QMenu, QSystemTrayIcon
from koapy.config import config
from koapy.utils.logging import set_verbosity
from koapy.utils.logging.pyside2.QObjectLogging import QObjectLogging


class KiwoomOpenApiPlusServerApplication(QObjectLogging):
    def __init__(self, args=()):
        self.logger.debug("Creating server application")

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

        self._max_workers = config.get_int(
            "koapy.backend.kiwoom_open_api_plus.grpc.server.max_workers",
            8,
        )
        self._thread_pool = QThreadPool(self)
        self._thread_pool.setMaxThreadCount(self._max_workers)
        self._thread_pool_executor = QThreadPoolExecutor(self._thread_pool, self)

        self._control = KiwoomOpenApiPlusQAxWidget()
        self._server = KiwoomOpenApiPlusServiceServer(
            control=self._control,
            port=self._port,
            thread_pool=self._thread_pool_executor,
        )
        self._control.OnEventConnect.connect(self._onEventConnect)

        self._tray = self._createSystemTrayIcon()
        self._onEventConnect(0)
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
        if reason == QSystemTrayIcon.DoubleClick:
            self._control.showNormal()
            self._control.activateWindow()

    def _createIcon(self):
        icon = QIcon()
        iconDir = os.path.join(os.path.dirname(__file__), "../data/icon/server")

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
        tooltip = "KOAPY Server Application"
        return tooltip

    def _createContextMenu(self):
        menu = QMenu()
        menu.addSection("Status")
        self._connectionStatusAction = menu.addAction("Status: Disconnected")
        self._connectionStatusAction.setEnabled(False)
        self._serverStatusAction = menu.addAction("Server: Unknown")
        self._serverStatusAction.setEnabled(False)
        menu.addSection("Exit")
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(self._exit)
        return menu

    @contextmanager
    def _execContext(self):
        with ExitStack() as stack:
            stack.enter_context(self._signal_handler)
            stack.enter_context(self._thread_pool_executor)
            stack.enter_context(self._server)
            yield

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
        self.logger.debug("Received %r for server application ", signal)
        self.exit(signal)

    def _onEventConnect(self, errcode):
        state = self._control.GetConnectState()
        if state == 1:
            icon = QIcon(self._icon.pixmap(16, QIcon.Normal))
            self._tray.setIcon(icon)
            self._connectionStatusAction.setText("Status: Connected")
            server = self._control.GetLoginInfo("GetServerGubun")
            if server == "1":
                self._serverStatusAction.setText("Server: Simulation")
            else:
                self._serverStatusAction.setText("Server: Real")
        else:
            icon = QIcon(self._icon.pixmap(16, QIcon.Disabled))
            self._tray.setIcon(icon)
            self._connectionStatusAction.setText("Status: Disconnected")


if __name__ == "__main__":
    KiwoomOpenApiPlusServerApplication.main()
