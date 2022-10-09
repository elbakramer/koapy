import ast

from pathlib import Path

try:
    from ast import unparse
except ImportError:
    from astunparse import unparse

from koapy.backend.daishin_cybos_plus.core.CybosPlusTypeLibSpec import (
    CPFOREDIB_CLSID,
    CPFORETRADE_CLSID,
    CPSYSDIB_CLSID,
    CPTRADE_CLSID,
    CPUTIL_CLSID,
    DSCBO1_CLSID,
)
from koapy.common.StubGenerator import make_stub_module


def main():
    script_dir = Path(__file__).parent
    stub_dir = script_dir / ".." / "stub"
    modules = {
        "CpForeDib": CPFOREDIB_CLSID,
        "CpForeTrade": CPFORETRADE_CLSID,
        "CpSysDib": CPSYSDIB_CLSID,
        "CpTrade": CPTRADE_CLSID,
        "CpUtil": CPUTIL_CLSID,
        "DsCbo1": DSCBO1_CLSID,
    }
    for name, clsid in modules.items():
        stub_filename = f"{name}.py"
        stub_filepath = stub_dir / stub_filename
        mod = make_stub_module(clsid)
        mod = ast.fix_missing_locations(mod)
        code = unparse(mod)
        with open(stub_filepath, "w", encoding="utf-8") as f:
            f.write(code)


if __name__ == "__main__":
    main()
