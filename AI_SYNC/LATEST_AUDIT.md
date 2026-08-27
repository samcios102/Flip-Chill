# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `39`
- Branch roboczy: `develop`
- Najwyższy priorytet: `P0-7A-CANONICAL-APP`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Przed zapisaniem realnego payloadu wykryto lukę w materializerze: akceptował dowolne nazwy pasujące do `best56.html.gz.b64.part*`. Exact SHA chronił wynik końcowy, ale niekanoniczna nazwa lub luka numeracji mogła tworzyć niejednoznaczny zestaw wejściowy.

Naprawiono:
- materializer wymaga dokładnego schematu `best56.html.gz.b64.part001..NNN`;
- numeracja musi być ciągła od 001;
- obca nazwa lub luka są odrzucane przed dekodowaniem;
- test kontraktu obejmuje złą nazwę i lukę `001,003`.

## Testy / CI

Workflow #303 na `676d78bb8a59a637f3b7f97ef84d0ab711b93465`:
- wszystkie gate’y przed aplikacją = PASS;
- `Verify canonical materializer contract` = PASS z nowym part-set guard;
- deterministic BEST56 packager = PASS;
- `Static application checks` = FAIL wyłącznie dlatego, że canonical app/source payload nie jest jeszcze utrwalony w repo;
- BEST40 checksum/stable = SKIPPED downstream.

Brak zmian zachowania aplikacji, danych biznesowych i finansów.

## P0 / P1

- P0 #7 — `MATERIALIZER_PART_SET_CI_PASS_LOCAL_PAYLOAD_PENDING`; 7A READY, 7B BLOCKED na exact BEST40.
- P0 #11 — aktywny, BLOCKED wyłącznie przez 7A.
- P1 #12 — bez zmiany; pełny lokalny bot runtime pozostaje otwarty.

## Handoff dla 3 botów

### PRIMARY
Claim `P0-7A-CANONICAL-APP`. Użyj wyłącznie exact BEST56 SHA-256 `3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92`. Preferowana ścieżka: `python scripts/package_best56_artifact.py --auto` → sprawdź kanoniczny ciąg `part001..NNN` → `python scripts/materialize_canonical_app.py` → `python tests/check_app.py app/FlippChill_Kalkulator.html`. Commituj payload/canonical app wyłącznie po exact round-trip SHA. Fallback: `python scripts/stage_canonical_app.py --auto`.

### SECOND_AUDIT
Po DONE 7A wykonaj realny test migracji schema 11→12 na `localStorage`; NIE czekaj na BEST40.

### THIRD_UI
Po DONE 7A wykonaj audyt 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression; NIE zmieniaj finansów.

## Auto-dispatch

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7A-CANONICAL-APP`
- `target_agent = PRIMARY`
- `source_iteration = 39`

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
