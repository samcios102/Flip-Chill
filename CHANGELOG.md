# Changelog

Wszystkie istotne zmiany projektu FlippChill są zapisywane tutaj wersja po wersji.

## BEST49 — 2026-08-25

### Statusy, filtry i szybkie płatności
- Żółty status `Przedwstępna` używa symbolu otwartej skrzyni zamiast rombu.
- `Sprzedana` ma własną ikonę zamknięcia/sprzedaży.
- Pierwszy filtr u góry Bazy zmieniono z `Otrzymane` na `Sprzedane`; filtr faktycznie wybiera transakcje o statusie `closed`.
- Kafelki płatności klienta zmieniają status bez otwierania modala: `Prognoza → Pewna → Faktura → Otrzymane → Prognoza`.
- Kafelki agenta są bezpośrednio klikalne: `oczekuje → do wypłaty → wypłacone`; po wypłacie kolejny klik wraca do `do wypłaty`.
- `Moje` stało się niezależnym filtrem nakładanym na filtr główny, więc działa równocześnie z `Wszystkie`, `Aktywne`, `W toku`, `Przedwstępne`, `Sprzedane` i `Termin ≤30 dni`.

### Kontrola
- 8/8 bloków JavaScript przechodzi `node --check`.
- 748/748 statycznych DOM ID jest unikalnych.
- BEST49 i stały `FlippChill_Kalkulator.html` mają identyczny SHA-256.
- Runtime Chromium w środowisku testowym nadal blokuje localhost polityką administratora (`ERR_BLOCKED_BY_ADMINISTRATOR`), więc wykonano kontrolę składniową i strukturalną.

## BEST48 — 2026-08-25

### Baza mieszkań — główny widok operacyjny
- `Baza mieszkań · wszystkie transakcje` jest teraz sekcją 1 i znajduje się przed panelem Portfel/Wynik/Wypłaty.
- Baza jest otwarta domyślnie po wejściu do widoku Portfolio.
- `Portfel · wynik, wypłaty i prognoza` jest sekcją 2 i pozostaje zwinięty domyślnie.
- Usunięto powtarzane w każdym wierszu przyciski `Rozlicz X/4` oraz `Daty`.
- Nad tabelą dodano jeden panel wybranej transakcji z przyciskami `Rozliczenie` i `Daty`.
- Kliknięcie wiersza wybiera mieszkanie; `Edytuj` nadal rozwija szczegóły rekordu.
- Kolumna Akcje zawiera teraz tylko `Edytuj`, `Duplikuj`, `Usuń`.
- Tabela została lekko powiększona: ok. 76 px / rekord, większe pola, statusy, wartości finansowe i płatności.
- Odzyskana szerokość po usunięciu dwóch przycisków z każdego wiersza została przekazana kluczowym kolumnom danych.

### Kontrola
- 4 lokalne bloki JavaScript przechodzą `node --check`.
- 747/747 statycznych DOM ID jest unikalnych.
- Baza ma `open`, a panel Portfel/Wynik/Wypłaty nie ma `open` i jest zamykany także w `setTab("portfolio")`.
- Test Chromium runtime nie został wykonany, ponieważ środowisko sesji blokuje nawigację do lokalnego pliku i localhost polityką administratora.

## Unreleased — QA / integralność testów — 2026-08-25

### Quality gate
- Naprawiono false positive kontroli zduplikowanych DOM ID: wcześniejszy regex liczył również `id=` zapisane wewnątrz stringów JavaScript służących do ponownego renderowania `<title>/<desc>` w SVG.
- `tests/check_app.py` zbiera teraz ID wyłącznie z realnych statycznych tagów HTML przez `html.parser.HTMLParser` i nadal blokuje rzeczywiste duplikaty DOM.
- Weryfikacja lokalnych artefaktów: BEST40 = 739/739 unikalnych statycznych ID; BEST45 = 743/743.
- Do backlogu dodano wymaganie finansowe: transakcje ze źródła `Slack / Marketing` muszą zasilać obrót do progów 50 000 / 100 000 PLN niezależnie od odrębnej stawki wynagrodzenia Slack.

