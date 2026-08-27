# CRM — Baza mieszkań / Synchronizacja

Ten plik jest ludzkim widokiem wspólnego stanu projektu. Każdy agent AI/OpenCode powinien przeczytać `sync/CRM_SOURCE_OF_TRUTH.json` i ten plik przed rozpoczęciem zmian.

## Aktualny stan

- Źródło pracy: `develop`
- Source of Truth jest zintegrowany bezpośrednio z `develop`
- P0 #7: dwa niezależne artefakty release gate — bieżący `app/FlippChill_Kalkulator.html` oraz zamrożony `versions/FlippChill_Kalkulator_BEST40.html`; 7A ma exact-SHA packager + materializer + runtime-verified stager, workflow #293 potwierdza packager PASS i oczekuje już na lokalne wykonanie packaging → materialization → static check; 7B pozostaje BLOCKED na exact BEST40
- P0 #11: migracja schema 11→12 ma zachować ręczne daty i dane biznesowe; runtime zależy tylko od canonical app 7A
- P1 #12: claim/lock, failure recovery, mutex, stale-mutex recovery, dependency guard, freshness, runtime handoff guard oraz root `OPENCODE.md` read-order są chronione CI; pełny lokalny bot runtime pozostaje otwarty
- P1 #13: CLOSED / CI_VERIFIED — dependency partition 7A/7B potwierdzony workflow #202
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

### 2026-08-26 — AUDYT BEST56 BAZA MIESZKAŃ, iteracja 25

- Wykryto lukę między kontraktem CI a runtime: `check_ai_sync_freshness.py` blokował stale handoff w CI, ale lokalny `agent_dispatch.py` nie miał niezależnej walidacji świeżości bezpośrednio przed subprocess.
- Dodano side-effect-free `scripts/handoff_runtime_guard.py` oraz `tests/check_handoff_runtime_guard.py`.
- Workflow #160 potwierdził `Verify runtime handoff guard contract = PASS`; wszystkie wcześniejsze gate'y automatyki również PASS, a `Static application checks` nadal FAIL wyłącznie przez P0 #7.
- P1 #12 ma stan `RUNTIME_GUARD_COMPONENT_CI_PASS_PENDING_DISPATCHER_INTEGRATION_AND_LOCAL_RUNTIME`; następny mały krok to wpięcie guardu do `agent_dispatch.py` bezpośrednio przed realnym subprocess, potem smoke z prawdziwym `FLIPPCHILL_BOT_COMMAND`.
- Reguły CRM, finanse i polityka wersji pozostają bez zmian: `BEST56 BAZA MIESZKAŃ AUDYT`, bez zwiększania numeru.

### 2026-08-26 — AUDYT BEST56 BAZA MIESZKAŃ, iteracja 26

- Wpięto `validate_repository_state()` z `scripts/handoff_runtime_guard.py` bezpośrednio do serializowanej ścieżki `claim_current_ready_task()` w dispatcherze.
- Guard uruchamia się przy zdobytym mutexie, po ponownym odczycie aktualnego `RUN_FIX + READY`, zależności i ownera, ale przed zmianą taska na `CLAIMED`; błąd guardu kończy dispatch bez subprocess.
- Dodano `tests/check_agent_dispatch_runtime_guard_integration.py` oraz krok CI `Verify dispatcher runtime guard integration`.
- Bieżący workflow został uruchomiony, ale podczas publikacji handoffu nadal oczekiwał w kolejce; nowego gate NIE oznaczono jeszcze jako PASS.
- P1 #12 ma stan `DISPATCHER_RUNTIME_GUARD_INTEGRATED_CI_PENDING_LOCAL_RUNTIME`; po wyniku CI pozostanie pełny lokalny smoke z rzeczywistym `FLIPPCHILL_BOT_COMMAND`.
- Reguły CRM, finanse i polityka wersji pozostają bez zmian: `BEST56 BAZA MIESZKAŃ AUDYT`, bez zwiększania numeru.

