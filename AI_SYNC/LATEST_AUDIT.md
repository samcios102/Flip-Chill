# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `42`
- Branch roboczy: `develop`
- Najwyższy priorytet: `P0-7A-CANONICAL-APP`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Audyt finansów wykazał lukę jakościową: wcześniejszy gate Source of Truth porównywał stałe, ale NIE wykonywał arytmetycznych scenariuszy. Dodano `tests/check_financial_scenarios.py` oraz osobny krok CI.

Kontrakt liczy teraz: VAT 23% gross→net i kwotę VAT, CIT 9% od dodatniego dochodu i 0 przy stracie, PIT 12%, granice progów 49 999 / 50 000 / 99 999 / 100 000 / 125 000 oraz wkład Slack/Marketing do obrotu progowego.

Issue #14 jest `closed/completed`. Reguły finansowe NIE zmieniły się — zwiększyła się ich ochrona regresyjna.

## Testy / CI

Workflow #330 na `8d0510cef2f4c56f7cd3687fe928cc690abf61e8`:
- `Verify BEST56 executable financial scenarios` = PASS;
- wszystkie pozostałe gate’y przed aplikacją = PASS;
- `Static application checks` = FAIL wyłącznie przez istniejący P0-7A — canonical app nadal nie jest utrwalony w repo;
- BEST40 checks = SKIPPED downstream.

## P0 / P1

- P0 #7 — 7A `READY` wyłącznie lokalną ścieżką packager → direct git commit; 7B BLOCKED na exact BEST40.
- P0 #11 — aktywny, BLOCKED wyłącznie przez 7A.
- P1 #12 — bez zmiany; pełny lokalny bot runtime pozostaje otwarty.
- P1 #14 — DONE / CI PASS workflow #330.

## Handoff dla 3 botów

### PRIMARY
Claim `P0-7A-CANONICAL-APP` lokalnie. Uruchom `python scripts/package_best56_artifact.py --auto` na exact BEST56 SHA-256 `3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92`, sprawdź exact round-trip SHA i kanoniczny ciąg `part001..NNN`, następnie `git add artifacts/best56` + commit na `develop` bez reserializacji przez czat/konektor. CI samo zmaterializuje canonical app i uruchomi static checks. NIE dotykaj `main`.

### SECOND_AUDIT
Kontrakt finansowy #14 jest DONE/PASS. Po DONE 7A wykonaj realny test migracji schema 11→12 na `localStorage`; NIE czekaj na BEST40.

### THIRD_UI
Po DONE 7A wykonaj audyt 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression; NIE zmieniaj finansów.

## Auto-dispatch

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7A-CANONICAL-APP`
- `target_agent = PRIMARY`
- `source_iteration = 42`

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
