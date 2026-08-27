# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `38`
- Branch roboczy: `develop`
- Najwyższy priorytet: `P0-7A-CANONICAL-APP`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Exact BEST56 jest ponownie dostępny w runtime: 857840 B i SHA-256 `3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92`. Pozostały ręczny krok 7A polegał na dzieleniu/enkodowaniu repozytoryjnego payloadu dla gotowego materializera.

Dodano:
- `scripts/package_best56_artifact.py` — exact-SHA-only packager;
- deterministyczny gzip `mtime=0` + base64;
- części `best56.html.gz.b64.partNNN` o stałym rozmiarze;
- atomowy zapis i pełny round-trip SHA przed zaakceptowaniem payloadu;
- `tests/check_package_best56_artifact.py` oraz osobny gate CI.

## Testy / CI

Workflow #293 na `356180385a41cb35dccd01ebed6e2f0cf5adbb3c`:
- wszystkie gate’y przed aplikacją = PASS;
- **Verify deterministic BEST56 artifact packager = PASS**;
- `Static application checks` = FAIL wyłącznie dlatego, że canonical app nie jest jeszcze utrwalony w repo;
- BEST40 checksum/stable = SKIPPED downstream.

Brak zmian zachowania aplikacji, danych i finansów.

## P0 / P1

- P0 #7 — `PACKAGER_CONTRACT_CI_PASS_LOCAL_PAYLOAD_PENDING`; 7A READY, 7B BLOCKED na exact BEST40.
- P0 #11 — aktywny, BLOCKED wyłącznie przez 7A.
- P1 #12 — bez zmiany; pełny lokalny bot runtime pozostaje otwarty.

## Handoff dla 3 botów

### PRIMARY
Claim `P0-7A-CANONICAL-APP`. Preferowana ścieżka: ustaw `FLIPPCHILL_ARTIFACT_ROOTS=<katalog>` jeśli potrzebne, uruchom `python scripts/package_best56_artifact.py --auto`, następnie `python scripts/materialize_canonical_app.py`, potem `python tests/check_app.py app/FlippChill_Kalkulator.html`. Commituj payload + canonical app wyłącznie po exact round-trip SHA. Fallback: `python scripts/stage_canonical_app.py --auto`.

### SECOND_AUDIT
Po DONE 7A wykonaj realny test migracji schema 11→12 na `localStorage`; NIE czekaj na BEST40.

### THIRD_UI
Po DONE 7A wykonaj audyt 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression; NIE zmieniaj finansów.

## Auto-dispatch

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7A-CANONICAL-APP`
- `target_agent = PRIMARY`
- `source_iteration = 38`

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
