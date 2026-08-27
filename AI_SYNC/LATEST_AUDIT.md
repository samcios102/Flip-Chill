# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `41`
- Branch roboczy: `develop`
- Najwyższy priorytet: `P0-7A-CANONICAL-APP`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Exact BEST56 nadal jest poprawny lokalnie: 857840 B, SHA-256 `3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92`. Deterministyczny gzip `mtime=0` + base64 round-trip przechodzi.

Próba dużego transferu payloadu przez konektor GitHub zmieniła bajty. Workflow #321 zatrzymał payload na `Verify canonical materializer contract`, zanim powstał canonical app. Wadliwy payload został natychmiast usunięty w `bc918d5a43174e1f9540010be4f6620757bb69f8`.

Wniosek wykonawczy: payload BEST56 musi być generowany i commitowany bezpośrednio z lokalnego repo przez `scripts/package_best56_artifact.py --auto`; NIE należy przenosić dużego base64 przez czat/konektor tekstowy.

## Testy / CI

Workflow #321 na `625d600cbef9f42346de604662106f35871436ab`:
- wszystkie gate’y przed materializerem = PASS;
- `Verify canonical materializer contract` = FAIL — bezpieczne odrzucenie nie-exact payloadu;
- dalsze kroki = SKIPPED.

Brak zmian zachowania aplikacji, danych biznesowych i finansów.

## P0 / P1

- P0 #7 — 7A `READY`, ale wyłącznie lokalną ścieżką packager → direct git commit; 7B BLOCKED na exact BEST40.
- P0 #11 — aktywny, BLOCKED wyłącznie przez 7A.
- P1 #12 — bez zmiany; pełny lokalny bot runtime pozostaje otwarty.

## Handoff dla 3 botów

### PRIMARY
Claim `P0-7A-CANONICAL-APP` lokalnie. Uruchom `python scripts/package_best56_artifact.py --auto` na exact BEST56 SHA-256 `3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92`, sprawdź exact round-trip SHA i kanoniczny ciąg `part001..NNN`, następnie `git add artifacts/best56` + commit na `develop` bez reserializacji przez czat/konektor. CI samo zmaterializuje canonical app i uruchomi static checks. NIE dotykaj `main`.

### SECOND_AUDIT
Po DONE 7A wykonaj realny test migracji schema 11→12 na `localStorage`; NIE czekaj na BEST40.

### THIRD_UI
Po DONE 7A wykonaj audyt 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression; NIE zmieniaj finansów.

## Auto-dispatch

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7A-CANONICAL-APP`
- `target_agent = PRIMARY`
- `source_iteration = 41`

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
