# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `32`
- Branch roboczy: `develop`
- Najwyższy priorytet: `P0-7A-CANONICAL-APP`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Dokładny lokalny BEST56 został wykonawczo sprawdzony przez kontrakt `stage_canonical_app.py`: dry-run = PASS, atomowe staging = PASS, SHA-256 wejścia i staged targetu = `3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92`.

To usuwa niepewność dotyczącą samego stagera. `P0-7A-CANONICAL-APP` nadal jest READY tylko dlatego, że zweryfikowany plik nie został jeszcze zapisany jako `app/FlippChill_Kalkulator.html` na `develop`.

## Testy / CI

- workflow #216 na `8b00996f...`: 15/15 gate'ów przed aplikacją = `PASS`;
- `Verify canonical app staging safety` = `PASS`;
- runtime dry-run exact BEST56 = `PASS`;
- runtime atomic staging exact BEST56 = `PASS`;
- staged target SHA-256 = exact baseline SHA-256;
- `Static application checks` = `FAIL` wyłącznie z powodu braku canonical app w repo;
- BEST40 checksum/stable = `SKIPPED` downstream;
- końcowy CI dla commitów handoffu iteracji 32 jest jeszcze do potwierdzenia.

## P0 / P1

- P0 #7 — aktywny: 7A READY po runtime-verified stagerze; 7B BLOCKED na exact BEST40.
- P0 #11 — aktywny, BLOCKED wyłącznie przez 7A.
- P1 #12 — lokalny realny bot runtime pozostaje otwarty.

## Handoff dla 3 botów

### PRIMARY
Claim `P0-7A-CANONICAL-APP`: stager jest już runtime-verified. Zapisz wyłącznie exact BEST56 SHA-256 `3bb0756f...f4044e92` jako `app/FlippChill_Kalkulator.html` na `develop`, uruchom Static application checks, NIE dotykaj main.

### SECOND_AUDIT
Po DONE 7A wykonaj realny test migracji schema 11→12 na `localStorage`; NIE czekaj na BEST40.

### THIRD_UI
Po DONE 7A wykonaj audyt 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression; NIE zmieniaj finansów.

## Auto-dispatch

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7A-CANONICAL-APP`
- `target_agent = PRIMARY`
- `source_iteration = 32`

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
