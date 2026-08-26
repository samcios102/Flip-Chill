# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `17`
- Branch roboczy: `develop`
- Testowany commit: `275bbf757cddba406b2d1e1c99ab04cd4797770a`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Dodano twardy gate `tests/check_ai_sync_protocol.py` i krok CI `Verify AI sync dispatch protocol`. Gate sprawdza spójność raportu, kolejki, triggera, locków, właścicieli zadań, aktywnych P0 oraz ścieżek dispatchera.

## Dowody

Workflow #73 na testowanym commicie:

- BEST56 audit manifest: PASS
- Source of Truth consistency: PASS
- schema 11→12 contract: PASS
- AI sync dispatch protocol: PASS
- Static application checks: FAIL przez aktywny P0 #7
- BEST40 checksum/stable: pominięte po P0 #7

## P0 / P1

- P0 #7 — nadal najwyższy READY task dla PRIMARY.
- P0 #11 — BLOCKED przez #7; po canonical app SECOND_AUDIT wykonuje realny runtime `localStorage`.
- P1 #12 — statyczny protokół jest już chroniony CI; pozostał lokalny pełny runtime dispatcher z rzeczywistą komendą bota.
- THIRD_UI czeka na canonical app.

## Handoff dla 3 botów

### PRIMARY

Claim `P0-7-CANONICAL-APP`. Przywróć kanoniczny `app/FlippChill_Kalkulator.html` oraz zweryfikowany zamrożony `versions/FlippChill_Kalkulator_BEST40.html`. Pracuj poza `main`, uruchom wszystkie gate'y i zaktualizuj AI_SYNC.

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
