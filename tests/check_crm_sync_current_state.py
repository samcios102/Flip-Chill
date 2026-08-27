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


def main() -> int:
    sot = json.loads(SOT_PATH.read_text(encoding="utf-8"))
    section = current_state_section(SYNC_PATH.read_text(encoding="utf-8"))

    if sot.get("release_target") != "BEST56 BAZA MIESZKAŃ":
        raise AssertionError("Source of Truth release target drifted from BEST56")
    if sot.get("audit_output_name") != "BEST56 BAZA MIESZKAŃ AUDYT":
        raise AssertionError("Source of Truth audit name drifted from BEST56 + AUDYT")
    policy = str(sot.get("audit_version_policy", ""))
    if "never increments to BEST57" not in policy:
        raise AssertionError("Source of Truth no longer explicitly forbids automatic BEST57")

    require(section, "Źródło pracy: `develop`", "develop source branch")
    require(section, "P0 #7", "active P0 #7")
    require(section, "7A", "canonical-app partition 7A")
    require(section, "7B", "frozen-BEST40 partition 7B")
    require(section, "P0 #11", "active P0 #11")
    require(section, "P1 #12", "active P1 #12")
    require(section, "CIT 9%", "CIT rule")
    require(section, "VAT 23%", "VAT rule")
    require(section, "PIT agenta 12%", "agent PIT rule")
    require(section, "50 000 / 100 000", "monthly threshold rule")

    active = {
        int(item["id"])
        for item in sot.get("current_blockers", [])
        if str(item.get("status", "")).upper() not in TERMINAL
    }
    expected = {7, 11, 12}
    if not expected.issubset(active):
        raise AssertionError(f"Expected active blockers {sorted(expected)}, got {sorted(active)}")

    partition = sot.get("release_gates", {}).get("dependency_partition", {})
    if partition.get("canonical_task") != "P0-7A-CANONICAL-APP":
        raise AssertionError("Source of Truth canonical task is not P0-7A-CANONICAL-APP")
    if partition.get("best40_task") != "P0-7B-FROZEN-BEST40":
        raise AssertionError("Source of Truth BEST40 task is not P0-7B-FROZEN-BEST40")
    if partition.get("runtime_migration_depends_only_on") != "P0-7A-CANONICAL-APP":
        raise AssertionError("Runtime migration must depend only on P0-7A-CANONICAL-APP")

    print("CRM_SYNC current-state semantic contract: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
