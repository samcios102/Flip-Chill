# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `40`
- Branch roboczy: `develop`
- Najwyższy priorytet: `P0-7A-CANONICAL-APP`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Exact BEST56 jest ponownie dostępny w runtime automatu: 857840 B, SHA-256 `3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92`.

Lokalna weryfikacja deterministycznego packaging/materialization:
- gzip `mtime=0` + base64 round-trip = exact SHA PASS;
- symulacja 16 części odtworzyła identyczny BEST56;
- statyczny gate na odtworzonym pliku: 763 ID, 0 duplikatów, 38/38 referencji, krytyczne markery UI obecne, VAT 23% i CIT 9% obecne, script/style zbilansowane.

W repo dodano CI auto-materialization: gdy `artifacts/best56/best56.html.gz.b64.part*` istnieje, workflow uruchamia `scripts/materialize_canonical_app.py` przed `Static application checks`. Test materializera wymusza także tę kolejność.

## Testy / CI

Workflow #313 na `3c0b1f7cbfada7f0f7a107a0dcd6ffa3f5df85d9`:
- wszystkie wcześniejsze gate’y = PASS;
- `Verify canonical materializer contract` = PASS;
- deterministic BEST56 packager = PASS;
- `Materialize canonical BEST56 app when repository payload exists` = PASS;
- `Static application checks` = FAIL, bo repozytoryjny payload nie jest jeszcze utrwalony;
- BEST40 checksum/stable = SKIPPED downstream.

Brak zmian zachowania aplikacji, danych biznesowych i finansów.

## P0 / P1

- P0 #7 — `CI_AUTO_MATERIALIZATION_PASS_LOCAL_PAYLOAD_PENDING`; 7A READY, 7B BLOCKED na exact BEST40.
- P0 #11 — aktywny, BLOCKED wyłącznie przez 7A.
- P1 #12 — bez zmiany; pełny lokalny bot runtime pozostaje otwarty.

## Handoff dla 3 botów

### PRIMARY
Claim `P0-7A-CANONICAL-APP`. Uruchom `python scripts/package_best56_artifact.py --auto` na exact BEST56 SHA-256 `3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92`, sprawdź exact round-trip SHA i kanoniczny ciąg `part001..NNN`, następnie commituj wyłącznie `artifacts/best56/` na `develop`. CI samo uruchomi materializer i static check. NIE dotykaj `main`.

### SECOND_AUDIT
Po DONE 7A wykonaj realny test migracji schema 11→12 na `localStorage`; NIE czekaj na BEST40.

### THIRD_UI
Po DONE 7A wykonaj audyt 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression; NIE zmieniaj finansów.

## Auto-dispatch

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7A-CANONICAL-APP`
- `target_agent = PRIMARY`
- `source_iteration = 40`

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
