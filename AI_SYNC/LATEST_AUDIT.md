# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `36`
- Branch roboczy: `develop`
- Najwyższy priorytet: `P0-7A-CANONICAL-APP`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Exact BEST56 został ponownie potwierdzony w runtime: SHA-256 `3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92`.

Dodano:
- `scripts/materialize_canonical_app.py` — deterministic gzip+base64 materializer z exact SHA gate i atomowym zapisem;
- `tests/check_materialize_canonical_app.py` — odrzuca błędny payload i pilnuje kontraktu exact-hash;
- krok CI `Verify canonical materializer contract`.

Repozytoryjny payload `artifacts/best56/` nie został zapisany częściowo: dostępny connector GitHub nie przyjmuje dużego lokalnego pliku jako file parameter. Bezpieczny transfer pozostaje następnym krokiem PRIMARY. Istniejący local stager nadal jest poprawną ścieżką awaryjną.

## Testy / CI

- ostatni zakończony workflow #263 na `f189ba52...`: pre-application gate’y = PASS; `Static application checks` = FAIL przez brak canonical app;
- materializer + test + CI step są już na `develop`, ale nowy head oczekuje na wynik workflow;
- żadna zmiana finansowa, danych transakcyjnych ani UX nie została wykonana.

## P0 / P1

- P0 #7 — aktywny: materializer contract committed; source payload / canonical app nadal oczekuje na bezpieczny zapis; 7B BLOCKED na exact BEST40.
- P0 #11 — aktywny, BLOCKED wyłącznie przez 7A.
- P1 #12 — pełny lokalny bot runtime pozostaje otwarty.

## Handoff dla 3 botów

### PRIMARY
Claim `P0-7A-CANONICAL-APP`. Preferowana ścieżka: zapisz exact BEST56 payload pod `artifacts/best56/`, uruchom `python scripts/materialize_canonical_app.py`, potem `python tests/check_app.py app/FlippChill_Kalkulator.html`. Bezpieczny fallback: `FLIPPCHILL_ARTIFACT_ROOTS=<katalog>` + `python scripts/stage_canonical_app.py --auto`. Akceptuj tylko SHA-256 `3bb0756f...f4044e92`.

### SECOND_AUDIT
Po DONE 7A wykonaj realny test migracji schema 11→12 na `localStorage`; NIE czekaj na BEST40.

### THIRD_UI
Po DONE 7A wykonaj audyt 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression; NIE zmieniaj finansów.

## Auto-dispatch

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7A-CANONICAL-APP`
- `target_agent = PRIMARY`
- `source_iteration = 36`

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
