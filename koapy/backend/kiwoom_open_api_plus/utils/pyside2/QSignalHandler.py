import signal as signal_module
import socket

from signal import Signals  # pylint: disable=no-name-in-module
from types import FrameType
from typing import Iterable, Optional, overload

from koapy.compat.pyside2.QtCore import QObject, Signal
from koapy.compat.pyside2.QtNetwork import QAbstractSocket
from koapy.utils.logging.pyside2.QAbstractSocketLogging import QAbstractSocketLogging


class QSignalHandler(QAbstractSocketLogging):

    signaled = Signal(Signals, FrameType)

    @overload
    def __init__(self, signals: Iterable[Signals], parent: Optional[QObject]):
        ...

    @overload
    def __init__(self, parent: Optional[QObject]):
        ...

    def __init__(self, *args, **kwargs):
        signals: Optional[Iterable[Signals]] = None
        parent: Optional[QObject] = None

        args = list(args)
        kwargs = dict(kwargs)

        if len(args) > 0 and not isinstance(args[0], QObject):
            signals = args.pop(0)
        elif "signals" in kwargs:
            signals = kwargs.pop("signals")

        if len(args) > 0:
            parent = args[0]
        elif "parent" in kwargs:
            parent = kwargs["parent"]

        self._signals = signals
        self._parent = parent

        QAbstractSocketLogging.__init__(
            self, QAbstractSocket.UdpSocket, *args, **kwargs
        )

        self._old_wakeup_fd = None
        self._old_signal_handlers = {}

        self._wsock, self._rsock = socket.socketpair(socket.AF_INET, socket.SOCK_STREAM)

        self.readyRead.connect(self.onReadyRead)

    def onReadyRead(self):
        # it is up to the library to remove any bytes from fd before calling poll or select again
        # check https://docs.python.org/3.9/library/signal.html#signal.set_wakeup_fd for more details
        data = self.readData(1)

        # not actually using this, since file descriptor is used for wakeup purpose only
        _signal = data[0]

    def emitSignal(self, signal, frame):
        signal = signal_module.Signals(signal)
        self.signaled.emit(signal, frame)

    def setWakeUpFileDescriptor(self, descriptor, warn_on_full_buffer=True):
        old_wakeup_fd = signal_module.set_wakeup_fd(
            descriptor, warn_on_full_buffer=warn_on_full_buffer
        )
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
            old_signal_handlers = dict(self._old_signal_handlers)
            for signal, handler in old_signal_handlers.items():
                self.restoreHandler(signal, handler)
            self._old_signal_handlers = {}

    def setAll(self):
        self.setSocketDescriptor(self._rsock.fileno())

        # setting warn_on_full_buffer=False, since we are using the wakeup fd only for wakeups
        # check https://docs.python.org/3.9/library/signal.html#signal.set_wakeup_fd for more details
        self.setWakeUpFileDescriptor(self._wsock.fileno(), warn_on_full_buffer=False)

        if self._signals:
            for signal in self._signals:
                self.setHandler(signal, self.emitSignal)

    def restoreAll(self):
        self.restoreWakeUpFileDescrptor()
        self.restoreAllHandlers()

    def __del__(self):
        self.restoreAll()

    def __enter__(self):
        self.setAll()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.restoreAll()
