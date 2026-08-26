#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "stage_canonical_app.py"
EXPECTED = "3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92"

spec = importlib.util.spec_from_file_location("stage_canonical_app", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)

assert module.EXPECTED_BEST56_SHA256 == EXPECTED, "BEST56 stager checksum drift"

with tempfile.TemporaryDirectory() as tmpdir:
    root = Path(tmpdir)
    candidate = root / "candidate.html"
    target = root / "app" / "FlippChill_Kalkulator.html"
    candidate.write_bytes(b"<html><title>fixture</title></html>\n")
    fixture_sha = hashlib.sha256(candidate.read_bytes()).hexdigest()

    original_expected = module.EXPECTED_BEST56_SHA256
    module.EXPECTED_BEST56_SHA256 = fixture_sha
    try:
        dry = module.stage(candidate, target, dry_run=True)
        assert dry["status"] == "VERIFIED_DRY_RUN"
        assert not target.exists(), "dry-run must not write target"

        staged = module.stage(candidate, target)
        assert staged["status"] == "STAGED"
        assert target.read_bytes() == candidate.read_bytes()
        assert staged["target_sha256"] == fixture_sha

        bad = root / "bad.html"
        bad.write_bytes(b"different")
        try:
            module.stage(bad, target)
        except ValueError:
            pass
        else:
            raise AssertionError("mismatched candidate must be rejected")

        # Auto-discovery accepts only exact SHA and deterministically returns the
        # lexicographically first exact match if the same audited bytes exist twice.
        search_a = root / "a"
        search_b = root / "b"
        search_a.mkdir()
        search_b.mkdir()
        exact_b = search_b / "FlippChill_Kalkulator_BEST56_BAZA_MIESZKAN.html"
        exact_a = search_a / "copy.html"
        exact_b.write_bytes(candidate.read_bytes())
        exact_a.write_bytes(candidate.read_bytes())
        (search_a / "near_match.html").write_bytes(b"not exact")

        discovered = module.discover_exact([search_b, search_a])
        expected_first = sorted([exact_a.resolve(), exact_b.resolve()], key=lambda p: str(p).lower())[0]
        assert discovered["candidate"] == expected_first
        assert discovered["candidate_sha256"] == fixture_sha
        assert len(discovered["matches"]) == 2
        assert discovered["scanned"] >= 3

        empty = root / "empty"
        empty.mkdir()
        try:
            module.discover_exact([empty])
        except FileNotFoundError:
            pass
        else:
            raise AssertionError("auto-discovery must block when exact BEST56 is absent")
    finally:
        module.EXPECTED_BEST56_SHA256 = original_expected

print("canonical app staging + auto-discovery contract: PASS")
