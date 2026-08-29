# CRM — Baza mieszkań / Synchronizacja

Ten plik jest ludzkim widokiem **aktualnego** wspólnego stanu projektu. Maszynowym źródłem prawdy jest `sync/CRM_SOURCE_OF_TRUTH.json`. Szczegółowa historia wcześniejszych iteracji BEST56 pozostaje zachowana w historii Git i w `audit/BEST56_*`; nie jest już kopiowana do sekcji bieżącego stanu.

## Aktualny stan

- Źródło pracy: `develop`
- **Najwyższy zweryfikowany standard:** `BEST73 BAZA MIESZKAŃ`
- **Repo release target:** `BEST73 BAZA MIESZKAŃ`
- **Bieżący audit:** `BEST73 BAZA MIESZKAŃ AUDYT`
- Exact BEST73: `FlippChill_Kalkulator_BEST73_BAZA_MIESZKAN(1).html`, 986881 B, SHA-256 `492a321a07729c480947e12a0afb6678f135717e8a66cd0f12d2cae40f1f89c4`
- P0 #19: reconciliation wersji wykonane — BEST56 przestał być bieżącym targetem i pozostaje historycznym baseline.
- P0 #20: **READY / PRIMARY** — zaimportować exact BEST73 do canonical app i uogólnić pipeline z BEST56-specific na current-standard.
- P0 #11: runtime migracji schema 11→12 pozostaje BLOCKED wyłącznie do canonical BEST73.
- P0 #7A: SUPERSEDED jako bieżący task; dotyczył canonical BEST56. P0 #7B / exact BEST40 pozostaje niezależną historią i nie blokuje BEST73.
- P1 #12: lokalny pełny watcher/bot runtime nadal wymaga rzeczywistego `FLIPPCHILL_BOT_COMMAND`.
- P1 #18: ciągła praca wielobotowa pozostaje regułą; po każdym handoffie system ma wybierać kolejne niezależne READY zadanie.
- DOM IDs: release gate wymaga 0 duplikatów.
- ARIA: release gate wymaga 0 uszkodzonych referencji.
- Finanse: CIT 9%, VAT 23%, domyślny PIT agenta 12%, search bonus 10%.
- Slack/Marketing zasila progi miesięczne 50 000 / 100 000 PLN.

## Baza mieszkań — decyzje obowiązujące

1. „Baza mieszkań / Wszystkie transakcje” otwarta domyślnie.
2. „Portfel”, „Wynik” i „Wypłaty” zwinięte domyślnie.
3. `+ Dodaj transakcję` w górnym prawym obszarze.
4. Globalny filtr działa ponad filtrami statusów i obejmuje wszystkie rekordy.
5. Status płatności i status agenta/transakcji mają być zmienialne kliknięciem, jeśli dana rola ma uprawnienie.
6. Widok danych ma być większy, czytelniejszy i zachowywać estetyczny desktopowy układ.
7. Ikonografia: otrzymane → sprzedane; żółta ikona → otwarta skrzynia skarbów.
8. Audyt sam w sobie **nie tworzy kolejnego numeru BEST**. Bieżący audyt ma numer faktycznej, zweryfikowanej bazy.
9. Każda misja zaczyna się od VERSION + MISSION DISCOVERY. Nowsza wersja może zostać promowana tylko po realnej weryfikacji i aktualizacji Source of Truth.

## Protokół pracy OpenCode

Przed zmianą stosuj dokładnie kanoniczny `sync_contract.required_read_order` z `sync/CRM_SOURCE_OF_TRUTH.json`:

1. `sync/CRM_SOURCE_OF_TRUTH.json`
2. `AI_SYNC/PROTOCOL.md`
3. `AI_SYNC/LATEST_AUDIT.json`
4. `AI_SYNC/BOT_QUEUE.json`
5. `AI_SYNC/TRIGGER.json`
6. `sync/CRM_SYNC.md`
7. `BACKLOG.md`
8. sprawdź otwarte Issues P0/P1 i aktualny CI

Po zmianie:

1. uruchom dostępne testy;
2. aktualizuj Source of Truth, jeśli zmieniła się wersja, reguła biznesowa lub blocker;
3. aktualizuj ten bieżący stan i BACKLOG;
4. aktualizuj `LATEST_AUDIT`, kolejkę oraz trigger;
5. nie modyfikuj `main` automatycznie;
6. nie deklaruj PASS bez dowodu CI/testów.

## Dziennik zmian — bieżąca linia

### 2026-08-29 — reconciliation do BEST73 / iteracja 92

- Najnowsza jawna decyzja użytkownika zastąpiła wcześniejsze przypięcie misji do BEST56: projekt ma być wyrównany do najwyższej zweryfikowanej wersji.
- Zweryfikowano BEST73 z Library: 986881 B, SHA-256 `492a321a07729c480947e12a0afb6678f135717e8a66cd0f12d2cae40f1f89c4`; nie znaleziono zweryfikowanego BEST74+ w dostępnych źródłach.
- `release_target`, `audit_base`, `LATEST_AUDIT`, `BOT_QUEUE` i `TRIGGER` zostały przełączone na BEST73.
- Utworzono issue #20 oraz task `P0-20-BEST73-CANONICAL-APP` dla PRIMARY.
- BEST56 i BEST40 pozostają historyczne; niczego nie usuwamy z Git history / audit archive.
- Runtime finanse, migracja 11→12 i THIRD_UI dla BEST73 pozostają zablokowane do czasu exact canonicalizacji BEST73.
