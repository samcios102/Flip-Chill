# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `44`
- Branch roboczy: `develop`
- Najwyższy priorytet: `P0-7A-CANONICAL-APP`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Dodano deterministyczny guard semantyki sekcji `CRM_SYNC.md -> Aktualny stan`: `tests/check_crm_sync_current_state.py`. Gate pilnuje zgodności z Source of Truth dla `develop`, P0 #7, partycji 7A/7B, P0 #11, P1 #12, CIT 9%, VAT 23%, PIT 12% oraz progów 50 000 / 100 000. Nie przywiązuje poprawności projektu do szybko starzejących się numerów workflow.

Issue #16 zamknięte jako completed po dowodzie CI. Reguły biznesowe i routing P0 nie zmieniły się.

## Testy / CI

Workflow #345 na `d1250ebab4aba26d12d8d5c1de05f107bd354fe9`:
- BEST56 manifest = PASS;
- Source of Truth = PASS;
- CRM sync current-state contract = PASS;
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
- P1 #16 — DONE / CI PASS; current-state semantyka CRM_SYNC ma teraz osobny gate.
- P2 #15 — DONE.

## Handoff dla 3 botów

### PRIMARY
Claim `P0-7A-CANONICAL-APP` lokalnie. Uruchom `python scripts/package_best56_artifact.py --auto` na exact BEST56 SHA-256 `3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92`, sprawdź exact round-trip SHA i kanoniczny ciąg `part001..NNN`, następnie `git add artifacts/best56` + commit na `develop` bez reserializacji przez czat/konektor. CI samo zmaterializuje canonical app i uruchomi static checks. NIE dotykaj `main`.

### SECOND_AUDIT
Po DONE 7A wykonaj realny test migracji schema 11→12 na `localStorage`; NIE czekaj na BEST40.

### THIRD_UI
Po DONE 7A wykonaj audyt 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression; NIE zmieniaj finansów.

## Auto-dispatch

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7A-CANONICAL-APP`
- `target_agent = PRIMARY`
- `source_iteration = 44`

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