### 2026-08-26 — AUDYT BEST56 BAZA MIESZKAŃ, iteracja 27

- Workflow #176 na commicie `9293c8766dd047bb233c5808391e282c6d5f5ac4` potwierdził PASS dla BEST56 manifest, Source of Truth, schema 11→12, AI_SYNC protocol/freshness, runtime handoff guard, bezpośredniej integracji guardu w dispatcherze, claim/failure/mutex/stale-mutex/dependencies oraz artifact preflight.
- `Static application checks` nadal FAIL przez aktywny P0 #7; BEST40 checksum i frozen stable pozostają pominięte downstream.
- P1 #12 przeszedł do `DISPATCHER_RUNTIME_GUARD_INTEGRATED_CI_PASS_PENDING_LOCAL_RUNTIME`; do pełnego zamknięcia pozostał tylko realny lokalny smoke z `FLIPPCHILL_BOT_COMMAND`.
- P0 #7 pozostaje jedynym READY taskiem dla PRIMARY; P0 #11 i THIRD_UI nadal są prawidłowo zablokowane zależnościami.
- Reguły CRM, finanse i polityka wersji pozostają bez zmian: `BEST56 BAZA MIESZKAŃ AUDYT`, bez zwiększania numeru.

### 2026-08-26 — AUDYT BEST56 BAZA MIESZKAŃ, iteracja 28

- Ponownie zweryfikowano lokalny bazowy BEST56: SHA-256 `3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92`, dokładnie zgodny z Source of Truth.
- Dodano `scripts/stage_canonical_app.py`: canonical `app/FlippChill_Kalkulator.html` może zostać przygotowany wyłącznie z exact baseline BEST56; mismatch kończy się `BLOCKED` bez kopiowania.
- Dodano `tests/check_stage_canonical_app.py` oraz krok CI `Verify canonical app staging safety` przed `Static application checks`.
- Historyczny BEST40 pozostaje niezależnym gate i nadal wymaga exact SHA-256 `c04106fe884d32dc257d852b320f2e145a93f80e5615409dc5fac17f5b171708`; żaden podobnie nazwany plik nie może go zastąpić.
- Workflow #188 na `30c94c1...`: wszystkie gate'y do canonical staging = PASS; `Static application checks` = FAIL przez brak canonical app.
- P0 #7 ma stan operacyjny przygotowany do lokalnego stage exact BEST56.
- Reguły CRM, finanse i polityka wersji pozostają bez zmian: `BEST56 BAZA MIESZKAŃ AUDYT`, bez zwiększania numeru.

### 2026-08-26 — AUDYT BEST56 BAZA MIESZKAŃ, iteracja 29

- Wykryto nadmierną zależność w kolejce: P0 #11 i THIRD_UI czekały na cały #7, mimo że do pracy potrzebują tylko canonical app, a historyczny BEST40 jest osobnym release gate.
- Rozdzielono issue #7 na `P0-7A-CANONICAL-APP` (READY, PRIMARY) oraz `P0-7B-FROZEN-BEST40` (BLOCKED na exact lokalny artefakt).
- `P0-11-RUNTIME-MIGRATION` i `P1-UI-RESPONSIVE-AUDIT` zależą teraz wyłącznie od 7A; po canonical app mogą ruszyć niezależnie od BEST40.
- Dodano `tests/check_queue_dependency_partition.py` i gate CI `Verify BEST56 queue dependency partition`.
- Utworzono issue #13 śledzące kontrakt zależności; Source of Truth, BACKLOG, AI_SYNC i trigger zostały zsynchronizowane.
- Reguły biznesowe, finanse i polityka wersji pozostają bez zmian: `BEST56 BAZA MIESZKAŃ AUDYT`, bez zwiększania numeru.

### 2026-08-26 — AUDYT BEST56 BAZA MIESZKAŃ, iteracja 31

