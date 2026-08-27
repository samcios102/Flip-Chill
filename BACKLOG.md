# BACKLOG — FlippChill

Jedno źródło prawdy dla dalszego rozwoju. Każdy punkt powinien mieć status i zostać zweryfikowany testem przed oznaczeniem jako ukończony.

## P0 — krytyczne błędy

- [ ] Przywrócić odtwarzalny build `app/FlippChill_Kalkulator.html` — śledzone w #7. Release gate ma dwa niezależne artefakty: 7A canonical BEST56 i 7B historyczny BEST40. Exact BEST56 SHA-256 `3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92` jest runtime-verified. Packager, strict materializer oraz CI auto-materialization są gotowe. Iteracja 41 potwierdziła dodatkową granicę bezpieczeństwa: duży payload przepisany przez konektor tekstowy zmienił bajty i został poprawnie odrzucony przez `Verify canonical materializer contract` w workflow #321; wadliwy payload usunięto w `bc918d5a43174e1f9540010be4f6620757bb69f8`. `P0-7A-CANONICAL-APP` pozostaje READY dla PRIMARY wyłącznie ścieżką lokalną: uruchomić `python scripts/package_best56_artifact.py --auto` w lokalnym repo na exact BEST56, sprawdzić round-trip SHA, a następnie commitować wygenerowane `artifacts/best56/` bez reserializacji przez czat/konektor. `P0-7B-FROZEN-BEST40` pozostaje BLOCKED do exact SHA-256 `c04106fe884d32dc257d852b320f2e145a93f80e5615409dc5fac17f5b171708`.
- [x] Zweryfikować raport 28 zduplikowanych ID DOM — audyt wykazał false positive testu: regex liczył `id=` wewnątrz stringów JavaScript renderujących SVG. Parser realnych tagów HTML potwierdza 0 statycznych duplikatów; test sprawdza teraz również statyczne referencje `for`, `aria-labelledby`, `aria-describedby`, `aria-controls` i lokalne `href="#..."`. Lokalnie: BEST40 = 739 ID / 38 poprawnych referencji, BEST49 = 748 / 38. Issue #8 zamknięte.
- [ ] P0 #11 — migracja schema 11→12 musi zachować ręczne `preliminaryDate`, `maxDealDate`, `paymentParts`, `id`, `startDate` i `finalDate`; status należy wyprowadzać z istniejących dat zamiast kasować dane. Kandydat AUDYT przechodzi test zachowania danych, ale issue pozostaje otwarte do czasu testu na kanonicznym artefakcie repo i realnym `localStorage`. Zależność runtime jest teraz wyłącznie od `P0-7A-CANONICAL-APP`; historyczny BEST40 NIE blokuje tego testu.
- [ ] Każda nowa regresja blokująca logowanie, zapis danych, otwieranie Bazy mieszkań, Rozliczenia lub Dat.
- [ ] Rozbieżności finansowe: VAT 23%, CIT 9%, PIT, search bonus 10% oraz podział prowizji muszą być kontrolowane testami liczbowymi.
- [ ] Utrata danych lokalnych albo niezgodność danych między kolejnymi wersjami BEST.

## P1 — do naprawy / twarde testy

