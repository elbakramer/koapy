import sys
import logging
import warnings

from concurrent import futures

# https://github.com/pywinauto/pywinauto/issues/472
sys.coinit_flags = 2
warnings.simplefilter("ignore", UserWarning)

import pywinauto

from PySide2.QtWidgets import QApplication

from koapy.pyside2.KiwoomOpenApiQAxWidget import KiwoomOpenApiQAxWidget
from koapy.openapi.KiwoomOpenApiError import KiwoomOpenApiError
from koapy.config import config
from koapy.openapi.tools.version_update.login_semiauto import login_semiauto

is_in_development = False

def enable_autologin_with_control(control):
    logging.info('start enabling autologin')
    executor = futures.ThreadPoolExecutor()
    logging.info('showing account window')
    _future = executor.submit(control.ShowAccountWindow)

    desktop = pywinauto.Desktop(allow_magic_lookup=False)
    account_window = desktop.window(title_re=r'계좌비밀번호 입력 \(버전: [0-9]+.+[0-9]+\)')

    try:
        logging.info('waiting for account window to show up')
        timeout_account_window_ready = 5
        account_window.wait('ready', timeout_account_window_ready)
    except pywinauto.timings.TimeoutError:
        logging.info('cannot find account window')
        raise
    else:
        logging.info('account window found')
        if is_in_development:
            account_window.logging.info_control_identifiers()

        logging.info('enabling auto login')
        account_window['CheckBox'].check()

        account_passwords = config.get('koapy.backend.kiwoom.login.account_passwords')

        account_combo = account_window['ComboBox']
        account_cnt = account_combo.item_count()

        logging.info('putting account passwords')
        for i in range(account_cnt):
            account_combo.select(i)
            account_no = account_combo.selected_text().split()[0]
            if account_no in account_passwords:
                account_window['Edit'].set_text(account_passwords[account_no])
            elif '0000000000' in account_passwords:
                account_window['Edit'].set_text(account_passwords['0000000000'])
            account_window['등록'].click()

        logging.info('closing account window')
        account_window['닫기'].click()

        try:
            logging.info('wating account window to be closed')
            timeout_account_window_done = 5
            account_window.wait_not('visible', timeout_account_window_done)
        except pywinauto.timings.TimeoutError:
            logging.info('cannot sure account window is closed')
            raise
        else:
            logging.info('account window closed')

    executor.shutdown()

def enable_autologin_after_version_update():
    logging.info('trying to enable autologin after version update')
    app = QApplication(sys.argv)
    control = KiwoomOpenApiQAxWidget()
    if control.GetConnectState() == 0:
        def OnEventConnect(errcode):
            logging.info('logged in')
            KiwoomOpenApiError.try_or_raise(errcode)
            enable_autologin_with_control(control)
            control.OnEventConnect.disconnect(OnEventConnect)
            app.exit(errcode)
        control.OnEventConnect.connect(OnEventConnect)
        KiwoomOpenApiError.try_or_raise(control.CommConnect())
        login_semiauto(wait_closed=False)
    return app.exec_()

if __name__ == '__main__':
    sys.exit(enable_autologin_after_version_update())
