# FlippChill AI_SYNC — 3-agent handoff and self-dispatch protocol

`AI_SYNC/` jest wspólną skrzynką PRIMARY, SECOND_AUDIT, THIRD_UI, ChatGPT, OpenCode i lokalnego watchera.

## KROK 0 — VERSION + MISSION DISCOVERY

Przed każdą misją i przed każdym audytem ustal najwyższy **zweryfikowany standard BEST** oraz najnowszą aktywną misję. Sprawdzaj dostępne źródła w tej kolejności:

1. live GitHub: branche, najnowsze commity, Source of Truth, release/audit manifests, repo tree i CI;
2. bieżące załączniki / ChatGPT Library, jeśli są dostępne;
3. lokalne artifact roots wykonawcy;
4. otwarte P0/P1 Issues oraz najnowszy handoff.

Dla kandydata wersji zapisuj co najmniej: nazwę pliku, numer BEST, STANDARD/AUDYT/TEST/BACKUP/CRM_AUTO, źródło, rozmiar i SHA-256, jeśli bytes są dostępne.

Publikuj osobno:
- `HIGHEST_VERIFIED_STANDARD_BEST`;
- `REPO_RELEASE_TARGET`;
- `STABLE_MAIN_BASE`;
- `AUDIT_BASE`.

Jeżeli się różnią, ustaw `VERSION_RECONCILIATION_REQUIRED` i najpierw napraw Source of Truth. Nie implementuj na starszej bazie po znalezieniu i zweryfikowaniu nowszego standardu.

### Aktualne rozstrzygnięcie wersji

Na podstawie jawnej decyzji użytkownika z 2026-08-29 oraz zweryfikowanego artefaktu:

- `HIGHEST_VERIFIED_STANDARD_BEST = BEST73 BAZA MIESZKAŃ`;
- `REPO_RELEASE_TARGET = BEST73 BAZA MIESZKAŃ`;
- `AUDIT_BASE = BEST73 BAZA MIESZKAŃ`;
- źródło: `FlippChill_Kalkulator_BEST73_BAZA_MIESZKAN(1).html` w ChatGPT Library;
- size = `986881 B`;
- SHA-256 = `492a321a07729c480947e12a0afb6678f135717e8a66cd0f12d2cae40f1f89c4`;
- BEST56 pozostaje historycznym audytowanym baseline;
- audyt BEST73 **nie tworzy BEST74**.

Issue #19 śledzi reconciliation; issue #20 śledzi canonicalizację BEST73 i uogólnienie starego BEST56-specific pipeline.

## Read order before normal work

Po KROKU 0 zawsze czytaj dokładnie:

1. `sync/CRM_SOURCE_OF_TRUTH.json`
2. `AI_SYNC/PROTOCOL.md`
3. `AI_SYNC/LATEST_AUDIT.json`
4. `AI_SYNC/BOT_QUEUE.json`
5. `AI_SYNC/TRIGGER.json`
6. `sync/CRM_SYNC.md`
7. `BACKLOG.md`
8. otwarte P0/P1 Issues, najnowsze commity i aktualny CI.

Repo jest głównym źródłem prawdy po wykonaniu discovery i reconciliation.

## Role

- `PRIMARY` — implementacja, integracja, canonical app/build/repo, current-standard pipeline.
- `SECOND_AUDIT` — dane, finanse, migracje, regresje i niezależna weryfikacja.
- `THIRD_UI` — UI/UX, responsive, accessibility i visual regression.

THIRD_UI nie zmienia finansów. SECOND_AUDIT nie przejmuje implementacji PRIMARY bez jawnego reassignmentu.

## Polityka wersji

- Audyt używa rzeczywistego `AUDIT_BASE` i dopisku `AUDYT`.
- Audyt sam w sobie nigdy nie zwiększa numeru standardowego BEST.
- Nowy standard BEST może powstać tylko z realnej zaakceptowanej zmiany produktu albo po zweryfikowaniu istniejącego nowszego artefaktu i aktualizacji Source of Truth.
- Historycznych baseline'ów i audit manifests nie kasuj.

## Format raportu dla użytkownika — stały kontrakt

