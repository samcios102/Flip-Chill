# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `52`
- Branch roboczy: `develop`
- Najwyższy priorytet: `P0-7A-CANONICAL-APP`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Wykryto drift operacyjny: kolejka i trigger już używały one-shot helpera, natomiast Source of Truth i BACKLOG nadal opisywały starszą ręczną ścieżkę packagera. Source of Truth i BACKLOG są teraz zsynchronizowane: preferowana i autorytatywna ścieżka P0-7A to:

`python scripts/primary_p0_7a_one_shot.py --auto --commit --push`

Aplikacja, finanse, dane i routing blockerów nie zostały zmienione.

## Testy / CI

Workflow #397 na `706a0a891d94e8454b8671d4df5616963fd245ee`:
- BEST56 manifest = PASS;
- Source of Truth = PASS dla stanu przed synchronizacją iteracji 52;
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

CI dla końcowego handoffu iteracji 52: oczekuje na wynik po commitach synchronizacyjnych; nowego PASS nie deklarujemy bez dowodu.

## P0 / P1

- P0 #7 — stan operacyjny: `ONE_SHOT_HELPER_CI_PASS_LOCAL_EXECUTION_PENDING`; 7A nadal `READY`, 7B BLOCKED na exact BEST40.
- P0 #11 — aktywny, BLOCKED wyłącznie przez 7A.
- P1 #12 — pełny lokalny bot runtime pozostaje otwarty.

## Handoff dla 3 botów

### PRIMARY
Na lokalnym repo z GitHub push access uruchom dokładnie:

`python scripts/primary_p0_7a_one_shot.py --auto --commit --push`

To jest teraz autorytatywna ścieżka Source of Truth. Helper sam wykonuje exact-hash packaging, canonical part validation, `git add artifacts/best56`, commit i jawny push bez dotykania `main`.

### SECOND_AUDIT
Po DONE 7A wykonaj realny test migracji schema 11→12 na `localStorage`; nie czekaj na BEST40.

### THIRD_UI
Po DONE 7A wykonaj audyt 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression; nie zmieniaj finansów.

## Auto-dispatch

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7A-CANONICAL-APP`
- `target_agent = PRIMARY`
- `source_iteration = 52`

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
