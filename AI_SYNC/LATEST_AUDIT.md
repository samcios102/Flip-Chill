# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `53`
- Branch roboczy: `develop`
- Najwyższy priorytet: `P0-7A-CANONICAL-APP`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Najnowszy zakończony workflow przeszedł z #397 do #404. Workflow #404 dla `b06fa076fd3a2fb5287c83576533256275d21068` potwierdza, że wszystkie gate’y przed aplikacją nadal przechodzą, a jedyny FAIL pozostaje na `Static application checks` z powodu braku repository payloadu P0-7A.

Aplikacja, finanse, dane, blocker semantics i routing nie zostały zmienione.

## Testy / CI

Workflow #404:
- kroki 4–24 = PASS;
- BEST56 manifest = PASS;
- Source of Truth = PASS;
- CRM sync current state = PASS;
- finanse = PASS;
- schema 11→12 = PASS;
- AI_SYNC protocol, dependency partition, freshness i runtime guard = PASS;
- dispatcher claim/failure/mutex/dependency contracts = PASS;
- artifact preflight, canonical staging, materializer i packager = PASS;
- `PRIMARY P0-7A one-shot helper` = PASS;
- auto-materialization ordering = PASS bez payloadu;
- `Static application checks` = FAIL wyłącznie przez brak payloadu P0-7A;
- BEST40 checks = SKIPPED downstream.

CI dla końcowego handoffu iteracji 53 oczekuje na wynik po commitach synchronizacyjnych; nowego PASS nie deklarujemy bez dowodu.

## P0 / P1

- P0 #7 — `P0-7A-CANONICAL-APP` nadal `READY`; 7B pozostaje BLOCKED na exact BEST40.
- P0 #11 — aktywny, BLOCKED wyłącznie przez 7A.
- P1 #12 — pełny lokalny bot runtime pozostaje otwarty.

## Handoff dla 3 botów

### PRIMARY
Na lokalnym repo z GitHub push access uruchom dokładnie:

`python scripts/primary_p0_7a_one_shot.py --auto --commit --push`

### SECOND_AUDIT
Po DONE 7A wykonaj realny test migracji schema 11→12 na `localStorage`; nie czekaj na BEST40.

### THIRD_UI
Po DONE 7A wykonaj audyt 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression; nie zmieniaj finansów.

## Auto-dispatch

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7A-CANONICAL-APP`
- `target_agent = PRIMARY`
- `source_iteration = 53`

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
