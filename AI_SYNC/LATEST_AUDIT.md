# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `60`
- Branch roboczy: `develop`
- Najwyższy priorytet: `P0-7A-CANONICAL-APP`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Audyt wykrył drift metadanych dowodowych: część wspólnego stanu nadal wskazywała starsze workflow #303/#397, mimo że najnowszym zakończonym zweryfikowanym runem jest #442.

Iteracja 60 odświeża machine-authoritative evidence do workflow #442. Logika aplikacji, dane, finanse, UX i routing blockerów nie zostały zmienione.

## Testy / CI

Workflow #442 na commicie `dd0247209e05e2d4312083a564bf124c5ec1627e`:
- kroki 4–24 = PASS;
- rozszerzony schema 11→12 contract = PASS;
- BEST56 manifest / Source of Truth / CRM sync = PASS;
- finanse = PASS;
- AI_SYNC / freshness / runtime guard / dispatcher = PASS;
- preflight / stager / materializer / packager / one-shot PRIMARY / auto-materialization = PASS;
- `Static application checks` = FAIL wyłącznie przez brak repozytoryjnego payloadu canonical BEST56 dla P0-7A;
- BEST40 = SKIPPED downstream.

CI dla zmian iteracji 60 jest uruchomione; nowego PASS nie deklarujemy przed wynikiem.

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
- `source_iteration = 60`

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
