#!/usr/bin/env python3
"""Deterministic contract test for dispatcher blocked_by enforcement."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "agent_dispatch.py"

spec = importlib.util.spec_from_file_location("agent_dispatch", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)

queue = {
    "tasks": [
        {"id": "P0-A", "status": "READY", "blocked_by": []},
        {"id": "P0-B", "status": "BLOCKED", "blocked_by": []},
        {"id": "P1-C", "status": "READY", "blocked_by": ["P0-B"]},
        {"id": "P1-D", "status": "READY", "blocked_by": ["MISSING"]},
        {"id": "P1-E", "status": "READY", "blocked_by": ["P0-A"]},
    ]
}

assert module.unresolved_dependencies(queue, queue["tasks"][0]) == []
assert module.unresolved_dependencies(queue, queue["tasks"][2]) == ["P0-B:BLOCKED"]
assert module.unresolved_dependencies(queue, queue["tasks"][3]) == ["MISSING:MISSING"]
assert module.unresolved_dependencies(queue, queue["tasks"][4]) == ["P0-A:READY"]

queue["tasks"][1]["status"] = "DONE"
assert module.unresolved_dependencies(queue, queue["tasks"][2]) == []
queue["tasks"][1]["status"] = "SUPERSEDED"
assert module.unresolved_dependencies(queue, queue["tasks"][2]) == []

source = MODULE_PATH.read_text(encoding="utf-8")
required_fragments = [
    'DEPENDENCY_TERMINAL_STATES = {"DONE", "SUPERSEDED"}',
    "def unresolved_dependencies",
    "blockers = unresolved_dependencies(queue, task)",
    "has unresolved dependencies",
    "not dispatching",
]
for fragment in required_fragments:
    assert fragment in source, f"missing dependency guard fragment: {fragment}"

print("PASS dispatcher dependency guard")
