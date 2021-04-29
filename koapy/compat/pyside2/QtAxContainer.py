from . import PYQT5, PYSIDE2, PythonQtError

if PYQT5:
    from PyQt5.QAxContainer import *
elif PYSIDE2:
    from PySide2.QtAxContainer import *
else:
    raise PythonQtError("No Qt bindings could be found")
