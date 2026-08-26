#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "artifact_preflight.py"
spec = importlib.util.spec_from_file_location("artifact_preflight", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        fake40 = root / "FlippChill_Kalkulator_BEST40.html"
        fake40.write_text("<html>wrong historical artifact</html>", encoding="utf-8")
        fake56 = root / "FlippChill_Kalkulator_BEST56_BAZA_MIESZKAN.html"
        fake56.write_text("<html>audit candidate</html>", encoding="utf-8")

        report = mod.discover([root])
        assert report["candidate_count"] == 2, report
        assert report["exact_best40_count"] == 0, report
        assert report["safe_to_import_best40"] is False, report
        bad = next(x for x in report["candidates"] if x["name"] == fake40.name)
        assert bad["best40_status"] == "NAME_ONLY_MISMATCH", bad
        assert bad["sha256"] == hashlib.sha256(fake40.read_bytes()).hexdigest()

        # Deterministically verify exact-hash classification without needing the
        # real frozen artifact in CI: monkeypatch expected checksum to fixture.
        mod.EXPECTED_BEST40_SHA256 = hashlib.sha256(fake40.read_bytes()).hexdigest()
        exact = mod.discover([root])
        assert exact["exact_best40_count"] == 1, exact
        assert exact["safe_to_import_best40"] is True, exact
        assert Path(exact["exact_best40_paths"][0]).name == fake40.name

    print("artifact preflight safety: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
