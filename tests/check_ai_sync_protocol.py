#!/usr/bin/env python3
import json
import sys
from pathlib import Path

REQUIRED_TASK_FIELDS = {"id", "priority", "owner", "status", "scope", "acceptance", "required_checks", "blocked_by", "lock"}
ACTIVE_LOCK_STATES = {"CLAIMED", "WORKING", "TESTING"}
VALID_AGENTS = {"PRIMARY", "SECOND_AUDIT", "THIRD_UI"}
TERMINAL_BLOCKER_STATES = {"DONE", "CLOSED", "RESOLVED", "COMPLETED", "SUPERSEDED", "REJECTED"}
REQUIRED_READ_ORDER = [
    "sync/CRM_SOURCE_OF_TRUTH.json",
    "AI_SYNC/PROTOCOL.md",
    "AI_SYNC/LATEST_AUDIT.json",
    "AI_SYNC/BOT_QUEUE.json",
    "AI_SYNC/TRIGGER.json",
    "sync/CRM_SYNC.md",
    "BACKLOG.md",
]


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


def assert_read_order(path: str, label: str) -> None:
    text_path = Path(path)
    if not text_path.is_file():
        fail(f"missing {label}: {path}")
    text = text_path.read_text(encoding="utf-8")
    positions = []
    for item in REQUIRED_READ_ORDER:
        marker = f"`{item}`"
        pos = text.find(marker)
        if pos < 0:
            fail(f"{label} missing required read-order entry: {item}")
        positions.append(pos)
    if positions != sorted(positions):
        fail(f"{label} read-order entries are not in canonical order")


def is_terminal_source_state(state: str) -> bool:
    upper = state.strip().upper()
    return upper in TERMINAL_BLOCKER_STATES or upper.startswith("DONE_") or upper.startswith("SUPERSEDED_")


def main() -> None:
    source = load("sync/CRM_SOURCE_OF_TRUTH.json")
    audit = load("AI_SYNC/LATEST_AUDIT.json")
    queue = load("AI_SYNC/BOT_QUEUE.json")
    trigger = load("AI_SYNC/TRIGGER.json")

    expected_baseline = source.get("release_target")
    expected_audit = source.get("audit_output_name")
    if not expected_baseline or not expected_audit:
        fail("Source of Truth must declare current release/audit names")
    for name, data in (("audit", audit), ("queue", queue)):
        if data.get("baseline") != expected_baseline:
            fail(f"{name} baseline must match Source of Truth: {expected_baseline}")
    if audit.get("artifact_name") != expected_audit or queue.get("audit_name") != expected_audit:
        fail("AI_SYNC audit naming must match current Source of Truth")

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
        state = str(item.get("status", ""))
        if not state:
            fail(f"P0 blocker {item.get('id')} must have a status")
        if not is_terminal_source_state(state):
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

    if contract.get("required_read_order") != REQUIRED_READ_ORDER:
        fail("canonical read order drifted")

    reconciliation = source.get("version_reconciliation", {})
    if reconciliation.get("audit_base") != expected_baseline:
        fail("AI_SYNC may not run against a baseline different from reconciled audit_base")

    assert_read_order("AI_SYNC/PROTOCOL.md", "AI_SYNC protocol")
    assert_read_order("OPENCODE.md", "OpenCode entrypoint")

    print("PASS: AI_SYNC report, queue, trigger, current standard, read order, P0 state and dispatcher contract are consistent")


if __name__ == "__main__":
    main()
