# CRM — Baza mieszkań / Synchronizacja

Ten plik jest ludzkim widokiem wspólnego stanu projektu. Każdy agent AI/OpenCode powinien przeczytać `sync/CRM_SOURCE_OF_TRUTH.json` i ten plik przed rozpoczęciem zmian.

## Aktualny stan

- Źródło pracy: `develop`
- Gałąź integracyjna rozwiązania: `feat/crm-source-of-truth`
- P0: reprodukowalny `app/FlippChill_Kalkulator.html`
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
