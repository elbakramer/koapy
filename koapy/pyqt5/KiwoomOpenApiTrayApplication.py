import sys
import logging
import argparse
import datetime
import signal
import contextlib

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QStyle
from PyQt5.QtCore import QTimer, QObject, pyqtSignal

from koapy.grpc.KiwoomOpenApiServiceServer import KiwoomOpenApiServiceServer
from koapy.openapi.KiwoomOpenApiError import KiwoomOpenApiError

from koapy.pyqt5.KiwoomOpenApiQAxWidget import KiwoomOpenApiQAxWidget

class KiwoomOpenApiTrayApplication(QObject):

    _should_restart = pyqtSignal(int)
    _should_restart_exit_code = 1

    def __init__(self, args=()):
        super().__init__()

        self._parser = argparse.ArgumentParser()
        self._parser.add_argument('-p', '--port')
        self._parsed_args, remaining_args = self._parser.parse_known_args(args and args[1:])

        self._port = self._parsed_args.port

        self._app = QApplication(args[:1] + remaining_args)
        self._control = KiwoomOpenApiQAxWidget()
        self._server = KiwoomOpenApiServiceServer(self._control, port=self._port)

        self._should_restart.connect(self._exit)
        self._startRestartNotifier()
        self._startEventLoopProcessor()

        self._tray = QSystemTrayIcon()
        self._tray.activated.connect(self._activate)

        icon = self._app.style().standardIcon(QStyle.SP_TitleBarMenuButton)

        menu = QMenu()
        menu.addSection('Connection')
        connectAction = menu.addAction('Login and Connect')
        connectAction.triggered.connect(self._connect)
        autoLoginAction = menu.addAction('Congifure Auto Login')
        autoLoginAction.triggered.connect(self._configureAutoLogin)
        menu.addSection('Status')
        self._connectionStatusAction = menu.addAction('Status: Disconnected')
        self._connectionStatusAction.setEnabled(False)
        self._serverStatusAction = menu.addAction('Server: Unknown')
        self._serverStatusAction.setEnabled(False)
        menu.addSection('Exit')
        exitAction = menu.addAction('Exit')
        exitAction.triggered.connect(self._exit)

        tooltip = 'Kiwoom OpenAPI Tray Application'

        self._tray.setIcon(icon)
        self._tray.setContextMenu(menu)
        self._tray.setToolTip(tooltip)

        self._tray.show()

        self._control.OnEventConnect.connect(self._OnEventConnect)

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
            maintanance_start_time = now.replace(hour=5, minute=5, second=0, microsecond=0)
            maintanance_end_time = now.replace(hour=5, minute=10, second=0, microsecond=0)
        else:
            maintanance_start_time = now.replace(hour=4, minute=0, second=0, microsecond=0)
            maintanance_end_time = now.replace(hour=4, minute=30, second=0, microsecond=0)

        if maintanance_start_time < now < maintanance_end_time:
            target = maintanance_end_time + datetime.timedelta(minutes=5)
            logging.warning('Connection lost due to maintanance, waiting until %s (then will try to reconnect)', target)
            timediff = target - now
            if callback is not None and callable(callback):
                QTimer.singleShot(timediff.total_seconds() * 1000, lambda: callback(*args, **kwargs))

    def _OnEventConnect(self, errcode):
        if errcode == 0:
            logging.debug('Connected to server')
            state = self._control.GetConnectState()
            if state == 1:
                self._connectionStatusAction.setText('Status: Connected')
                server = self._control.GetLoginInfo('GetServerGubun')
                if server == '1':
                    self._serverStatusAction.setText('Server: Simulation')
                else:
                    self._serverStatusAction.setText('Server: Real')
            else:
                raise RuntimeError('Unexpected case')
        elif errcode == KiwoomOpenApiError.OP_ERR_SOCKET_CLOSED:
            logging.error('Socket closed')
            state = self._control.GetConnectState()
            if state == 0:
                self._connectionStatusAction.setText('Status: Disconnected')
            def callback():
                logging.warning('Trying to reconnect')
                self._ensureConnectedAndThen() # 재연결 시도
            self._checkAndWaitForMaintananceAndThen(callback)
        elif errcode == KiwoomOpenApiError.OP_ERR_CONNECT:
            logging.error('Failed to connect')
            state = self._control.GetConnectState()
            if state == 0:
                self._connectionStatusAction.setText('Status: Disconnected')

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
                    raise TypeError('Function is not callable')
                callback(*args, **kwargs)
        else:
            if callback is not None:
                if not callable(callback):
                    raise TypeError('Function is not callable')
                def callbackAndDisconnect(errcode):
                    self._control.OnEventConnect.disconnect(callbackAndDisconnect)
                    if errcode == 0:
                        callback(*args, **kwargs)
                self._control.OnEventConnect.connect(callbackAndDisconnect)
            self._control.CommConnect()

    def _connect(self):
        self._ensureConnectedAndThen()

    def _showAccountWindow(self):
        self._control.koapy_Functions('ShowAccountWindow', '')

    def _configureAutoLogin(self):
        self._ensureConnectedAndThen(self._showAccountWindow)

    def _onInterrupt(self, signum, _frame):
        self._exit(signum + 100)

    def _exec(self):
        with contextlib.ExitStack() as stack:
            orig_handler = signal.signal(signal.SIGINT, self._onInterrupt)
            stack.callback(signal.signal, signal.SIGINT, orig_handler)
            logging.debug('Starting app')
            logging.debug('Starting server')
            try:
                self._server.start()
            except ValueError as e:
                logging.warning('Error: %s', e)
            logging.debug('Started server')
            return self._app.exec_()

    def _exit(self, return_code=0):
        logging.debug('Exiting app')
        logging.debug('Stopping server')
        self._server.stop(10)
        logging.debug('Waiting for server to stop')
        self._server.wait_for_termination(10)
        logging.debug('Stopped server')
        logging.debug('Quitting app')
        self._app.exit(return_code)
        logging.debug('Quitted app')

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
            QTimer.singleShot((timediff.total_seconds() + 1) * 1000, notify_and_wait_for_next)
        now = datetime.datetime.now()
        next_restart_time = self._nextRestartTime()
        timediff = next_restart_time - now
        QTimer.singleShot((timediff.total_seconds() + 1) * 1000, notify_and_wait_for_next)

    def _startEventLoopProcessor(self):
        interval = 5 * 1000
        def process_and_wait():
            QApplication.processEvents()
            QTimer.singleShot(interval, process_and_wait)
        QTimer.singleShot(interval, process_and_wait)

    def _exitForRestart(self):
        return self._exit(self._should_restart_exit_code)

    def execAndExit(self):
        code = self._exec()
        sys.exit(code)

    def execAndExitWithAutomaticRestart(self):
        should_restart = True
        while should_restart:
            code = self._exec()
            logging.debug('App exitted with return code: %d', code)
            should_restart = code == self._should_restart_exit_code
            if should_restart:
                logging.warning('Exitted app for restart')
                logging.warning('Restarting app')
        sys.exit(code)

    @classmethod
    def main(cls, args):
        app = cls(args)
        app.execAndExitWithAutomaticRestart()
