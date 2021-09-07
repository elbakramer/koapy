import re

from typing import List

from koapy.compat.pyside2.QtCore import Signal
from koapy.compat.pywinauto import Desktop, WindowSpecification
from koapy.compat.pywinauto.timings import TimeoutError as PywinautoTimeoutError
from koapy.utils.logging.pyside2.QThreadLogging import QThreadLogging


class QDialogHandler(QThreadLogging):

    readyDialog = Signal(WindowSpecification)
    notReadyDialog = Signal(WindowSpecification)

    def __init__(self, titles=None, parent=None):
        QThreadLogging.__init__(self, parent)

        self._titles = titles
        self._titles_escaped = [re.escape(title) for title in titles]

        self._desktop = Desktop(allow_magic_lookup=False)

        self._dialogs_not_ready: List[WindowSpecification] = [
            self._desktop.window(title_re=title_re) for title_re in self._titles_escaped
        ]
        self._dialogs_ready: List[WindowSpecification] = []

        self._title_by_dialog = dict(zip(self._dialogs_not_ready, self._titles))

        self._should_stop = False

        self._timeout = 1 / len(self._dialogs_not_ready)
        self._retry_interval = self._timeout / 5

        assert self._timeout >= self._retry_interval * 2

    def run(self):
        while not self._should_stop:
            for dialog in list(self._dialogs_not_ready):
                try:
                    dialog.wait("ready", self._timeout, self._retry_interval)
                except PywinautoTimeoutError:
                    continue
                else:
                    dialog_text = self._title_by_dialog.get(dialog)
                    self.logger.debug("Dialog found: %s", dialog_text)
                    self._dialogs_not_ready.remove(dialog)
                    self._dialogs_ready.append(dialog)
                    self.readyDialog.emit(dialog)

            for dialog in list(self._dialogs_ready):
                try:
                    dialog.wait_not("ready", self._timeout, self._retry_interval)
                except PywinautoTimeoutError:
                    continue
                else:
                    dialog_text = self._title_by_dialog.get(dialog)
                    self.logger.debug("Dialog closed: %s", dialog_text)
                    self._dialogs_ready.remove(dialog)
                    self._dialogs_not_ready.append(dialog)
                    self.notReadyDialog.emit(dialog)

    def stop(self):
        self._should_stop = True

    def wait_for_termination(self, timeout=None):
        if timeout is not None:
            return self.wait(timeout)
        else:
            return self.wait()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
        self.wait_for_termination()
