# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `31`
- Branch roboczy: `develop`
- Najwyższy priorytet: `P0-7A-CANONICAL-APP`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Usunięto niespójność wspólnego stanu: issue #13 było już `closed/completed`, Source of Truth nie traktował go jako aktywny blocker, ale BACKLOG i nagłówek CRM_SYNC nadal przedstawiały je jako otwarte/pending. BACKLOG oznacza teraz #13 jako ukończone, a CRM_SYNC ma `CLOSED / CI_VERIFIED` z dowodem workflow #202.

## Testy / CI

- workflow #209 na `cbdd2c960...`: wszystkie gate'y przed aplikacją = `PASS`;
- `Static application checks` = `FAIL` z powodu aktywnego P0 #7 / braku canonical app;
- BEST40 checksum/stable = `SKIPPED` downstream;
- commity iteracji 31 są synchronizacyjne; ich końcowy CI jest oczekiwany przed deklaracją nowego PASS.

## P0 / P1

- P0 #7 — aktywny: 7A READY, 7B BLOCKED na exact BEST40.
- P0 #11 — aktywny, BLOCKED wyłącznie przez 7A.
- P1 #12 — lokalny realny bot runtime pozostaje otwarty.
- P1 #13 — CLOSED / CI_VERIFIED; NIE jest aktywnym blockerem.

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
- `source_iteration = 31`

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
