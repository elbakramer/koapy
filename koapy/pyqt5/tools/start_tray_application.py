import sys

from koapy.pyqt5.KiwoomOpenApiTrayApplication import KiwoomOpenApiTrayApplication

def start_tray_application(args):
    KiwoomOpenApiTrayApplication.main(args)

if __name__ == '__main__':
    start_tray_application(sys.argv)
    