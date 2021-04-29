import os

import PySide2

QT_QPA_PLATFORM_PLUGIN_PATH = os.path.join(
    os.path.dirname(PySide2.__file__), "plugins", "platforms"
)
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QT_QPA_PLATFORM_PLUGIN_PATH

import sys

from PySide2.QtAxContainer import QAxWidget
from PySide2.QtWidgets import QApplication

app = QApplication(sys.argv)
control = QAxWidget("{A1574A0D-6BFA-4BD7-9020-DED88711818D}")

APIModulePath = control.dynamicCall("GetAPIModulePath()")

print(APIModulePath)
