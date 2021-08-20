from koapy.backend.kiwoom_open_api_plus.utils.pyside2.QDialogHandler import (
    QDialogHandler,
)


class KiwoomOpenApiPlusDialogHandler(QDialogHandler):
    def __init__(self, app, parent=None):
        self._app = app
        self._parent = parent

        """
        TITLE: 안녕하세요. 키움증권 입니다.
        TIME: 04:45
        BODY:
        안녕하세요. 키움증권 입니다.
        시스템의 안정적인 운영을 위하여
        매일 시스템 점검을 하고 있습니다.
        점검시간은 월~토요일 (05:05 ~ 05:10)
                  일요일    (04:00 ~ 04:30) 까지 입니다.
        따라서 해당 시간대에는 접속단절이 될 수 있습니다.
        참고하시기 바랍니다.
        """

        """
        TITLE: KHOpenAPI
        TIME: 05:05
        BODY:
        통신 연결이 끊겼습니다. 프로그램 종료후 재접속 해주시기 바랍니다.
        """

        """
        TITLE: [HTS 재접속 안내]
        TIME: 06:50
        BODY:
        안녕하세요. 키움증권입니다.

        오전 6시 50분 이전에 접속하신 고객님께서는
        영웅문을 재접속하여 주시기 바랍니다.
        재접속을 하지 않을 경우 거래종목 정보, 전일 거래에
        대한 결제분 등이 반영되지 않아 실제 잔고와 차이가
        발생할 수 있습니다.
                               -키움증권-
        """

        self._titles = [
            "안녕하세요. 키움증권 입니다.",
            "KHOpenAPI",
            "[HTS 재접속 안내]",
        ]
        self._titles_should_restart = self._titles[-1:]
        super().__init__(self._titles, self._parent)

        self.readyDialog.connect(self.onReadyDialog)

    def onReadyDialog(self, dialog):
        self.logger.debug("Clicking confirm button on dialog")
        dialog["Button"].click()
        dialog_title = dialog.wrapper_object().window_text()
        if dialog_title in self._titles_should_restart:
            self.logger.debug("Restarting by following the dialog's instruction")
            self._app.shouldRestart.emit(0)