- [ ] P1 #12 — uruchomić lokalny `scripts/agent_dispatch.py --watch` z rzeczywistą komendą OpenCode/bota i potwierdzić pełny cykl `RUN_FIX → guard → claim → wykonanie → test → handoff`. Claim/lock, failure recovery, mutex READY→CLAIMED, bezpieczne odzyskanie starego osieroconego mutexa, dependency guard, świeżość handoffu oraz bezpośrednia integracja runtime guardu z dispatcherem są deterministycznie wymuszane przez CI. Root `OPENCODE.md` jest zsynchronizowany z kanonicznym `sync_contract.required_read_order`, w tym `AI_SYNC/PROTOCOL.md` jako krokiem 2. Pozostał pełny lokalny runtime z rzeczywistym `FLIPPCHILL_BOT_COMMAND`.
- [x] P1 #13 — rozdzielenie zależności #7 na `P0-7A-CANONICAL-APP` i `P0-7B-FROZEN-BEST40` zweryfikowane przez CI; P0 #11 oraz THIRD_UI zależą tylko od canonical app 7A. `tests/check_queue_dependency_partition.py` = PASS w workflow #202; issue #13 zamknięte jako completed.
- [x] P1 #14 — wykonywalny kontrakt finansowy BEST56: `tests/check_financial_scenarios.py` sprawdza VAT 23%, CIT 9% na dodatnim dochodzie i 0 przy stracie, PIT 12%, granice progów 49 999 / 50 000 / 99 999 / 100 000 / 125 000 oraz wkład Slack/Marketing do obrotu progowego. Gate `Verify BEST56 executable financial scenarios` = PASS w workflow #330; issue #14 zamknięte jako completed.
- [x] P1 #17 — wykonywalny kontrakt finansowy sprawdza teraz również `search_bonus = 10%`; gate `Verify BEST56 executable financial scenarios` = PASS w workflow #352. Reguła biznesowa nie została zmieniona, tylko objęta ochroną regresyjną.
- [ ] Zbudować test migracji danych między kolejnymi wersjami HTML i stałymi kluczami `localStorage`.
- [ ] Zbudować automatyczny test: logowanie → Baza mieszkań → filtr → Rozlicz → Daty → status → zapis → ponowne otwarcie.
- [ ] Zweryfikować wszystkie przyciski HOME prowadzące dawniej do osobnych widoków Płatności/Rozliczeń po ich integracji z Bazą.
- [ ] Sprawdzić responsywność Bazy mieszkań na iPhone 15 Pro i małych ekranach Android/Chrome.
- [ ] Zweryfikować, czy wszystkie 4 części płatności klienta i 4 stany wypłaty agentowi zachowują się spójnie po duplikowaniu rekordu.
- [ ] Dodać test i regułę biznesową: mieszkania / transakcje ze źródła `Slack / Marketing` mają zasilać miesięczny obrót liczony do progów 50 000 PLN i 100 000 PLN tak samo jak pozostałe źródła; odrębna stawka wynagrodzenia Slack nie może wyłączać ich z progu.

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
- [x] Skorygować zbyt dużą kompresję desktopową — BEST41: ok. 60 px / rekord, większe statusy i przyciski przy zachowaniu zwartego układu.
- [ ] Audyt gęstości i responsywności na iPhone 15 Pro oraz małym Androidzie.
- [ ] Skróty klawiaturowe dla częstych operacji (wyszukaj, nowa transakcja, rozlicz, daty).
- [ ] Szybki panel „wymaga uwagi”: po terminie, faktura bez wpłaty, klient zapłacił / agent niewypłacony.

## P2 — analityka i finanse

- [x] Jednostkowe testy finansowe na kilku znanych scenariuszach prowizji i podatków — pokryte wykonywalnym kontraktem `tests/check_financial_scenarios.py`; PASS w workflow #352 obejmuje VAT, CIT, PIT, search bonus 10%, progi 50k/100k i Slack/Marketing.
- [ ] Wskaźnik należności: klient → spółka oraz spółka → agent, rozdzielone liczbowo.
- [ ] Prognoza cash-flow według faktycznych dat płatności, a nie tylko statusu transakcji.
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

## Ukończone — punkt startowy repo

- [x] BEST40 jako stabilny punkt startowy.
- [x] Wiersz Bazy zmniejszony z ok. 202 px do ok. 46 px.
- [x] Rozliczenie skompaktowane z ok. 729 px do ok. 435 px.
- [x] Pełna baza 28/28 mieszkań ładuje się w teście BEST40.
- [x] Multi-select płatności i podsumowania w Bazie.
- [x] Rozdzielenie „klient zapłacił” od „agent wypłacony”.
- [x] Oś czasu ze spójnymi symbolami statusu.
- [x] BEST41: zbalansowana gęstość desktopowa, 60 px / rekord przy teście 1536×900, 28/28 rekordów, 0 błędów JS.