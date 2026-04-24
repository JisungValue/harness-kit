#!/usr/bin/env python3

from __future__ import annotations

import runpy
import sys
from pathlib import Path


TARGET = Path(__file__).resolve().parents[1] / "bootstrap" / "scripts" / "adopt_common.py"

if str(TARGET.parent) not in sys.path:
    sys.path.insert(0, str(TARGET.parent))

if __name__ == "__main__":
    runpy.run_path(str(TARGET), run_name="__main__")
else:
    module_globals = runpy.run_path(str(TARGET))
    for key in ("__name__", "__file__", "__cached__", "__package__", "__spec__"):
        module_globals.pop(key, None)
    globals().update(module_globals)
