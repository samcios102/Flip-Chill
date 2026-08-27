# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `37`
- Branch roboczy: `develop`
- Najwyższy priorytet: `P0-7A-CANONICAL-APP`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Wykryto drift root entrypointu OpenCode: `OPENCODE.md` pomijał `AI_SYNC/PROTOCOL.md`, mimo że Source of Truth wymaga tego pliku jako kroku 2 kanonicznego read order. Lokalny bot mógł więc wejść w kolejkę bez najnowszych zasad lock/claim/freshness/runtime guard.

Naprawiono:
- `OPENCODE.md` ma teraz pełny kanoniczny `required_read_order` 1:1;
- `tests/check_ai_sync_protocol.py` sprawdza read order zarówno w `AI_SYNC/PROTOCOL.md`, jak i `OPENCODE.md`;
- Source of Truth zapisuje dowód `PASS_WORKFLOW_282` dla kontraktu read order.

## Testy / CI

Workflow #282 na `f2bd0f7861ce6b830e69a68ef2e0996ce4d28034` potwierdził PASS dla:
- BEST56 manifest,
- Source of Truth,
- schema 11→12,
- AI_SYNC protocol + **OpenCode entrypoint read order**,
- dependency partition + freshness,
- runtime/dispatcher gates,
- artifact preflight,
- canonical staging safety,
- canonical materializer contract.

`Static application checks` nadal FAIL wyłącznie przez P0-7A — canonical app nie jest jeszcze utrwalony w repo. BEST40 checksum/stable pozostają SKIPPED downstream.

Brak zmian zachowania aplikacji, danych i finansów.

## P0 / P1

- P0 #7 — `MATERIALIZER_CONTRACT_CI_PASS_SOURCE_ARTIFACT_PENDING`; 7A READY, 7B BLOCKED na exact BEST40.
- P0 #11 — aktywny, BLOCKED wyłącznie przez 7A.
- P1 #12 — `OPENCODE_ENTRYPOINT_READ_ORDER_CI_PASS_PENDING_LOCAL_RUNTIME`; pełny lokalny bot runtime pozostaje otwarty.

## Handoff dla 3 botów

### PRIMARY
Claim `P0-7A-CANONICAL-APP`. Preferowana ścieżka: bezpiecznie zapisz exact BEST56 payload pod `artifacts/best56/`, uruchom `python scripts/materialize_canonical_app.py`, potem `python tests/check_app.py app/FlippChill_Kalkulator.html`. Bezpieczny fallback: `FLIPPCHILL_ARTIFACT_ROOTS=<katalog>` + `python scripts/stage_canonical_app.py --auto`. Akceptuj wyłącznie SHA-256 `3bb0756f...f4044e92`.

### SECOND_AUDIT
Po DONE 7A wykonaj realny test migracji schema 11→12 na `localStorage`; NIE czekaj na BEST40.

### THIRD_UI
Po DONE 7A wykonaj audyt 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression; NIE zmieniaj finansów.

## Auto-dispatch

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7A-CANONICAL-APP`
- `target_agent = PRIMARY`
- `source_iteration = 37`

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
