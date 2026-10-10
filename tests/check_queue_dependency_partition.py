#!/usr/bin/env python3
import json
import sys
from pathlib import Path

QUEUE = Path("AI_SYNC/BOT_QUEUE.json")
CANONICAL = "P0-20-BEST73-CANONICAL-APP"
BEST40 = "P0-7B-FROZEN-BEST40"
MIGRATION = "P0-11-RUNTIME-MIGRATION"
UI = "P1-UI-RESPONSIVE-AUDIT"
FINANCE = "P1-73-FINANCIAL-REGRESSION"


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    data = json.loads(QUEUE.read_text(encoding="utf-8"))
    tasks = {task["id"]: task for task in data.get("tasks", [])}
    for task_id in (CANONICAL, BEST40, MIGRATION, UI, FINANCE):
        if task_id not in tasks:
            fail(f"missing queue task: {task_id}")

    canonical = tasks[CANONICAL]
    best40 = tasks[BEST40]
    migration = tasks[MIGRATION]
    ui = tasks[UI]
    finance = tasks[FINANCE]

    if canonical.get("issue") != 20 or canonical.get("owner") != "PRIMARY":
        fail("current BEST73 canonical task must belong to issue #20 and PRIMARY")
    if best40.get("issue") != 7 or best40.get("owner") != "PRIMARY":
        fail("historical BEST40 task must remain attached to issue #7 and PRIMARY")
    if migration.get("owner") != "SECOND_AUDIT" or finance.get("owner") != "SECOND_AUDIT":
        fail("migration and finance verification must remain SECOND_AUDIT work")
    if ui.get("owner") != "THIRD_UI":
        fail("responsive audit must remain THIRD_UI work")

    for label, task in (("migration", migration), ("finance", finance), ("ui", ui)):
        blocked_by = task.get("blocked_by") or []
        if blocked_by != [CANONICAL]:
            fail(f"{label} must depend only on current canonical app; got {blocked_by}")
        if BEST40 in blocked_by:
            fail(f"{label} must not wait for historical BEST40")

    if canonical.get("blocked_by") not in ([], None):
        fail("current canonical BEST73 task must be dispatchable without historical blockers")

    print("PASS: current BEST73 canonical app and historical BEST40 dependencies are partitioned safely")


if __name__ == "__main__":
    main()
