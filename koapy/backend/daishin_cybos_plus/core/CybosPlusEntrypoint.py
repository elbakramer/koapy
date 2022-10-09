from koapy.backend.daishin_cybos_plus.core.CybosPlusDispatch import CybosPlusDispatch
from koapy.backend.daishin_cybos_plus.core.CybosPlusEntrypointMixin import (
    CybosPlusEntrypointMixin,
)
from koapy.utils.platform import is_32bit


class CybosPlusEntrypoint(CybosPlusEntrypointMixin):

    """
    http://cybosplus.github.io/
    """

    def __init__(self):
        assert is_32bit(), "Control object should be created in 32bit environment"

    def __getitem__(self, name):
        return CybosPlusDispatch(name)
