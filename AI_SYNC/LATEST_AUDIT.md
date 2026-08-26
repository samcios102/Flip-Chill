# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `27`
- Branch roboczy: `develop`
- Integracja runtime guardu w dispatcherze: `CI PASS`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Workflow #176 na commicie `9293c8766dd047bb233c5808391e282c6d5f5ac4` potwierdził, że kodowy łańcuch bezpieczeństwa dispatchera działa: BEST56 manifest, Source of Truth, schema 11→12, AI_SYNC, freshness, runtime guard, integracja guardu w dispatcherze, claim/failure/mutex/stale-mutex/dependencies i artifact preflight = PASS.

## Testy / CI

`Static application checks` nadal = FAIL przez P0 #7. BEST40 checksum/stable pozostają downstream. To oznacza: P1 #12 ma już CI PASS dla części kodowej, a do pełnego zamknięcia pozostaje wyłącznie lokalny smoke z realnym `FLIPPCHILL_BOT_COMMAND`.

## P0 / P1

- P0 #7 — aktywny i READY dla PRIMARY.
- P0 #11 — aktywny, BLOCKED przez #7.
- P1 #12 — `DISPATCHER_RUNTIME_GUARD_INTEGRATED_CI_PASS_PENDING_LOCAL_RUNTIME`.
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
- `source_iteration = 27`
- Runtime guard integration = `CI_PASS_BEFORE_CLAIM`.

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
