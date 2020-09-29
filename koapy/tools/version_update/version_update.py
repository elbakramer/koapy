import os
import sys
import time
import logging
import subprocess
import atexit

import pywinauto

from koapy.tools.version_update.login_semiauto import login_semiauto

is_in_development = False

def disable_autologin():
    cmd = [sys.executable, os.path.join(os.path.dirname(__file__), 'disable_autologin.py')]
    return subprocess.check_call(cmd)

def open_login_window():
    cmd = [sys.executable, os.path.join(os.path.dirname(__file__), 'open_login_window.py')]
    creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
    p = subprocess.Popen(cmd, creationflags=creationflags)
    atexit.register(p.kill)
    return p

def enable_autologin_after_version_update():
    cmd = [sys.executable, os.path.join(os.path.dirname(__file__), 'enable_autologin_after_version_update.py')]
    completed = subprocess.run(cmd, check=False)
    if completed.returncode not in [0, 3221226525]:
        raise subprocess.CalledProcessError(completed.returncode, completed.args)

def update_version():
    p = open_login_window()

    login_window = login_semiauto(wait_closed=False)

    desktop = pywinauto.Desktop(allow_magic_lookup=False)
    version_window = desktop.window(title='opstarter')

    try:
        logging.info('wating for possible version update')
        timeout_version_update = 30
        version_window.wait('ready', timeout_version_update)
    except pywinauto.timings.TimeoutError:
        logging.info('no version update required')
        logging.info('enable autologin back')
        enable_autologin_after_version_update()
        return False
    else:
        logging.info('version update required')
        if is_in_development:
            version_window.print_control_identifiers()

        logging.info('closing login app')
        p.kill()
        p.wait()
        logging.info('killed process')
        timeout_login_screen_closed = 30
        login_window.close(timeout_login_screen_closed)
        try:
            login_window.wait_not('visible', timeout_login_screen_closed)
        except pywinauto.timings.TimeoutError:
            logging.info('cannot close login window')
            raise
        else:
            logging.info('closed login window')

            logging.info('starting to update version')
            version_window['Button'].click()

            versionup_window = desktop.window(title='opversionup')
            confirm_window = desktop.window(title='업그레이드 확인')

            try:
                logging.info('wating for possible failure')
                timeout_confirm_update = 10
                versionup_window.wait('ready', timeout_confirm_update)
            except pywinauto.timings.TimeoutError:
                logging.info('cannot find confirmation popup')
            else:
                logging.info('failed update')
                raise RuntimeError

            try:
                logging.info('wating for confirmation popup after update')
                timeout_confirm_update = 10
                confirm_window.wait('ready', timeout_confirm_update)
            except pywinauto.timings.TimeoutError:
                logging.info('cannot find confirmation popup')
                raise
            else:
                logging.info('confirming update')
                confirm_window['Button'].click()

            logging.info('done update')
            return True

    return False

def main(args=()):
    disable_autologin()
    updated = update_version()
    if updated:
        time.sleep(2)
        enable_autologin_after_version_update()
    return 0

if __name__ == '__main__':
    sys.exit(main())
