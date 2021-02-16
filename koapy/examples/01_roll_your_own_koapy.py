import sys

from koapy.compat.pyside2.QtWidgets import QApplication
from koapy import KiwoomOpenApiPlusQAxWidget

app = QApplication(sys.argv)
control = KiwoomOpenApiPlusQAxWidget()

APIModulePath = control.GetAPIModulePath()

print(APIModulePath)
