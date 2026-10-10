# BEST47 — przywrócenie szybkiego dodawania transakcji

Zmiana względem BEST46:

- przywrócony stały przycisk `+ Dodaj transakcję` w prawym górnym rogu głównego paska,
- przycisk jest widoczny również w widoku `Baza mieszkań`,
- w Bazie kliknięcie nadal uruchamia istniejący mechanizm dodawania nieruchomości/transakcji (`#fac-portfolio-add`),
- usunięto zmianę etykiety na `Dodaj nieruchomość` w widoku Bazy,
- pozostałe zachowania przycisku są zachowane: `Dodaj czas` w Czasie i `Nowy raport AML` w AML.

QA lokalne:
- 8/8 bloków `<script>` przechodzi `node --check`,
- liczba tagów `<script>` i `<style>` jest zbilansowana,
- logika ukrywania przycisku w widoku portfolio została usunięta.
