#!/usr/bin/env python3
"""Deterministic contract test for orphaned dispatcher mutex recovery."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "agent_dispatch.py"

spec = importlib.util.spec_from_file_location("agent_dispatch", MODULE_PATH)
assert spec and spec.loader
agent_dispatch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agent_dispatch)


def write_lock(path: Path, pid: int, age_seconds: float) -> None:
    path.write_text(f"pid={pid} claimed_at=2000-01-01T00:00:00Z\n", encoding="utf-8")
    stamp = time.time() - age_seconds
    os.utime(path, (stamp, stamp))


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        lock = Path(tmp) / ".dispatcher_claim.lock"
        agent_dispatch.DISPATCH_MUTEX = lock
        agent_dispatch.DISPATCH_MUTEX_STALE_SECONDS = 30.0

        # Old + dead PID: safe to recover and acquire.
        write_lock(lock, 999_999_999, 120.0)
        fd = agent_dispatch.acquire_dispatch_mutex()
        assert fd is not None, "old orphaned mutex should be recovered"
        raw = lock.read_text(encoding="utf-8")
        assert f"pid={os.getpid()}" in raw, "replacement mutex must belong to current process"
        agent_dispatch.release_dispatch_mutex(fd)
        assert not lock.exists(), "owned mutex should be released"

        # Fresh lock: never steal, even when recorded PID is absent.
        write_lock(lock, 999_999_999, 1.0)
        assert agent_dispatch.acquire_dispatch_mutex() is None, "fresh mutex must not be stolen"
        lock.unlink()

        # Old lock owned by a live process: never steal.
        write_lock(lock, os.getpid(), 120.0)
        assert agent_dispatch.acquire_dispatch_mutex() is None, "live-process mutex must not be stolen"
        lock.unlink()

    print("PASS: stale dispatcher mutex recovery contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
