from koapy.compat.pyside2.QtCore import QProcess, Signal
from koapy.utils.logging.pyside2.QObjectLogging import QObjectLogging
from koapy.utils.subprocess import function_to_subprocess_args


class KiwoomOpenApiPlusDialogHandler(QObjectLogging):

    readyDialog = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._process = QProcess(self)

    @classmethod
    def main(cls):
        import datetime
        import json
        import re
        import sys

        import pywinauto

        titles = [
            "안녕하세요. 키움증권 입니다.",
            "KHOpenAPI",
            "[HTS 재접속 안내]",
        ]
        titles_escaped = [re.escape(title) for title in titles]
        title_re = "({})".format("|".join(titles_escaped))

        desktop = pywinauto.Desktop(allow_magic_lookup=False)
        dialog = desktop.window(title_re=title_re)

        channel = sys.stdout
        should_stop = False

        while not should_stop:
            try:
                timeout = 5
                retry_interval = 1
                dialog.wait("ready", timeout, retry_interval)
            except pywinauto.timings.TimeoutError as e:
                continue
            else:
                wrapper_object = dialog.wrapper_object()
                cls.logger.debug("New dialog found: %s", wrapper_object.window_text())
                now = datetime.datetime.now()
                filename = now.strftime("%Y%m%d%H%M%S") + ".log"
                dialog.print_control_identifiers(filename=filename)
                event = {
                    "timestamp": now.isoformat(),
                    "class_name": wrapper_object.class_name(),
                    "friendly_class_name": wrapper_object.friendly_class_name(),
                    "process_id": wrapper_object.process_id(),
                    "texts": wrapper_object.texts(),
                    "window_text": wrapper_object.window_text(),
                    "filename": filename,
                }
                event_message = json.dumps(event, ensure_ascii=False)
                cls.logger.debug("Emitting dialog event: %s", event_message)
                print(event_message, file=channel)
                cls.logger.debug("Clicking confirm button in order to close the dialog")
                dialog["Button"].click()

    def _onReadyRead(self):
        while self._process.canReadLine():
            line = self._process.readLine()
            self.readyDialog.emit(line)

    def start(self):
        def main():
            from koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusDialogHandler import (
                KiwoomOpenApiPlusDialogHandler,
            )

            KiwoomOpenApiPlusDialogHandler.main()

        args = function_to_subprocess_args(main)
        program = args[0]
        arguments = args[1:]

        self._process.connect(self._process.readyRead, self._onReadyRead)
        self._process.start(program, arguments)

    def stop(self, wait=True):
        self._process.disconnect(self._process.readyRead, self._onReadyRead)
        self._process.terminate()

        if wait:
            return self._process.waitForFinished()
