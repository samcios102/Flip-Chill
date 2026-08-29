# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `85`
- Branch roboczy: `develop`
- Najwyższy priorytet: `P0-7A-CANONICAL-APP`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Iteracja 85 synchronizuje handoff z zakończonym workflow #553 dla `develop = 1f397adb8c737b9631907ae16570c31d138668f7`.

Nie wykryto nowej regresji aplikacji, danych, finansów ani UX. Routing blockerów pozostaje bez zmian: repo nadal nie zawiera canonical payloadu BEST56 wymaganego przez `P0-7A-CANONICAL-APP`.

## Testy / CI

Workflow #553 dla `1f397adb8c737b9631907ae16570c31d138668f7`:
- kroki 4–24 = PASS;
- BEST56 manifest / Source of Truth / CRM sync = PASS;
- finanse = PASS;
- schema 11→12 = PASS;
- AI_SYNC / freshness / runtime guard / dispatcher = PASS;
- preflight / stager / materializer / packager / one-shot PRIMARY / auto-materialization = PASS;
- `Static application checks` = FAIL przez brak repozytoryjnego payloadu canonical BEST56 dla P0-7A;
- BEST40 = SKIPPED downstream.

CI commitów handoffu iteracji 85 jest sprawdzany osobno; pełnego PASS nie deklarujemy bez zakończonego runu.

## P0 / P1

- P0 #7 — `P0-7A-CANONICAL-APP` nadal `READY`; 7B pozostaje BLOCKED na exact BEST40.
- P0 #11 — nadal aktywny i BLOCKED wyłącznie przez 7A.
- P1 #12 — pełny lokalny bot runtime pozostaje otwarty.

## Handoff dla 3 botów

### PRIMARY
Na lokalnym repo z GitHub push access uruchom dokładnie:
`python scripts/primary_p0_7a_one_shot.py --auto --commit --push`

### SECOND_AUDIT
Po DONE 7A wykonaj realny test migracji schema 11→12 na `localStorage`. Nie czekaj na BEST40.

### THIRD_UI
Po DONE 7A wykonaj audyt 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression; nie zmieniaj finansów.

## Auto-dispatch

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7A-CANONICAL-APP`
- `target_agent = PRIMARY`
- `source_iteration = 85`

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
