# BACKLOG — FlippChill

Jedno źródło prawdy dla dalszego rozwoju. Każdy punkt powinien mieć status i zostać zweryfikowany testem przed oznaczeniem jako ukończony. Bieżący standard produktu jest odczytywany z `sync/CRM_SOURCE_OF_TRUTH.json`; historyczne BEST56/BEST40 pozostają w archiwum i historii Git.

## P0 — krytyczne błędy

- [x] P0 #19 — uzgodnić najwyższą zweryfikowaną standardową wersję BEST z repozytoryjnym release targetem. **ROZSTRZYGNIĘTE 2026-08-29:** jawna decyzja użytkownika wyrównała bieżący projekt do `BEST73 BAZA MIESZKAŃ`. Zweryfikowany artefakt: 986881 B, SHA-256 `492a321a07729c480947e12a0afb6678f135717e8a66cd0f12d2cae40f1f89c4`. `release_target` i `audit_base` = BEST73; BEST56 pozostaje historyczny; sam audyt nie tworzy BEST74.
- [ ] **P0 #20 — CURRENT / READY / PRIMARY:** zaimportować exact `BEST73 BAZA MIESZKAŃ` do repo jako odtwarzalny canonical app i uogólnić dotychczasowy BEST56-specific packager/materializer/stager/one-shot do konfiguracji `current standard` z Source of Truth. `app/FlippChill_Kalkulator.html` ma materializować dokładnie SHA-256 `492a321a07729c480947e12a0afb6678f135717e8a66cd0f12d2cae40f1f89c4`. BEST56 i BEST40 zachować jako historię. Nie zmieniać `main`; nie tworzyć BEST74 przez audyt.
- [ ] P0 #11 — migracja schema 11→12 musi zachować ręczne `preliminaryDate`, `maxDealDate`, `paymentParts`, `id`, `startDate`, `finalDate` oraz pozostałe pola biznesowe. Runtime test ma być wykonany na **canonical BEST73** i zależy wyłącznie od `P0-20-BEST73-CANONICAL-APP`; historyczny BEST40 go nie blokuje.
- [ ] P0 #7B — historyczny frozen BEST40: importować wyłącznie exact SHA-256 `c04106fe884d32dc257d852b320f2e145a93f80e5615409dc5fac17f5b171708`; zadanie historyczne i niezależne od current BEST73.
- [x] P0 #7A — dawny canonical BEST56 jako bieżący release gate: **SUPERSEDED** przez P0 #20 po reconciliation do BEST73. Historycznych artefaktów/testów BEST56 nie usuwać.
- [x] Zweryfikować raport 28 zduplikowanych ID DOM — false positive testu; parser realnych tagów HTML potwierdził 0 statycznych duplikatów.
- [ ] Każda nowa regresja blokująca logowanie, zapis danych, otwieranie Bazy mieszkań, Rozliczenia lub Dat.
- [ ] Rozbieżności finansowe: VAT 23%, CIT 9%, PIT 12%, search bonus 10% oraz podział prowizji muszą być kontrolowane testami liczbowymi.
- [ ] Utrata danych lokalnych albo niezgodność danych między kolejnymi wersjami BEST.

## P1 — do naprawy / twarde testy

- [ ] P1 #18 — ciągła praca wielobotowa: po każdym audycie i każdym handoffie przeliczaj kolejkę, uruchamiaj najwyższe bezpieczne READY zadanie, a przy blockerze wybieraj inne niezależne zadanie. PRIMARY / SECOND_AUDIT / THIRD_UI pracują równolegle tylko na rozłącznych scope i lockach; system przechodzi do IDLE dopiero gdy nie ma bezpiecznej pracy READY.
- [ ] P1 #12 — uruchomić lokalny `scripts/agent_dispatch.py --watch` z rzeczywistą komendą OpenCode/bota i potwierdzić pełny cykl `RUN_FIX → guard → claim → wykonanie → test → handoff`. Pozostał pełny lokalny runtime z rzeczywistym `FLIPPCHILL_BOT_COMMAND`.
- [ ] P1 BEST73 — po canonicalizacji #20 wykonać finansowy regression audit bieżącego standardu: VAT 23%, CIT 9%, PIT 12%, search bonus 10%, progi 50k/100k i Slack/Marketing do progów.
- [ ] Zbudować/uruchomić test migracji danych między kolejnymi wersjami HTML i stałymi kluczami `localStorage` na canonical BEST73.
- [ ] Zbudować automatyczny test: logowanie → Baza mieszkań → filtr → Rozlicz → Daty → status → zapis → ponowne otwarcie.
- [ ] Zweryfikować wszystkie przyciski HOME prowadzące dawniej do osobnych widoków Płatności/Rozliczeń po ich integracji z Bazą.
- [ ] Sprawdzić responsywność Bazy mieszkań na iPhone 15 Pro i małych ekranach Android/Chrome po canonicalizacji BEST73.
- [ ] Zweryfikować, czy wszystkie 4 części płatności klienta i 4 stany wypłaty agentowi zachowują się spójnie po duplikowaniu rekordu.
- [x] P1 #13 — historyczne rozdzielenie zależności #7 na canonical app i BEST40 zweryfikowane przez CI; nowa bieżąca zależność jest chroniona przez current-standard `tests/check_queue_dependency_partition.py`.
- [x] P1 #14 — historyczny wykonywalny kontrakt finansowy BEST56 zachowany jako regresyjne evidence; nie jest automatycznie uznawany za runtime PASS BEST73.
- [x] P1 #17 — search bonus 10% jest objęty historycznym wykonywalnym kontraktem; dla BEST73 wymagany jest nowy runtime regression po #20.
- [x] Transakcje ze źródła `Slack / Marketing` zasilają miesięczny obrót liczony do progów 50 000 PLN i 100 000 PLN; reguła pozostaje w Source of Truth.

