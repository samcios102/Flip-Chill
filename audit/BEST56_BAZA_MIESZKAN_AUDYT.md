# BEST56 BAZA MIESZKAŃ AUDYT

## Baseline

- Plik wejściowy: `FlippChill_Kalkulator_BEST56_BAZA_MIESZKAN.html`
- SHA-256: `3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92`
- Rozmiar: 857 840 B
- Linie: 5 799
- Polityka wersji: automat audytowy zachowuje numer `BEST56`; kolejne wyniki otrzymują dopisek `AUDYT` i NIE tworzą `BEST57`.

## Wynik iteracji bazowej

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

## Iteracja audytowa — quality gate manifestu

- Ponownie potwierdzono fingerprint przesłanego BEST56: SHA-256 `3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92`, 857 840 B, 5 799 linii.
- Dodano `tests/check_best56_audit_manifest.py`.
- Test blokuje zmianę nazwy audytu, automatyczne przejście do BEST57, zmianę fingerprintu oraz niespójność liczników DOM/JS i podstawowych asercji finansowych.
- Quality workflow uruchamia gate BEST56 przed historycznym gate aplikacji kanonicznej.
- GitHub Actions: `Verify BEST56 Baza Mieszkań audit manifest` = PASS.
- Cały workflow nadal = FAIL wyłącznie na kolejnym kroku `Static application checks`, zgodnie z otwartym P0 #7 dotyczącym brakującego `app/FlippChill_Kalkulator.html`.

## Ryzyka / blokery repo

- P0 #7 nadal dotyczy historycznego kanonicznego `app/FlippChill_Kalkulator.html` i obecnego quality gate repo.
- Pełny artefakt BEST56 nadal powinien zostać trwale zamrożony w repo przed automatycznymi migracjami/refaktoryzacją.
- `sync/CRM_SOURCE_OF_TRUTH.json` nadal nie znajduje się bezpośrednio na `develop`; Source of Truth pozostaje w otwartym PR #9 i wymaga bezpiecznej integracji z aktualnym `develop`.
- Runtime E2E w przeglądarce pozostaje osobnym poziomem walidacji; dotychczasowe cykle obejmują audyt statyczny + finansowy + CI manifestu.

## Następny pakiet o najwyższym stosunku wartości do ryzyka

1. Zamrozić pełny artefakt BEST56 BAZA MIESZKAŃ w repo i powiązać go z fingerprintem audytu.
2. Dodać test migracji kluczy `localStorage` oraz płatności 4-częściowych.
3. Zintegrować Source of Truth z aktualnym `develop` bez naruszania `main`.

Issue: #10.
