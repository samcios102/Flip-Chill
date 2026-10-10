#!/usr/bin/env python3
"""Verify that AI_SYNC handoff is not older than shared state it dispatches."""

from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sync" / "CRM_SOURCE_OF_TRUTH.json"
QUEUE = ROOT / "AI_SYNC" / "BOT_QUEUE.json"
AUDIT = ROOT / "AI_SYNC" / "LATEST_AUDIT.json"
TRIGGER = ROOT / "AI_SYNC" / "TRIGGER.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_iso(value: str, label: str) -> datetime:
    if not value:
        raise AssertionError(f"missing timestamp: {label}")
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise AssertionError(f"timestamp must be timezone-aware: {label}")
    return parsed


def main() -> None:
    source = load(SOURCE)
    queue = load(QUEUE)
    audit = load(AUDIT)
    trigger = load(TRIGGER)

    source_time = parse_iso(source.get("updated_at"), "source.updated_at")
    queue_time = parse_iso(queue.get("updated_at"), "queue.updated_at")
    audit_time = parse_iso(audit.get("generated_at"), "audit.generated_at")
    trigger_time = parse_iso(trigger.get("updated_at"), "trigger.updated_at")
    shared_state_time = max(source_time, queue_time)

    if audit_time < shared_state_time:
        raise AssertionError(
            f"LATEST_AUDIT is stale: {audit_time.isoformat()} < shared state {shared_state_time.isoformat()}"
        )
    if trigger_time < shared_state_time:
        raise AssertionError(
            f"TRIGGER is stale: {trigger_time.isoformat()} < shared state {shared_state_time.isoformat()}"
        )

    if trigger.get("source_iteration") != audit.get("iteration"):
        raise AssertionError("TRIGGER.source_iteration must equal LATEST_AUDIT.iteration")

    machine = audit.get("machine_action") or {}
    for key in ("action", "task_id", "target_agent"):
        if trigger.get(key) != machine.get(key):
            raise AssertionError(f"trigger/audit machine_action mismatch for {key}")

    task = next(
        (item for item in queue.get("tasks", []) if item.get("id") == trigger.get("task_id")),
        None,
    )
    if trigger.get("action") == "RUN_FIX":
        if task is None:
            raise AssertionError("RUN_FIX trigger points to task missing from BOT_QUEUE")
        if task.get("owner") != trigger.get("target_agent"):
            raise AssertionError("RUN_FIX target_agent must equal queue task owner")
        if task.get("status") != "READY":
            raise AssertionError("RUN_FIX trigger may point only to READY task")

    print(
        "AI_SYNC freshness PASS: "
        f"shared={shared_state_time.isoformat()} audit={audit_time.isoformat()} "
        f"trigger={trigger_time.isoformat()} iteration={audit.get('iteration')}"
    )


if __name__ == "__main__":
    main()
