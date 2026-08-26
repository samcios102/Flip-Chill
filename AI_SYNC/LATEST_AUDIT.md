# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `21`
- Branch roboczy: `develop`
- Testowany commit: `d98dfacd5af264c1380ebf66ce54ce59389c21b6`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Naprawiono dwa gate’y CI, które błędnie uznawały P0 za aktywne tylko przy literalnym `status=OPEN`. Etapowe nie-terminalne statusy, np. `PREFLIGHT_CI_PASS_AWAITING_EXACT_ARTIFACT_IMPORT`, są teraz poprawnie traktowane jako aktywne. Jawne terminalne stany (`DONE`, `CLOSED`, `RESOLVED`, `COMPLETED`, `SUPERSEDED`, `REJECTED`) wyłączają blocker.

## Dowody

Workflow dla `d98dfacd...`:

- BEST56 audit manifest: PASS
- Source of Truth consistency: PASS
- schema 11→12 contract: PASS
- AI sync dispatch protocol: PASS
- local dispatcher claim contract: PASS
- local dispatcher failure recovery: PASS
- artifact discovery preflight safety: PASS
- Static application checks: FAIL przez aktywny P0 #7
- BEST40 checksum/stable: pominięte po P0 #7

## P0 / P1

- P0 #7 — aktywny i READY dla PRIMARY.
- P0 #11 — aktywny, BLOCKED przez #7.
- P1 #12 — lokalny runtime dispatch czeka na rzeczywistą komendę bota.
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

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
