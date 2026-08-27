# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `59`
- Branch roboczy: `develop`
- Najwyższy priorytet: `P0-7A-CANONICAL-APP`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Audyt P0 #11 wykazał lukę w samym oracle migracji schema 11→12: kontrakt chronił daty i `paymentParts`, ale nie sprawdzał jawnie reprezentatywnych pozostałych pól biznesowych rekordu.

`tests/check_schema_11_12_contract.py` chroni teraz dodatkowo: `property`, `clientName`, `agent`, `commissionGross`, `source`, `settlementStatus` i `notes` we wszystkich trzech fixture'ach status/data. Kod aplikacji i reguły biznesowe nie zostały zmienione.

## Testy / CI

Workflow #436 na commicie `301d483d2bae20d8ee51789a37077280f43c41ce`:
- rozszerzony schema 11→12 contract = PASS;
- BEST56 manifest / Source of Truth / CRM sync = PASS;
- finanse = PASS;
- AI_SYNC / freshness / runtime guard / dispatcher = PASS;
- preflight / stager / materializer / packager / one-shot PRIMARY / auto-materialization = PASS;
- `Static application checks` = FAIL wyłącznie przez brak repozytoryjnego payloadu canonical BEST56 dla P0-7A;
- BEST40 = SKIPPED downstream.

## P0 / P1

- P0 #7 — `P0-7A-CANONICAL-APP` nadal `READY`; 7B pozostaje BLOCKED na exact BEST40.
- P0 #11 — nadal aktywny i BLOCKED wyłącznie przez 7A; jego fixture contract ma teraz szerszą ochronę integralności pól biznesowych.
- P1 #12 — pełny lokalny bot runtime pozostaje otwarty.

## Handoff dla 3 botów

### PRIMARY
Na lokalnym repo z GitHub push access uruchom dokładnie:

`python scripts/primary_p0_7a_one_shot.py --auto --commit --push`

### SECOND_AUDIT
Po DONE 7A wykonaj realny test migracji schema 11→12 na `localStorage`. Sprawdź daty, `paymentParts` oraz pola biznesowe objęte kontraktem iteracji 59. Nie czekaj na BEST40.

### THIRD_UI
Po DONE 7A wykonaj audyt 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression; nie zmieniaj finansów.

## Auto-dispatch

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7A-CANONICAL-APP`
- `target_agent = PRIMARY`
- `source_iteration = 59`

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