- Usunięto niespójność dokumentacji stanu: issue #13 jest `closed/completed`, a workflow #202 potwierdził `Verify BEST56 queue dependency partition = PASS`.
- `BACKLOG.md` oznacza teraz #13 jako ukończone; sekcja „Aktualny stan” tego pliku ma `P1 #13: CLOSED / CI_VERIFIED`.
- Source of Truth już wcześniej poprawnie usuwał #13 z aktywnych blockerów, więc reguły biznesowe i aktywne P0/P1 nie zmieniły się.
- Najwyższy READY task pozostaje `P0-7A-CANONICAL-APP` dla PRIMARY; numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.

### 2026-08-26 — AUDYT BEST56 BAZA MIESZKAŃ, iteracja 32

- Wykonano rzeczywisty runtime test `scripts/stage_canonical_app.py` na exact lokalnym BEST56: dry-run = PASS oraz atomowe staging do tymczasowego targetu = PASS.
- SHA-256 wejścia i staged targetu są identyczne: `3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92`.
- Workflow #216 na `8b00996f...` potwierdził 15/15 gate'ów przed aplikacją = PASS; `Static application checks` nadal FAIL, ponieważ canonical app nie jest jeszcze zapisany w repo.
- Source of Truth zmienił stan #7 na `CANONICAL_STAGER_RUNTIME_VERIFIED_AWAITING_REPOSITORY_STAGE_BEST40_BLOCKED`.
- `P0-7A-CANONICAL-APP` pozostaje READY dla PRIMARY, ale nie wymaga już ponownego sprawdzania stagera — następny krok to zapis exact BEST56 jako `app/FlippChill_Kalkulator.html` na `develop` i uruchomienie Static application checks.
- P0 #11 nadal zależy wyłącznie od 7A; reguły finansowe i polityka wersji pozostają bez zmian: `BEST56 BAZA MIESZKAŃ AUDYT`.

### 2026-08-27 — AUDYT BEST56 BAZA MIESZKAŃ, iteracja 34

- Wykryto przenośnościowy blocker 7A: `--auto` znał tylko stałe lokalne rooty, podczas gdy różne runtime'y agentów mogą montować exact BEST56 w innych katalogach.
- Dodano `FLIPPCHILL_ARTIFACT_ROOTS`; rooty z env są sprawdzane przed cwd/Downloads/Desktop/OneDrive, nadal wyłącznie po exact SHA-256 `3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92`.
- Rozszerzono `tests/check_stage_canonical_app.py` o env-root discovery i deterministyczny wybór.
- Workflow #239 oraz finalny workflow #247: wszystkie gate'y przed aplikacją = PASS, w tym canonical staging; `Static application checks` nadal FAIL wyłącznie przez brak `app/FlippChill_Kalkulator.html` w repo, BEST40 pozostaje downstream/skipped.
- Source of Truth, BACKLOG, issue #7 oraz AI_SYNC handoff zostały zsynchronizowane do iteracji 34.
- NEXT READY TASK pozostaje `P0-7A-CANONICAL-APP` dla PRIMARY; trigger `RUN_FIX / READY / iteration 34`.
- Reguły CRM, finansowe i polityka wersji pozostają bez zmian: `BEST56 BAZA MIESZKAŃ AUDYT`, bez zwiększania numeru.

### 2026-08-27 — AUDYT BEST56 BAZA MIESZKAŃ, iteracja 36

