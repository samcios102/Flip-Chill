#!/usr/bin/env python3
"""Deterministic runtime check: failed bot subprocess must not leave stale CLAIMED state."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "agent_dispatch.py"


def load_dispatcher():
    spec = importlib.util.spec_from_file_location("agent_dispatch", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load agent_dispatch.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    dispatch = load_dispatcher()

    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        sync = root / "AI_SYNC"
        source_dir = root / "sync"
        sync.mkdir()
        source_dir.mkdir()

        dispatch.ROOT = root
        dispatch.SYNC = sync
        dispatch.TRIGGER = sync / "TRIGGER.json"
        dispatch.QUEUE = sync / "BOT_QUEUE.json"
        dispatch.SOURCE = source_dir / "CRM_SOURCE_OF_TRUTH.json"
        dispatch.AUDIT = sync / "LATEST_AUDIT.json"
        dispatch.INBOX = sync / "BOT_INBOX.md"

        write_json(dispatch.TRIGGER, {
            "action": "RUN_FIX",
            "status": "READY",
            "task_id": "FAIL-TASK",
            "target_agent": "PRIMARY"
        })
        write_json(dispatch.QUEUE, {
            "tasks": [{
                "id": "FAIL-TASK",
                "title": "failure recovery check",
                "priority": "P1",
                "status": "READY",
                "owner": "PRIMARY",
                "scope": ["test"],
                "acceptance": ["failed subprocess releases stale claim"],
                "required_checks": ["failure recovery"],
                "lock": {"owner": None, "claimed_at": None}
            }]
        })
        write_json(dispatch.SOURCE, {"release_target": "BEST56 BAZA MIESZKAŃ"})
        write_json(dispatch.AUDIT, {
            "baseline": "BEST56 BAZA MIESZKAŃ",
            "artifact_name": "BEST56 BAZA MIESZKAŃ AUDYT",
            "summary": {}
        })

        old_command = os.environ.get("FLIPPCHILL_BOT_COMMAND")
        os.environ["FLIPPCHILL_BOT_COMMAND"] = 'python -c "import sys; sys.exit(7)"'
        try:
            rc = dispatch.dispatch_once(dry_run=False)
        finally:
            if old_command is None:
                os.environ.pop("FLIPPCHILL_BOT_COMMAND", None)
            else:
                os.environ["FLIPPCHILL_BOT_COMMAND"] = old_command

        if rc != 7:
            raise SystemExit(f"FAIL: expected subprocess return 7, got {rc}")

        queue = json.loads(dispatch.QUEUE.read_text(encoding="utf-8"))
        trigger = json.loads(dispatch.TRIGGER.read_text(encoding="utf-8"))
        task = queue["tasks"][0]

        if task.get("status") != "BLOCKED":
            raise SystemExit("FAIL: failed subprocess did not move task to BLOCKED")
        if task.get("lock") != {"owner": None, "claimed_at": None}:
            raise SystemExit("FAIL: failed subprocess did not release task lock")
        error = task.get("last_error", {})
        if error.get("type") != "BOT_SUBPROCESS_EXIT" or error.get("returncode") != 7:
            raise SystemExit("FAIL: task failure metadata missing")
        if trigger.get("action") != "IDLE" or trigger.get("status") != "BLOCKED":
            raise SystemExit("FAIL: trigger did not become IDLE/BLOCKED")
        trigger_error = trigger.get("last_error", {})
        if trigger_error.get("returncode") != 7:
            raise SystemExit("FAIL: trigger failure metadata missing")

    print("PASS: failed local bot subprocess releases claim and records BLOCKED state")


if __name__ == "__main__":
    main()
