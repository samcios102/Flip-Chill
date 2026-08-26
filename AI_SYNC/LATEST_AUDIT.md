# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `33`
- Branch roboczy: `develop`
- Najwyższy priorytet: `P0-7A-CANONICAL-APP`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

`stage_canonical_app.py` potrafi teraz sam odnaleźć dokładny BEST56 przez `--auto`. Wyszukiwanie jest ograniczone i deterministyczne, a każdy kandydat musi mieć exact SHA-256 `3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92`. Inny plik jest odrzucany.

To usuwa ostatni ręczny krok wskazywania ścieżki kandydata dla PRIMARY. Canonical app nadal nie jest jeszcze zapisany w repo, więc P0-7A pozostaje READY.

## Testy / CI

- workflow #226 na `77783db9...`: wszystkie gate'y przed aplikacją = `PASS`;
- rozszerzony `Verify canonical app staging safety` obejmujący auto-discovery = `PASS`;
- exact BEST56 SHA-256 = `3bb0756f...f4044e92`;
- `Static application checks` = `FAIL` wyłącznie z powodu braku `app/FlippChill_Kalkulator.html` w repo;
- BEST40 checksum/stable = `SKIPPED` downstream;
- końcowy CI po commitach handoffu iteracji 33 jest jeszcze do potwierdzenia.

## P0 / P1

- P0 #7 — aktywny: 7A READY, teraz z auto-discovery; 7B BLOCKED na exact BEST40.
- P0 #11 — aktywny, BLOCKED wyłącznie przez 7A.
- P1 #12 — lokalny realny bot runtime pozostaje otwarty.

## Handoff dla 3 botów

### PRIMARY
Claim `P0-7A-CANONICAL-APP` i uruchom `python scripts/stage_canonical_app.py --auto`. Skrypt ma przyjąć tylko exact BEST56 SHA-256 `3bb0756f...f4044e92`, zapisać `app/FlippChill_Kalkulator.html`, następnie uruchomić `python tests/check_app.py` i commitować na `develop`. NIE dotykaj `main`.

### SECOND_AUDIT
Po DONE 7A wykonaj realny test migracji schema 11→12 na `localStorage`; NIE czekaj na BEST40.

### THIRD_UI
Po DONE 7A wykonaj audyt 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression; NIE zmieniaj finansów.

## Auto-dispatch

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7A-CANONICAL-APP`
- `target_agent = PRIMARY`
- `source_iteration = 33`

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
