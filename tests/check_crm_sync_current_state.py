#!/usr/bin/env python3
"""Guard the human CRM sync current-state section against semantic drift."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOT_PATH = ROOT / "sync" / "CRM_SOURCE_OF_TRUTH.json"
SYNC_PATH = ROOT / "sync" / "CRM_SYNC.md"
TERMINAL = {"DONE", "CLOSED", "COMPLETED", "RESOLVED", "SUPERSEDED", "REJECTED"}


def current_state_section(text: str) -> str:
    marker = "## Aktualny stan"
    start = text.find(marker)
    if start < 0:
        raise AssertionError("CRM_SYNC.md missing '## Aktualny stan'")
    next_heading = text.find("\n## ", start + len(marker))
    return text[start:] if next_heading < 0 else text[start:next_heading]


def require(haystack: str, needle: str, label: str) -> None:
    if needle not in haystack:
        raise AssertionError(f"CRM_SYNC current state missing {label}: {needle!r}")


def is_terminal(state: str) -> bool:
    upper = state.strip().upper()
    return upper in TERMINAL or upper.startswith("DONE_") or upper.startswith("SUPERSEDED_")


def main() -> int:
    sot = json.loads(SOT_PATH.read_text(encoding="utf-8"))
    section = current_state_section(SYNC_PATH.read_text(encoding="utf-8"))
    release = sot.get("release_target")
    audit = sot.get("audit_output_name")

    if release != "BEST73 BAZA MIESZKAŃ":
        raise AssertionError(f"Expected reconciled BEST73 release target, got {release!r}")
    if audit != f"{release} AUDYT":
        raise AssertionError("Source of Truth audit name must follow current release target")
    if sot.get("version_reconciliation", {}).get("status") != "RESOLVED_TO_BEST73":
        raise AssertionError("Version reconciliation must be resolved to BEST73")

    require(section, "Źródło pracy: `develop`", "develop source branch")
    require(section, "BEST73 BAZA MIESZKAŃ", "current standard")
    require(section, "P0 #20", "current canonical BEST73 blocker")
    require(section, "P0 #11", "runtime migration blocker")
    require(section, "P1 #12", "local dispatcher runtime")
    require(section, "P1 #18", "continuous multi-bot policy")
    require(section, "CIT 9%", "CIT rule")
    require(section, "VAT 23%", "VAT rule")
    require(section, "PIT agenta 12%", "agent PIT rule")
    require(section, "search bonus 10%", "search bonus rule")
    require(section, "50 000 / 100 000", "monthly threshold rule")

    active = {
        int(item["id"])
        for item in sot.get("current_blockers", [])
        if not is_terminal(str(item.get("status", "")))
    }
    if not {20, 11, 12, 18}.issubset(active):
        raise AssertionError(f"Expected active blockers 20/11/12/18, got {sorted(active)}")

    partition = sot.get("release_gates", {}).get("dependency_partition", {})
    if partition.get("canonical_task") != "P0-20-BEST73-CANONICAL-APP":
        raise AssertionError("Current canonical task must be P0-20-BEST73-CANONICAL-APP")
    if partition.get("best40_task") != "P0-7B-FROZEN-BEST40":
        raise AssertionError("Historical BEST40 task changed unexpectedly")
    if partition.get("runtime_migration_depends_only_on") != "P0-20-BEST73-CANONICAL-APP":
        raise AssertionError("Runtime migration must depend only on current canonical BEST73")

    print("CRM_SYNC current-state semantic contract: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
