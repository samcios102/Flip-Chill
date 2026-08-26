#!/usr/bin/env python3
"""Local dispatcher for FlippChill AI_SYNC.

Polls AI_SYNC/TRIGGER.json. When it sees RUN_FIX + READY it builds
AI_SYNC/BOT_INBOX.md from the queued task and optionally invokes a local bot
command configured in FLIPPCHILL_BOT_COMMAND.

Command template placeholders:
  {prompt_file} {agent} {task_id}

The script intentionally does not assume a particular OpenCode CLI syntax.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
SYNC = ROOT / "AI_SYNC"
TRIGGER = SYNC / "TRIGGER.json"
QUEUE = SYNC / "BOT_QUEUE.json"
SOURCE = ROOT / "sync" / "CRM_SOURCE_OF_TRUTH.json"
AUDIT = SYNC / "LATEST_AUDIT.json"
INBOX = SYNC / "BOT_INBOX.md"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def find_task(queue: dict, task_id: str) -> dict:
    for task in queue.get("tasks", []):
        if task.get("id") == task_id:
            return task
    raise KeyError(f"task not found: {task_id}")


def build_prompt(trigger: dict, task: dict, audit: dict, source: dict) -> str:
    checks = "\n".join(f"- {x}" for x in task.get("required_checks", [])) or "- Use repository-defined checks"
    acceptance = "\n".join(f"- {x}" for x in task.get("acceptance", [])) or "- Meet issue acceptance criteria"
    scope = "\n".join(f"- `{x}`" for x in task.get("scope", [])) or "- repository scope from issue"
    return f"""# FLIPPCHILL BOT WORK ORDER

Agent: {trigger.get('target_agent')}
Task: {task.get('id')} — {task.get('title')}
Priority: {task.get('priority')}
Issue: #{task.get('issue') if task.get('issue') else 'n/a'}
Baseline: {audit.get('baseline')}
Audit artifact: {audit.get('artifact_name')}
Branch policy: develop / feature branch only; DO NOT write main.
Version policy: BEST56 BAZA MIESZKAŃ AUDYT only; DO NOT create BEST57 automatically.

## Required read-before-work
1. sync/CRM_SOURCE_OF_TRUTH.json
2. AI_SYNC/LATEST_AUDIT.json
3. AI_SYNC/BOT_QUEUE.json
4. BACKLOG.md
5. relevant GitHub issue(s)

## Scope
{scope}

## Acceptance
{acceptance}

## Required checks
{checks}

## Operating rules
- Claim only this task; do not take another agent's locked task.
- Preserve data integrity and financial semantics before UX or feature expansion.
- Make the smallest safe change that resolves root cause.
- Run deterministic tests before marking DONE.
- If blocked, record exact blocker and leave task BLOCKED instead of fabricating PASS.
- Update AI_SYNC/LATEST_AUDIT.json, AI_SYNC/LATEST_AUDIT.md, AI_SYNC/BOT_QUEUE.json and AI_SYNC/TRIGGER.json after the cycle.
- Update sync/CRM_SYNC.md / BACKLOG.md / issue when shared state changes.

## Current Source of Truth release target
{source.get('release_target')}

## Current audit summary
{json.dumps(audit.get('summary', {}), ensure_ascii=False, indent=2)}
"""


def dispatch_once(dry_run: bool = False) -> int:
    if not TRIGGER.exists() or not QUEUE.exists() or not AUDIT.exists() or not SOURCE.exists():
        print("AI_SYNC files missing; nothing dispatched", file=sys.stderr)
        return 2

    trigger = load_json(TRIGGER)
    if trigger.get("action") != "RUN_FIX" or trigger.get("status") != "READY":
        print("IDLE: no READY RUN_FIX trigger")
        return 0

    queue = load_json(QUEUE)
    audit = load_json(AUDIT)
    source = load_json(SOURCE)
    task = find_task(queue, trigger["task_id"])

    if task.get("status") not in {"READY", "OPEN"}:
        print(f"Task {task.get('id')} is {task.get('status')}; not dispatching")
        return 0

    target = trigger.get("target_agent")
    if task.get("owner") and task.get("owner") != target:
        print(f"Owner mismatch: queue={task.get('owner')} trigger={target}", file=sys.stderr)
        return 3

    prompt = build_prompt(trigger, task, audit, source)
    INBOX.write_text(prompt, encoding="utf-8")
    print(f"Prepared {INBOX.relative_to(ROOT)} for {target} / {task['id']}")

    command_template = os.environ.get("FLIPPCHILL_BOT_COMMAND", "").strip()
    if not command_template:
        print("READY: set FLIPPCHILL_BOT_COMMAND to auto-launch the local bot")
        return 0

    command = command_template.format(
        prompt_file=str(INBOX),
        agent=target,
        task_id=task["id"],
    )
    print(f"Dispatching agent {target} task {task['id']}")
    if dry_run:
        print(f"DRY RUN command: {command}")
        return 0

    completed = subprocess.run(command, shell=True, cwd=ROOT)
    return completed.returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--watch", action="store_true", help="poll trigger continuously")
    parser.add_argument("--interval", type=float, default=15.0, help="poll interval seconds")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.watch:
        return dispatch_once(args.dry_run)

    last_signature = None
    while True:
        try:
            signature = TRIGGER.read_text(encoding="utf-8") if TRIGGER.exists() else ""
            if signature != last_signature:
                dispatch_once(args.dry_run)
                last_signature = signature
        except KeyboardInterrupt:
            return 0
        except Exception as exc:
            print(f"dispatcher error: {exc}", file=sys.stderr)
        time.sleep(max(args.interval, 2.0))


if __name__ == "__main__":
    raise SystemExit(main())
