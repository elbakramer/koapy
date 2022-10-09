from typing import Union

from pywintypes import IID

from koapy.backend.daishin_cybos_plus.core.CybosPlusDispatch import CybosPlusDispatch
from koapy.common.DispatchProxyServiceServicer import DispatchProxyServiceServicer


class CybosPlusDispatchProxyServiceServicer(DispatchProxyServiceServicer):
    def _GetDispatch(self, iid: Union[IID, str]) -> CybosPlusDispatch:
        return CybosPlusDispatch(iid)