- Exact BEST56 został ponownie potwierdzony: SHA-256 `3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92`.
- Dodano `scripts/materialize_canonical_app.py`, `tests/check_materialize_canonical_app.py` oraz gate CI `Verify canonical materializer contract`; materializer wymaga exact SHA po dekodowaniu/dekompresji i zapisuje atomowo.
- Workflow #274 oraz finalny #279: wszystkie gate'y automatyki, bezpieczeństwa artefaktów, canonical staging i canonical materializer contract = PASS; `Static application checks` nadal FAIL przez brak utrwalonego `app/FlippChill_Kalkulator.html`; BEST40 pozostaje downstream/skipped.
- `artifacts/best56/` pozostaje `PENDING_SAFE_TRANSFER`; w tej iteracji NIE zapisano częściowego ani niezweryfikowanego payloadu.
- P0 #7 ma stan `MATERIALIZER_CONTRACT_CI_PASS_SOURCE_ARTIFACT_PENDING`; `P0-7A-CANONICAL-APP` pozostaje READY dla PRIMARY, a P0 #11 nadal zależy wyłącznie od 7A.
- NEXT READY TASK: `P0-7A-CANONICAL-APP`; TARGET AGENT: `PRIMARY`; TRIGGER: `RUN_FIX / READY / iteration 36`.
- Reguły CRM, finanse, UX, `main` i polityka wersji pozostają bez zmian: `BEST56 BAZA MIESZKAŃ AUDYT`, bez zwiększania numeru.

### 2026-08-27 — AUDYT BEST56 BAZA MIESZKAŃ, iteracja 37

- Wykryto drift root entrypointu: `OPENCODE.md` pomijał `AI_SYNC/PROTOCOL.md`, mimo że `sync_contract.required_read_order` wymaga go jako kroku 2.
- Zsynchronizowano `OPENCODE.md` z pełnym kanonicznym read order.
- Rozszerzono `tests/check_ai_sync_protocol.py`, aby CI sprawdzało kolejność zarówno w `AI_SYNC/PROTOCOL.md`, jak i `OPENCODE.md`.
- Workflow #282 na `f2bd0f7861ce6b830e69a68ef2e0996ce4d28034`: wszystkie gate'y przed aplikacją, w tym nowy OpenCode entrypoint read-order guard = PASS; `Static application checks` nadal FAIL wyłącznie przez P0-7A; BEST40 checks pozostają SKIPPED downstream.
- P1 #12 ma stan `OPENCODE_ENTRYPOINT_READ_ORDER_CI_PASS_PENDING_LOCAL_RUNTIME`; pełny lokalny runtime z rzeczywistym `FLIPPCHILL_BOT_COMMAND` pozostaje otwarty.
- NEXT READY TASK pozostaje `P0-7A-CANONICAL-APP`; TARGET AGENT `PRIMARY`; TRIGGER `RUN_FIX / READY / iteration 37`.
- Reguły biznesowe, finanse, UX, `main` i polityka wersji pozostają bez zmian: `BEST56 BAZA MIESZKAŃ AUDYT`.

### 2026-08-27 — AUDYT BEST56 BAZA MIESZKAŃ, iteracja 38

- Exact baseline BEST56 jest dostępny w runtime: 857840 B, SHA-256 `3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92`.
- Dodano `scripts/package_best56_artifact.py`: exact-SHA-only, deterministyczny gzip `mtime=0`, base64, stałe części `partNNN`, atomowy zapis i pełny round-trip SHA przed zaakceptowaniem payloadu.
- Dodano `tests/check_package_best56_artifact.py` i gate `Verify deterministic BEST56 artifact packager`.
- Workflow #293 na `356180385a41cb35dccd01ebed6e2f0cf5adbb3c`: wszystkie gate'y przed aplikacją = PASS, packager = PASS; `Static application checks` nadal FAIL, bo canonical app nie jest jeszcze utrwalony w repo; BEST40 pozostaje SKIPPED downstream.
- P0 #7 przeszedł do `PACKAGER_CONTRACT_CI_PASS_LOCAL_PAYLOAD_PENDING`; PRIMARY może teraz wykonać `package_best56_artifact.py --auto → materialize_canonical_app.py → check_app.py` bez ręcznego dzielenia payloadu.
- P0 #11 nadal zależy wyłącznie od 7A; reguły biznesowe, finanse, UX, `main` i polityka wersji pozostają bez zmian.
- NEXT READY TASK: `P0-7A-CANONICAL-APP`; TARGET AGENT: `PRIMARY`; TRIGGER: `RUN_FIX / READY / iteration 38`.
