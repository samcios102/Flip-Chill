# BEST44 — remove duplicate status from Prognoza

Zmiana UI w Bazie mieszkań:

- status transakcji pozostaje tylko po lewej stronie przy nieruchomości: `↻ / ◆ / ✓`,
- z kolumny `Prognoza` usunięto drugi zestaw ikon i tekstów `W toku / Przedwstępna / Zrealizowane`,
- kolumna `Prognoza` pokazuje wyłącznie kwotę oczekiwanego przychodu,
- celem jest usunięcie dublowania informacji i uproszczenie prawej strony tabeli.

Kontrola lokalna BEST44:
- 4 bloki JavaScript przechodzą `node --check`,
- brak wystąpień usuniętych etykiet statusu w rendererze Prognozy.
