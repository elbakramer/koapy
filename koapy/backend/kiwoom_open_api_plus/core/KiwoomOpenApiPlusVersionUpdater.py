import os
import sys
import ctypes
import subprocess
import atexit

from koapy.utils.logging.Logging import Logging

class KiwoomOpenApiPlusVersionUpdater(Logging):

    __is_in_development = False
    __use_set_text = False

    def __init__(self, credential):
        self._credential = credential

    @classmethod
    def __disable_autologin(cls):
        from koapy.compat.pyside2.QtWidgets import QApplication
        from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidget import KiwoomOpenApiPlusQAxWidget
        cls.logger.info('Disabling auto login')
        app = QApplication(sys.argv) # pylint: disable=unused-variable
        control = KiwoomOpenApiPlusQAxWidget()
        module_path = control.GetAPIModulePath()
        autologin_dat = os.path.join(module_path, 'system', 'Autologin.dat')
        if os.path.exists(autologin_dat):
            cls.logger.info('Removing %s', autologin_dat)
            os.remove(autologin_dat)
            cls.logger.info('Disabled auto login')
            return True
        else:
            cls.logger.info('Autologin is already disabled')
            return False

    def disable_autologin(self):
        cmd = [sys.executable, __file__, 'disable_autologin']
        return subprocess.check_call(cmd)

    @classmethod
    def __open_login_window(cls):
        from koapy.compat.pyside2.QtWidgets import QApplication
        from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidget import KiwoomOpenApiPlusQAxWidget
        from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError import KiwoomOpenApiPlusError
        cls.logger.info('Opening login window')
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
        cmd = [sys.executable, __file__, 'open_login_window']
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
        proc = subprocess.Popen(cmd, creationflags=creationflags)
        atexit.register(proc.kill)
        return proc

    @classmethod
    def __show_account_window(cls):
        from koapy.compat.pyside2.QtWidgets import QApplication
        from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidget import KiwoomOpenApiPlusQAxWidget
        from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError import KiwoomOpenApiPlusError
        cls.logger.info('Showing account window')
        app = QApplication(sys.argv)
        control = KiwoomOpenApiPlusQAxWidget()
        if control.GetConnectState() == 0:
            def OnEventConnect(errcode):
                control.OnEventConnect.disconnect(OnEventConnect)
                KiwoomOpenApiPlusError.try_or_raise(errcode)
                control.KOA_Functions('ShowAccountWindow', '')
                app.exit(errcode)
            control.OnEventConnect.connect(OnEventConnect)
            KiwoomOpenApiPlusError.try_or_raise(control.CommConnect())
        return app.exec_()

    def show_account_window(self):
        cmd = [sys.executable, __file__, 'show_account_window']
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
        proc = subprocess.Popen(cmd, creationflags=creationflags)
        atexit.register(proc.kill)
        return proc

    @classmethod
    def __enable_autologin_using_pywinauto(cls, account_passwords):
        # https://github.com/pywinauto/pywinauto/issues/472
        import sys
        sys.coinit_flags = 2
        import warnings
        warnings.simplefilter("ignore", UserWarning)
        import pywinauto

        desktop = pywinauto.Desktop(allow_magic_lookup=False)
        account_window = desktop.window(title_re=r'계좌비밀번호 입력 \(버전: [0-9]+.+[0-9]+\)')

        try:
            cls.logger.info('Waiting for account window to show up')
            timeout_account_window_ready = 5
            account_window.wait('ready', timeout_account_window_ready)
        except pywinauto.timings.TimeoutError:
            cls.logger.info('Cannot find account window')
            raise
        else:
            cls.logger.info('Account window found')
            if cls.__is_in_development:
                account_window.logging.info_control_identifiers()

            cls.logger.info('Enabling auto login')
            account_window['CheckBox'].check()

            account_combo = account_window['ComboBox']
            account_cnt = account_combo.item_count()

            cls.logger.info('Putting account passwords')
            for i in range(account_cnt):
                account_combo.select(i)
                account_no = account_combo.selected_text().split()[0]
                if account_no in account_passwords:
                    account_window['Edit'].set_text(account_passwords[account_no])
                elif '0000000000' in account_passwords:
                    account_window['Edit'].set_text(account_passwords['0000000000'])
                account_window['등록'].click()

            cls.logger.info('Closing account window')
            account_window['닫기'].click()

            try:
                cls.logger.info('Wating account window to be closed')
                timeout_account_window_done = 5
                account_window.wait_not('visible', timeout_account_window_done)
            except pywinauto.timings.TimeoutError:
                cls.logger.info('Cannot sure account window is closed')
                raise
            else:
                cls.logger.info('Account window closed')

    @classmethod
    def __login_using_pywinauto(cls, credential, wait_closed=False):
        # https://github.com/pywinauto/pywinauto/issues/472
        import sys
        sys.coinit_flags = 2
        import warnings
        warnings.simplefilter("ignore", UserWarning)
        import pywinauto

        userid = credential.get('user_id')
        password = credential.get('user_password')
        cert = credential.get('cert_password')

        check_save_userid = credential.get('check_save_userid', False)
        is_simulation = credential.get('is_simulation', False)

        desktop = pywinauto.Desktop(allow_magic_lookup=False)
        login_window = desktop.window(title='Open API Login')

        try:
            cls.logger.info('Waiting for login screen')
            timeout_login_screen_ready = 30
            login_window.wait('ready', timeout_login_screen_ready)
        except pywinauto.timings.TimeoutError:
            cls.logger.info('Cannot find login screen')
            raise
        else:
            cls.logger.info('Login screen found')
            if cls.__is_in_development:
                login_window.print_control_identifiers()

            if userid:
                cls.logger.info('Putting userid')
                if cls.__use_set_text:
                    login_window['Edit1'].set_text(userid)
                else:
                    login_window['Edit1'].set_focus()
                    pywinauto.keyboard.send_keys(userid)
                    pywinauto.keyboard.send_keys('{TAB}')
            if password:
                cls.logger.info('Putting password')
                if cls.__use_set_text:
                    login_window['Edit2'].set_text(password)
                else:
                    login_window['Edit2'].set_focus()
                    pywinauto.keyboard.send_keys(password)
                    pywinauto.keyboard.send_keys('{TAB}')
            else:
                raise RuntimeError('Password not set')

            if False:
                # below does not work properly
                if check_save_userid:
                    cls.logger.info('Checking to save userid')
                    login_window['Button6'].check_by_click()
                else:
                    cls.logger.info('Unchecking to save userid')
                    login_window['Button6'].uncheck_by_click()

            if not is_simulation:
                if not login_window['Edit3'].is_enabled():
                    cls.logger.info('Unchecking to use simulation server')
                    login_window['Button5'].uncheck_by_click()
                if cert:
                    cls.logger.info('Putting cert password')
                    if cls.__use_set_text:
                        login_window['Edit3'].set_text(cert)
                    else:
                        login_window['Edit3'].set_focus()
                        pywinauto.keyboard.send_keys(cert)
                        pywinauto.keyboard.send_keys('{TAB}')
                else:
                    raise RuntimeError('Cert passowrd not set')
            else:
                if login_window['Edit3'].is_enabled():
                    cls.logger.info('Checking to use simulation server')
                    login_window['Button5'].check_by_click()

            cls.logger.info('Logging in')
            login_window['Button1'].click()

        if wait_closed:
            try:
                cls.logger.info('Waiting login screen to be closed')
                timeout_login_screen_closed = 30
                login_window.wait_not('visible', timeout_login_screen_closed)
            except pywinauto.timings.TimeoutError:
                cls.logger.info('Login screen is not closing')
                raise
            else:
                cls.logger.info('Login screen closed')

    def enable_autologin(self):
        self.logger.info('Start enabling auto login')

        account_window_proc = self.show_account_window() # pylint: disable=unused-variable

        credential = self._credential
        account_passwords = credential.get('account_passwords')

        self.__login_using_pywinauto(credential)
        self.__enable_autologin_using_pywinauto(account_passwords)

    def try_version_update(self):
        # https://github.com/pywinauto/pywinauto/issues/472
        import sys
        sys.coinit_flags = 2
        import warnings
        warnings.simplefilter("ignore", UserWarning)
        import pywinauto

        self.logger.info('Trying version update')
        self.disable_autologin()

        login_window_proc = self.open_login_window()

        desktop = pywinauto.Desktop(allow_magic_lookup=False)
        login_window = desktop.window(title='Open API Login')

        credential = self._credential
        self.__login_using_pywinauto(credential)

        version_window = desktop.window(title='opstarter')

        try:
            self.logger.info('Wating for possible version update')
            timeout_version_update = 30
            version_window.wait('ready', timeout_version_update)
        except pywinauto.timings.TimeoutError:
            self.logger.info('No version update required')
            self.logger.info('Enabling auto login back')
            self.enable_autologin()
            self.logger.info('There was no version update, enabled auto login')
            return False
        else:
            self.logger.info('Version update required')
            if self.__is_in_development:
                version_window.print_control_identifiers()

            self.logger.info('Closing login app')
            login_window_proc.kill()
            login_window_proc.wait()
            self.logger.info('Killed login app process')
            timeout_login_screen_closed = 30
            login_window.close(timeout_login_screen_closed)
            try:
                login_window.wait_not('visible', timeout_login_screen_closed)
            except pywinauto.timings.TimeoutError:
                self.logger.info('Cannot close login window')
                raise
            else:
                self.logger.info('Closed login window')

                self.logger.info('Starting to update version')
                version_window['Button'].click()

                versionup_window = desktop.window(title='opversionup')
                confirm_window = desktop.window(title='업그레이드 확인')

                try:
                    self.logger.info('Wating for possible failure')
                    timeout_confirm_update = 10
                    versionup_window.wait('ready', timeout_confirm_update)
                except pywinauto.timings.TimeoutError:
                    self.logger.info('Cannot find failure confirmation popup')
                else:
                    self.logger.info('Failed update')
                    raise RuntimeError

                try:
                    self.logger.info('Wating for confirmation popup after update')
                    timeout_confirm_update = 10
                    confirm_window.wait('ready', timeout_confirm_update)
                except pywinauto.timings.TimeoutError:
                    self.logger.info('Cannot find confirmation popup')
                    raise
                else:
                    self.logger.info('Confirming update')
                    confirm_window['Button'].click()

                self.logger.info('Done update')
                self.logger.info('Enabling auto login back')
                self.enable_autologin()
                self.logger.info('Done update, enabled auto login')

                return True

        return False

    def is_admin(self):
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

    def update_version_if_necessary(self):
        assert self.is_admin(), 'Automatic version update requires to be run as administrator'
        return self.try_version_update()

    @classmethod
    def main(cls, args):
        import argparse
        parser = argparse.ArgumentParser()
        command_choices = [
            'update_version_if_necessary',
            'disable_autologin',
            'open_login_window',
            'show_account_window',
        ]
        default_command = 'update_version_if_necessary'
        parser.add_argument('command', nargs='?', choices=command_choices, default=default_command)
        args = parser.parse_args(args)
        if args.command == 'update_version_if_necessary':
            from koapy.config import config
            credential = config.get('koapy.backend.kiwoom_open_api_plus.credential')
            updater = cls(credential)
            updater.update_version_if_necessary()
        elif args.command == 'disable_autologin':
            cls.__disable_autologin()
        elif args.command == 'open_login_window':
            cls.__open_login_window()
        elif args.command == 'show_account_window':
            cls.__show_account_window()
        return 0

if __name__ == '__main__':
    sys.exit(KiwoomOpenApiPlusVersionUpdater.main(sys.argv[1:]))
