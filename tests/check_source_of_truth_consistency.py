#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

EXPECTED_APP_PATH = "app/FlippChill_Kalkulator.html"
EXPECTED_BEST40_PATH = "versions/FlippChill_Kalkulator_BEST40.html"
EXPECTED_BEST40_SHA256 = "c04106fe884d32dc257d852b320f2e145a93f80e5615409dc5fac17f5b171708"
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


def best_number(value: str) -> int:
    match = re.search(r"BEST(\d+)", value or "")
    if not match:
        fail(f"missing BEST number in {value!r}")
    return int(match.group(1))


def main() -> None:
    source = load(Path("sync/CRM_SOURCE_OF_TRUTH.json"))
    release = source.get("release_target", "")
    audit_name = source.get("audit_output_name", "")
    baseline = source.get("audit_baseline", {})
    reconciliation = source.get("version_reconciliation", {})

    if not release or not audit_name:
        fail("Source of Truth must declare release_target and audit_output_name")
    if audit_name != f"{release} AUDYT":
        fail("audit_output_name must follow the current release target with AUDYT suffix")
    if reconciliation.get("highest_verified_standard_best") != release:
        fail("release target must equal highest verified standard after reconciliation")
    if reconciliation.get("repo_release_target") != release or reconciliation.get("audit_base") != release:
        fail("version reconciliation values must agree with release target")
    if not str(reconciliation.get("status", "")).startswith("RESOLVED"):
        fail("version reconciliation must be resolved before normal current-standard work")

    policy = str(source.get("audit_version_policy", ""))
    if "never increments" not in policy and "never increment" not in policy:
        fail("audit policy must explicitly forbid creating a new BEST number from an audit alone")

    artifact = baseline.get("artifact")
    expected_artifact = f"FlippChill_Kalkulator_BEST{best_number(release)}_BAZA_MIESZKAN.html"
    if artifact != expected_artifact:
        fail(f"current baseline artifact mismatch: expected {expected_artifact}, got {artifact}")
    sha = str(baseline.get("sha256", ""))
    if len(sha) != 64:
        fail("current baseline must have a 64-character SHA-256")

    manifest_path = Path(f"audit/BEST{best_number(release)}_BAZA_MIESZKAN_AUDYT.json")
    audit = load(manifest_path)
    if audit.get("artifact") != artifact or audit.get("sha256") != sha:
        fail("current audit manifest and Source of Truth disagree on baseline artifact/SHA")
    if audit.get("audit_name") != audit_name:
        fail("current audit manifest name disagrees with Source of Truth")

    gates = source.get("release_gates", {})
    if gates.get("canonical_app_path") != EXPECTED_APP_PATH:
        fail("canonical app path drifted")
    if gates.get("canonical_app_expected_sha256") != sha:
        fail("canonical app expected SHA must match current baseline SHA")
    if gates.get("canonical_app_expected_standard") != release:
        fail("canonical app expected standard must match release target")
    if gates.get("frozen_best40_path") != EXPECTED_BEST40_PATH:
        fail("frozen BEST40 path drifted")
    if gates.get("frozen_best40_sha256") != EXPECTED_BEST40_SHA256:
        fail("frozen BEST40 SHA-256 drifted")
    if gates.get("duplicate_dom_ids") != 0 or gates.get("broken_aria_refs") != 0 or gates.get("console_errors") != 0:
        fail("release quality gates must remain zero-tolerance")
    if gates.get("ci_required") is not True:
        fail("CI release gate must remain required")

    blockers = []
    for blocker in source.get("current_blockers", []):
        state = str(blocker.get("status", "")).strip().upper()
        if blocker.get("priority") == "P0" and state not in TERMINAL_BLOCKER_STATES and not state.startswith("DONE_") and not state.startswith("SUPERSEDED_"):
            blockers.append(int(blocker["id"]))
    if not blockers:
        fail("current standard must expose at least one active P0 while canonicalization/runtime verification is pending")

    finance = source.get("modules", {}).get("financial_rules", {})
    if finance.get("cit") != 0.09 or finance.get("vat") != 0.23 or finance.get("agent_pit_default") != 0.12:
        fail("core tax rules drifted")
    if finance.get("slack_marketing_counts_toward_thresholds") is not True:
        fail("Slack/Marketing must count toward monthly thresholds")
    if finance.get("search_bonus") != 0.10:
        fail("search bonus must remain 10%")
    if finance.get("monthly_bonus_thresholds") != [
        {"threshold": 50000, "bonus": 0.05},
        {"threshold": 100000, "bonus": 0.10},
    ]:
        fail("monthly bonus thresholds drifted")

    print(f"PASS: {release} Source of Truth, current audit manifest, release gates and finance rules are consistent")


if __name__ == "__main__":
    main()
