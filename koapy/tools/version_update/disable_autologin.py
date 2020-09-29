import os
import sys
import logging

from PyQt5.QtWidgets import QApplication

from koapy import KiwoomOpenApiQAxWidget

def disable_autologin():
    logging.info('disabling autologin')
    _app = QApplication(sys.argv)
    control = KiwoomOpenApiQAxWidget()
    module_path = control.GetAPIModulePath()
    autologin_dat = os.path.join(module_path, 'system', 'Autologin.dat')
    if os.path.exists(autologin_dat):
        logging.info('removing %s', autologin_dat)
        os.remove(autologin_dat)
        logging.info('disabled autologin')
    else:
        logging.info('autologin already disabled')

if __name__ == '__main__':
    disable_autologin()
