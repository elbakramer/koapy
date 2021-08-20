import re

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

        self._desktop = Desktop(allow_magic_lookup=False)

        titles_escaped = [re.escape(title) for title in titles]
        title_re = "({})".format("|".join(titles_escaped))

        self._dialog = self._desktop.window(title_re=title_re)

        self._should_stop = False

        self._timeout = 1
        self._retry_interval = 0.1

    def run(self):
        while not self._should_stop:
            try:
                self._dialog.wait("ready", self._timeout, self._retry_interval)
            except PywinautoTimeoutError:
                continue
            else:
                wrapper_object = self._dialog.wrapper_object()
                self.logger.debug("Dialog found: %s", wrapper_object.window_text())
                self.readyDialog.emit(self._dialog)
                while not self._should_stop:
                    try:
                        self._dialog.wait_not(
                            "ready", self._timeout, self._retry_interval
                        )
                    except PywinautoTimeoutError:
                        continue
                    else:
                        wrapper_object = self._dialog.wrapper_object()
                        self.logger.debug(
                            "Dialog closed: %s", wrapper_object.window_text()
                        )
                        self.notReadyDialog.emit(self._dialog)
                        break

    def stop(self):
        self._should_stop = True
        return self.quit()

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
