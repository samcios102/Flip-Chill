# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `20`
- Branch roboczy: `develop`
- Testowany commit: `315b274f7701abe35c82ddf0688ad8d7b261444c`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Dodano `scripts/artifact_preflight.py`. PRIMARY może przeskanować lokalne katalogi z artefaktami, a BEST40 jest oznaczany jako `EXACT_MATCH` wyłącznie przy SHA-256 `c04106fe884d32dc257d852b320f2e145a93f80e5615409dc5fac17f5b171708`. Nazwa pliku bez zgodnego hasha NIE wystarcza do importu.

## Dowody

Workflow #106:

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

- P0 #7 — `PREFLIGHT_CI_PASS_AWAITING_EXACT_ARTIFACT_IMPORT`; nadal READY dla PRIMARY.
- P0 #11 — BLOCKED przez #7; po canonical app SECOND_AUDIT wykonuje realny runtime `localStorage`.
- P1 #12 — pełny lokalny runtime nadal czeka na rzeczywistą komendę bota.
- THIRD_UI czeka na canonical app.

## Handoff dla 3 botów

### PRIMARY

Claim `P0-7-CANONICAL-APP`. Najpierw uruchom `python scripts/artifact_preflight.py <katalogi_z_artefaktami> --output AI_SYNC/ARTIFACT_PREFLIGHT.json`. Importuj historyczny BEST40 tylko przy `EXACT_MATCH`; przy braku exact match oznacz task BLOCKED. Następnie przywróć kanoniczny `app/FlippChill_Kalkulator.html` i uruchom pełny workflow.

### SECOND_AUDIT

Po zielonym P0 #7 wykonaj realny test migracji schema 11→12 na `localStorage`: daty, `paymentParts`, status derivation i ponowne otwarcie.

### THIRD_UI

Po canonical app wykonaj 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression. Nie zmieniaj finansów.

## Auto-dispatch

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7-CANONICAL-APP`
- `target_agent = PRIMARY`

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
