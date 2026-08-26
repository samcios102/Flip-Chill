#!/usr/bin/env python3
import json
import sys
from pathlib import Path

QUEUE = Path("AI_SYNC/BOT_QUEUE.json")
CANONICAL = "P0-7A-CANONICAL-APP"
BEST40 = "P0-7B-FROZEN-BEST40"
MIGRATION = "P0-11-RUNTIME-MIGRATION"


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    data = json.loads(QUEUE.read_text(encoding="utf-8"))
    tasks = {task["id"]: task for task in data.get("tasks", [])}
    for task_id in (CANONICAL, BEST40, MIGRATION):
        if task_id not in tasks:
            fail(f"missing queue task: {task_id}")

    canonical = tasks[CANONICAL]
    best40 = tasks[BEST40]
    migration = tasks[MIGRATION]

    if canonical.get("issue") != 7 or best40.get("issue") != 7:
        fail("both release-gate subtasks must remain attached to issue #7")
    if canonical.get("owner") != "PRIMARY" or best40.get("owner") != "PRIMARY":
        fail("issue #7 release-gate subtasks must remain owned by PRIMARY")
    if migration.get("owner") != "SECOND_AUDIT":
        fail("runtime migration must remain owned by SECOND_AUDIT")

    blocked_by = migration.get("blocked_by") or []
    if blocked_by != [CANONICAL]:
        fail(f"runtime migration must depend only on canonical app; got {blocked_by}")
    if BEST40 in blocked_by:
        fail("runtime migration must not wait for historical BEST40")

    print("PASS: canonical app and historical BEST40 dependencies are partitioned safely")


if __name__ == "__main__":
    main()
