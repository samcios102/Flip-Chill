#!/usr/bin/env python3
"""Stage the canonical BEST56 app only from the exact audited baseline artifact.

This script is intentionally conservative: it refuses to copy any candidate whose
SHA-256 differs from the Source-of-Truth BEST56 audit baseline. It never touches
`main`; it only prepares the working-tree path `app/FlippChill_Kalkulator.html`.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import shutil
import sys

EXPECTED_BEST56_SHA256 = "3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92"
DEFAULT_TARGET = Path("app/FlippChill_Kalkulator.html")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stage(candidate: Path, target: Path = DEFAULT_TARGET, dry_run: bool = False) -> dict:
    candidate = candidate.expanduser().resolve()
    target = target.expanduser()
    if not candidate.is_file():
        raise FileNotFoundError(f"candidate not found: {candidate}")

    candidate_sha = sha256(candidate)
    if candidate_sha != EXPECTED_BEST56_SHA256:
        raise ValueError(
            "BEST56 SHA-256 mismatch: "
            f"expected {EXPECTED_BEST56_SHA256}, got {candidate_sha} ({candidate})"
        )

    target_abs = target.resolve()
    report = {
        "candidate": str(candidate),
        "candidate_sha256": candidate_sha,
        "target": str(target_abs),
        "status": "VERIFIED_DRY_RUN" if dry_run else "STAGED",
    }
    if dry_run:
        return report

    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(target.suffix + ".tmp")
    try:
        shutil.copyfile(candidate, tmp)
        with tmp.open("rb") as fh:
            os.fsync(fh.fileno())
        staged_sha = sha256(tmp)
        if staged_sha != EXPECTED_BEST56_SHA256:
            raise RuntimeError(f"staged temp hash mismatch: {staged_sha}")
        os.replace(tmp, target)
    finally:
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass

    target_sha = sha256(target)
    if target_sha != EXPECTED_BEST56_SHA256:
        raise RuntimeError(f"canonical target hash mismatch after replace: {target_sha}")
    report["target_sha256"] = target_sha
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", help="exact BEST56 baseline HTML candidate")
    parser.add_argument("--target", default=str(DEFAULT_TARGET), help="canonical app destination")
    parser.add_argument("--dry-run", action="store_true", help="verify only; do not copy")
    args = parser.parse_args()

    try:
        report = stage(Path(args.candidate), Path(args.target), args.dry_run)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 2

    print(f"{report['status']}: {report['candidate_sha256']} -> {report['target']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
