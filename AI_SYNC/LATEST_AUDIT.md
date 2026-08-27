# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `43`
- Branch roboczy: `develop`
- Najwyższy priorytet: `P0-7A-CANONICAL-APP`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Wykryto drift dokumentacyjny: ogólny punkt P2 „Jednostkowe testy finansowe” pozostawał otwarty, mimo że wykonywalny kontrakt `tests/check_financial_scenarios.py` jest już wdrożony, issue #14 zakończone, a workflow #337 potwierdza gate finansowy = PASS.

BACKLOG został zsynchronizowany z rzeczywistym stanem: ogólny punkt testów finansowych jest teraz ukończony. Reguły finansowe NIE zmieniły się.

## Testy / CI

Workflow #337 na `6b6a041d305489ba47e33e90c3ef2e60ac526811`:
- BEST56 manifest = PASS;
- Source of Truth = PASS;
- executable financial scenarios = PASS;
- schema 11→12 = PASS;
- wszystkie gate’y AI_SYNC / dispatcher / artifact / materializer = PASS;
- `Static application checks` = FAIL wyłącznie przez istniejący P0-7A — canonical app nadal nie jest utrwalony w repo;
- BEST40 checks = SKIPPED downstream.

## P0 / P1

- P0 #7 — 7A `READY` wyłącznie lokalną ścieżką packager → direct git commit; 7B BLOCKED na exact BEST40.
- P0 #11 — aktywny, BLOCKED wyłącznie przez 7A.
- P1 #12 — bez zmiany; pełny lokalny bot runtime pozostaje otwarty.
- P1 #14 — DONE / CI PASS.
- P2 #15 — DONE; backlog finansowy zsynchronizowany z istniejącym dowodem CI.

## Handoff dla 3 botów

### PRIMARY
Claim `P0-7A-CANONICAL-APP` lokalnie. Uruchom `python scripts/package_best56_artifact.py --auto` na exact BEST56 SHA-256 `3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92`, sprawdź exact round-trip SHA i kanoniczny ciąg `part001..NNN`, następnie `git add artifacts/best56` + commit na `develop` bez reserializacji przez czat/konektor. CI samo zmaterializuje canonical app i uruchomi static checks. NIE dotykaj `main`.

### SECOND_AUDIT
Kontrakt finansowy i synchronizacja backlogu są DONE. Po DONE 7A wykonaj realny test migracji schema 11→12 na `localStorage`; NIE czekaj na BEST40.

### THIRD_UI
Po DONE 7A wykonaj audyt 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression; NIE zmieniaj finansów.

## Auto-dispatch

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7A-CANONICAL-APP`
- `target_agent = PRIMARY`
- `source_iteration = 43`

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
