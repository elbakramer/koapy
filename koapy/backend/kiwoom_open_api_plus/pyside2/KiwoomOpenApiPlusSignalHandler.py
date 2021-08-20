import signal as signal_module

from koapy.backend.kiwoom_open_api_plus.utils.pyside2.QSignalHandler import (
    QSignalHandler,
)


class KiwoomOpenApiPlusSignalHandler(QSignalHandler):
    def __init__(self, app, parent=None):
        self._app = app
        self._parent = parent

        self._signals = [
            signal_module.SIGINT,
            signal_module.SIGTERM,
        ]
        super().__init__(self._signals, self._parent)