### Status wydania
- Repo nadal wymaga odtwarzalnego `app/FlippChill_Kalkulator.html` i zamrożonego artefaktu BEST40 w CI (#7).

## BEST45 — 2026-08-25

### Baza mieszkań — prawa strona i gęstość
- Usunięto zbędną legendę `↻ w toku / ◆ przedwstępna / ✓ sprzedana` nad tabelą; status pozostaje wyłącznie przy każdym mieszkaniu.
- Wysokość głównego wiersza zwiększona do ok. 72 px, aby tabela była mniej agresywnie skompaktowana.
- Przebalansowano szerokości kolumn: więcej miejsca dla `Akcje`, mniej dla `Prognoza`, `Cena` i `Agent`.
- `Akcje` mają własne 19–21% szerokości zależnie od ekranu i nie nachodzą już na `Prognozę`.
- Powiększono nieznacznie pola, statusy, kafelki płatności i przyciski.

### Test 1366×768
- Tabela: 1322 px przy kontenerze 1324 px — brak poziomego overflow.
- Główny wiersz: 72 px.
- Kolumna `Akcje`: 251 px; zawartość przycisków: 240 px.
- Kolumna `Prognoza`: 112 px.
- Pełna baza: 28/28 rekordów.
- 0 błędów JavaScript podczas renderu testowego.

## BEST44 — 2026-08-25

### Baza mieszkań — uproszczenie Prognozy
- Usunięto drugi, powtórzony status transakcji z kolumny `Prognoza`.
- Status `↻ / ◆ / ✓` pozostaje tylko po lewej stronie przy nieruchomości.
- `Prognoza` pokazuje teraz wyłącznie kwotę oczekiwanego przychodu.
- Prawa część tabeli jest dzięki temu czytelniejsza i mniej przeładowana.

### Test
- Wszystkie 4 bloki JavaScript przechodzą `node --check`.
- Renderer Prognozy nie zawiera już etykiet `W toku / Przedwstępna / Zrealizowane` ani ich ikon.

## BEST43 — 2026-08-25

### Baza mieszkań — finanse i prognoza
- Usunięto techniczne skróty `B` i `N` z głównego wiersza.
- Finanse pokazują teraz cztery czytelne pozycje: `Brutto`, `Netto`, `Po CIT`, `Agent`.
- Prognoza ma opis nagłówka `oczekiwany przychód` oraz czytelny status modelu: `↻ 80% W toku`, `◆ 100% Przedwstępna` albo `✓ 100% Zrealizowane`.
- Uporządkowano opisy nagłówków: Cena = wartość, Finanse = przychód/wynik/agent, Płatności = 4 etapy klient/agent.

### Test
- Wszystkie 8 bloków JavaScript przechodzą `node --check`.
- Liczba istniejących powtórzonych identyfikatorów w źródle nie wzrosła względem BEST42.
- Struktura `<script>` i `<style>` pozostaje zbilansowana.

## BEST42 — 2026-08-25

### Baza mieszkań — czytelność i wykorzystanie szerokości
- Wysokość głównego wiersza zwiększona z ok. 60 px do 66 px.
- Zwężono kolumny `Cena` i `Agent` oraz delikatnie `Nieruchomość`.
- Odzyskaną szerokość przekazano głównie `Płatnościom`, finansom i akcjom.
- Nagłówki tabeli mają teraz nazwę główną i krótki opis znaczenia kolumny.
- Powiększono statusy, pola, kafelki płatności, prognozę oraz przyciski bez powrotu do wysokich wierszy sprzed BEST40.

### Test
- Widok testowy 1366×768: tabela 1322 px, bez poziomego overflow.
- Pełna Baza mieszkań: 28/28 rekordów.
- Filtr `Otrzymane`: 15 rekordów, po wyczyszczeniu ponownie 28/28.
- Modal Rozliczenia i modal Dat otwierają się poprawnie.
- 0 błędów JavaScript; 0 zduplikowanych ID DOM.

## BEST41 — 2026-08-25

### UI / czytelność
- Skorygowano zbyt agresywne zagęszczenie BEST40.
- Wysokość głównego wiersza Bazy ustawiona na ok. 60 px zamiast 46 px.
- Powiększono pola, symbole statusu, kafelki płatności, prognozę i przyciski bez powrotu do rozlanego układu.
- Oś czasu otrzymała ten sam poziom czytelności: większe statusy, nazwy i przyciski.

### Test
- Pełna Baza mieszkań: 28/28 rekordów.
- Zmierzona wysokość głównego wiersza: 60 px przy widoku 1536×900.
- Symbole statusu: 22×22 px; przyciski akcji: 27 px wysokości; kafelki płatności: 24 px.
- 0 błędów JavaScript w teście przeglądarkowym.

## BEST40 — 2026-08-25

### Stabilizacja
- Baza mieszkań została ustawiona jako główne centrum transakcji.
- Osobne pozycje nawigacji „Płatności klientów” i „Rozliczenie” zostały usunięte; funkcje są dostępne z poziomu mieszkania.
- Multi-select statusów płatności został przeniesiony na górę Bazy mieszkań.
- Rozliczenie otwiera się w modalu bez zmiany strony.
- Dodano rozdzielenie: „klient zapłacił” vs „agent wypłacony”.
- Dodano modal Daty: Start / Przedwstępna / Końcowa / Maks. termin.
- Ujednolicono statusy ↻ W toku / ◆ Przedwstępna / ✓ Sprzedana w Bazie i na osi czasu.

### Wydajność / UI
- Naprawiono CSS bezpośrednio na komórkach tabeli, który powodował nadmierną wysokość wierszy.
- Główny wiersz Bazy zmniejszony z ok. 202 px do ok. 46 px (~77% mniej).
- Modal Rozliczenia zmniejszony z ok. 729 px do ok. 435 px.
- Usunięto zbędne pola z Bazy: Prezentacja, Kryteria poszukiwania, Klient nadal poszukujący.

### Testy wykonane przed bootstrapem repo
- Załadowanie pełnej Bazy mieszkań: 28/28.
- Logowanie → Baza → filtry → Rozlicz → Daty → status → oś czasu.
- 0 wykrytych błędów składni JavaScript w końcowej wersji.
- 0 zduplikowanych identyfikatorów DOM w końcowej kontroli.

## BEST39 i wcześniejsze

Historia wcześniejszych iteracji powstała przed uruchomieniem repozytorium jako głównego systemu wersjonowania. BEST40 jest oficjalnym punktem startowym dalszej historii Git.
