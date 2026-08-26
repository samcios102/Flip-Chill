# AUDYT BEST56 BAZA MIESZKAŃ — LATEST HANDOFF

## Stan

- Baseline: `BEST56 BAZA MIESZKAŃ`
- Automat: `BEST56 BAZA MIESZKAŃ AUDYT`
- Iteracja: `25`
- Branch roboczy: `develop`
- Zweryfikowany workflow: `#160`
- Automatyczne podbijanie numeru BEST: zabronione

## Nowa zmiana

Wykryto lukę runtime: CI weryfikowało świeżość `LATEST_AUDIT`/`TRIGGER`, ale lokalny dispatcher nie wykonywał tej samej walidacji bezpośrednio przed subprocess. Dodano side-effect-free `scripts/handoff_runtime_guard.py` oraz deterministyczny test `tests/check_handoff_runtime_guard.py`.

Guard sprawdza: świeżość timestamps względem Source of Truth/BOT_QUEUE, zgodność `source_iteration`, zgodność `action/task_id/target_agent` z `machine_action`, istnienie taska READY oraz zgodność ownera. Bezpośrednia integracja guardu do `agent_dispatch.py` przed realnym subprocess pozostaje następnym krokiem P1 #12.

## Dowody

Workflow #160 dla `e7254f340ee20f95664cf89f307fe74b41078108`:

- BEST56 audit manifest: PASS
- Source of Truth consistency: PASS
- schema 11→12 contract: PASS
- AI sync dispatch protocol: PASS
- AI sync handoff freshness: PASS
- runtime handoff guard contract: PASS
- local dispatcher claim contract: PASS
- local dispatcher failure recovery: PASS
- local dispatcher mutex contract: PASS
- stale mutex recovery: PASS
- dispatcher dependency guard: PASS
- artifact discovery preflight safety: PASS
- Static application checks: FAIL przez aktywny P0 #7
- BEST40 checksum/stable: pominięte po P0 #7

## P0 / P1

- P0 #7 — aktywny i READY dla PRIMARY.
- P0 #11 — aktywny, BLOCKED przez #7.
- P1 #12 — runtime guard component ma CI PASS; integracja w dispatcherze i pełny lokalny runtime nadal oczekują wykonania.
- THIRD_UI czeka na canonical app.

## Handoff dla 3 botów

### PRIMARY

Claim `P0-7-CANONICAL-APP`. Uruchom lokalny artifact preflight i importuj historyczny BEST40 wyłącznie przy dokładnym SHA-256. Następnie przywróć kanoniczny `app/FlippChill_Kalkulator.html` i uruchom pełny workflow. P1 #12 osobno wymaga wpięcia runtime guardu bezpośrednio przed subprocess.

### SECOND_AUDIT

Po P0 #7 wykonaj realny test migracji schema 11→12 na `localStorage`.

### THIRD_UI

Po canonical app wykonaj audyt 390px / 768px / 1366×768 / 1440×900, accessibility i visual regression. Nie zmieniaj finansów.

## Auto-dispatch

- `action = RUN_FIX`
- `status = READY`
- `task_id = P0-7-CANONICAL-APP`
- `target_agent = PRIMARY`
- Handoff freshness = CI PASS.
- Runtime guard component = CI PASS; dispatcher integration = PENDING.

Numer pozostaje `BEST56 BAZA MIESZKAŃ AUDYT`.
