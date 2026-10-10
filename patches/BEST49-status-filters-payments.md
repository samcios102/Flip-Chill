# BEST49 — statusy, filtry i szybkie płatności

## Zmiany
- Żółty status `Przedwstępna` używa własnego symbolu otwartej skrzyni zamiast rombu.
- Status `Sprzedana` ma własną ikonę sprzedaży/zamknięcia.
- Pierwszy filtr u góry Bazy zmieniono z `Otrzymane` na `Sprzedane`; filtr działa po statusie transakcji `closed`, a nie tylko po nazwie.
- Kafelki płatności klienta zmieniają status bez otwierania modala: `Prognoza → Pewna → Faktura → Otrzymane → Prognoza`.
- Kafelki agenta pozostają bezpośrednio klikalne i przechodzą logicznie przez `oczekuje → do wypłaty → wypłacone`; po wypłacie kolejny klik wraca do `do wypłaty`.
- Pełne Rozliczenie nadal jest dostępne z górnego panelu wybranej transakcji.
- `Moje` jest teraz niezależnym filtrem nakładanym na filtr główny. Można łączyć np. `Moje + Aktywne`, `Moje + W toku`, `Moje + Przedwstępne`, `Moje + Sprzedane`, `Moje + Termin ≤30 dni`.

## Kontrola
- 8/8 bloków JavaScript przechodzi `node --check`.
- 748/748 statycznych DOM ID jest unikalnych.
- Stary atrybut `data-payment-jump` został usunięty z szybkich kafelków Bazy; zastępuje go `data-payment-cycle`.
- BEST49 i stały `FlippChill_Kalkulator.html` mają identyczny SHA-256: `41e3cbe392703cd04f9dfc26f551219089714a1074a926efaa0fcb58bdf739c2`.
- Test runtime Chromium pozostaje zablokowany przez politykę administratora środowiska (`ERR_BLOCKED_BY_ADMINISTRATOR` dla localhost); wykonano kontrolę składniową i strukturalną.
