# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `34`
- Branch roboczy: `develop`
- Najwyższy priorytet: `P0-7A-CANONICAL-APP`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

`stage_canonical_app.py` obsługuje teraz `FLIPPCHILL_ARTIFACT_ROOTS`. Dzięki temu PRIMARY i inne runtime'y mogą wskazać katalog montowany/pobrany bez wpisywania platformowej ścieżki do repo. Te rooty mają pierwszeństwo przed cwd/Downloads/Desktop/OneDrive.

Bezpieczeństwo pozostaje twarde: kandydat jest akceptowany wyłącznie przy exact SHA-256 `3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92`.

## Testy / CI

- workflow #239 na `167efab6...`: wszystkie gate'y przed aplikacją = `PASS`;
- `Verify canonical app staging safety` z testem `FLIPPCHILL_ARTIFACT_ROOTS` = `PASS`;
- `Static application checks` = `FAIL` wyłącznie z powodu braku `app/FlippChill_Kalkulator.html` w repo;
- BEST40 checksum/stable = `SKIPPED` downstream;
- końcowy CI po commitach handoffu iteracji 34 pozostaje do potwierdzenia.

## P0 / P1

- P0 #7 — aktywny: 7A READY z portable artifact roots; 7B BLOCKED na exact BEST40.
- P0 #11 — aktywny, BLOCKED wyłącznie przez 7A.
- P1 #12 — lokalny realny bot runtime pozostaje otwarty.

## Handoff dla 3 botów

### PRIMARY
Claim `P0-7A-CANONICAL-APP`. Jeśli exact BEST56 jest poza domyślnymi katalogami, ustaw `FLIPPCHILL_ARTIFACT_ROOTS=<katalog>`, następnie uruchom `python scripts/stage_canonical_app.py --auto`. Skrypt ma przyjąć tylko exact BEST56 SHA-256 `3bb0756f...f4044e92`, zapisać `app/FlippChill_Kalkulator.html`, uruchomić `python tests/check_app.py app/FlippChill_Kalkulator.html` i commitować na `develop`. NIE dotykaj `main`.

### SECOND_AUDIT
Po DONE 7A wykonaj realny test migracji schema 11→12 na `localStorage`; NIE czekaj na BEST40.

### THIRD_UI
Po DONE 7A wykonaj audyt 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression; NIE zmieniaj finansów.

## Auto-dispatch

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7A-CANONICAL-APP`
- `target_agent = PRIMARY`
- `source_iteration = 34`

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
