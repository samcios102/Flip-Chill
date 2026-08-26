# CRM — Baza mieszkań / Synchronizacja

Ten plik jest ludzkim widokiem wspólnego stanu projektu. Każdy agent AI/OpenCode powinien przeczytać `sync/CRM_SOURCE_OF_TRUTH.json` i ten plik przed rozpoczęciem zmian.

## Aktualny stan

- Źródło pracy: `develop`
- Source of Truth jest zintegrowany bezpośrednio z `develop`
- P0 #7: dwa niezależne artefakty release gate — bieżący `app/FlippChill_Kalkulator.html` oraz zamrożony `versions/FlippChill_Kalkulator_BEST40.html` o referencyjnym SHA-256
- P0 #11: migracja schema 11→12 ma zachować ręczne daty i dane biznesowe
- DOM IDs: quality gate ma wymagać 0 duplikatów
- ARIA: quality gate ma wymagać 0 uszkodzonych referencji
- Finanse: CIT 9%, VAT 23%, domyślny PIT agenta 12%
- Slack/Marketing zasila progi miesięczne 50 000 / 100 000 PLN

## Baza mieszkań — decyzje obowiązujące

1. „Baza mieszkań / Wszystkie transakcje” otwarta domyślnie.
2. „Portfel”, „Wynik” i „Wypłaty” zwinięte domyślnie.
3. `+ Dodaj transakcję` w górnym prawym obszarze.
4. Globalny filtr działa ponad filtrami statusów i obejmuje wszystkie rekordy.
5. Status płatności i status agenta/transakcji mają być zmienialne kliknięciem, jeśli dana rola ma uprawnienie.
6. Widok danych ma być większy, czytelniejszy i zachowywać estetyczny desktopowy układ.
7. Ikonografia: otrzymane → sprzedane; żółta ikona → otwarta skrzynia skarbów.

## Protokół pracy OpenCode

Przed zmianą:

1. `git pull`
2. przeczytaj `sync/CRM_SOURCE_OF_TRUTH.json`
3. przeczytaj `sync/CRM_SYNC.md`
4. przeczytaj `BACKLOG.md`
5. sprawdź otwarte Issues P0/P1

Po zmianie:

1. uruchom testy
2. zaktualizuj `sync/CRM_SOURCE_OF_TRUTH.json`, jeśli zmieniła się reguła biznesowa lub status blokera
3. dopisz TYLKO nowe ustalenia do sekcji „Dziennik zmian” poniżej
4. zaktualizuj `BACKLOG.md`
5. commituj kod + aktualizację stanu razem

## Dziennik zmian

### 2026-08-25 — inicjalizacja wspólnego źródła prawdy

- Utworzono maszynowy manifest `sync/CRM_SOURCE_OF_TRUTH.json`.
- Ustalono repozytorium jako kanał synchronizacji między OpenCode, CRM Baza mieszkań i audytami.
- Ustalono zasadę: reguły biznesowe mają jedno źródło prawdy i nie są kopiowane niezależnie między modułami.

### 2026-08-25 — AUDYT BEST56 BAZA MIESZKAŃ, iteracja 9

- Potwierdzono na aktualnym kandydacie realny P0 migracji schema 11→12: ręczna `preliminaryDate` nie może być czyszczona.
- Bezpieczny kandydat audytowy zachowuje `preliminaryDate` i wyprowadza status z istniejących dat (`finalDate` → `closed`, `preliminaryDate` → `preliminary`).
- Walidacja kandydata: 9/9 bloków JavaScript PASS, 766 unikalnych ID DOM, 0 duplikatów, 38/38 referencji DOM poprawnych.
- `tests/check_app.py` został dostosowany do aktualnego UX BEST56: Daty otwierają się z jednego przycisku wybranej transakcji `#fac-portfolio-dates-selected`, zamiast wymagać usuniętego przycisku per-row `data-open-pf-dates=`.
- P0 #7 pozostaje otwarte do czasu umieszczenia kanonicznego `app/FlippChill_Kalkulator.html`; polityka wersji pozostaje BEST56 + dopisek `AUDYT`.

### 2026-08-26 — AUDYT BEST56 BAZA MIESZKAŃ, iteracja 10

- PR #9 został bezpiecznie scalony do `develop`; `OPENCODE.md`, `sync/CRM_SOURCE_OF_TRUTH.json` i `sync/CRM_SYNC.md` są teraz bezpośrednio w gałęzi roboczej.
- Usunięto zależność operacyjną od osobnej gałęzi `feat/crm-source-of-truth`.
- Reguły biznesowe i polityka wersji nie zmieniły się: automat zachowuje BEST56 i dopisek `AUDYT`.
- P0 #7 i P0 #11 pozostają aktywne; następny techniczny priorytet to kanoniczny artefakt aplikacji oraz realny test migracji `localStorage`.

### 2026-08-26 — AUDYT BEST56 BAZA MIESZKAŃ, iteracja 11

- P1 #10 został zamknięty jako zakończony: fingerprint bazowego BEST56, kontrola DOM/ARIA/JS, reguły finansowe oraz osobny gate CI BEST56 AUDYT są już udokumentowane i zweryfikowane.
- `CRM_SOURCE_OF_TRUTH.json` został zsynchronizowany: #10 usunięto z `current_blockers`; aktywne pozostają P0 #7 i P0 #11.
- Reguły biznesowe i polityka wersji nie zmieniły się. Automat nadal utrzymuje `BEST56 BAZA MIESZKAŃ AUDYT` i NIE tworzy BEST57.

### 2026-08-26 — AUDYT BEST56 BAZA MIESZKAŃ, iteracja 13

- Zsynchronizowano Source of Truth z potwierdzoną diagnozą P0 #7: release gate składa się z dwóch niezależnych artefaktów, bieżącego `app/FlippChill_Kalkulator.html` i historycznego `versions/FlippChill_Kalkulator_BEST40.html`.
- Do manifestu dodano ścieżkę zamrożonego BEST40 i referencyjny SHA-256 `c04106fe884d32dc257d852b320f2e145a93f80e5615409dc5fac17f5b171708`.
- Workflow #53 dla poprzedniego commitu zakończył się `failure`; status P0 #7 i P0 #11 pozostaje OPEN.
- Reguły biznesowe oraz polityka wersji pozostają bez zmian: `BEST56 BAZA MIESZKAŃ AUDYT`, bez podbijania numeru.
