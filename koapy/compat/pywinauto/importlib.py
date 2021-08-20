import importlib
import sys
import warnings

from importlib.abc import Loader, MetaPathFinder

import pythoncom


class PyWinAutoFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname == "pywinauto":
            self.unregister()
            spec = importlib.util.find_spec(fullname)
            spec.loader = PyWinAutoLoader()
            return spec

    @classmethod
    def register(cls):
        sys.meta_path = [cls()] + sys.meta_path

    @classmethod
    def unregister(cls):
        sys.meta_path = [x for x in sys.meta_path if not isinstance(x, cls)]


class PyWinAutoLoader(Loader):
    def __init__(self):
        self._original_coinit_flags_defined = False
        self._original_coinit_flags = None

    def set_sys_coinit_flags(self):
        self._original_coinit_flags_defined = hasattr(sys, "coinit_flags")
        self._original_coinit_flags = getattr(sys, "coinit_flags", None)
        sys.coinit_flags = pythoncom.COINIT_APARTMENTTHREADED

    def reset_sys_coinit_flags(self):
        if not self._original_coinit_flags_defined:
            del sys.coinit_flags
        else:
            sys.coinit_flags = self._original_coinit_flags

    def create_module(self, spec):
        # set sys.coinit_flags = 2
        # check https://github.com/pywinauto/pywinauto/issues/472 for more information
        self.set_sys_coinit_flags()

        # ensure that qt binding is imported before pywinauto import
        from koapy.compat import pyside2

        # import pywinauto
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            module = importlib.import_module(spec.name)
        return module

    def exec_module(self, module):
        pass
