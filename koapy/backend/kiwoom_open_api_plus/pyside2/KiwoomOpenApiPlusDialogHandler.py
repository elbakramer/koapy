import datetime
import re

from typing import Optional

import pytz

from koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusManagerApplication import (
    KiwoomOpenApiPlusManagerApplication,
)
from koapy.backend.kiwoom_open_api_plus.utils.pyside2.QDialogHandler import (
    QDialogHandler,
)
from koapy.compat.pyside2.QtCore import QObject
from koapy.compat.pywinauto import Desktop, WindowSpecification
from koapy.compat.pywinauto.findwindows import ElementNotFoundError
from koapy.utils.logging.Logging import Logging


class DialogToHandle:
    def should_handle(self, dialog: WindowSpecification) -> bool:
        ...

    def handle(self, dialog: WindowSpecification):
        ...

    def handle_if_needed(self, dialog: WindowSpecification):
        if self.should_handle(dialog):
            return self.handle(dialog)


class KiwoomOpenApiPlusDialogToHandle(DialogToHandle, Logging):
    @classmethod
    def should_handle_by_title(cls, dialog: WindowSpecification, title: str):
        try:
            cls.logger.debug("Checking dialog title")
            dialog_text = dialog.wrapper_object().window_text()
        except ElementNotFoundError:
            cls.logger.warning("Could not find dialog to check")
        else:
            return dialog_text == title

    @classmethod
    def handle_by_clicking_button(cls, dialog: WindowSpecification):
        try:
            cls.logger.debug("Clicking confirm button on dialog")
            dialog["Button"].click()
        except ElementNotFoundError:
            cls.logger.warning("Could not find dialog to confirm")

    @classmethod
    def handle_by_emiting_should_restart_signal(
        cls,
        app: KiwoomOpenApiPlusManagerApplication,
        restart_type: KiwoomOpenApiPlusManagerApplication.RestartType,
    ):
        cls.logger.debug("Restarting based on the dialog's instruction")
        app.shouldRestart.emit(restart_type)

    def __init__(
        self,
        title: Optional[str] = None,
        time: Optional[datetime.time] = None,
        body: Optional[str] = None,
        app: Optional[KiwoomOpenApiPlusManagerApplication] = None,
        restart_type: Optional[KiwoomOpenApiPlusManagerApplication.RestartType] = None,
    ):
        self._title = title
        self._time = time
        self._body = body

        self._app = app
        self._restart_type = restart_type

    def to_specification(self) -> WindowSpecification:
        desktop = Desktop(allow_magic_lookup=False)
        title_re = re.escape(self._title)
        specification = desktop.window(title_re=title_re)
        return specification

    def should_handle(self, dialog: WindowSpecification) -> bool:
        return self.should_handle_by_title(dialog, self._title)

    def handle(self, dialog: WindowSpecification):
        self.handle_by_clicking_button(dialog)
        if self._restart_type is not None:
            self.handle_by_emiting_should_restart_signal(self._app, self._restart_type)

    def handle_if_needed(self, dialog: WindowSpecification):
        if self.should_handle(dialog):
            return self.handle(dialog)


class KiwoomOpenApiPlusDialogHandler(QDialogHandler):
    def __init__(
        self,
        app: KiwoomOpenApiPlusManagerApplication,
        parent: Optional[QObject] = None,
    ):
        self._app = app
        self._parent = parent

        kst = pytz.timezone("Asia/Seoul")

        system_check_noticie = KiwoomOpenApiPlusDialogToHandle(
            title="안녕하세요. 키움증권 입니다.",
            time=datetime.time(hour=4, minute=45, tzinfo=kst),
            body="""
            안녕하세요. 키움증권 입니다.
            시스템의 안정적인 운영을 위하여
            매일 시스템 점검을 하고 있습니다.
            점검시간은 월~토요일 (05:05 ~ 05:10)
                    일요일    (04:00 ~ 04:30) 까지 입니다.
            따라서 해당 시간대에는 접속단절이 될 수 있습니다.
            참고하시기 바랍니다.
            """,
            app=app,
        )
        connection_lost = KiwoomOpenApiPlusDialogToHandle(
            title="KHOpenAPI",
            time=datetime.time(hour=5, minute=5, tzinfo=kst),
            body="""
            통신 연결이 끊겼습니다. 프로그램 종료후 재접속 해주시기 바랍니다.
            """,
            app=app,
        )
        hts_reconnect_notice = KiwoomOpenApiPlusDialogToHandle(
            title="[HTS 재접속 안내]",
            time=datetime.time(hour=6, minute=50, tzinfo=kst),
            body="""
            안녕하세요. 키움증권입니다.

            오전 6시 50분 이전에 접속하신 고객님께서는
            영웅문을 재접속하여 주시기 바랍니다.
            재접속을 하지 않을 경우 거래종목 정보, 전일 거래에
            대한 결제분 등이 반영되지 않아 실제 잔고와 차이가
            발생할 수 있습니다.
                                -키움증권-
            """,
            app=app,
            restart_type=KiwoomOpenApiPlusManagerApplication.RestartType.RESTART_AND_RESTORE,
        )

        self._dialogs_to_handle = [
            system_check_noticie,
            connection_lost,
            hts_reconnect_notice,
        ]
        self._specifications = [
            dialog.to_specification() for dialog in self._dialogs_to_handle
        ]

        super().__init__(self._specifications, self._parent)

        self.readyDialog.connect(self.onReadyDialog)

    def onReadyDialog(self, dialog: WindowSpecification):
        for dialog_to_handle in self._dialogs_to_handle:
            try:
                # pylint: disable=unused-variable
                dialog_wrapper_object = dialog.wrapper_object()
            except ElementNotFoundError:
                break
            else:
                dialog_to_handle.handle_if_needed(dialog)
