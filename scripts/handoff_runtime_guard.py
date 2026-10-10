#!/usr/bin/env python3
"""Runtime guard for FlippChill AI_SYNC handoff state.

Validates the exact state a local dispatcher is about to consume. This module is
side-effect free: it never claims tasks or mutates repository state.
"""

from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sync" / "CRM_SOURCE_OF_TRUTH.json"
QUEUE = ROOT / "AI_SYNC" / "BOT_QUEUE.json"
AUDIT = ROOT / "AI_SYNC" / "LATEST_AUDIT.json"
TRIGGER = ROOT / "AI_SYNC" / "TRIGGER.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_iso(value: str | None, label: str) -> datetime:
    if not value:
        raise ValueError(f"missing timestamp: {label}")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError(f"timestamp must be timezone-aware: {label}")
    return parsed


def validate_handoff(source: dict, queue: dict, audit: dict, trigger: dict) -> list[str]:
    errors: list[str] = []
    try:
        source_time = parse_iso(source.get("updated_at"), "source.updated_at")
        queue_time = parse_iso(queue.get("updated_at"), "queue.updated_at")
        audit_time = parse_iso(audit.get("generated_at"), "audit.generated_at")
        trigger_time = parse_iso(trigger.get("updated_at"), "trigger.updated_at")
        shared_time = max(source_time, queue_time)
        if audit_time < shared_time:
            errors.append("LATEST_AUDIT is older than shared Source of Truth/BOT_QUEUE state")
        if trigger_time < shared_time:
            errors.append("TRIGGER is older than shared Source of Truth/BOT_QUEUE state")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))

    if trigger.get("source_iteration") != audit.get("iteration"):
        errors.append("TRIGGER.source_iteration does not match LATEST_AUDIT.iteration")

    machine = audit.get("machine_action") or {}
    for key in ("action", "task_id", "target_agent"):
        if trigger.get(key) != machine.get(key):
            errors.append(f"TRIGGER.{key} does not match LATEST_AUDIT.machine_action.{key}")

    if trigger.get("action") == "RUN_FIX":
        task = next(
            (item for item in queue.get("tasks", []) if item.get("id") == trigger.get("task_id")),
            None,
        )
        if task is None:
            errors.append("RUN_FIX task is missing from BOT_QUEUE")
        else:
            if task.get("status") != "READY":
                errors.append("RUN_FIX task is not READY")
            if task.get("owner") != trigger.get("target_agent"):
                errors.append("RUN_FIX target_agent does not match BOT_QUEUE owner")

    return errors


def validate_repository_state() -> list[str]:
    return validate_handoff(
        load_json(SOURCE),
        load_json(QUEUE),
        load_json(AUDIT),
        load_json(TRIGGER),
    )


def main() -> int:
    try:
        errors = validate_repository_state()
    except (OSError, json.JSONDecodeError) as exc:
        print(f"HANDOFF BLOCKED: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"HANDOFF BLOCKED: {error}", file=sys.stderr)
        return 4
    print("HANDOFF RUNTIME GUARD PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
