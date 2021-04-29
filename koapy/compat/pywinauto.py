import importlib
import sys
import warnings
from importlib.abc import Loader, MetaPathFinder
from importlib.machinery import ModuleSpec

import pythoncom


class PyWinAutoFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):  # pylint: disable=unused-argument
        if fullname == "pywinauto":
            self.unregister()
            spec = importlib.util.find_spec(fullname)
            spec = ModuleSpec(
                spec.name,
                PyWinAutoLoader(),
                origin=spec.origin,
                loader_state=spec.loader_state,
                is_package=spec.submodule_search_locations is not None,
            )
            return spec

    @classmethod
    def register(cls):
        sys.meta_path = [cls()] + sys.meta_path

    @classmethod
    def unregister(cls):
        sys.meta_path = [x for x in sys.meta_path if not isinstance(x, cls)]


class PyWinAutoLoader(Loader):  # pylint: disable=abstract-method
    def __init__(self):
        self._original_has_coinit_flags = False
        self._original_coinit_flags = None

    def set_sys_coinit_flags(self):
        self._original_has_coinit_flags = hasattr(sys, "coinit_flags")
        self._original_coinit_flags = getattr(sys, "coinit_flags", None)
        sys.coinit_flags = pythoncom.COINIT_APARTMENTTHREADED

    def reset_sys_coinit_flags(self):
        if not self._original_has_coinit_flags:
            del sys.coinit_flags
        else:
            sys.coinit_flags = self._original_coinit_flags

    def create_module(self, spec):
        # https://github.com/pywinauto/pywinauto/issues/472
        self.set_sys_coinit_flags()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            PyWinAutoFinder.unregister()
            module = importlib.import_module(spec.name)
        return module

    def exec_module(self, module):
        pass
