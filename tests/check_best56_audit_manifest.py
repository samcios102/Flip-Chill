#!/usr/bin/env python3
import hashlib
import json
import re
import sys
from pathlib import Path

EXPECTED_NAME = "BEST56 BAZA MIESZKAŃ AUDYT"
EXPECTED_ARTIFACT = "FlippChill_Kalkulator_BEST56_BAZA_MIESZKAN.html"
EXPECTED_SHA256 = "3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92"
EXPECTED_SIZE = 857840
EXPECTED_LINES = 5799
EXPECTED_MIGRATION_ITERATION = "audit/BEST56_BAZA_MIESZKAN_AUDYT_ITERACJA_5.json"
REQUIRED_FINANCE = {
    "vat": ("PASS", "23%"),
    "cit": ("PASS", "0.09"),
    "pit": ("PASS", "12%"),
    "threshold_50000": ("PASS", "+5%"),
    "threshold_100000": ("PASS", "+10%"),
    "slack_marketing_thresholds": ("PASS", "source"),
}
REQUIRED_MIGRATION_PRESERVATION = (
    "manual_preliminaryDate_preserved",
    "status_derived_as_preliminary",
    "id_preserved",
    "startDate_preserved",
    "maxDealDate_preserved",
    "paymentParts_preserved",
)


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path) -> dict:
    if not path.is_file():
        fail(f"missing manifest: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read JSON manifest {path}: {exc}")


def check_migration_contract(path: Path) -> None:
    data = load_json(path)
    if data.get("artifact") != EXPECTED_NAME:
        fail("migration audit artifact must remain BEST56 BAZA MIESZKAŃ AUDYT")
    if data.get("baseline") != "BEST56 BAZA MIESZKAŃ":
        fail("migration audit baseline changed")
    if data.get("release_state") != "AUDIT CANDIDATE ONLY":
        fail("migration result must remain audit-only until canonical runtime validation")

    policy = str(data.get("release_policy", ""))
    if "version 56" not in policy or "no BEST57 promotion" not in policy:
        fail("migration audit release policy must keep BEST56 and prohibit BEST57 promotion")

    finding = data.get("finding", {})
    if finding.get("priority") != "P0" or finding.get("issue") != 11:
        fail("migration preservation finding must remain linked to P0 #11")
    if finding.get("source_candidate_contains_unsafe_clear") is not True:
        fail("audit must record the unsafe source migration expression")
    if "preliminaryDate" not in str(finding.get("unsafe_expression", "")):
        fail("unsafe migration expression fingerprint changed")

    contract = data.get("migration_contract_test", {})
    if contract.get("schema_from") != 11 or contract.get("schema_to") != 12:
        fail("unexpected migration schema contract")
    for key in REQUIRED_MIGRATION_PRESERVATION:
        if contract.get(key) is not True:
            fail(f"migration contract lost required preservation assertion: {key}")
    if contract.get("result") != "PASS":
        fail("schema 11→12 migration preservation contract is not PASS")


def main() -> None:
    manifest_path = Path(sys.argv[1] if len(sys.argv) > 1 else "audit/BEST56_BAZA_MIESZKAN_AUDYT.json")
    migration_path = Path(sys.argv[2] if len(sys.argv) > 2 else EXPECTED_MIGRATION_ITERATION)
    data = load_json(manifest_path)

    if data.get("audit_name") != EXPECTED_NAME:
        fail("audit_name must remain BEST56 BAZA MIESZKAŃ AUDYT")
    if data.get("artifact") != EXPECTED_ARTIFACT:
        fail("unexpected BEST56 audit artifact name")

    policy = str(data.get("version_policy", ""))
    if "keep BEST56" not in policy or "never increment to BEST57 automatically" not in policy:
        fail("version policy must keep BEST56 and prohibit automatic BEST57")

    sha = str(data.get("sha256", ""))
    if not re.fullmatch(r"[0-9a-f]{64}", sha) or sha != EXPECTED_SHA256:
        fail("BEST56 audit SHA-256 fingerprint changed")
    if data.get("size_bytes") != EXPECTED_SIZE or data.get("lines") != EXPECTED_LINES:
        fail("BEST56 audit size/line fingerprint changed")

    static = data.get("static_checks", {})
    if static.get("script_blocks") != static.get("script_blocks_node_check_passed"):
        fail("not all JavaScript blocks passed node --check")
    if static.get("static_dom_ids") != static.get("unique_static_dom_ids"):
        fail("static DOM IDs are not unique")
    if static.get("duplicate_static_dom_ids") != 0:
        fail("duplicate static DOM IDs detected")
    if static.get("missing_static_references") != 0:
        fail("missing static DOM references detected")

    finance = data.get("finance_checks", {})
    for key, required_tokens in REQUIRED_FINANCE.items():
        value = str(finance.get(key, ""))
        if not all(token in value for token in required_tokens):
            fail(f"finance audit check {key} lost required assertion")

    if data.get("status") != "AUDITED_STATICALLY":
        fail("unexpected BEST56 audit status")

    check_migration_contract(migration_path)
    print("PASS: BEST56 BAZA MIESZKAŃ AUDYT manifest and schema 11→12 preservation contract are consistent")


if __name__ == "__main__":
    main()
