#!/usr/bin/env python3
"""Deterministic contract test for local dispatcher READY->CLAIMED mutex."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "agent_dispatch.py"

spec = importlib.util.spec_from_file_location("agent_dispatch", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)

with tempfile.TemporaryDirectory() as tmp:
    module.DISPATCH_MUTEX = Path(tmp) / ".dispatcher_claim.lock"

    first = module.acquire_dispatch_mutex()
    assert first is not None, "first watcher must acquire mutex"
    assert module.DISPATCH_MUTEX.exists(), "mutex file must exist while claimed"

    second = module.acquire_dispatch_mutex()
    assert second is None, "second watcher must not acquire an existing mutex"

    module.release_dispatch_mutex(first)
    assert not module.DISPATCH_MUTEX.exists(), "mutex must be released after critical section"

    third = module.acquire_dispatch_mutex()
    assert third is not None, "mutex must be reusable after release"
    module.release_dispatch_mutex(third)

source = MODULE_PATH.read_text(encoding="utf-8")
required_fragments = [
    "os.O_CREAT | os.O_EXCL",
    "claim_current_ready_task",
    "trigger = load_json(TRIGGER)",
    "queue = load_json(QUEUE)",
    "finally:",
    "release_dispatch_mutex(mutex_fd)",
]
for fragment in required_fragments:
    assert fragment in source, f"missing dispatcher mutex contract fragment: {fragment}"

print("PASS dispatcher READY-to-CLAIMED mutex contract")