## P1 — brakujące / niedokończone funkcje

- [ ] Centralny model danych transakcji zamiast duplikowania danych między `portfolio` i `records`.
- [ ] Import aktualnego Excela/CSV z mapowaniem pól i raportem błędów importu.
- [ ] Eksport pełnej Bazy mieszkań wraz z datami, statusem, płatnościami i rozliczeniem.
- [ ] Historia zmian rekordu: kto, kiedy i co zmienił.
- [ ] Mechanizm kopii zapasowej / eksportu JSON i przywracania danych.
- [ ] Prawdziwa synchronizacja wielourządzeniowa zamiast wyłącznie pamięci przeglądarki.
- [ ] Uporządkowanie modułu Poszukujący i połączenie go z klientami, bez pól poszukiwawczych w Bazie mieszkań.

## P2 — UI / UX

- [x] Baza mieszkań jako główne centrum transakcji.
- [x] Osobne zakładki Płatności klientów i Rozliczenie usunięte z głównej nawigacji.
- [x] Multi-select filtrów: Otrzymane / Faktura / Pewna / Prognoza / Rabat bezpośrednio w Bazie.
- [x] Rozliczenie w modalu bez opuszczania Bazy.
- [x] Daty w modalu: Start / Przedwstępna / Końcowa / Maks. termin.
- [x] Spójne symbole statusu ↻ / ◆ / ✓.
- [x] Mocno skompaktowane główne wiersze Bazy (~46 px w BEST40).
- [x] Skorygować zbyt dużą kompresję desktopową — BEST41: ok. 60 px / rekord.
- [ ] Audyt gęstości i responsywności na iPhone 15 Pro oraz małym Androidzie — po canonical BEST73.
- [ ] Skróty klawiaturowe dla częstych operacji.
- [ ] Szybki panel „wymaga uwagi”: po terminie, faktura bez wpłaty, klient zapłacił / agent niewypłacony.

## P2 — analityka i finanse

- [x] Historyczne jednostkowe testy finansowe BEST56 pokrywają VAT, CIT, PIT, search bonus 10%, progi 50k/100k i Slack/Marketing.
- [ ] Potwierdzić te same reguły wykonywalnie na canonical BEST73 po #20.
- [ ] Wskaźnik należności: klient → spółka oraz spółka → agent, rozdzielone liczbowo.
- [ ] Prognoza cash-flow według faktycznych dat płatności.
- [ ] Dashboard miesięczny: 100% przedwstępnych + 80% w toku, łączna kwota i tempo / 5 mies.
- [ ] Kontrola anomalii: nietypowy procent prowizji, suma części ≠ 100%, brak daty przy zamkniętej transakcji.

## P3 — architektura

- [ ] Rozdzielić monolityczny HTML na moduły źródłowe (`src/`) i generować pojedynczy plik dystrybucyjny.
- [ ] Dodać testy Playwright dla krytycznych przepływów.
- [ ] Dodać JSON Schema dla modelu transakcji i migracje wersji danych.
- [ ] Dodać formatter/linter dla HTML/CSS/JS.
- [ ] Wprowadzić semantyczne commity i automatyczne generowanie changelogu.
- [ ] Po ustabilizowaniu źródeł: PWA/offline installable app na telefon i desktop.

## Pomysły warte sprawdzenia

- [ ] Widok „Dzisiaj”: transakcje z terminem, płatnością albo follow-upem na dziś.
- [ ] Automatyczne alerty o płatności i terminach.
- [ ] Jedno pole wyszukiwania globalnego po mieszkaniach, klientach, agentach i dokumentach.
- [ ] Audit score wydania: testy, regresje, wydajność, integralność danych, responsywność.
- [ ] Feature flags dla nowych modułów, aby rozwijać je bez destabilizacji stabilnej wersji.

## Ukończone — historyczne punkty startowe repo

- [x] BEST40 jako historyczny stabilny punkt startowy repo.
- [x] BEST56 jako historycznie audytowana baza z zachowanym SHA i audit manifestem.
- [x] Wiersz Bazy zmniejszony z ok. 202 px do ok. 46 px.
- [x] Rozliczenie skompaktowane z ok. 729 px do ok. 435 px.
- [x] Pełna baza 28/28 mieszkań ładowała się w historycznym teście BEST40.
- [x] Multi-select płatności i podsumowania w Bazie.
- [x] Rozdzielenie „klient zapłacił” od „agent wypłacony”.
- [x] Oś czasu ze spójnymi symbolami statusu.
- [x] BEST41: zbalansowana gęstość desktopowa, 60 px / rekord przy teście 1536×900.
