#!/usr/bin/env python3
from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[1]
DISPATCHER = ROOT / "scripts" / "agent_dispatch.py"

source = DISPATCHER.read_text(encoding="utf-8")
tree = ast.parse(source)

imports_guard = any(
    isinstance(node, ast.ImportFrom)
    and node.module == "handoff_runtime_guard"
    and any(alias.name == "validate_repository_state" for alias in node.names)
    for node in tree.body
)
assert imports_guard, "agent_dispatch.py must import validate_repository_state"

claim_fn = next(
    node for node in tree.body
    if isinstance(node, ast.FunctionDef) and node.name == "claim_current_ready_task"
)
segment = ast.get_source_segment(source, claim_fn) or ""

runtime_guard_pos = segment.find("validate_repository_state()")
claim_pos = segment.find("return claim_task(queue, trigger, task)")
assert runtime_guard_pos >= 0, "runtime guard must be invoked in serialized claim path"
assert claim_pos >= 0, "claim_task call missing"
assert runtime_guard_pos < claim_pos, "runtime guard must run before READY->CLAIMED transition"
assert "if handoff_errors:" in segment, "guard errors must block dispatch"
assert 'print(f"HANDOFF BLOCKED: {error}"' in segment, "guard failure must be observable"
assert "return None" in segment[runtime_guard_pos:claim_pos], "guard failure must abort claim"

print("PASS: dispatcher invokes runtime handoff guard before claim/subprocess")
