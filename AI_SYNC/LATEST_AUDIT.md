# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `24`
- Branch roboczy: `develop`
- Zweryfikowany workflow: `#153`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Wykryto, że Source of Truth i BOT_QUEUE były nowsze niż LATEST_AUDIT/TRIGGER, mimo że wcześniejszy AI_SYNC gate przechodził. Dodano `tests/check_ai_sync_freshness.py` i krok CI, który wymaga, aby raport i trigger nie były starsze niż wspólny stan, `TRIGGER.source_iteration` odpowiadał iteracji raportu, a `action/task_id/target_agent` zgadzały się z `machine_action`.

Dodatkowo dispatcher ma już dependency guard: brakująca lub nierozwiązana zależność `blocked_by` blokuje claim taska.

## Dowody

Workflow #153 dla `4aeab79a...`:

- BEST56 audit manifest: PASS
- Source of Truth consistency: PASS
- schema 11→12 contract: PASS
- AI sync dispatch protocol: PASS
- AI sync handoff freshness: PASS
- local dispatcher claim contract: PASS
- local dispatcher failure recovery: PASS
- local dispatcher mutex contract: PASS
- stale mutex recovery: PASS
- dispatcher dependency guard: PASS
- artifact discovery preflight safety: PASS
- Static application checks: FAIL przez aktywny P0 #7
- BEST40 checksum/stable: pominięte po P0 #7

## P0 / P1

- P0 #7 — aktywny i READY dla PRIMARY.
- P0 #11 — aktywny, BLOCKED przez #7.
- P1 #12 — freshness/dependency/claim/failure/mutex/stale-mutex są chronione CI; pełny lokalny runtime czeka na rzeczywistą komendę bota.
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
- Handoff freshness = CI PASS.
- READY→CLAIMED jest lokalnie serializowane przez mutex.
- unresolved `blocked_by` blokuje claim.

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
