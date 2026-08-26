# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `26`
- Branch roboczy: `develop`
- Integracja runtime guardu w dispatcherze: `WDROŻONA`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

`agent_dispatch.py` wywołuje teraz `validate_repository_state()` z `handoff_runtime_guard.py` wewnątrz serializowanej ścieżki claimu, gdy lokalny mutex jest już zdobyty i aktualny READY state został ponownie odczytany. Błąd guardu kończy ścieżkę przed `CLAIMED`, więc realny subprocess nie może wystartować na starym lub niespójnym handoffie.

Dodano `tests/check_agent_dispatch_runtime_guard_integration.py` i krok CI `Verify dispatcher runtime guard integration`.

## Testy / CI

Nowy workflow po wdrożeniu został uruchomiony, ale podczas tej iteracji pozostawał w kolejce. Dlatego nowego gate NIE oznaczono jeszcze jako PASS. Poprzedni workflow #168 kończył się na istniejącym P0 #7 po przejściu wcześniejszych gate'ów.

## P0 / P1

- P0 #7 — aktywny i READY dla PRIMARY.
- P0 #11 — aktywny, BLOCKED przez #7.
- P1 #12 — część kodowa integracji runtime guardu jest wdrożona; pozostał wynik bieżącego CI oraz pełny lokalny smoke z rzeczywistym `FLIPPCHILL_BOT_COMMAND`.
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
- `source_iteration = 26`
- Runtime guard integration = `INTEGRATED_BEFORE_CLAIM`.

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
