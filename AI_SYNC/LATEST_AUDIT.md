# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Branch roboczy: `develop`
- Automatyczne podbijanie numeru BEST: zabronione

## Najwyższy priorytet

`P0-7-CANONICAL-APP` — przywrócić kanoniczny `app/FlippChill_Kalkulator.html` oraz zweryfikowany zamrożony `versions/FlippChill_Kalkulator_BEST40.html` bez modyfikacji `main`.

## Aktualne dowody

- BEST56 audit manifest gate: PASS
- schema 11→12 contract gate: PASS
- Source of Truth consistency gate: PASS
- Static application checks: BLOCKED przez P0 #7
- pełne CI: FAIL do czasu usunięcia P0 #7

## Handoff dla 3 botów

### PRIMARY

Claim `P0-7-CANONICAL-APP`. Napraw release gate na `develop`/feature branch. Nie zmieniaj `main`. Po naprawie uruchom wszystkie dostępne gate'y i zapisz wynik w `AI_SYNC/BOT_QUEUE.json` + `AI_SYNC/LATEST_AUDIT.json`.

### SECOND_AUDIT

Czeka na P0 #7. Po zielonym canonical app wykonaj runtime test migracji schema 11→12 na realnym `localStorage` dla issue #11. Zweryfikuj daty i `paymentParts`.

### THIRD_UI

Czeka na canonical app. Następnie audyt 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression. Nie zmieniaj reguł finansowych.

## Auto-dispatch

Raport ustawia `AI_SYNC/TRIGGER.json` na:

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7-CANONICAL-APP`
- `target_agent = PRIMARY`

Watcher uruchomiony przez `python scripts/agent_dispatch.py --watch` może przejąć to zadanie automatycznie i zbudować prompt dla bota.

## Następne po naprawie P0 #7

1. P0 #11 — runtime localStorage migration.
2. THIRD_UI — responsywność i accessibility.
3. Ponowny audyt CI + kolejny raport nadal jako `BEST56 BAZA MIESZKAŃ AUDYT`.
