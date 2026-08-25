# BEST56 BAZA MIESZKAŃ AUDYT

## Baseline

- Plik wejściowy: `FlippChill_Kalkulator_BEST56_BAZA_MIESZKAN.html`
- SHA-256: `3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92`
- Rozmiar: 857 840 B
- Linie: 5 799
- Polityka wersji: automat audytowy zachowuje numer `BEST56`; kolejne wyniki otrzymują dopisek `AUDYT` i NIE tworzą `BEST57`.

## Wynik iteracji

### Integralność HTML / DOM

- 763 statyczne ID DOM, 763 unikalne.
- 0 duplikatów statycznych ID.
- 0 brakujących statycznych referencji `for`, `aria-labelledby`, `aria-describedby`, `aria-controls` i lokalnych `href="#..."`.
- 39/39 bloków `<style>` zamkniętych.

### JavaScript

- 9/9 bloków JavaScript przechodzi `node --check`.
- 9/9 tagów `<script>` ma odpowiadający tag zamykający.

### Finanse

- VAT: logika netto `gross / 1.23` — zgodna z 23% VAT.
- CIT: `citBase = max(0, wynik)` i `cit = citBase * .09` — zgodne z CIT 9% dla modelu aplikacji.
- PIT: domyślne stawki poziomów = 12%.
- Próg 50 000 zł: +5%.
- Próg 100 000 zł: +10%.
- Marketing / Slack: obrót do progów jest liczony na bazie miesięcznego przychodu netto niezależnie od źródła; odrębna korekta wynagrodzenia Marketing/Slack jest nakładana osobno.

## Ryzyka / blokery repo

- P0 #7 nadal dotyczy historycznego kanonicznego `app/FlippChill_Kalkulator.html` i obecnego quality gate repo.
- Ten audyt identyfikuje BEST56 jednoznacznym fingerprintem, ale pełny artefakt BEST56 nadal powinien zostać trwale zamrożony w repo przed automatycznymi migracjami/refaktoryzacją.
- Runtime E2E w przeglądarce pozostaje osobnym poziomem walidacji; ten cykl jest audytem statycznym + finansowym.

## Następny pakiet o najwyższym stosunku wartości do ryzyka

1. Dodać test automatyczny, który waliduje fingerprint BEST56 BAZA MIESZKAŃ AUDYT i podstawowe reguły finansowe.
2. Dodać test migracji kluczy `localStorage` oraz płatności 4-częściowych.
3. Dopiero po zielonym quality gate wykonywać bezpieczne poprawki UX, nadal pod nazwą `BEST56 BAZA MIESZKAŃ AUDYT`.

Issue: #10.
