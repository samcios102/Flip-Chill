# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `75`
- Branch roboczy: `develop`
- Najwyższy priorytet: `P0-7A-CANONICAL-APP`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Workflow #514 jest zakończonym dowodem dla develop `dd0a78342f5cbc26ef35ff807b96dde2caa7894c` i potwierdza ten sam stan blockerów co iteracja 74.

Iteracja 75 odświeża handoff do workflow #514 bez zmiany logiki aplikacji, danych, finansów, UX ani routingu blockerów.

## Testy / CI

Workflow #514:
- kroki 4–24 = PASS;
- BEST56 manifest / Source of Truth / CRM sync = PASS;
- finanse = PASS;
- schema 11→12 = PASS;
- AI_SYNC / freshness / runtime guard / dispatcher = PASS;
- preflight / stager / materializer / packager / one-shot PRIMARY / auto-materialization = PASS;
- `Static application checks` = FAIL wyłącznie przez brak repozytoryjnego payloadu canonical BEST56 dla P0-7A;
- BEST40 = SKIPPED downstream.

CI dla commitów handoffu iteracji 75 jest sprawdzany osobno; pełnego PASS nie deklarujemy bez zakończonego runu.

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
- `source_iteration = 75`

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
