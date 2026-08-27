#!/usr/bin/env python3
import json
import math
import sys
from pathlib import Path


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def assert_close(actual: float, expected: float, label: str) -> None:
    if not math.isclose(actual, expected, rel_tol=0, abs_tol=0.01):
        fail(f"{label}: expected {expected:.2f}, got {actual:.2f}")


def load_rules() -> dict:
    path = Path("sync/CRM_SOURCE_OF_TRUTH.json")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read {path}: {exc}")
    rules = data.get("modules", {}).get("financial_rules", {})
    if not rules:
        fail("missing modules.financial_rules")
    return rules


def bonus_for_turnover(turnover: float, thresholds: list[dict]) -> float:
    bonus = 0.0
    for item in sorted(thresholds, key=lambda x: x["threshold"]):
        if turnover >= float(item["threshold"]):
            bonus = float(item["bonus"])
    return bonus


def main() -> None:
    rules = load_rules()
    vat = float(rules.get("vat", -1))
    cit = float(rules.get("cit", -1))
    pit = float(rules.get("agent_pit_default", -1))
    search_bonus = float(rules.get("search_bonus", -1))
    thresholds = rules.get("monthly_bonus_thresholds", [])

    # Tax arithmetic contracts on deliberately simple known bases.
    gross = 12300.00
    net = gross / (1.0 + vat)
    vat_amount = gross - net
    assert_close(net, 10000.00, "VAT gross->net extraction")
    assert_close(vat_amount, 2300.00, "VAT amount extraction")

    profit = 100000.00
    assert_close(max(profit, 0.0) * cit, 9000.00, "CIT 9% on positive profit")
    assert_close(max(-25000.00, 0.0) * cit, 0.00, "CIT must not become negative on loss")

    agent_tax_base = 10000.00
    assert_close(agent_tax_base * pit, 1200.00, "agent PIT default 12%")

    # Search / buyer-side bonus is a business rule, not only documentation.
    assert_close(search_bonus, 0.10, "search bonus must remain 10%")

    # Boundary tests catch off-by-one and wrong-threshold regressions.
    expected_bonus = {
        0: 0.00,
        49999: 0.00,
        50000: 0.05,
        99999: 0.05,
        100000: 0.10,
        125000: 0.10,
    }
    for turnover, expected in expected_bonus.items():
        actual = bonus_for_turnover(turnover, thresholds)
        assert_close(actual, expected, f"monthly bonus at turnover {turnover}")

    if rules.get("slack_marketing_counts_toward_thresholds") is not True:
        fail("Slack/Marketing must count toward monthly threshold turnover")

    # A Slack/Marketing transaction must be able to cross a threshold exactly
    # like any other source; source-specific pay logic must not remove turnover.
    ordinary_turnover = 45000.00
    slack_marketing_turnover = 5000.00
    combined = ordinary_turnover + slack_marketing_turnover
    assert_close(bonus_for_turnover(combined, thresholds), 0.05, "Slack/Marketing threshold contribution")

    print("PASS: executable BEST56 financial scenarios — VAT, CIT, PIT, search bonus, threshold boundaries and Slack/Marketing turnover")


if __name__ == "__main__":
    main()
