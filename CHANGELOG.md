# Changelog

Wszystkie istotne zmiany projektu FlippChill są zapisywane tutaj wersja po wersji.

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
