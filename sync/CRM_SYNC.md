# CRM — Baza mieszkań / Synchronizacja

Ten plik jest ludzkim widokiem wspólnego stanu projektu. Każdy agent AI/OpenCode powinien przeczytać `sync/CRM_SOURCE_OF_TRUTH.json` i ten plik przed rozpoczęciem zmian.

## Aktualny stan

- Źródło pracy: `develop`
- Source of Truth jest zintegrowany bezpośrednio z `develop`
- P0 #7: dwa niezależne artefakty release gate — bieżący `app/FlippChill_Kalkulator.html` oraz zamrożony `versions/FlippChill_Kalkulator_BEST40.html` o referencyjnym SHA-256; preflight exact-hash jest już chroniony CI
- P0 #11: migracja schema 11→12 ma zachować ręczne daty i dane biznesowe
- P1 #12: claim/lock, failure recovery i lokalny mutex READY→CLAIMED dispatchera są chronione CI; pełny runtime czeka wyłącznie na rzeczywistą komendę bota
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

### 2026-08-26 — AUDYT BEST56 BAZA MIESZKAŃ, iteracja 14

- Dodano wykonywalny test kontraktu `tests/check_schema_11_12_contract.py` z trzema fixture'ami migracji: ręczna `preliminaryDate`, istniejąca `finalDate` oraz rekord `ongoing` bez dat.
- Test wymusza zachowanie `id`, `startDate`, `preliminaryDate`, `finalDate`, `maxDealDate` i całych `paymentParts`, a status normalizuje wyłącznie z istniejących dat.
- Test został wpięty do `.github/workflows/quality.yml` jako osobny gate przed statyczną kontrolą aplikacji.
- Workflow #57: manifest BEST56 AUDYT = PASS, nowy gate migracji 11→12 = PASS; workflow nadal zatrzymuje się na P0 #7 przy `Static application checks` z powodu braku kanonicznego `app/FlippChill_Kalkulator.html`.
- P0 #11 pozostaje OPEN, ponieważ pełne kryterium nadal wymaga uruchomienia rzeczywistej migracji w kanonicznym artefakcie i `localStorage`.
- Reguły biznesowe i polityka wersji pozostają bez zmian: `BEST56 BAZA MIESZKAŃ AUDYT`, bez zwiększania numeru.

### 2026-08-26 — AUDYT BEST56 BAZA MIESZKAŃ, iteracja 17

- Dodano `tests/check_ai_sync_protocol.py`, który deterministycznie sprawdza spójność `LATEST_AUDIT.json`, `BOT_QUEUE.json`, `TRIGGER.json`, locków, właścicieli, aktywnych P0 i ścieżek dispatchera.
- Gate został wpięty do CI jako `Verify AI sync dispatch protocol` przed `Static application checks`.
- Workflow #73: BEST56 manifest = PASS, Source of Truth consistency = PASS, schema 11→12 = PASS, AI sync dispatch protocol = PASS; workflow nadal zatrzymuje się wyłącznie na P0 #7 przy `Static application checks`.
- P1 #12 przeszedł do stanu `CI_GUARDED_PENDING_LOCAL_RUNTIME_DISPATCH_CHECK`; pozostał lokalny pełny test watcher → claim → bot → test → handoff z rzeczywistym `FLIPPCHILL_BOT_COMMAND`.
- Kolejka nadal wystawia `P0-7-CANONICAL-APP` jako jedyny READY task dla PRIMARY; P0 #11, runtime dispatch #12 i THIRD_UI pozostają poprawnie zablokowane zależnościami.
- Reguły biznesowe i polityka wersji pozostają bez zmian: `BEST56 BAZA MIESZKAŃ AUDYT`, bez zwiększania numeru.

### 2026-08-26 — AUDYT BEST56 BAZA MIESZKAŃ, iteracja 18

- Wykryto i naprawiono lukę runtime dispatch: `scripts/agent_dispatch.py` wcześniej mógł uruchomić realną komendę bota bez wcześniejszego zapisania `CLAIMED` i locka, co tworzyło ryzyko równoległego startu tego samego taska przez dwa watchery.
- Dispatcher teraz zapisuje `task.status=CLAIMED`, `lock.owner`, `lock.claimed_at` oraz `TRIGGER.status=CLAIMED` bezpośrednio przed subprocess; bez `FLIPPCHILL_BOT_COMMAND` stan pozostaje READY.
- Dodano `tests/check_agent_dispatch_claim.py` i gate `Verify local dispatcher claim contract`; workflow #83 potwierdził PASS dla BEST56 manifest, Source of Truth, schema 11→12, AI_SYNC protocol i dispatcher claim. CI nadal zatrzymuje się dopiero na P0 #7 `Static application checks`.
- Potwierdzono istnienie dokładnego historycznego `FlippChill_Kalkulator_BEST40.html` w ChatGPT File Library. Repo nadal go nie zawiera; PRIMARY ma importować lokalny artefakt wyłącznie po exact SHA-256 `c04106fe884d32dc257d852b320f2e145a93f80e5615409dc5fac17f5b171708`, a przy braku takiego pliku oznaczyć task BLOCKED.
- P1 #12 ma teraz stan `CLAIM_GUARDED_CI_PASS_PENDING_LOCAL_BOT_RUNTIME`; pozostał pełny lokalny runtime z rzeczywistym `FLIPPCHILL_BOT_COMMAND`.
- Reguły biznesowe i polityka wersji pozostają bez zmian: `BEST56 BAZA MIESZKAŃ AUDYT`, bez zwiększania numeru.

