# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `30`
- Branch roboczy: `develop`
- Najwyższy priorytet: `P0-7A-CANONICAL-APP`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Kontrakt rozdzielenia issue #7 na 7A canonical app i 7B frozen BEST40 został potwierdzony przez CI. Workflow #202 dla `3daaef3b...` ma `Verify BEST56 queue dependency partition = PASS`. Issue #13 zamknięto jako completed.

## Testy / CI

- wszystkie gate'y przed aplikacją, w tym dependency partition, = `PASS`;
- `Static application checks` = `FAIL` z powodu aktywnego P0 #7 / braku canonical app;
- BEST40 checksum/stable = `SKIPPED` downstream.

## P0 / P1

- P0 #7 — aktywny: 7A READY, 7B BLOCKED na exact BEST40.
- P0 #11 — aktywny, BLOCKED wyłącznie przez 7A.
- P1 #12 — lokalny realny bot runtime pozostaje otwarty.
- P1 #13 — CLOSED / CI VERIFIED.

## Handoff dla 3 botów

### PRIMARY
Claim `P0-7A-CANONICAL-APP`: stage exact BEST56 SHA-256 `3bb0756f...f4044e92` do `app/FlippChill_Kalkulator.html`, uruchom Static application checks, nie dotykaj main.

### SECOND_AUDIT
Po DONE 7A wykonaj realny test migracji schema 11→12 na `localStorage`; NIE czekaj na BEST40.

### THIRD_UI
Po DONE 7A wykonaj audyt 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression; NIE zmieniaj finansów.

## Auto-dispatch

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7A-CANONICAL-APP`
- `target_agent = PRIMARY`
- `source_iteration = 30`

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
