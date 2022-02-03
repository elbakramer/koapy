import os
import subprocess
import sys

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin import (
    KiwoomOpenApiPlusQAxWidgetMixin,
)
from koapy.utils.ctypes import is_admin
from koapy.utils.logging.Logging import Logging
from koapy.utils.platform import is_32bit
from koapy.utils.subprocess import Popen, function_to_subprocess_args


class KiwoomOpenApiPlusVersionUpdater(Logging):
    def __init__(self, credentials):
        self._credentials = credentials

    def get_api_module_path(self):
        from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusTypeLib import (
            API_MODULE_PATH,
        )

        module_path = API_MODULE_PATH
        return module_path

    def get_autologin_dat(self):
        module_path = self.get_api_module_path()
        autologin_dat = module_path / "system" / "Autologin.dat"
        return autologin_dat

    def is_autologin_enabled(self):
        autologin_dat = self.get_autologin_dat()
        return autologin_dat.exists()

    def disable_autologin(self):
        self.logger.info("Disabling auto login")
        autologin_dat = self.get_autologin_dat()
        if autologin_dat.exists():
            self.logger.info("Removing %s", autologin_dat)
            os.remove(autologin_dat)
            self.logger.info("Disabled auto login")
            return True
        else:
            self.logger.info("Autologin is already disabled")
            return False

    @classmethod
    def open_login_window_impl(cls):
        from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError import (
            KiwoomOpenApiPlusError,
        )
        from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidget import (
            KiwoomOpenApiPlusQAxWidget,
        )
        from koapy.compat.pyside2.QtWidgets import QApplication

        cls.logger.info("Opening login window")
        app = QApplication(sys.argv)
        control = KiwoomOpenApiPlusQAxWidget()
        if control.GetConnectState() == 0:

            def OnEventConnect(errcode):
                control.OnEventConnect.disconnect(OnEventConnect)
                KiwoomOpenApiPlusError.try_or_raise(errcode)
                app.exit(errcode)

            control.OnEventConnect.connect(OnEventConnect)
            KiwoomOpenApiPlusError.try_or_raise(control.CommConnect())
        return app.exec_()

    def open_login_window(self):
        # opening login window is a blocking process. (`app.exec_()` is the blocking process and will wait for `app.exit()`)
        # also it's hard to use both PySide2/PyQt5 and pywinauto at the same time in the same process due to compatibility issue.
        #
        # in order to avoid the issues mentioned above we are creating login window in a separate process.
        # and then will do login using pywinauto in another process using `login_using_pywinauto()` function.
        #
        # this process will stay alive until `OnEventConnect` event happens, hopefully a successful login.
        #
        # for more information about the compatibility issue between PySide2/PyQt5 and pywinauto, check the following link:
        #   https://github.com/pywinauto/pywinauto/issues/472

        def main():
            # pylint: disable=redefined-outer-name,import-self
            from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusVersionUpdater import (
                KiwoomOpenApiPlusVersionUpdater,
            )

            KiwoomOpenApiPlusVersionUpdater.open_login_window_impl()

        cmd = function_to_subprocess_args(main)
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
        proc = Popen(cmd, creationflags=creationflags)
        return proc

    @classmethod
    def show_account_window_impl(cls):
        from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError import (
            KiwoomOpenApiPlusError,
        )
        from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidget import (
            KiwoomOpenApiPlusQAxWidget,
        )
        from koapy.compat.pyside2.QtWidgets import QApplication

        cls.logger.info("Showing account window")
        app = QApplication(sys.argv)
        control = KiwoomOpenApiPlusQAxWidget()
        if control.GetConnectState() == 0:

            def OnEventConnect(errcode):
                control.OnEventConnect.disconnect(OnEventConnect)
                KiwoomOpenApiPlusError.try_or_raise(errcode)
                control.KOA_Functions("ShowAccountWindow", "")
                app.exit(errcode)

            control.OnEventConnect.connect(OnEventConnect)
            KiwoomOpenApiPlusError.try_or_raise(control.CommConnect())
        return app.exec_()

    def show_account_window(self):
        # this function does pretty much the same job like the `open_login_window()` function.
        # but the difference is that it will show up the account setting window after successful login,
        # so that we can (re-)enable the auto login functionality provided by the OpenAPI itself.
        #
        # this process will stay live until the account window is closed in the `OnEventConnect` event,
        # hopefully after successfully enabling the auto login functionality.
        #
        # note that the `control.KOA_Functions('ShowAccountWindow', '')` line is also blocking process.
        # so it will block until the account window is closed after enabling the auto login.

        def main():
            # pylint: disable=redefined-outer-name,import-self
            from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusVersionUpdater import (
                KiwoomOpenApiPlusVersionUpdater,
            )

            KiwoomOpenApiPlusVersionUpdater.show_account_window_impl()

        cmd = function_to_subprocess_args(main)
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
        proc = Popen(cmd, creationflags=creationflags)
        return proc

    @classmethod
    def check_apply_simulation_window(cls):
        import pywinauto

        desktop = pywinauto.Desktop(allow_magic_lookup=False)
        apply_simulation_window = desktop.window(title="모의투자 참가신청")

        try:
            timeout_apply_simulation = 5
            apply_simulation_window.wait("ready", timeout_apply_simulation)
        except pywinauto.timings.TimeoutError:
            pass
        else:
            cls.logger.warning("Please apply for simulation server before using it")
            raise RuntimeError("Please apply for simulation server before using it")

    @classmethod
    def login_using_pywinauto(cls, credentials):
        # reusing the implementation in the mixin
        KiwoomOpenApiPlusQAxWidgetMixin.LoginUsingPywinauto_Impl(credentials)
        cls.check_apply_simulation_window()

    @classmethod
    def enable_autologin_using_pywinauto(cls, credentials):
        # reusing the implementation in the mixin
        account_passwords = credentials.get("account_passwords")
        KiwoomOpenApiPlusQAxWidgetMixin.EnableAutoLoginUsingPywinauto_Impl(
            account_passwords
        )

    def enable_autologin(self):
        self.logger.info("Start enabling auto login")

        # pylint: disable=unused-variable
        account_window_proc = self.show_account_window()

        credentials = self._credentials

        self.login_using_pywinauto(credentials)
        self.enable_autologin_using_pywinauto(credentials)

    @classmethod
    def handle_version_upgrade_using_pywinauto(cls, pid):
        return KiwoomOpenApiPlusQAxWidgetMixin.HandleVersionUpgradeUsingPywinauto_Impl(
            pid
        )

    def try_version_update_using_pywinauto(self):
        self.logger.info("Trying version update")

        is_autologin_enabled = self.is_autologin_enabled()

        if is_autologin_enabled:
            self.disable_autologin()

        login_window_proc = self.open_login_window()

        credentials = self._credentials

        self.login_using_pywinauto(credentials)

        is_updated = self.handle_version_upgrade_using_pywinauto(login_window_proc.pid)

        if is_autologin_enabled:
            self.logger.info("Enabling auto login back")
            self.enable_autologin()
            if is_updated:
                self.logger.info("Done update, enabled auto login")
            else:
                self.logger.info("There was no version update, enabled auto login")

        return is_updated

    def update_version_if_necessary(self):
        assert (
            is_32bit()
        ), "Automatic version update requires to be run in 32bit environment"
        assert (
            is_admin()
        ), "Automatic version update requires to be run as administrator"
        return self.try_version_update_using_pywinauto()