### 2026-08-26 — AUDYT BEST56 BAZA MIESZKAŃ, iteracja 19

- Wykryto drugą lukę lokalnego dispatchera: niezerowy exit code subprocess pozostawiał task i trigger w `CLAIMED`, co mogło zamrozić kolejkę.
- Dispatcher teraz po błędzie procesu zmienia wyłącznie nadal własny `CLAIMED` task na `BLOCKED`, zapisuje `last_error`, zwalnia lock i ustawia trigger `IDLE/BLOCKED`; jeśli bot wcześniej zmienił stan, jego nowszy stan pozostaje nadrzędny.
- Dodano `tests/check_agent_dispatch_failure_recovery.py` oraz gate `Verify local dispatcher failure recovery`.
- Workflow #95: BEST56 manifest, Source of Truth, schema 11→12, AI_SYNC protocol, claim contract oraz failure recovery = PASS; `Static application checks` nadal FAIL wyłącznie przez P0 #7, a BEST40 checks są pominięte downstream.
- P1 #12 ma teraz stan `FAILURE_RECOVERY_CI_PASS_PENDING_LOCAL_BOT_RUNTIME`; pozostał wyłącznie pełny lokalny runtime z prawdziwym `FLIPPCHILL_BOT_COMMAND`.
- Reguły biznesowe i polityka wersji pozostają bez zmian: `BEST56 BAZA MIESZKAŃ AUDYT`, bez zwiększania numeru.

### 2026-08-26 — AUDYT BEST56 BAZA MIESZKAŃ, iteracja 20

- Dodano `scripts/artifact_preflight.py`, który lokalnie skanuje kandydatów HTML i klasyfikuje BEST40 jako bezpieczny wyłącznie przy exact SHA-256 `c04106fe884d32dc257d852b320f2e145a93f80e5615409dc5fac17f5b171708`.
- Dodano `tests/check_artifact_preflight.py` oraz gate CI `Verify artifact discovery preflight safety`.
- Workflow #106: BEST56 manifest, Source of Truth, schema 11→12, AI_SYNC, dispatcher claim/failure recovery i artifact preflight = PASS; `Static application checks` nadal FAIL wyłącznie przez P0 #7.
- P0 #7 ma stan `PREFLIGHT_CI_PASS_AWAITING_EXACT_ARTIFACT_IMPORT`; PRIMARY ma wykonać lokalny preflight, importować historyczny BEST40 tylko przy `EXACT_MATCH`, a potem przywrócić kanoniczny `app/FlippChill_Kalkulator.html`.
- Reguły biznesowe i polityka wersji pozostają bez zmian: `BEST56 BAZA MIESZKAŃ AUDYT`, bez zwiększania numeru.

### 2026-08-26 — AUDYT BEST56 BAZA MIESZKAŃ, iteracja 22

- Wykryto race-condition lokalnego dispatchera: dwa watchery mogły równolegle odczytać `RUN_FIX + READY` przed zapisaniem `CLAIMED` i oba przejść walidację na starym stanie.
- Dodano cross-platform mutex `AI_SYNC/.dispatcher_claim.lock` przez atomowe `O_CREAT|O_EXCL`; po jego zdobyciu dispatcher ponownie czyta `TRIGGER.json` i `BOT_QUEUE.json`, a dopiero potem wykonuje READY→CLAIMED.
- Dodano `tests/check_agent_dispatch_mutex.py` i gate CI `Verify local dispatcher mutex contract`.
- Workflow #125: BEST56 manifest, Source of Truth, schema 11→12, AI_SYNC protocol, claim, failure recovery, nowy mutex i artifact preflight = PASS; cały workflow nadal kończy się dopiero na osobnym P0 #7 `Static application checks`.
- P1 #12 ma teraz stan `MUTEX_CI_PASS_PENDING_LOCAL_BOT_RUNTIME`; do pełnego zamknięcia pozostaje runtime z rzeczywistym `FLIPPCHILL_BOT_COMMAND`.
- Reguły biznesowe i polityka wersji pozostają bez zmian: `BEST56 BAZA MIESZKAŃ AUDYT`, bez zwiększania numeru.
