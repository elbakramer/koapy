import re

from typing import Dict, List, Optional, Sequence, Set

from koapy.compat.pyside2.QtCore import QObject, Signal
from koapy.compat.pywinauto import Desktop, WindowSpecification
from koapy.compat.pywinauto.findwindows import ElementNotFoundError
from koapy.compat.pywinauto.timings import TimeoutError as PywinautoTimeoutError
from koapy.utils.logging.pyside2.QThreadLogging import QThreadLogging


class QDialogHandler(QThreadLogging):

    readyDialog = Signal(WindowSpecification)
    notReadyDialog = Signal(WindowSpecification)

    def __init__(
        self,
        specifications: Optional[Sequence[WindowSpecification]] = None,
        parent: Optional[QObject] = None,
    ):
        QThreadLogging.__init__(self, parent)

        self._specifications: List[WindowSpecification] = (
            specifications and list(self._specifications) or []
        )

        self._dialogs_not_ready: Set[WindowSpecification] = set(self._specifications)
        self._dialogs_ready: Set[WindowSpecification] = set()

        self._text_by_dialog: Dict[WindowSpecification, str] = {}

        self._should_stop = False

        self._timeout = 1 / len(self._dialogs_not_ready)
        self._retry_interval = self._timeout / 5

        assert self._timeout >= self._retry_interval * 2

    @classmethod
    def from_titles(cls, titles: Sequence[str], allow_magic_lookup: bool = False):
        titles_escaped = [re.escape(title) for title in titles]
        desktop = Desktop(allow_magic_lookup=allow_magic_lookup)
        specifications = [
            desktop.window(title_re=title_re) for title_re in titles_escaped
        ]
        return cls(specifications)

    def get_text_of_dialog(
        self,
        dialog: WindowSpecification,
        default: Optional[str] = None,
    ):
        if dialog in self._text_by_dialog:
            dialog_text = self._text_by_dialog[dialog]
        else:
            try:
                dialog_text = dialog.wrapper_object().window_text()
            except ElementNotFoundError:
                dialog_text = default
            else:
                self._text_by_dialog[dialog] = dialog_text
        return dialog_text

    def run(self):
        while not self._should_stop:
            for dialog in list(self._dialogs_not_ready):
                try:
                    dialog.wait("ready", self._timeout, self._retry_interval)
                except (PywinautoTimeoutError, ElementNotFoundError):
                    continue
                else:
                    dialog_text = self.get_text_of_dialog(dialog)
                    self.logger.debug("Dialog found: %s", dialog_text)
                    self._dialogs_not_ready.remove(dialog)
                    self._dialogs_ready.add(dialog)
                    self.readyDialog.emit(dialog)

            for dialog in list(self._dialogs_ready):
                try:
                    dialog.wait_not("ready", self._timeout, self._retry_interval)
                except (PywinautoTimeoutError, ElementNotFoundError):
                    continue
                else:
                    dialog_text = self.get_text_of_dialog(dialog) or "(Unknown)"
                    self.logger.debug("Dialog closed: %s", dialog_text)
                    self._dialogs_ready.remove(dialog)
                    self._dialogs_not_ready.add(dialog)
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
