# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `35`
- Branch roboczy: `develop`
- Najwyższy priorytet: `P0-7A-CANONICAL-APP`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Wykryto drift protokołu 3 botów: `AI_SYNC/PROTOCOL.md` pomijał `sync/CRM_SYNC.md` w obowiązkowej kolejności odczytu, mimo że automat i wspólny stan wymagają tego pliku przed BACKLOG.

Naprawa:
- `sync/CRM_SOURCE_OF_TRUTH.json` ma teraz kanoniczne `sync_contract.required_read_order`;
- `AI_SYNC/PROTOCOL.md` odtwarza tę kolejność 1:1;
- `tests/check_ai_sync_protocol.py` blokuje przyszły drift manifestu i kolejności w Markdown.

Brak zmian zachowania aplikacji, danych i finansów.

## Testy / CI

- poprzedni workflow #249 na `f6ca0dbd...`: wszystkie gate'y przed aplikacją = `PASS`;
- nowy kontrakt read-order = `COMMITTED / CI PENDING`;
- `Static application checks` pozostaje P0 #7 do czasu canonical app;
- BEST40 checksum/stable pozostaje osobnym downstream gate 7B.

## P0 / P1

- P0 #7 — aktywny: 7A READY; 7B BLOCKED na exact BEST40.
- P0 #11 — aktywny, BLOCKED wyłącznie przez 7A.
- P1 #12 — read-order contract dodany; pełny lokalny bot runtime pozostaje otwarty.

## Handoff dla 3 botów

### PRIMARY
Claim `P0-7A-CANONICAL-APP`. Jeśli exact BEST56 jest poza domyślnymi katalogami, ustaw `FLIPPCHILL_ARTIFACT_ROOTS=<katalog>`, uruchom `python scripts/stage_canonical_app.py --auto`, zaakceptuj wyłącznie SHA-256 `3bb0756f...f4044e92`, następnie uruchom `python tests/check_app.py app/FlippChill_Kalkulator.html`. Pracuj na `develop`; `main` pozostaje stabilny.

### SECOND_AUDIT
Po DONE 7A wykonaj realny test migracji schema 11→12 na `localStorage`; NIE czekaj na BEST40.

### THIRD_UI
Po DONE 7A wykonaj audyt 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression; NIE zmieniaj finansów.

## Auto-dispatch

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7A-CANONICAL-APP`
- `target_agent = PRIMARY`
- `source_iteration = 35`

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
