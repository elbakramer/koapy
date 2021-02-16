import signal
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
        self._old_wakeup_fd = signal.set_wakeup_fd(self._wsock.fileno())

        self.readyRead.connect(self._readSignal)

    def __del__(self):
        if hasattr(self, '_old_wakeup_fd') and self._old_wakeup_fd is not None:
            signal.set_wakeup_fd(self._old_wakeup_fd)
        if hasattr(self, '_old_signal_handlers') and self._old_signal_handlers:
            for signal_, handler in self._old_signal_handlers.items():
                self.restoreHandler(signal_, handler)

    def _readSignal(self):
        data = self.readData(1)
        self.signalReceived.emit(data[0])

    def setHandler(self, signal_, handler):
        old_handler = signal.signal(signal_, handler)
        if signal_ not in self._old_signal_handlers:
            self._old_signal_handlers[signal_] = old_handler
        return old_handler

    def restoreHandler(self, signal_, default=None):
        if default is None:
            default = signal.SIG_DFL
        if signal_ in self._old_signal_handlers:
            return signal.signal(signal_, self._old_signal_handlers.pop(signal_, default))
