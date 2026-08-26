# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `19`
- Branch roboczy: `develop`
- Testowany commit: `9de64f55346155a5e68b97fba4169eaaec68ea3b`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Naprawiono drugi przypadek blokowania lokalnego dispatchera. Jeśli uruchomiony bot kończy się niezerowym kodem i task nadal jest `CLAIMED` przez tego samego agenta, dispatcher zapisuje `BLOCKED`, `last_error`, zwalnia lock oraz przełącza trigger na `IDLE/BLOCKED`. Jeśli bot sam zdążył zmienić stan na WORKING/TESTING/DONE/BLOCKED, dispatcher zachowuje nowszy stan bota.

## Dowody

Workflow #95:

- BEST56 audit manifest: PASS
- Source of Truth consistency: PASS
- schema 11→12 contract: PASS
- AI sync dispatch protocol: PASS
- local dispatcher claim contract: PASS
- local dispatcher failure recovery: PASS
- Static application checks: FAIL przez aktywny P0 #7
- BEST40 checksum/stable: pominięte po P0 #7

## P0 / P1

- P0 #7 — nadal najwyższy READY task dla PRIMARY.
- P0 #11 — BLOCKED przez #7; po canonical app SECOND_AUDIT wykonuje realny runtime `localStorage`.
- P1 #12 — claim/lock i failure recovery są zabezpieczone testami CI; pozostał pełny lokalny runtime z rzeczywistą komendą bota.
- THIRD_UI czeka na canonical app.

## Handoff dla 3 botów

### PRIMARY

Claim `P0-7-CANONICAL-APP`. Importuj historyczny BEST40 tylko przy dokładnym SHA-256 `c04106fe884d32dc257d852b320f2e145a93f80e5615409dc5fac17f5b171708`; przy braku exact match oznacz task BLOCKED. Następnie przywróć kanoniczny `app/FlippChill_Kalkulator.html`, uruchom gate'y i zaktualizuj AI_SYNC.

### SECOND_AUDIT

Po zielonym P0 #7 wykonaj realny test migracji schema 11→12 na `localStorage`: daty, `paymentParts`, status derivation i ponowne otwarcie.

### THIRD_UI

Po canonical app wykonaj 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression. Nie zmieniaj finansów.

## Auto-dispatch

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7-CANONICAL-APP`
- `target_agent = PRIMARY`

`P1-12-LOCAL-DISPATCH-RUNTIME` pozostaje BLOCKED wyłącznie do czasu lokalnego ustawienia `FLIPPCHILL_BOT_COMMAND` i potwierdzenia pełnego cyklu watcher → claim → bot → test → handoff.
