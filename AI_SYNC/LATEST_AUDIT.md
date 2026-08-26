# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `21`
- Branch roboczy: `develop`
- Testowany commit: `2bf529b7148c28b550d4427be6862a381da168b8`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Naprawiono semantykę aktywnych blockerów w `tests/check_ai_sync_protocol.py`. P0 pozostaje aktywny także przy etapowym, nie-terminalnym statusie typu `PREFLIGHT_CI_PASS_AWAITING_EXACT_ARTIFACT_IMPORT`; checker nie wymaga już literalnego `OPEN`.

## P0 / P1

- P0 #7 — nadal aktywny i READY dla PRIMARY.
- P0 #11 — nadal aktywny, BLOCKED przez #7.
- P1 #12 — lokalny runtime dispatch nadal czeka na rzeczywistą komendę bota.
- THIRD_UI czeka na canonical app.

## Handoff dla 3 botów

### PRIMARY

Claim `P0-7-CANONICAL-APP`. Uruchom lokalny artifact preflight i importuj historyczny BEST40 wyłącznie przy dokładnym SHA-256. Następnie przywróć kanoniczny `app/FlippChill_Kalkulator.html` i uruchom pełny workflow.

### SECOND_AUDIT

Po P0 #7 wykonaj realny test migracji schema 11→12 na `localStorage`.

### THIRD_UI

Po canonical app wykonaj audyt 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression. Nie zmieniaj finansów.

## Auto-dispatch

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7-CANONICAL-APP`
- `target_agent = PRIMARY`

Workflow dla poprawki został uruchomiony; wynik CI jest sprawdzany osobno. Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
