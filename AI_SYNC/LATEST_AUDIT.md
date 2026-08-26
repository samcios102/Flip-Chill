# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `18`
- Branch roboczy: `develop`
- Testowany commit: `6eb3038c173b9f07c63e7fc77be55b8920d9cbab`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Naprawiono lukę w `scripts/agent_dispatch.py`: realny bot subprocess nie startuje już przed zapisaniem `CLAIMED` i locka. Dispatcher zapisuje `task.status=CLAIMED`, `lock.owner`, `lock.claimed_at` oraz `TRIGGER.status=CLAIMED` bezpośrednio przed uruchomieniem komendy. Bez `FLIPPCHILL_BOT_COMMAND` task pozostaje READY.

Dodatkowo potwierdzono, że dokładny historyczny `FlippChill_Kalkulator_BEST40.html` istnieje w ChatGPT File Library. PRIMARY ma zaakceptować lokalny plik wyłącznie po SHA-256 `c04106fe884d32dc257d852b320f2e145a93f80e5615409dc5fac17f5b171708`; inny plik NIE może zastąpić BEST40.

## Dowody

Workflow #83:

- BEST56 audit manifest: PASS
- Source of Truth consistency: PASS
- schema 11→12 contract: PASS
- AI sync dispatch protocol: PASS
- local dispatcher claim contract: PASS
- Static application checks: FAIL przez aktywny P0 #7
- BEST40 checksum/stable: pominięte po P0 #7

## P0 / P1

- P0 #7 — nadal najwyższy READY task dla PRIMARY; najpierw lokalne wyszukanie artefaktów i exact-SHA guard.
- P0 #11 — BLOCKED przez #7; po canonical app SECOND_AUDIT wykonuje realny runtime `localStorage`.
- P1 #12 — claim/lock jest już zabezpieczony testem i CI; pozostał pełny lokalny runtime z rzeczywistą komendą bota.
- THIRD_UI czeka na canonical app.

## Handoff dla 3 botów

### PRIMARY

Claim `P0-7-CANONICAL-APP`. Najpierw wyszukaj lokalny BEST40. Importuj go tylko przy dokładnym SHA-256 `c04106fe884d32dc257d852b320f2e145a93f80e5615409dc5fac17f5b171708`; jeśli go nie ma, oznacz task BLOCKED zamiast podstawiać inną wersję. Następnie przywróć kanoniczny `app/FlippChill_Kalkulator.html`, uruchom wszystkie gate'y i zaktualizuj AI_SYNC.

### SECOND_AUDIT

Po zielonym P0 #7 wykonaj realny test migracji schema 11→12 na `localStorage`: daty, `paymentParts`, status derivation i ponowne otwarcie.

### THIRD_UI

Po canonical app wykonaj 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression. Nie zmieniaj finansów.

## Auto-dispatch

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7-CANONICAL-APP`
- `target_agent = PRIMARY`

`P1-12-LOCAL-DISPATCH-RUNTIME` pozostaje BLOCKED wyłącznie do czasu lokalnego ustawienia `FLIPPCHILL_BOT_COMMAND` i potwierdzenia pełnego cyklu watcher → claim → bot → test → handoff.
