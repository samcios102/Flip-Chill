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
REQUIRED_FINANCE = {
    "vat": ("PASS", "23%"),
    "cit": ("PASS", "0.09"),
    "pit": ("PASS", "12%"),
    "threshold_50000": ("PASS", "+5%"),
    "threshold_100000": ("PASS", "+10%"),
    "slack_marketing_thresholds": ("PASS", "source"),
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    manifest_path = Path(sys.argv[1] if len(sys.argv) > 1 else "audit/BEST56_BAZA_MIESZKAN_AUDYT.json")
    if not manifest_path.is_file():
        fail(f"missing manifest: {manifest_path}")

    data = json.loads(manifest_path.read_text(encoding="utf-8"))

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

    print("PASS: BEST56 BAZA MIESZKAŃ AUDYT manifest is internally consistent")


if __name__ == "__main__":
    main()
