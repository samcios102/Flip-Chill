#!/usr/bin/env python3
"""Deterministic tests for scripts/handoff_runtime_guard.py."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "handoff_runtime_guard.py"
spec = importlib.util.spec_from_file_location("handoff_runtime_guard", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def fixture():
    source = {"updated_at": "2026-08-26T15:00:00+02:00"}
    queue = {
        "updated_at": "2026-08-26T15:01:00+02:00",
        "tasks": [{"id": "T1", "status": "READY", "owner": "PRIMARY"}],
    }
    audit = {
        "generated_at": "2026-08-26T15:02:00+02:00",
        "iteration": 25,
        "machine_action": {"action": "RUN_FIX", "task_id": "T1", "target_agent": "PRIMARY"},
    }
    trigger = {
        "updated_at": "2026-08-26T15:02:00+02:00",
        "source_iteration": 25,
        "action": "RUN_FIX",
        "task_id": "T1",
        "target_agent": "PRIMARY",
    }
    return source, queue, audit, trigger


def main() -> None:
    source, queue, audit, trigger = fixture()
    assert module.validate_handoff(source, queue, audit, trigger) == []

    source, queue, audit, trigger = fixture()
    trigger["updated_at"] = "2026-08-26T14:59:00+02:00"
    errors = module.validate_handoff(source, queue, audit, trigger)
    assert any("TRIGGER is older" in error for error in errors)

    source, queue, audit, trigger = fixture()
    audit["generated_at"] = "2026-08-26T14:59:00+02:00"
    errors = module.validate_handoff(source, queue, audit, trigger)
    assert any("LATEST_AUDIT is older" in error for error in errors)

    source, queue, audit, trigger = fixture()
    trigger["source_iteration"] = 24
    errors = module.validate_handoff(source, queue, audit, trigger)
    assert any("source_iteration" in error for error in errors)

    source, queue, audit, trigger = fixture()
    trigger["target_agent"] = "SECOND_AUDIT"
    errors = module.validate_handoff(source, queue, audit, trigger)
    assert any("machine_action.target_agent" in error for error in errors)
    assert any("BOT_QUEUE owner" in error for error in errors)

    source, queue, audit, trigger = fixture()
    queue["tasks"][0]["status"] = "CLAIMED"
    errors = module.validate_handoff(source, queue, audit, trigger)
    assert any("not READY" in error for error in errors)

    print("handoff runtime guard contract PASS")


if __name__ == "__main__":
    main()
