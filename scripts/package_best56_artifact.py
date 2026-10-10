#!/usr/bin/env python3
"""Package the exact audited BEST56 HTML into deterministic repository parts.

The packager accepts either an explicit candidate or the same bounded auto-discovery
used by the canonical stager. It refuses every non-exact artifact, gzip-compresses
with mtime=0 for deterministic bytes, base64-encodes the result, writes fixed-size
parts atomically, then performs a full round-trip SHA-256 verification.
"""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import os
from pathlib import Path
import tempfile

from stage_canonical_app import EXPECTED_BEST56_SHA256, discover_exact, sha256

DEFAULT_PARTS_DIR = Path("artifacts/best56")
DEFAULT_PART_SIZE = 64 * 1024
PART_PREFIX = "best56.html.gz.b64.part"


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass
        raise


def deterministic_payload(html: bytes) -> bytes:
    return base64.b64encode(gzip.compress(html, compresslevel=9, mtime=0))


def _roundtrip(parts_dir: Path) -> tuple[bytes, str]:
    parts = sorted(parts_dir.glob(f"{PART_PREFIX}*"))
    if not parts:
        raise RuntimeError(f"no payload parts found in {parts_dir}")
    encoded = b"".join(part.read_bytes().strip() for part in parts)
    html = gzip.decompress(base64.b64decode(encoded, validate=True))
    return html, hashlib.sha256(html).hexdigest()


def package(candidate: Path, parts_dir: Path = DEFAULT_PARTS_DIR, part_size: int = DEFAULT_PART_SIZE) -> dict:
    candidate = candidate.expanduser().resolve()
    if not candidate.is_file():
        raise FileNotFoundError(f"candidate not found: {candidate}")
    if part_size < 1024:
        raise ValueError("part size must be at least 1024 bytes")

    candidate_sha = sha256(candidate)
    if candidate_sha != EXPECTED_BEST56_SHA256:
        raise ValueError(
            "BEST56 SHA-256 mismatch: "
            f"expected {EXPECTED_BEST56_SHA256}, got {candidate_sha} ({candidate})"
        )

    html = candidate.read_bytes()
    payload = deterministic_payload(html)
    chunks = [payload[i : i + part_size] for i in range(0, len(payload), part_size)]
    if not chunks:
        raise RuntimeError("empty payload")

    parts_dir.mkdir(parents=True, exist_ok=True)
    old_parts = list(parts_dir.glob(f"{PART_PREFIX}*"))
    expected_names = {f"{PART_PREFIX}{idx:03d}" for idx in range(1, len(chunks) + 1)}

    for idx, chunk in enumerate(chunks, 1):
        _atomic_write(parts_dir / f"{PART_PREFIX}{idx:03d}", chunk + b"\n")

    for old in old_parts:
        if old.name not in expected_names:
            old.unlink()

    restored, restored_sha = _roundtrip(parts_dir)
    if restored != html or restored_sha != EXPECTED_BEST56_SHA256:
        raise RuntimeError(f"round-trip SHA mismatch: {restored_sha}")

    return {
        "candidate": str(candidate),
        "candidate_sha256": candidate_sha,
        "parts_dir": str(parts_dir.resolve()),
        "parts": len(chunks),
        "encoded_bytes": len(payload),
        "roundtrip_sha256": restored_sha,
        "status": "PACKAGED_EXACT_BEST56",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", nargs="?", help="exact BEST56 baseline HTML")
    parser.add_argument("--auto", action="store_true", help="discover exact BEST56 by SHA-256")
    parser.add_argument("--search-root", action="append", default=[], help="root used by --auto; may repeat")
    parser.add_argument("--parts-dir", default=str(DEFAULT_PARTS_DIR))
    parser.add_argument("--part-size", type=int, default=DEFAULT_PART_SIZE)
    args = parser.parse_args()

    if bool(args.candidate) == bool(args.auto):
        parser.error("choose exactly one: explicit candidate or --auto")

    try:
        candidate = Path(args.candidate) if args.candidate else discover_exact(
            [Path(p) for p in args.search_root] or None
        )["candidate"]
        report = package(candidate, Path(args.parts_dir), args.part_size)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"BLOCKED: {exc}")
        return 2

    print(
        f"{report['status']}: sha256={report['candidate_sha256']} "
        f"parts={report['parts']} encoded_bytes={report['encoded_bytes']} dir={report['parts_dir']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
