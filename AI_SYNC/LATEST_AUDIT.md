# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `22`
- Branch roboczy: `develop`
- Testowany commit: `5bbe358ad344b6ea98e43a0f1b059c3875f37bb8`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Wykryto race-condition lokalnego dispatchera: dwa watchery mogły równolegle odczytać `RUN_FIX + READY` przed zapisaniem `CLAIMED`. Dispatcher ma teraz cross-platform mutex `AI_SYNC/.dispatcher_claim.lock` tworzony atomowo przez `O_CREAT|O_EXCL`. Po zdobyciu mutexa ponownie czyta `TRIGGER.json` i `BOT_QUEUE.json`; tylko aktualny `READY` może przejść do `CLAIMED`. Mutex jest zwalniany przed subprocess bota.

## Dowody

Workflow #125 dla `5bbe358a...`:

- BEST56 audit manifest: PASS
- Source of Truth consistency: PASS
- schema 11→12 contract: PASS
- AI sync dispatch protocol: PASS
- local dispatcher claim contract: PASS
- local dispatcher failure recovery: PASS
- local dispatcher mutex contract: PASS
- artifact discovery preflight safety: PASS
- Static application checks: FAIL przez aktywny P0 #7
- BEST40 checksum/stable: pominięte po P0 #7

## P0 / P1

- P0 #7 — aktywny i READY dla PRIMARY.
- P0 #11 — aktywny, BLOCKED przez #7.
- P1 #12 — mutex/claim/failure recovery są już chronione CI; pełny lokalny runtime czeka na rzeczywistą komendę bota.
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
- READY→CLAIMED jest lokalnie serializowane przez mutex.

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
