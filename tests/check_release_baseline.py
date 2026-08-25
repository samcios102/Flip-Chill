#!/usr/bin/env python3
"""Verify that a frozen release artifact matches the expected SHA-256 exactly."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def main() -> None:
    if len(sys.argv) != 3:
        fail("usage: check_release_baseline.py <file> <expected-sha256>")

    artifact = Path(sys.argv[1])
    expected = sys.argv[2].strip().lower()

    if len(expected) != 64 or any(ch not in "0123456789abcdef" for ch in expected):
        fail("expected SHA-256 must be 64 lowercase hexadecimal characters")
    if not artifact.is_file():
        fail(f"missing frozen release artifact: {artifact}")

    actual = hashlib.sha256(artifact.read_bytes()).hexdigest()
    if actual != expected:
        fail(f"SHA-256 mismatch for {artifact}: expected {expected}, got {actual}")

    print(f"PASS: frozen release artifact checksum matches {actual}")


if __name__ == "__main__":
    main()
