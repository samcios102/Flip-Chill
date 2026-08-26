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
from datetime import datetime, timezone
import json
import os
from pathlib import Path
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
DISPATCH_MUTEX = SYNC / ".dispatcher_claim.lock"
DISPATCH_MUTEX_STALE_SECONDS = max(
    30.0, float(os.environ.get("FLIPPCHILL_DISPATCH_MUTEX_STALE_SECONDS", "120"))
)
DEPENDENCY_TERMINAL_STATES = {"DONE", "SUPERSEDED"}


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def save_json(path: Path, payload: dict) -> None:
    """Persist state via same-directory replace so readers never see partial JSON."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def find_task(queue: dict, task_id: str) -> dict:
    for task in queue.get("tasks", []):
        if task.get("id") == task_id:
            return task
    raise KeyError(f"task not found: {task_id}")


def unresolved_dependencies(queue: dict, task: dict) -> list[str]:
    """Return blockers that are missing or not in an explicitly resolved state."""
    blockers = []
    for dependency_id in task.get("blocked_by", []) or []:
        try:
            dependency = find_task(queue, dependency_id)
        except KeyError:
            blockers.append(f"{dependency_id}:MISSING")
            continue
        state = str(dependency.get("status") or "UNKNOWN")
        if state not in DEPENDENCY_TERMINAL_STATES:
            blockers.append(f"{dependency_id}:{state}")
    return blockers


def _parse_mutex_pid(raw: str) -> int | None:
    for token in raw.split():
        if token.startswith("pid="):
            try:
                pid = int(token.split("=", 1)[1])
            except ValueError:
                return None
            return pid if pid > 0 else None
    return None


def _process_is_alive(pid: int) -> bool:
    """Best-effort local PID liveness check using only the standard library."""
    if pid == os.getpid():
        return True
    if os.name == "nt":
        try:
            import ctypes
            from ctypes import wintypes

            process_query_limited_information = 0x1000
            still_active = 259
            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            open_process = kernel32.OpenProcess
            open_process.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
            open_process.restype = wintypes.HANDLE
            get_exit_code = kernel32.GetExitCodeProcess
            get_exit_code.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
            get_exit_code.restype = wintypes.BOOL
            close_handle = kernel32.CloseHandle
            close_handle.argtypes = [wintypes.HANDLE]
            close_handle.restype = wintypes.BOOL

            handle = open_process(process_query_limited_information, False, pid)
            if not handle:
                return False
            try:
                code = wintypes.DWORD()
                if not get_exit_code(handle, ctypes.byref(code)):
                    return True
                return code.value == still_active
            finally:
                close_handle(handle)
        except Exception:
            return True

    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    return True


def _recover_orphaned_dispatch_mutex() -> bool:
    """Remove only an old mutex whose recorded local PID is definitely gone."""
    try:
        initial_stat = DISPATCH_MUTEX.stat()
        raw = DISPATCH_MUTEX.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return False

    pid = _parse_mutex_pid(raw)
    age_seconds = max(0.0, time.time() - initial_stat.st_mtime)
    if pid is None or age_seconds < DISPATCH_MUTEX_STALE_SECONDS or _process_is_alive(pid):
        return False

    try:
        current_stat = DISPATCH_MUTEX.stat()
    except FileNotFoundError:
        return False
    fingerprint_before = (
        initial_stat.st_dev,
        initial_stat.st_ino,
        initial_stat.st_mtime_ns,
        initial_stat.st_size,
    )
    fingerprint_now = (
        current_stat.st_dev,
        current_stat.st_ino,
        current_stat.st_mtime_ns,
        current_stat.st_size,
    )
    if fingerprint_now != fingerprint_before:
        return False

    try:
        DISPATCH_MUTEX.unlink()
    except FileNotFoundError:
        return False
    print(f"Recovered orphaned dispatcher mutex from dead pid={pid} age={age_seconds:.1f}s")
    return True


def acquire_dispatch_mutex():
    """Acquire a cross-platform local mutex for the READY->CLAIMED transition."""
    for attempt in range(2):
        try:
            fd = os.open(str(DISPATCH_MUTEX), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            if attempt == 0 and _recover_orphaned_dispatch_mutex():
                continue
            return None
        payload = f"pid={os.getpid()} claimed_at={utc_now()}\n".encode("utf-8")
        try:
            os.write(fd, payload)
            os.fsync(fd)
        except Exception:
            os.close(fd)
            try:
                DISPATCH_MUTEX.unlink()
            except FileNotFoundError:
                pass
            raise
        return fd
    return None


def release_dispatch_mutex(fd) -> None:
    if fd is None:
        return
    try:
        os.close(fd)
    finally:
        try:
            DISPATCH_MUTEX.unlink()
        except FileNotFoundError:
            pass


def claim_task(queue: dict, trigger: dict, task: dict) -> str:
    """Claim exactly one READY task before launching the local bot."""
    target = trigger.get("target_agent")
    blockers = unresolved_dependencies(queue, task)
    if blockers:
        raise RuntimeError(f"task {task.get('id')} has unresolved dependencies: {', '.join(blockers)}")
    if task.get("status") != "READY":
        raise RuntimeError(f"cannot claim task in state {task.get('status')}")
    if task.get("owner") != target:
        raise RuntimeError(f"owner mismatch: queue={task.get('owner')} trigger={target}")
    lock = task.get("lock")
    if not isinstance(lock, dict) or lock.get("owner") is not None:
        raise RuntimeError(f"task {task.get('id')} already locked")

    claimed_at = utc_now()
    task["status"] = "CLAIMED"
    task["lock"] = {"owner": target, "claimed_at": claimed_at}
    trigger["status"] = "CLAIMED"
    trigger["claimed_at"] = claimed_at
    trigger["claimed_by"] = target

    save_json(QUEUE, queue)
    save_json(TRIGGER, trigger)
    return claimed_at


def claim_current_ready_task(task_id: str, target: str):
    """Serialize, reload and claim current READY state."""
    mutex_fd = acquire_dispatch_mutex()
    if mutex_fd is None:
        print("Another dispatcher is claiming work; skipping this cycle")
        return None
    try:
        trigger = load_json(TRIGGER)
        queue = load_json(QUEUE)
        if (
            trigger.get("action") != "RUN_FIX"
            or trigger.get("status") != "READY"
            or trigger.get("task_id") != task_id
            or trigger.get("target_agent") != target
        ):
            print("Dispatch state changed before claim; skipping this cycle")
            return None
        task = find_task(queue, task_id)
        blockers = unresolved_dependencies(queue, task)
        if blockers:
            print(f"Task {task_id} blocked by {', '.join(blockers)}; skipping")
            return None
        if task.get("status") != "READY":
            print(f"Task {task_id} changed to {task.get('status')} before claim; skipping")
            return None
        return claim_task(queue, trigger, task)
    finally:
        release_dispatch_mutex(mutex_fd)


def recover_failed_dispatch(task_id: str, target: str, returncode: int) -> bool:
    """Release a stale dispatcher claim after a failed bot process."""
    queue = load_json(QUEUE)
    trigger = load_json(TRIGGER)
    task = find_task(queue, task_id)
    lock = task.get("lock") if isinstance(task.get("lock"), dict) else {}

    if task.get("status") != "CLAIMED" or lock.get("owner") != target:
        return False

    failed_at = utc_now()
    task["status"] = "BLOCKED"
    task["last_error"] = {
        "type": "BOT_SUBPROCESS_EXIT",
        "returncode": returncode,
        "at": failed_at,
    }
    task["lock"] = {"owner": None, "claimed_at": None}
    save_json(QUEUE, queue)

    if (
        trigger.get("task_id") == task_id
        and trigger.get("status") == "CLAIMED"
        and trigger.get("claimed_by") == target
    ):
        trigger["action"] = "IDLE"
        trigger["status"] = "BLOCKED"
        trigger["last_error"] = {
            "type": "BOT_SUBPROCESS_EXIT",
            "returncode": returncode,
            "at": failed_at,
        }
        save_json(TRIGGER, trigger)

    return True


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

    if task.get("status") != "READY":
        print(f"Task {task.get('id')} is {task.get('status')}; not dispatching")
        return 0

    blockers = unresolved_dependencies(queue, task)
    if blockers:
        print(f"Task {task.get('id')} blocked by {', '.join(blockers)}; not dispatching", file=sys.stderr)
        return 4

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

    claimed_at = claim_current_ready_task(task["id"], target)
    if claimed_at is None:
        return 0
    print(f"Claimed {task['id']} for {target} at {claimed_at}")
    completed = subprocess.run(command, shell=True, cwd=ROOT)
    if completed.returncode != 0:
        recovered = recover_failed_dispatch(task["id"], target, completed.returncode)
        if recovered:
            print(
                f"Bot failed with exit {completed.returncode}; task {task['id']} moved to BLOCKED and claim released",
                file=sys.stderr,
            )
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
