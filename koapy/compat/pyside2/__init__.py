import os

from koapy.config import config

# Set QT_API environment variable for correct Qt backend usage
os.environ["QT_API"] = config.get("koapy.qtpy.qt_api", "pyside2")

# Import proper Qt binding using qtpy
from qtpy import *
from qtpy import PYQT5, PYSIDE2, PythonQtError

# PySide2 patch
if PYSIDE2:
    import PySide2

    if "QT_QPA_PLATFORM_PLUGIN_PATH" not in os.environ and hasattr(PySide2, "__file__"):
        QT_QPA_PLATFORM_PLUGIN_PATH = os.path.join(
            os.path.dirname(PySide2.__file__), "plugins", "platforms"
        )
        os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QT_QPA_PLATFORM_PLUGIN_PATH
