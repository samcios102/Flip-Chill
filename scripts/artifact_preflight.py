#!/usr/bin/env python3
"""Discover local FlippChill HTML artifacts without importing them.

The preflight is intentionally conservative. BEST40 is considered usable only
when its SHA-256 exactly matches the frozen Source-of-Truth checksum. BEST56
candidates are reported for PRIMARY to inspect; they are never auto-promoted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

EXPECTED_BEST40_SHA256 = "c04106fe884d32dc257d852b320f2e145a93f80e5615409dc5fac17f5b171708"
DEFAULT_PATTERNS = ("*.html", "*.htm")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def classify(path: Path, digest: str) -> dict:
    name = path.name.upper()
    is_best40_named = "BEST40" in name
    is_best56_named = "BEST56" in name or "BAZA_MIESZKAN" in name or "BAZA MIESZKAŃ" in name
    exact_best40 = digest == EXPECTED_BEST40_SHA256
    return {
        "path": str(path.resolve()),
        "name": path.name,
        "size": path.stat().st_size,
        "sha256": digest,
        "best40_name_hint": is_best40_named,
        "best56_name_hint": is_best56_named,
        "best40_status": "EXACT_MATCH" if exact_best40 else ("NAME_ONLY_MISMATCH" if is_best40_named else "NOT_CANDIDATE"),
    }


def discover(roots: list[Path]) -> dict:
    seen: set[Path] = set()
    candidates: list[dict] = []
    for root in roots:
        root = root.expanduser().resolve()
        if not root.exists():
            continue
        paths = [root] if root.is_file() else [p for pattern in DEFAULT_PATTERNS for p in root.rglob(pattern)]
        for path in paths:
            if not path.is_file():
                continue
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            upper = path.name.upper()
            if "FLIPPCHILL" not in upper and "BEST40" not in upper and "BEST56" not in upper and "BAZA" not in upper:
                continue
            candidates.append(classify(path, sha256(path)))

    exact = [x for x in candidates if x["best40_status"] == "EXACT_MATCH"]
    return {
        "schema_version": 1,
        "expected_best40_sha256": EXPECTED_BEST40_SHA256,
        "roots": [str(p.expanduser().resolve()) for p in roots],
        "candidate_count": len(candidates),
        "exact_best40_count": len(exact),
        "exact_best40_paths": [x["path"] for x in exact],
        "candidates": candidates,
        "safe_to_import_best40": len(exact) == 1,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("roots", nargs="*", default=["."], help="files/directories to scan recursively")
    parser.add_argument("--output", help="optional JSON output path")
    args = parser.parse_args()

    report = discover([Path(x) for x in args.roots])
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
