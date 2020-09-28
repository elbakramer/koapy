import os
import sys
import warnings

from concurrent import futures

# https://github.com/pywinauto/pywinauto/issues/472
sys.coinit_flags = 2
warnings.simplefilter("ignore", UserWarning)

import pywinauto

from PyQt5.QtWidgets import QApplication

from koapy import KiwoomOpenApiQAxWidget
from koapy.config import config

def disable_autologin():
    app = QApplication(sys.argv)
    control = KiwoomOpenApiQAxWidget()
    module_path = control.GetAPIModulePath()
    autologin_dat = os.path.join(module_path, 'system', 'Autologin.dat')
    if os.path.exists(autologin_dat):
        os.remove(autologin_dat)

def login_semiauto(login_window):
    login_config = config.get('koapy.backend.kiwoom.login')

    userid = login_config.get('id')
    password = login_config.get('password')
    cert = login_config.get('cert')

    is_save_userid = True
    is_simulation = login_config.get('is_simulation')

    try:
        login_window.wait('ready', 10)
    except pywinauto.timings.TimeoutError:
        raise
    else:
        login_window.print_control_identifiers()

        if userid:
            login_window['Edit1'].set_text(userid)
        if password:
            login_window['Edit2'].set_text(password)
        else:
            raise RuntimeError

        if is_save_userid:
            login_window['Button6'].check()

        if not is_simulation:
            if not login_window['Edit3'].is_enabled():
                login_window['Button5'].click()
            if cert:
                login_window['Edit3'].set_text(cert)
            else:
                raise RuntimeError
        else:
            if login_window['Edit3'].is_enabled():
                login_window['Button5'].click()

        login_window['Button1'].click()

def update_version():
    desktop = pywinauto.Desktop(allow_magic_lookup=False)

    login_window = desktop.window(title='Open API Login')
    version_window = desktop.window(title='opstarter')

    app = QApplication(sys.argv)
    control = KiwoomOpenApiQAxWidget()
    control.CommConnect()

    login_semiauto(login_window)

    try:
        version_window.wait('ready', 20)
    except pywinauto.timings.TimeoutError:
        pass
    else:
        version_window.print_control_identifiers()
        version_window['Button'].click()

def enable_autologin():
    desktop = pywinauto.Desktop(allow_magic_lookup=False)

    login_window = desktop.window(title='Open API Login')

    app = QApplication(sys.argv)
    control = KiwoomOpenApiQAxWidget()
    control.CommConnect()

    login_semiauto(login_window)

    try:
        login_window.wait_not('visible', 20)
    except pywinauto.timings.TimeoutError:
        raise

    executor = futures.ThreadPoolExecutor()
    future = executor.submit(control.ShowAccountWindow)

    account_window = desktop.window(title_re=r'계좌비밀번호 입력 \(버전: [0-9].+[0-9]+\)')

    try:
        account_window.wait('ready', 3)
    except pywinauto.timings.TimeoutError:
        raise
    else:
        account_window.print_control_identifiers()
        account_window['AUTO'].check()

        account_passwords = config.get('koapy.backend.kiwoom.login.account_passwords')

        account_combo = account_window['ComboBox']
        account_cnt = account_combo.item_count()

        for i in range(account_cnt):
            account_combo.select(i)
            account_no = account_combo.selected_text().split()[0]
            if account_no in account_passwords:
                account_window['Edit'].set_text(account_passwords[account_no])
            elif '0000000000' in account_passwords:
                account_window['Edit'].set_text(account_passwords['0000000000'])
            account_window['등록'].click()

        account_window['닫기'].click()

def main():
    disable_autologin()
    update_version()
    enable_autologin()

if __name__ == '__main__':
    main()
