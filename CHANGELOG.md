# Changelog

Wszystkie istotne zmiany projektu FlippChill są zapisywane tutaj wersja po wersji.

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
- Powiększono pola, symbole statusu, kafelki płatności, prognozę i przyciski akcji bez powrotu do rozlanego układu.
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
