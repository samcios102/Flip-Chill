#!/usr/bin/env python3
"""Materialize canonical BEST56 app from deterministic repository artifact parts."""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import os
from pathlib import Path
import tempfile

EXPECTED_SHA256 = "3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92"
DEFAULT_PARTS_DIR = Path("artifacts/best56")
DEFAULT_OUTPUT = Path("app/FlippChill_Kalkulator.html")


def load_payload(parts_dir: Path) -> bytes:
    parts = sorted(parts_dir.glob("best56.html.gz.b64.part*"))
    if not parts:
        raise SystemExit(f"no artifact parts found in {parts_dir}")
    encoded = b"".join(p.read_bytes().strip() for p in parts)
    try:
        compressed = base64.b64decode(encoded, validate=True)
        html = gzip.decompress(compressed)
    except Exception as exc:
        raise SystemExit(f"artifact decode failed: {exc}") from exc
    actual = hashlib.sha256(html).hexdigest()
    if actual != EXPECTED_SHA256:
        raise SystemExit(f"BEST56 sha256 mismatch: expected {EXPECTED_SHA256}, got {actual}")
    return html


def atomic_write(target: Path, data: bytes) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{target.name}.", dir=str(target.parent))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, target)
    except Exception:
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--parts-dir", type=Path, default=DEFAULT_PARTS_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()

    html = load_payload(args.parts_dir)
    if not args.check_only:
        atomic_write(args.output, html)
    print(f"BEST56 EXACT_MATCH sha256={EXPECTED_SHA256} bytes={len(html)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
