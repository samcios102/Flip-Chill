#!/usr/bin/env python3
"""Deterministic runtime check: dispatcher must claim before bot execution."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import sys
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
            "task_id": "TEST-TASK",
            "target_agent": "PRIMARY"
        })
        write_json(dispatch.QUEUE, {
            "tasks": [{
                "id": "TEST-TASK",
                "title": "claim check",
                "priority": "P1",
                "status": "READY",
                "owner": "PRIMARY",
                "scope": ["test"],
                "acceptance": ["claimed before execution"],
                "required_checks": ["runtime claim"],
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
        os.environ["FLIPPCHILL_BOT_COMMAND"] = "echo dispatched"
        try:
            rc = dispatch.dispatch_once(dry_run=False)
        finally:
            if old_command is None:
                os.environ.pop("FLIPPCHILL_BOT_COMMAND", None)
            else:
                os.environ["FLIPPCHILL_BOT_COMMAND"] = old_command

        if rc != 0:
            raise SystemExit(f"FAIL: dispatcher command returned {rc}")

        queue = json.loads(dispatch.QUEUE.read_text(encoding="utf-8"))
        trigger = json.loads(dispatch.TRIGGER.read_text(encoding="utf-8"))
        task = queue["tasks"][0]

        if task.get("status") != "CLAIMED":
            raise SystemExit("FAIL: task was not CLAIMED before execution")
        if task.get("lock", {}).get("owner") != "PRIMARY":
            raise SystemExit("FAIL: task lock owner was not persisted")
        if not task.get("lock", {}).get("claimed_at"):
            raise SystemExit("FAIL: task claimed_at was not persisted")
        if trigger.get("status") != "CLAIMED":
            raise SystemExit("FAIL: trigger was not moved to CLAIMED")
        if trigger.get("claimed_by") != "PRIMARY" or not trigger.get("claimed_at"):
            raise SystemExit("FAIL: trigger claim metadata missing")
        if not dispatch.INBOX.is_file():
            raise SystemExit("FAIL: BOT_INBOX.md was not generated")

    print("PASS: dispatcher claims and locks READY task before local bot execution")


if __name__ == "__main__":
    main()