Pełny cykl:
1. nagłówek `<AUDIT_BASE> AUDYT — ITERACJA <N>`;
2. status `🟢 GOTOWE`, `🟡 W TOKU` albo `🔴 BLOKER`;
3. `WERSJA / MISJA`;
4. `CO SIĘ ZMIENIŁO` — maksymalnie 3 krótkie punkty;
5. `CO TO ZNACZY` — praktyczny wpływ;
6. `TESTY / CI` — tylko dowody, bez fikcyjnego PASS;
7. `NASTĘPNY RUCH` — task, agent, trigger;
8. commit/PR/branch w jednej zwartej linii.

DELTA:
- pokazuj wyłącznie zmienione sekcje;
- jeśli zmienił się tylko CI, pokaż tylko CI i ewentualną zmianę następnego ruchu;
- jeśli nic istotnego się nie zmieniło: dokładnie `BRAK NOWYCH ZMIAN`;
- `SOURCE-OF-TRUTH UPDATE REQUIRED` tylko gdy realnie zmienia się reguła lub blocker.

## Queue lifecycle

`OPEN -> READY -> CLAIMED -> WORKING -> TESTING -> DONE`

Stany terminalne/alternatywne: `BLOCKED`, `REJECTED`, `SUPERSEDED`.

Każde zadanie ma dokładnie jednego `owner`. Aktywne taski używają `lock.owner` + `lock.claimed_at`.

## Continuous work / automatic bot reactivation

Po każdym audycie i po każdym wyniku bota:

1. powtórz discovery, jeśli mogła pojawić się nowa wersja/misja;
2. odczytaj queue, P0/P1 i CI;
3. wykryj błędy, regresje, niedokończoną pracę i taski, które właśnie się odblokowały;
4. utwórz brakujące canonical taski bez dublowania ID;
5. przypisz według roli;
6. nie zostawiaj agenta bezczynnego, jeśli istnieje bezpieczny niezależny READY task dla jego roli;
7. gdy najwyższy task jest BLOCKED, szukaj następnego niezależnego READY;
8. równoległa praca jest dozwolona wyłącznie przy rozłącznych scope/lockach;
9. po `DONE`, `TESTING` lub `BLOCKED` natychmiast przelicz queue i wystaw kolejny trigger;
10. działaj w pętli `DISCOVERY → AUDYT → QUEUE → DISPATCH → BOT → TEST → HANDOFF → NEXT TASK`;
11. `IDLE` tylko gdy naprawdę nie istnieje bezpieczna praca READY.

Priorytet: version/source integrity + dane/finanse > regresje > UX > nowe funkcje.

## Trigger lifecycle

`AI_SYNC/TRIGGER.json` jest maszynowym zleceniem dla `python scripts/agent_dispatch.py --watch`.

- `action=RUN_FIX`, `status=READY` → watcher może przygotować pracę dla `target_agent`;
- `action=IDLE` → brak bezpiecznego READY taska;
- `source_iteration` musi odpowiadać `LATEST_AUDIT.iteration`;
- trigger task/agent musi odpowiadać `LATEST_AUDIT.machine_action`;
- runtime guard i mutex muszą zostać sprawdzone przed claimem;
- dependency guard blokuje task z nierozwiązanymi `blocked_by`;
- bez realnego `FLIPPCHILL_BOT_COMMAND` dispatcher nie udaje wykonania i pozostawia task READY;
- błąd subprocess zwalnia claim zgodnie z failure recovery i scheduler szuka następnego bezpiecznego taska.

## Safety gates

- `main` pozostaje stabilny i nie jest automatycznie modyfikowany.
- Normalna praca: `develop`, `feature/*`, `fix/*`, `audit/*`.
- Czerwony CI blokuje promocję stabilną, ale nie blokuje niezależnych bezpiecznych napraw/audytów.
- Task nie może dostać `DONE` bez deterministycznego dowodu.
- Canonical app musi mieć exact SHA bieżącego release targetu z Source of Truth.

## Handoff contract

Po każdym cyklu aktualizuj:
- `AI_SYNC/LATEST_AUDIT.json`;
- `AI_SYNC/LATEST_AUDIT.md`;
- `AI_SYNC/BOT_QUEUE.json`;
- `AI_SYNC/TRIGGER.json`;
- `sync/CRM_SOURCE_OF_TRUTH.json`, `sync/CRM_SYNC.md`, `BACKLOG.md` i issue, jeśli zmienił się wspólny stan.

Maszynowy stan ma być zgodny ze świeżością, kolejką, triggerem i current-standard Source of Truth przed uruchomieniem bota.
