# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `51`
- Branch roboczy: `develop`
- Najwyższy priorytet: `P0-7A-CANONICAL-APP`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Dodano CI-guarded one-shot dla PRIMARY: `scripts/primary_p0_7a_one_shot.py`. Helper redukuje lokalny P0-7A do jednego polecenia, przyjmuje wyłącznie exact BEST56, blokuje `main/master`, ogranicza staging do `artifacts/best56` i wymaga jawnego `--push`.

Nie zmieniono aplikacji, finansów, danych ani routingu blockerów.

## Testy / CI

Workflow #392 na `05a05551b02b0a8c75523f5b015643b51ea4cb62`:
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
- `Static application checks` = FAIL przez P0-7A;
- BEST40 checks = SKIPPED downstream.

## P0 / P1

- P0 #7 — 7A nadal `READY`; 7B BLOCKED na exact BEST40.
- P0 #11 — aktywny, BLOCKED wyłącznie przez 7A.
- P1 #12 — pełny lokalny bot runtime pozostaje otwarty.

## Handoff dla 3 botów

### PRIMARY
Na lokalnym repo z GitHub push access uruchom dokładnie:

`python scripts/primary_p0_7a_one_shot.py --auto --commit --push`

Helper sam wykonuje exact-hash packaging, canonical part validation, `git add artifacts/best56`, commit i jawny push bez dotykania `main`.

### SECOND_AUDIT
Po DONE 7A wykonaj realny test migracji schema 11→12 na `localStorage`; nie czekaj na BEST40.

### THIRD_UI
Po DONE 7A wykonaj audyt 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression; nie zmieniaj finansów.

## Auto-dispatch

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7A-CANONICAL-APP`
- `target_agent = PRIMARY`
- `source_iteration = 51`

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
