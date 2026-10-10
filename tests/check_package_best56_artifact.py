#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import package_best56_artifact as packager  # noqa: E402


def main() -> int:
    exact = ("<!doctype html><title>BEST56 BAZA MIESZKAN</title>\n" * 512).encode("utf-8")
    exact_sha = hashlib.sha256(exact).hexdigest()
    original_expected = packager.EXPECTED_BEST56_SHA256
    packager.EXPECTED_BEST56_SHA256 = exact_sha
    try:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            candidate = root / "FlippChill_Kalkulator_BEST56_BAZA_MIESZKAN.html"
            candidate.write_bytes(exact)
            parts = root / "parts"

            report1 = packager.package(candidate, parts, part_size=2048)
            snapshot1 = {p.name: p.read_bytes() for p in sorted(parts.iterdir())}
            report2 = packager.package(candidate, parts, part_size=2048)
            snapshot2 = {p.name: p.read_bytes() for p in sorted(parts.iterdir())}

            assert report1["status"] == "PACKAGED_EXACT_BEST56"
            assert report1["candidate_sha256"] == exact_sha
            assert report1["roundtrip_sha256"] == exact_sha
            assert report2["roundtrip_sha256"] == exact_sha
            assert snapshot1 == snapshot2, "gzip+base64 payload must be deterministic"
            assert all(len(data.rstrip(b"\n")) <= 2048 for data in snapshot2.values())

            restored, restored_sha = packager._roundtrip(parts)
            assert restored == exact
            assert restored_sha == exact_sha

            near_match = root / "near.html"
            near_match.write_bytes(exact + b"<!-- changed -->")
            try:
                packager.package(near_match, root / "bad")
            except ValueError as exc:
                assert "SHA-256 mismatch" in str(exc)
            else:
                raise AssertionError("near-match artifact must be rejected")

        print("BEST56 artifact packager contract PASS")
        return 0
    finally:
        packager.EXPECTED_BEST56_SHA256 = original_expected


if __name__ == "__main__":
    raise SystemExit(main())
