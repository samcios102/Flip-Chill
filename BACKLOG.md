# BACKLOG — FlippChill

Jedno źródło prawdy dla dalszego rozwoju. Każdy punkt powinien mieć status i zostać zweryfikowany testem przed oznaczeniem jako ukończony.

## P0 — krytyczne błędy

- [ ] Przywrócić odtwarzalny build `app/FlippChill_Kalkulator.html` — aktualne CI na `develop` kończy się błędem `missing app file`; śledzone w #7. Dokładny historyczny BEST40 został odnaleziony w ChatGPT File Library, ale repo nadal go nie zawiera. Dodano `scripts/artifact_preflight.py`, który lokalnie wyszukuje kandydatów i uznaje BEST40 za bezpieczny do importu wyłącznie przy SHA-256 `c04106fe884d32dc257d852b320f2e145a93f80e5615409dc5fac17f5b171708`; gate preflight przechodzi CI. PRIMARY ma uruchomić preflight na lokalnych katalogach i importować tylko exact match.
- [x] Zweryfikować raport 28 zduplikowanych ID DOM — audyt wykazał false positive testu: regex liczył `id=` wewnątrz stringów JavaScript renderujących SVG. Parser realnych tagów HTML potwierdza 0 statycznych duplikatów; test sprawdza teraz również statyczne referencje `for`, `aria-labelledby`, `aria-describedby`, `aria-controls` i lokalne `href="#..."`. Lokalnie: BEST40 = 739 ID / 38 poprawnych referencji, BEST49 = 748 / 38. Issue #8 zamknięte.
- [ ] P0 #11 — migracja schema 11→12 musi zachować ręczne `preliminaryDate`, `maxDealDate`, `paymentParts`, `id`, `startDate` i `finalDate`; status należy wyprowadzać z istniejących dat zamiast kasować dane. Kandydat AUDYT przechodzi test zachowania danych, ale issue pozostaje otwarte do czasu testu na kanonicznym artefakcie repo i realnym `localStorage`.
- [ ] Każda nowa regresja blokująca logowanie, zapis danych, otwieranie Bazy mieszkań, Rozliczenia lub Dat.
- [ ] Rozbieżności finansowe: VAT 23%, CIT 9%, PIT oraz podział prowizji muszą być kontrolowane testami liczbowymi.
- [ ] Utrata danych lokalnych albo niezgodność danych między kolejnymi wersjami BEST.

## P1 — do naprawy / twarde testy

- [ ] P1 #12 — uruchomić lokalny `scripts/agent_dispatch.py --watch` z rzeczywistą komendą OpenCode/bota i potwierdzić pełny cykl `RUN_FIX → claim → wykonanie → test → handoff`. Claim/lock, failure recovery, mutex READY→CLAIMED, bezpieczne odzyskanie starego osieroconego mutexa i dependency guard są deterministycznie wymuszane przez CI. Iteracja 24 dodaje osobny gate świeżości handoffu: LATEST_AUDIT/TRIGGER nie mogą być starsze niż Source of Truth/BOT_QUEUE. Pozostał pełny runtime z rzeczywistym `FLIPPCHILL_BOT_COMMAND`.
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

- [ ] Jednostkowe testy finansowe na kilku znanych scenariuszach prowizji i podatków.
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
