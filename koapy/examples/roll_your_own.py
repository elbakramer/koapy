import sys

from PySide2.QtWidgets import QApplication
from PySide2.QtAxContainer import QAxWidget

app = QApplication(sys.argv)
control = QAxWidget('{A1574A0D-6BFA-4BD7-9020-DED88711818D}')

print(control.dynamicCall('GetAPIModulePath()'))
