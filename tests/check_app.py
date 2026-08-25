#!/usr/bin/env python3
"""Fast static quality gate for the single-file FlippChill build."""
from __future__ import annotations

import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

APP = Path(sys.argv[1] if len(sys.argv) > 1 else "app/FlippChill_Kalkulator.html")


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"OK: {message}")


class StaticDomCollector(HTMLParser):
    """Collect real static DOM IDs and ID references, ignoring JS/CSS strings."""

    REFERENCE_ATTRS = ("for", "aria-labelledby", "aria-describedby", "aria-controls")

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.references: list[tuple[str, str, str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        element_id = attrs_dict.get("id") or ""

        for name, value in attrs:
            if name == "id" and value:
                self.ids.append(value)

        for attr in self.REFERENCE_ATTRS:
            value = attrs_dict.get(attr)
            if not value:
                continue
            for target in value.split():
                self.references.append((attr, target, tag, element_id))

        href = attrs_dict.get("href")
        if href and href.startswith("#") and len(href) > 1:
            self.references.append(("href", href[1:], tag, element_id))


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

parser = StaticDomCollector()
parser.feed(text)
counts = Counter(parser.ids)
duplicates = sorted(item for item, count in counts.items() if count > 1)
if duplicates:
    fail("duplicate static DOM ids: " + ", ".join(duplicates[:20]))
ok(f"static DOM ids unique ({len(parser.ids)} ids)")

static_ids = set(parser.ids)
broken_references = [item for item in parser.references if item[1] not in static_ids]
if broken_references:
    sample = "; ".join(
        f'{attr}="{target}" on <{tag} id="{element_id or "-"}">' 
        for attr, target, tag, element_id in broken_references[:20]
    )
    fail(f"broken static DOM references ({len(broken_references)}): {sample}")
ok(f"static DOM references resolve ({len(parser.references)} references)")

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
