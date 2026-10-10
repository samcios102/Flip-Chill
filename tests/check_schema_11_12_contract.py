#!/usr/bin/env python3
"""Executable business-contract fixtures for BEST56 schema 11→12 migration.

This does not replace runtime/localStorage validation of the canonical app. It freezes
what the migration is allowed to do, so a later implementation test has an explicit
oracle for data preservation and status normalization.
"""
from copy import deepcopy


def migrate_contract(record: dict) -> dict:
    item = deepcopy(record)
    # Contract: existing business dates win over stale status metadata.
    if item.get("finalDate"):
        item["status"] = "closed"
    elif item.get("preliminaryDate"):
        item["status"] = "preliminary"
    return item


def assert_preserved(before: dict, after: dict, keys: tuple[str, ...]) -> None:
    for key in keys:
        assert after.get(key) == before.get(key), f"{key} changed during migration"


def main() -> None:
    common = {
        "id": "tx-56-audit",
        "startDate": "2026-08-01",
        "maxDealDate": "2026-12-31",
        "property": "Warszawa, Testowa 56/12",
        "clientName": "Klient Testowy",
        "agent": "Agent Testowy",
        "commissionGross": 24600,
        "source": "Slack / Marketing",
        "settlementStatus": "unsettled",
        "notes": "manual business note",
        "paymentParts": [
            {"kind": "preliminary", "clientPaid": True, "agentPaid": False},
            {"kind": "sellerFinal", "clientPaid": False, "agentPaid": False},
            {"kind": "buyerFinal", "clientPaid": False, "agentPaid": False},
            {"kind": "other", "clientPaid": False, "agentPaid": False},
        ],
    }
    preserved_business_keys = (
        "id",
        "startDate",
        "preliminaryDate",
        "finalDate",
        "maxDealDate",
        "property",
        "clientName",
        "agent",
        "commissionGross",
        "source",
        "settlementStatus",
        "notes",
        "paymentParts",
    )

    ongoing_with_preliminary = {
        **common,
        "status": "ongoing",
        "preliminaryDate": "2026-09-15",
        "finalDate": "",
    }
    migrated = migrate_contract(ongoing_with_preliminary)
    assert migrated["status"] == "preliminary"
    assert_preserved(ongoing_with_preliminary, migrated, preserved_business_keys)

    stale_status_with_final = {
        **common,
        "id": "tx-56-final",
        "status": "ongoing",
        "preliminaryDate": "2026-09-15",
        "finalDate": "2026-10-20",
    }
    migrated = migrate_contract(stale_status_with_final)
    assert migrated["status"] == "closed"
    assert_preserved(stale_status_with_final, migrated, preserved_business_keys)

    ongoing_without_dates = {
        **common,
        "id": "tx-56-ongoing",
        "status": "ongoing",
        "preliminaryDate": "",
        "finalDate": "",
    }
    migrated = migrate_contract(ongoing_without_dates)
    assert migrated["status"] == "ongoing"
    assert_preserved(ongoing_without_dates, migrated, preserved_business_keys)

    print(
        "PASS: BEST56 schema 11→12 executable contract preserves dates, payment parts "
        "and representative business fields across 3 status/date fixtures"
    )


if __name__ == "__main__":
    main()
