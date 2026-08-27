# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `48`
- Branch roboczy: `develop`
- Najwyższy priorytet: `P0-7A-CANONICAL-APP`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Exact BEST56 jest dostępny w runtime: 857840 B, SHA-256 `3bb0756f6d3e55a0f5eeb35baec1489be4862ddddabb93c9df97acd9f4044e92`.

Aktualny runtime NIE ma bezpośredniego transportu Git do GitHub: DNS dla `github.com` nie rozwiązuje się. Po wcześniejszym SHA mismatch duży payload nadal NIE może być przepychany przez czat/konektor tekstowy. P0-7A pozostaje więc `READY` dla PRIMARY na lokalnym checkoutcie z Git push access.

## Testy / CI

Workflow #372 na aktualnym `develop` `f4761f4c3cfc945753eb7db8ac64b8c70673a43c`:
- wszystkie gate’y przed aplikacją = PASS;
- Source of Truth / CRM sync / finanse / schema 11→12 = PASS;
- AI_SYNC / dispatcher / materializer / packager = PASS;
- `Static application checks` = FAIL wyłącznie przez brak canonical payload/app P0-7A;
- BEST40 checks = SKIPPED downstream.

## P0 / P1

- P0 #7 — 7A `READY`; pozostał bezpieczny direct local git commit payloadu. 7B BLOCKED na exact BEST40.
- P0 #11 — aktywny, BLOCKED wyłącznie przez 7A.
- P1 #12 — pełny lokalny bot runtime pozostaje otwarty.

## Handoff dla 3 botów

### PRIMARY
Na lokalnym repo z Git push access uruchom `python scripts/package_best56_artifact.py --auto`, sprawdź exact SHA i kanoniczny part-set, następnie `git add artifacts/best56` i commit na `develop`. NIE przenoś payloadu przez czat/konektor tekstowy. CI samo materializuje canonical app i uruchomi static checks.

### SECOND_AUDIT
Po DONE 7A wykonaj realny test migracji schema 11→12 na `localStorage`; NIE czekaj na BEST40.

### THIRD_UI
Po DONE 7A wykonaj audyt 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression; NIE zmieniaj finansów.

## Auto-dispatch

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7A-CANONICAL-APP`
- `target_agent = PRIMARY`
- `source_iteration = 48`

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
