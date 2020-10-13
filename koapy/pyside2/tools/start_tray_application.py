import sys

from koapy.pyside2.KiwoomOpenApiTrayApplication import KiwoomOpenApiTrayApplication

def start_tray_application(args):
    KiwoomOpenApiTrayApplication.main(args)

if __name__ == '__main__':
    start_tray_application(sys.argv)
