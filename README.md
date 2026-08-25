# FlippChill — Kalkulator / CRM

Główne repozytorium rozwoju narzędzi operacyjnych Flipp&Chill.

## Cel

Rozwijać aplikację szybko, ale stabilnie: każda zmiana ma przejść przez audyt, testy i wersjonowanie. Priorytetem jest poprawność danych i brak regresji przed tempem dodawania funkcji.

## Aktualna baza

- Stabilna wersja startowa projektu: **BEST40**.
- `main` — ostatnia wersja uznana za stabilną.
- `develop` — bieżący rozwój następnej wersji.
- `versions/` — zamrożone punkty przywracania BEST.
- `app/FlippChill_Kalkulator.html` — aktualna stabilna aplikacja.
- `BACKLOG.md` — jedna lista błędów, funkcji, optymalizacji i pomysłów.
- `CHANGELOG.md` — historia zmian wersja po wersji.
- `docs/` — architektura, zasady rozwoju i materiały historyczne.

## Pętla rozwoju

1. Pobierz najnowszy kod.
2. Uruchom testy automatyczne i test interfejsu.
3. Sprawdź backlog i wcześniejsze wymagania.
4. Wybierz mały pakiet zmian o najwyższej wartości.
5. Wprowadź zmianę na `develop`.
6. Ponownie wykonaj testy i audyt regresji.
7. Jeśli wynik jest stabilny — nadaj kolejny numer BEST, zaktualizuj changelog i scal do `main`.
8. Dopiero potem przejdź do kolejnego pakietu.

## Zasada jakości

**Najpierw poprawność → potem szybkość → potem liczba funkcji.**

Nie dokładamy kilku ryzykownych zmian naraz. Duże funkcje dzielimy na małe, testowalne kroki. Każdy wykryty błąd trafia do backlogu, a krytyczne regresje blokują wydanie.

## Najważniejsze obszary

- Baza mieszkań jako centrum transakcji.
- Płatności klientów i wypłaty agentów.
- Rozliczenia, prowizje, VAT/CIT/PIT.
- Daty i statusy transakcji.
- Prognozy portfela i osi czasu.
- Role użytkowników, logowanie i trwałość danych.
- CRM / follow-up / poszukujący.
- Integracje i automatyzacje.

## Uruchomienie

Aplikacja jest obecnie samodzielnym plikiem HTML. Otwórz `app/FlippChill_Kalkulator.html` w aktualnym Chrome/Edge.

## Historia

Pierwotna zawartość repo sprzed uruchomienia projektu aplikacji została zachowana w `docs/legacy/`.
