#!/usr/bin/env python3
"""Contract checks for scripts/primary_p0_7a_one_shot.py."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "primary_p0_7a_one_shot.py"

spec = importlib.util.spec_from_file_location("primary_p0_7a_one_shot", SCRIPT)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def expect_blocked(branch: str) -> None:
    try:
        mod.assert_safe_branch(branch)
    except RuntimeError:
        return
    raise AssertionError(f"branch should be blocked: {branch}")


def main() -> int:
    expect_blocked("main")
    expect_blocked("master")
    expect_blocked("release")
    for allowed in ("develop", "feature/test", "fix/p0-7a", "audit/best56"):
        mod.assert_safe_branch(allowed)

    source = SCRIPT.read_text(encoding="utf-8")
    required = [
        "EXPECTED_SHA256",
        "package(candidate",
        "validated_parts(parts_dir)",
        "load_payload(parts_dir)",
        "git\", \"add\", \"--\"",
        "git\", \"commit\"",
        "--push requires --commit",
        "refusing P0-7A write on protected branch",
    ]
    for token in required:
        if token not in source:
            raise AssertionError(f"missing one-shot safety contract token: {token}")

    # The helper must never stage arbitrary repository changes.
    if "git\", \"add\", \".\"" in source or "[\"add\", \".\"]" in source:
        raise AssertionError("one-shot helper must not git add the entire repository")

    with tempfile.TemporaryDirectory() as td:
        parts = Path(td)
        # Empty payload is rejected before any commit path can run.
        try:
            mod.verify_payload(parts)
        except SystemExit:
            pass
        else:
            raise AssertionError("empty artifact directory must be rejected")

    print("PASS: PRIMARY P0-7A one-shot helper contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
