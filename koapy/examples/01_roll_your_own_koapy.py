import sys

from koapy import KiwoomOpenApiPlusQAxWidget
from koapy.compat.pyside2.QtWidgets import QApplication

app = QApplication(sys.argv)
control = KiwoomOpenApiPlusQAxWidget()

APIModulePath = control.GetAPIModulePath()

print(APIModulePath)
