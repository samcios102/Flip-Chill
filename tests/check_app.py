#!/usr/bin/env python3
"""Fast static quality gate for the single-file FlippChill build."""
from __future__ import annotations

import re
import sys
from pathlib import Path

APP = Path(sys.argv[1] if len(sys.argv) > 1 else "app/FlippChill_Kalkulator.html")


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"OK: {message}")


if not APP.exists():
    fail(f"missing app file: {APP}")

text = APP.read_text(encoding="utf-8")
if len(text) < 100_000:
    fail("app file looks unexpectedly small")
ok(f"app size {len(text):,} chars")

required = [
    'data-view="portfolio"',
    'id="fac-pf-payment-filters"',
    'id="fac-inline-pay-dialog"',
    'id="fac-pf-dates-dialog"',
    'data-open-client-payments=',
    'data-open-pf-dates=',
    'fac-timeline-status-dots',
]
for token in required:
    if token not in text:
        fail(f"required feature marker missing: {token}")
ok("critical portfolio/payment/date/timeline markers present")

for obsolete in ['data-tab="payments"', 'data-tab="ledger"']:
    if obsolete in text:
        fail(f"obsolete top-level navigation returned: {obsolete}")
ok("obsolete Payments/Settlement top-level tabs absent")

ids = re.findall(r'\bid=["\']([^"\']+)["\']', text)
seen: set[str] = set()
duplicates: set[str] = set()
for item in ids:
    if item in seen:
        duplicates.add(item)
    seen.add(item)
if duplicates:
    fail("duplicate DOM ids: " + ", ".join(sorted(duplicates)[:20]))
ok(f"DOM ids unique ({len(ids)} ids)")

if "CIT 9%" not in text:
    fail("CIT 9% marker missing")
if "VAT 23%" not in text:
    fail("VAT 23% marker missing")
ok("tax labels VAT 23% and CIT 9% present")

if text.count("<script") != text.count("</script>"):
    fail("script tag count mismatch")
if text.count("<style") != text.count("</style>"):
    fail("style tag count mismatch")
ok("script/style tag counts balanced")

print("PASS: FlippChill static quality gate")
