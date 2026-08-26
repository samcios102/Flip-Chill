# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `28`
- Branch roboczy: `develop`
- Najwyższy priorytet: `P0-7-CANONICAL-APP`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Dodano `scripts/stage_canonical_app.py`. Stager przyjmuje bieżący BEST56 wyłącznie przy exact SHA-256 `3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92` i atomowo przygotowuje `app/FlippChill_Kalkulator.html`. Dodano też `tests/check_stage_canonical_app.py` oraz osobny krok CI.

Lokalny artefakt BEST56 został ponownie sprawdzony: fingerprint jest dokładnie zgodny z Source of Truth. Historyczny BEST40 pozostaje niezależnym gate i nadal wymaga exact SHA-256 `c04106fe884d32dc257d852b320f2e145a93f80e5615409dc5fac17f5b171708`.

## Testy / CI

- lokalny fingerprint BEST56: `PASS`
- canonical app staging contract: `COMMITTED / CI PENDING`
- ostatni pełny dowód gate'ów dispatchera: workflow #176 = `PASS` przed P0 #7
- najnowszy widoczny workflow #182 jest nadal `QUEUED` na starszym commicie `0cb2c531...`
- `Static application checks`: oczekuje na realne wystawienie canonical app
- BEST40 checksum: oczekuje na exact artefakt

Nie deklarujemy nowego CI PASS dla iteracji 28 bez wyniku workflow.

## P0 / P1

- P0 #7 — aktywny i READY dla PRIMARY; ma teraz bezpieczny exact-hash stager BEST56.
- P0 #11 — aktywny, BLOCKED przez #7.
- P1 #12 — `DISPATCHER_RUNTIME_GUARD_INTEGRATED_CI_PASS_PENDING_LOCAL_RUNTIME`.
- THIRD_UI czeka na canonical app.

## Handoff dla 3 botów

### PRIMARY

Claim `P0-7-CANONICAL-APP`.

1. Uruchom `python scripts/stage_canonical_app.py <ścieżka-do-exact-BEST56>`.
2. Kandydat musi mieć SHA-256 `3bb0756f...f4044e92`.
3. Uruchom `artifact_preflight.py` i importuj historyczny BEST40 wyłącznie przy exact SHA-256 `c04106fe...171708`.
4. Uruchom pełny workflow; `main` pozostaje bez zmian.

### SECOND_AUDIT

Po P0 #7 wykonaj realny test migracji schema 11→12 na `localStorage`.

### THIRD_UI

Po canonical app wykonaj audyt 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression. Nie zmieniaj finansów.

## Auto-dispatch

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7-CANONICAL-APP`
- `target_agent = PRIMARY`
- `source_iteration = 28`

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
