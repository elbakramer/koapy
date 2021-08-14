import signal as signal_module
import socket

from koapy.compat.pyside2.QtCore import Signal
from koapy.compat.pyside2.QtNetwork import QAbstractSocket


class QSignalHandler(QAbstractSocket):

    signalReceived = Signal(int)

    def __init__(self, parent=None):
        super().__init__(QAbstractSocket.UdpSocket, parent)

        self._old_wakeup_fd = None
        self._old_signal_handlers = {}

        self._wsock, self._rsock = socket.socketpair(socket.AF_INET, socket.SOCK_STREAM)
        self.setSocketDescriptor(self._rsock.fileno())
        self.setWakeUpFileDescriptor(self._wsock.fileno())

        self.readyRead.connect(self.onReadyRead)

    def onReadyRead(self):
        data = self.readData(1)
        self.signalReceived.emit(data[0])

    def setWakeUpFileDescriptor(self, descriptor):
        old_wakeup_fd = signal_module.set_wakeup_fd(descriptor)
        # remember first time replcement only
        if self._old_wakeup_fd is None:
            self._old_wakeup_fd = old_wakeup_fd
        return old_wakeup_fd

    def restoreWakeUpFileDescrptor(self):
        if self._old_wakeup_fd is not None:
            old_wakeup_fd = signal_module.set_wakeup_fd(self._old_wakeup_fd)
            self._old_wakeup_fd = None
            return old_wakeup_fd

    def setHandler(self, signal, handler):
        old_handler = signal_module.signal(signal, handler)
        # remember first time replcement only
        if signal not in self._old_signal_handlers:
            self._old_signal_handlers[signal] = old_handler
        return old_handler

    def restoreHandler(self, signal, default=None):
        if signal in self._old_signal_handlers:
            if default is None:
                default = signal_module.SIG_DFL
            old_handler = self._old_signal_handlers.pop(signal, default)
            old_handler = signal_module.signal(signal, old_handler)
            return old_handler

    def restoreAllHandlers(self):
        if self._old_signal_handlers:
            for signal, handler in self._old_signal_handlers.items():
                self.restoreHandler(signal, handler)
            self._old_signal_handlers = {}

    def restoreAll(self):
        self.restoreWakeUpFileDescrptor()
        self.restoreAllHandlers()

    def __del__(self):
        self.restoreAll()
