import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QAxContainer import QAxWidget

app = QApplication(sys.argv)
control = QAxWidget('{A1574A0D-6BFA-4BD7-9020-DED88711818D}')

APIModulePath = control.dynamicCall('GetAPIModulePath()')

print(APIModulePath)
