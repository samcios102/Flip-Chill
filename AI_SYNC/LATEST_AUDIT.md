# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `29`
- Branch roboczy: `develop`
- Najwyższy priorytet: `P0-7A-CANONICAL-APP`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Rozdzielono issue #7 na dwa niezależne zadania kolejki:

- `P0-7A-CANONICAL-APP` — bieżący exact BEST56 jako `app/FlippChill_Kalkulator.html`;
- `P0-7B-FROZEN-BEST40` — historyczny BEST40 z exact SHA-256.

Dzięki temu `P0-11-RUNTIME-MIGRATION` i `P1-UI-RESPONSIVE-AUDIT` czekają tylko na canonical app 7A. Historyczny BEST40 pozostaje osobnym release gate i NIE blokuje już audytu integralności danych ani UI po wystawieniu canonical app.

## Testy / CI

- workflow #188 na `30c94c1...`: wszystkie gate'y do `Verify canonical app staging safety` = `PASS`;
- `Static application checks` = `FAIL` z powodu aktywnego P0 #7 / braku canonical app;
- nowy `tests/check_queue_dependency_partition.py`: dodany i wpięty do CI;
- wynik nowego gate'u dla iteracji 29: `CI PENDING`.

## P0 / P1

- P0 #7 — aktywny, rozdzielony operacyjnie na 7A READY i 7B BLOCKED.
- P0 #11 — aktywny, BLOCKED wyłącznie przez 7A.
- P1 #12 — lokalny realny bot runtime pozostaje otwarty.
- P1 #13 — dependency partition wdrożony, oczekuje na dowód CI.

## Handoff dla 3 botów

### PRIMARY

Claim `P0-7A-CANONICAL-APP`.

1. Uruchom `python scripts/stage_canonical_app.py <ścieżka-do-exact-BEST56>`.
2. Kandydat musi mieć SHA-256 `3bb0756f...f4044e92`.
3. Uruchom `Static application checks`.
4. BEST40 obsługuj osobno jako `P0-7B-FROZEN-BEST40`, wyłącznie po `EXACT_MATCH`.
5. `main` pozostaje bez zmian.

### SECOND_AUDIT

Po DONE `P0-7A-CANONICAL-APP` wykonaj realny test migracji schema 11→12 na `localStorage`. NIE czekaj na BEST40.

### THIRD_UI

Po DONE `P0-7A-CANONICAL-APP` wykonaj audyt 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression. NIE zmieniaj finansów.

## Auto-dispatch

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7A-CANONICAL-APP`
- `target_agent = PRIMARY`
- `source_iteration = 29`

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
