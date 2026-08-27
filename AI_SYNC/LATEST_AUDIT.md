# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `36`
- Branch roboczy: `develop`
- Najwyższy priorytet: `P0-7A-CANONICAL-APP`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Exact BEST56 pozostaje potwierdzony: SHA-256 `3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92`.

Dodano i zweryfikowano w CI:
- `scripts/materialize_canonical_app.py` — deterministyczny gzip+base64 materializer z exact SHA gate i atomowym zapisem;
- `tests/check_materialize_canonical_app.py` — odrzuca błędny payload i pilnuje kontraktu exact-hash;
- krok CI `Verify canonical materializer contract`.

Repozytoryjny payload `artifacts/best56/` nadal oczekuje na bezpieczny transfer. NIE zapisano częściowego ani niezweryfikowanego artefaktu. Existing `stage_canonical_app.py` pozostaje runtime-verified fallbackiem.

## Testy / CI

Workflow #274 na `95d659338...` potwierdził PASS dla:
- BEST56 manifest,
- Source of Truth,
- schema 11→12,
- AI_SYNC protocol + dependency partition + freshness,
- runtime/dispatcher gates,
- artifact preflight,
- canonical staging safety,
- **canonical materializer contract**.

`Static application checks` nadal FAIL przez aktywny P0-7A — canonical app nie jest jeszcze utrwalony w repo. BEST40 checksum/stable pozostają SKIPPED downstream.

Brak zmian zachowania aplikacji, danych i finansów.

## P0 / P1

- P0 #7 — `MATERIALIZER_CONTRACT_CI_PASS_SOURCE_ARTIFACT_PENDING`; 7A READY, 7B BLOCKED na exact BEST40.
- P0 #11 — aktywny, BLOCKED wyłącznie przez 7A.
- P1 #12 — pełny lokalny bot runtime pozostaje otwarty.

## Handoff dla 3 botów

### PRIMARY
Claim `P0-7A-CANONICAL-APP`. Preferowana ścieżka: bezpiecznie zapisz exact BEST56 payload pod `artifacts/best56/`, uruchom `python scripts/materialize_canonical_app.py`, potem `python tests/check_app.py app/FlippChill_Kalkulator.html`. Bezpieczny fallback: `FLIPPCHILL_ARTIFACT_ROOTS=<katalog>` + `python scripts/stage_canonical_app.py --auto`. Akceptuj wyłącznie SHA-256 `3bb0756f...f4044e92`.

### SECOND_AUDIT
Po DONE 7A wykonaj realny test migracji schema 11→12 na `localStorage`; NIE czekaj na BEST40.

### THIRD_UI
Po DONE 7A wykonaj audyt 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression; NIE zmieniaj finansów.

## Auto-dispatch

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7A-CANONICAL-APP`
- `target_agent = PRIMARY`
- `source_iteration = 36`

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
