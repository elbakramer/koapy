import logging
import pywinauto

from koapy.config import config

is_in_development = False

set_text_userid = False
set_text_password = False
set_text_cert = False

def login_semiauto(wait_closed=False):
    logging.info('starting to login')
    login_config = config.get('koapy.backend.kiwoom.login')

    userid = login_config.get('id')
    password = login_config.get('password')
    cert = login_config.get('cert')

    is_save_userid = True
    is_simulation = login_config.get('is_simulation')

    desktop = pywinauto.Desktop(allow_magic_lookup=False)
    login_window = desktop.window(title='Open API Login')

    try:
        logging.info('waiting for login screen')
        timeout_login_screen_ready = 30
        login_window.wait('ready', timeout_login_screen_ready)
    except pywinauto.timings.TimeoutError:
        logging.info('cannot find login screen')
        raise
    else:
        logging.info('login screen found')
        if is_in_development:
            login_window.print_control_identifiers()

        if userid:
            logging.info('putting userid')
            if set_text_userid:
                login_window['Edit1'].set_text(userid)
            else:
                login_window['Edit1'].set_focus()
                pywinauto.keyboard.send_keys(userid)
                pywinauto.keyboard.send_keys('{TAB}')
        if password:
            logging.info('putting password')
            if set_text_password:
                login_window['Edit2'].set_text(password)
            else:
                login_window['Edit2'].set_focus()
                pywinauto.keyboard.send_keys(password)
                pywinauto.keyboard.send_keys('{TAB}')
        else:
            raise RuntimeError('password not set, please check config file')

        # not working properly
        if is_save_userid:
            logging.info('checking to save userid')
            login_window['Button6'].check()
        else:
            logging.info('unchecking to save userid')
            login_window['Button6'].uncheck_by_click()

        if not is_simulation:
            if not login_window['Edit3'].is_enabled():
                logging.info('unchecking to use simulation server')
                login_window['Button5'].uncheck_by_click()
            if cert:
                logging.info('putting cert password')
                if set_text_cert:
                    login_window['Edit3'].set_text(cert)
                else:
                    login_window['Edit3'].set_focus()
                    pywinauto.keyboard.send_keys(cert)
                    pywinauto.keyboard.send_keys('{TAB}')
            else:
                raise RuntimeError('cert passowrd not set, please check config file')
        else:
            if login_window['Edit3'].is_enabled():
                logging.info('checking to use simulation server')
                login_window['Button5'].check_by_click()

        logging.info('logging in')
        login_window['Button1'].click()

    if wait_closed:
        try:
            logging.info('waiting login screen to be closed')
            timeout_login_screen_closed = 30
            login_window.wait_not('visible', timeout_login_screen_closed)
        except pywinauto.timings.TimeoutError:
            logging.info('login screen is not closing')
            raise
        else:
            logging.info('login screen closed')

    return login_window

if __name__ == '__main__':
    login_semiauto(wait_closed=True)
