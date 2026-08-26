#!/usr/bin/env python3
import json
import sys
from pathlib import Path

EXPECTED_BASELINE = "BEST56 BAZA MIESZKAŃ"
EXPECTED_AUDIT = "BEST56 BAZA MIESZKAŃ AUDYT"
REQUIRED_TASK_FIELDS = {"id", "priority", "owner", "status", "scope", "acceptance", "required_checks", "lock"}
ACTIVE_LOCK_STATES = {"CLAIMED", "WORKING", "TESTING"}
VALID_AGENTS = {"PRIMARY", "SECOND_AUDIT", "THIRD_UI"}
TERMINAL_BLOCKER_STATES = {"DONE", "CLOSED", "RESOLVED", "COMPLETED", "SUPERSEDED", "REJECTED"}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def load(path: str) -> dict:
    p = Path(path)
    if not p.is_file():
        fail(f"missing file: {path}")
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read {path}: {exc}")


def main() -> None:
    source = load("sync/CRM_SOURCE_OF_TRUTH.json")
    audit = load("AI_SYNC/LATEST_AUDIT.json")
    queue = load("AI_SYNC/BOT_QUEUE.json")
    trigger = load("AI_SYNC/TRIGGER.json")

    for name, data in (("audit", audit), ("queue", queue)):
        if data.get("baseline") != EXPECTED_BASELINE:
            fail(f"{name} baseline must remain BEST56")
    if audit.get("artifact_name") != EXPECTED_AUDIT or queue.get("audit_name") != EXPECTED_AUDIT:
        fail("AI_SYNC audit naming drifted from BEST56 + AUDYT")
    if "BEST57" in json.dumps({"audit": audit, "queue": queue, "trigger": trigger}, ensure_ascii=False):
        fail("automatic AI_SYNC state must not promote to BEST57")

    tasks = queue.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        fail("BOT_QUEUE must contain tasks")
    by_id = {}
    for task in tasks:
        missing = REQUIRED_TASK_FIELDS - set(task)
        if missing:
            fail(f"task {task.get('id')} missing fields: {sorted(missing)}")
        task_id = task.get("id")
        if not task_id or task_id in by_id:
            fail(f"task id missing or duplicated: {task_id}")
        owner = task.get("owner")
        if owner not in VALID_AGENTS:
            fail(f"task {task_id} has invalid owner: {owner}")
        lock = task.get("lock")
        if not isinstance(lock, dict) or "owner" not in lock or "claimed_at" not in lock:
            fail(f"task {task_id} has invalid lock")
        if task.get("status") in ACTIVE_LOCK_STATES and lock.get("owner") != owner:
            fail(f"task {task_id} active state requires lock owned by {owner}")
        if task.get("status") == "READY" and lock.get("owner") is not None:
            fail(f"READY task {task_id} must have empty lock")
        by_id[task_id] = task

    action = trigger.get("action")
    status = trigger.get("status")
    if action == "RUN_FIX" and status == "READY":
        task_id = trigger.get("task_id")
        target = trigger.get("target_agent")
        task = by_id.get(task_id)
        if task is None:
            fail("RUN_FIX trigger points to missing task")
        if task.get("status") != "READY":
            fail("RUN_FIX trigger must point to READY task")
        if task.get("owner") != target:
            fail("trigger target_agent must match task owner")
    elif action != "IDLE":
        fail(f"unsupported trigger state: action={action}, status={status}")

    source_p0 = set()
    for item in source.get("current_blockers", []):
        if item.get("priority") != "P0":
            continue
        state = str(item.get("status", "")).strip().upper()
        if not state:
            fail(f"P0 blocker {item.get('id')} must have a status")
        if state not in TERMINAL_BLOCKER_STATES:
            source_p0.add(int(item["id"]))
    audit_p0 = {int(x) for x in audit.get("summary", {}).get("active_p0", [])}
    if source_p0 != audit_p0:
        fail(f"active P0 drift: source={sorted(source_p0)}, audit={sorted(audit_p0)}")

    contract = source.get("sync_contract", {})
    expected_paths = {
        "agent_protocol_file": "AI_SYNC/PROTOCOL.md",
        "latest_audit_machine": "AI_SYNC/LATEST_AUDIT.json",
        "latest_audit_human": "AI_SYNC/LATEST_AUDIT.md",
        "bot_queue_file": "AI_SYNC/BOT_QUEUE.json",
        "trigger_file": "AI_SYNC/TRIGGER.json",
        "local_dispatcher": "scripts/agent_dispatch.py",
    }
    for key, expected in expected_paths.items():
        if contract.get(key) != expected:
            fail(f"Source of Truth sync path drifted: {key}")
        if not Path(expected).is_file():
            fail(f"declared sync path missing: {expected}")

    print("PASS: AI_SYNC report, queue, trigger, P0 state and dispatcher contract are consistent")


if __name__ == "__main__":
    main()
