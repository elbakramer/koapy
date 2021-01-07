import win32com.client

from pywintypes import com_error as ComError # pylint: disable=no-name-in-module

from koapy.backend.cybos.CybosPlusComObjectMixin import CybosPlusComObjectMixin
from koapy.backend.cybos.CybosPlusBlockRequestRateLimiter import CybosPlusBlockRequestRateLimiter
from koapy.backend.cybos.CybosPlusBlockRequestError import CybosPlusBlockRequestError

class CybosPlusComObjectDispatch:

    def __init__(self, dispatch):
        self._dispatch = dispatch

    @CybosPlusBlockRequestRateLimiter()
    def RateLimitedBlockRequest(self):
        return CybosPlusBlockRequestError.try_or_raise(
            self._dispatch.BlockRequest()
        )

    def __getattr__(self, name):
        return getattr(self._dispatch, name)

class CybosPlusComObjectInner:

    def __init__(self, parent, prefix):
        self._parent = parent
        self._prefix = prefix
        self._dispatches = {}

    def __getattr__(self, name):
        dispatch = self._dispatches.get(name)
        if dispatch is None:
            try:
                dispatch = win32com.client.Dispatch('%s.%s' % (self._prefix, name))
            except ComError:
                if len(self._dispatches) == 0:
                    del self._parent._inners[self._prefix]
                raise
            else:
                dispatch = CybosPlusComObjectDispatch(dispatch)
                self._dispatches[name] = dispatch
        return dispatch

class CybosPlusComObject(CybosPlusComObjectMixin):

    """
    http://cybosplus.github.io/
    """

    def __init__(self):
        self._inners = {}

    def __getattr__(self, name):
        if name.startswith('Cp') or name.startswith('Ds'):
            return self._inners.setdefault(name, CybosPlusComObjectInner(self, name))
        raise AttributeError

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return
