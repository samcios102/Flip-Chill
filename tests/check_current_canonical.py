#!/usr/bin/env python3
import hashlib
import json
import sys
from pathlib import Path

SOURCE = Path("sync/CRM_SOURCE_OF_TRUTH.json")


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    gates = source.get("release_gates", {})
    app_path = Path(gates.get("canonical_app_path", ""))
    expected_sha = gates.get("canonical_app_expected_sha256")
    expected_standard = gates.get("canonical_app_expected_standard")
    release = source.get("release_target")

    if expected_standard != release:
        fail(f"canonical expected standard {expected_standard!r} != release target {release!r}")
    if not expected_sha or len(expected_sha) != 64:
        fail("missing valid current canonical SHA-256 in Source of Truth")
    if not app_path.is_file():
        fail(f"current canonical app missing: {app_path} (expected {release})")

    actual = hashlib.sha256(app_path.read_bytes()).hexdigest()
    if actual != expected_sha:
        fail(f"current canonical app SHA mismatch: expected {expected_sha}, got {actual}")

    print(f"PASS: current canonical app is exact {release} / {actual}")


if __name__ == "__main__":
    main()
