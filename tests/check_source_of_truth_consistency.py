#!/usr/bin/env python3
import json
import sys
from pathlib import Path

EXPECTED_RELEASE = "BEST56 BAZA MIESZKAŃ"
EXPECTED_AUDIT = "BEST56 BAZA MIESZKAŃ AUDYT"
EXPECTED_ARTIFACT = "FlippChill_Kalkulator_BEST56_BAZA_MIESZKAN.html"
EXPECTED_SHA256 = "3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92"
EXPECTED_APP_PATH = "app/FlippChill_Kalkulator.html"
EXPECTED_BEST40_PATH = "versions/FlippChill_Kalkulator_BEST40.html"
EXPECTED_BEST40_SHA256 = "c04106fe884d32dc257d852b320f2e145a93f80e5615409dc5fac17f5b171708"
EXPECTED_BLOCKERS = {7: "P0", 11: "P0"}
TERMINAL_BLOCKER_STATES = {"DONE", "CLOSED", "RESOLVED", "COMPLETED", "SUPERSEDED", "REJECTED"}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def load(path: Path) -> dict:
    if not path.is_file():
        fail(f"missing JSON file: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read {path}: {exc}")


def main() -> None:
    source = load(Path("sync/CRM_SOURCE_OF_TRUTH.json"))
    audit = load(Path("audit/BEST56_BAZA_MIESZKAN_AUDYT.json"))

    if source.get("release_target") != EXPECTED_RELEASE:
        fail("Source of Truth release_target drifted from BEST56")
    if source.get("audit_output_name") != EXPECTED_AUDIT:
        fail("Source of Truth audit output name drifted")

    policy = str(source.get("audit_version_policy", ""))
    if "BEST56" not in policy or "never increments to BEST57" not in policy:
        fail("audit version policy must keep BEST56 and prohibit BEST57 increment")

    baseline = source.get("audit_baseline", {})
    if baseline.get("artifact") != EXPECTED_ARTIFACT:
        fail("Source of Truth baseline artifact changed")
    if baseline.get("sha256") != EXPECTED_SHA256:
        fail("Source of Truth BEST56 fingerprint differs from audited baseline")
    if audit.get("artifact") != EXPECTED_ARTIFACT or audit.get("sha256") != EXPECTED_SHA256:
        fail("audit manifest and Source of Truth disagree on BEST56 baseline")
    if audit.get("audit_name") != EXPECTED_AUDIT:
        fail("audit manifest name disagrees with Source of Truth")

    gates = source.get("release_gates", {})
    if gates.get("canonical_app_path") != EXPECTED_APP_PATH:
        fail("canonical app path drifted")
    if gates.get("frozen_best40_path") != EXPECTED_BEST40_PATH:
        fail("frozen BEST40 path drifted")
    if gates.get("frozen_best40_sha256") != EXPECTED_BEST40_SHA256:
        fail("frozen BEST40 SHA-256 drifted")
    if gates.get("duplicate_dom_ids") != 0 or gates.get("broken_aria_refs") != 0 or gates.get("console_errors") != 0:
        fail("release quality gates must remain zero-tolerance")
    if gates.get("ci_required") is not True:
        fail("CI release gate must remain required")

    blockers = {}
    for blocker in source.get("current_blockers", []):
        try:
            blocker_id = int(blocker.get("id"))
        except (TypeError, ValueError):
            fail("blocker id must be numeric")
        state = str(blocker.get("status", "")).strip().upper()
        if not state:
            fail(f"blocker {blocker_id} must have a status")
        if state not in TERMINAL_BLOCKER_STATES:
            blockers[blocker_id] = blocker.get("priority")
    if blockers != EXPECTED_BLOCKERS:
        fail(f"active blocker set drifted: expected {EXPECTED_BLOCKERS}, got {blockers}")

    finance = source.get("modules", {}).get("financial_rules", {})
    if finance.get("cit") != 0.09 or finance.get("vat") != 0.23 or finance.get("agent_pit_default") != 0.12:
        fail("core tax rules drifted")
    if finance.get("slack_marketing_counts_toward_thresholds") is not True:
        fail("Slack/Marketing must count toward monthly thresholds")
    if finance.get("monthly_bonus_thresholds") != [
        {"threshold": 50000, "bonus": 0.05},
        {"threshold": 100000, "bonus": 0.10},
    ]:
        fail("monthly bonus thresholds drifted")

    print("PASS: BEST56 Source of Truth, audit manifest, release gates, blockers and finance rules are consistent")


if __name__ == "__main__":
    main()
