# BEST48 — Baza mieszkań jako pierwszy widok operacyjny

## Zmiany
- `Baza mieszkań · wszystkie transakcje` jest sekcją 1 i znajduje się przed panelem Portfel/Wynik/Wypłaty.
- Baza jest otwarta domyślnie przy wejściu do widoku Portfolio.
- `Portfel · wynik, wypłaty i prognoza` jest sekcją 2 i pozostaje zwinięty domyślnie.
- Przyciski `Rozlicz X/4` i `Daty` zostały usunięte z każdego wiersza.
- Nad tabelą dodano jeden panel wybranej transakcji z przyciskami `Rozliczenie` i `Daty`.
- Kliknięcie wiersza wybiera mieszkanie; `Edytuj` nadal odpowiada za rozwinięcie szczegółów.
- Wybrany wiersz otrzymuje subtelne podświetlenie.
- Kolumna Akcje zawiera tylko `Edytuj`, `Duplikuj`, `Usuń`.
- Odzyskana szerokość została przekazana nieruchomości, finansom i płatnościom.
- Wiersz tabeli zwiększono do ok. 76 px; pola, statusy i wartości zostały delikatnie powiększone.

## Kontrola statyczna
- 4 lokalne bloki JavaScript przechodzą `node --check`.
- 747/747 statycznych DOM ID jest unikalnych.
- `fac-portfolio-ledger-panel` ma `open` w HTML.
- `fac-portfolio-overview` nie ma `open` i dodatkowo jest zamykany przez `setTab("portfolio")`.
- Renderer wiersza nie zawiera przycisku `Rozlicz X/4` ani przycisku `Daty` w kolumnie Akcje.
- Środowisko Chromium w tej sesji blokuje nawigację do lokalnego pliku/localhost polityką administratora, dlatego test runtime nie został zaliczony jako wykonany; zmiana została zweryfikowana składniowo i strukturalnie.
