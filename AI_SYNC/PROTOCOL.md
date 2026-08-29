# FlippChill AI_SYNC — 3-agent handoff and self-dispatch protocol

`AI_SYNC/` is the shared mailbox for PRIMARY, SECOND_AUDIT, THIRD_UI, ChatGPT automations, OpenCode and the local watcher/supervisor.

## Read order before any work

The canonical order is defined by `sync/CRM_SOURCE_OF_TRUTH.json -> sync_contract.required_read_order` and MUST be followed exactly:

1. `sync/CRM_SOURCE_OF_TRUTH.json`
2. `AI_SYNC/PROTOCOL.md`
3. `AI_SYNC/LATEST_AUDIT.json`
4. `AI_SYNC/BOT_QUEUE.json`
5. `AI_SYNC/TRIGGER.json`
6. `sync/CRM_SYNC.md`
7. `BACKLOG.md`
8. relevant open GitHub P0/P1 issues and current CI state

Repository state is authoritative over conversational memory.

## Roles

- `PRIMARY` — implementation/integration on `develop` or a feature branch; never silently promotes `main`.
- `SECOND_AUDIT` — independent audit, regression/data/finance verification; does not take ownership of PRIMARY's implementation task unless reassigned.
- `THIRD_UI` — UI/UX/responsive/accessibility/visual verification; does not rewrite core financial logic unless explicitly assigned.

## Audit output naming

Automation baseline remains `BEST56 BAZA MIESZKAŃ`.
Automatic audit artifacts use `BEST56 BAZA MIESZKAŃ AUDYT` and NEVER increment the BEST number.

## Human report format — persistent conversation contract

User-facing reports in this ChatGPT conversation and `AI_SYNC/LATEST_AUDIT.md` MUST be optimized for fast scanning and understanding. This format is persistent until the user explicitly changes it; any later explicit user instruction updates this contract.

Default full-cycle report:

1. Header: `BEST56 BAZA MIESZKAŃ AUDYT — ITERACJA <N>`.
2. One-line status banner using one of: `🟢 GOTOWE`, `🟡 W TOKU`, `🔴 BLOKER`.
3. `CO SIĘ ZMIENIŁO` — only new facts from this cycle, plain Polish, maximum 3 concise bullets.
4. `CO TO ZNACZY` — one short explanation of practical impact on CRM/Baza mieszkań.
5. `TESTY / CI` — compact PASS/FAIL/WAITING counts or the smallest useful checklist; clearly identify the failing gate and reason. Never claim PASS without evidence.
6. `NASTĘPNY RUCH` — visually prominent task, target agent and trigger status.
7. Footer metadata — commit, PR and branch on one compact line.

Default delta report:

- Show ONLY changed sections since the immediately previous report.
- If only CI changed, show only `TESTY / CI` plus any consequence for `NASTĘPNY RUCH`.
- If nothing material changed, output exactly `BRAK NOWYCH ZMIAN`.
- Use `SOURCE-OF-TRUTH UPDATE REQUIRED` only when a shared rule or blocker state truly changed.

Readability rules:

- Polish user-facing language; explain machine identifiers in human terms on first relevant occurrence.
- Prefer short sections, whitespace, bold key state, and compact symbols/status markers over dense prose.
- Do not repeat unchanged blocker descriptions, business decisions, queue state or historical test detail.
- Surface the practical consequence before implementation detail.
- Preserve exact task IDs, commit SHAs, workflow IDs, branch names and trigger values.
- Keep machine-readable truth in `LATEST_AUDIT.json`, `BOT_QUEUE.json`, `TRIGGER.json`; the Markdown/user report is the human layer.
- The report format itself is part of repository protocol so future agents/bots can reproduce it consistently.

## Queue lifecycle

Task states:

`OPEN -> READY -> CLAIMED -> WORKING -> TESTING -> DONE`

Alternative terminal states:

`BLOCKED`, `REJECTED`, `SUPERSEDED`.

Each task has exactly one `owner` while CLAIMED/WORKING/TESTING. `lock.owner` + `lock.claimed_at` prevent two bots from modifying the same scope simultaneously.

## Continuous work / automatic bot reactivation — persistent user contract

The automation must keep the project moving whenever safe work exists. This is a persistent rule until the user explicitly changes it.

After EVERY audit iteration and after EVERY bot completion/failure/handoff:

1. Re-read `AI_SYNC/BOT_QUEUE.json`, open P0/P1 issues and current CI.
2. Detect:
   - newly found errors/regressions,
   - unfinished work,
   - READY tasks,
   - tasks that became unblocked because dependencies reached DONE/SUPERSEDED,
   - independent work that can continue even if another task is BLOCKED.
3. Convert each actionable finding into a queue task if it does not already exist; preserve one canonical task ID per problem.
4. Assign by domain:
   - `PRIMARY` → implementation, integration, canonical app/build/repo changes;
   - `SECOND_AUDIT` → data integrity, finance, migration, regression verification;
   - `THIRD_UI` → UI/UX, responsive, accessibility, visual regression.
5. Never leave an agent idle if that agent has a safe, dependency-resolved READY task within its role.
6. If the current highest-priority task is BLOCKED, scan for the next independent safe READY task instead of stopping the whole system.
7. Different agents may work in parallel only when scopes are independent and locks do not overlap. Never allow two agents to modify the same locked scope/task.
8. After a task reaches DONE, TESTING or BLOCKED, immediately recompute the queue and publish the next valid dispatch action.
9. Continue the loop `AUDYT → QUEUE → DISPATCH → BOT → TEST → HANDOFF → NEXT TASK` for as long as safe actionable work exists.
10. Only enter `IDLE` when there is genuinely no dependency-resolved safe READY task. A later audit/queue change must wake the system again.

Continuous mode safety:

- priority order remains: data/financial integrity > regressions > UX/performance > new features;
- `main` is never modified automatically;
- normal autonomous work stays on `develop` / feature / fix / audit branches;
- red CI blocks stable promotion, but does NOT block unrelated safe audit/fix work on independent scopes;
- a bot may not self-reassign another agent's active locked task;
- failed subprocesses release claims according to failure-recovery rules, then the scheduler must look for another independent READY task;
- automatic iterations and automatic bot work NEVER increment BEST; output remains `BEST56 BAZA MIESZKAŃ AUDYT`.

This policy is tracked by GitHub issue #18 and is part of the stable conversation/repository instruction set.

## Trigger lifecycle

`AI_SYNC/TRIGGER.json` is the machine dispatch signal.

- `action=IDLE`: nothing to launch.
- `action=RUN_FIX`, `status=READY`: watcher/supervisor may prepare the work order for the bot named by `target_agent`.
- `LATEST_AUDIT.generated_at` and `TRIGGER.updated_at` must be at least as new as the newest shared-state timestamp from Source of Truth / BOT_QUEUE. A stale report or trigger must not dispatch work.
- `TRIGGER.source_iteration` must equal `LATEST_AUDIT.iteration`, and trigger `action/task_id/target_agent` must equal `LATEST_AUDIT.machine_action`.
- `scripts/handoff_runtime_guard.py` is the side-effect-free runtime validator for those freshness/machine-action constraints.
- `scripts/agent_dispatch.py` invokes that guard inside the serialized claim path while the local mutex is held, after reloading current READY/dependency state and before READY→CLAIMED. Any guard error aborts claim and prevents the subprocess.
- if no real local bot command is configured, dispatcher leaves task and trigger READY; it does not claim work it cannot execute.
- immediately before a real bot subprocess, watcher acquires the local atomic mutex `AI_SYNC/.dispatcher_claim.lock` using an exclusive create operation, then reloads queue + trigger while holding that mutex.
- only one watcher in the same checkout can perform the READY→CLAIMED transition; a second watcher skips the cycle while the mutex is occupied or if reloaded state is no longer READY.
- a mutex older than the configured stale threshold is recovered only when its recorded local PID is confirmed dead; fresh locks, unparseable locks and locks owned by live processes are never stolen.
- while holding the mutex, watcher validates the runtime handoff, then atomically persists task `CLAIMED`, `lock.owner`, `lock.claimed_at` and trigger `status=CLAIMED`; the mutex is then released before the bot subprocess starts.
- dependencies listed in `blocked_by` must be in explicit resolved states before claim; missing or unresolved dependencies block dispatch.
- if the bot subprocess exits non-zero while the task is still `CLAIMED` by that same agent, dispatcher records `task.status=BLOCKED`, `last_error`, releases the task lock and moves trigger to `action=IDLE`, `status=BLOCKED`.
- if the bot already advanced the task to WORKING/TESTING/DONE/BLOCKED, dispatcher does not overwrite the newer bot-owned state.
- bot runs the requested checks and writes outcome back to queue/audit state.
- after a successful verified cycle, trigger becomes `IDLE` or points to the next READY task.

A report can therefore create work by publishing a READY queue item and setting the trigger to RUN_FIX. CI protects freshness, dependencies, lock/claim/failure recovery, mutex behavior and dispatcher↔runtime-guard integration.

## Safety gates

- `main` remains stable.
- Normal work uses `develop` or a feature branch based on develop.
- Never merge to main while CI is red.
- Never mark a task DONE without deterministic verification/test evidence.
- P0 integrity/financial/data-loss issues outrank UI and feature work.
- Automation never creates BEST57; it stays BEST56 + AUDYT.

## Handoff contract

Every completed bot cycle updates:

- `AI_SYNC/LATEST_AUDIT.json` — current machine state and evidence,
- `AI_SYNC/LATEST_AUDIT.md` — compact human-readable handoff,
- `AI_SYNC/BOT_QUEUE.json` — task status/owner/result,
- `AI_SYNC/TRIGGER.json` — next action,
- `sync/CRM_SYNC.md` if shared project state changed,
- `BACKLOG.md` / issue if blocker scope/status changed.

CI runs `tests/check_ai_sync_freshness.py` to ensure the handoff does not lag behind shared state and that trigger/audit machine action stays aligned. CI also runs `tests/check_handoff_runtime_guard.py` plus `tests/check_agent_dispatch_runtime_guard_integration.py` to verify the runtime guard contract and direct dispatcher integration.

## Local self-dispatch

Run `python scripts/agent_dispatch.py --watch` from the repository root. The dispatcher polls `AI_SYNC/TRIGGER.json`. When `RUN_FIX + READY` appears, it builds `AI_SYNC/BOT_INBOX.md` from the task. When `FLIPPCHILL_BOT_COMMAND` is configured, it serializes the claim, revalidates the current handoff with the runtime guard, claims the task, then invokes the local bot.

The command template may contain `{prompt_file}`, `{agent}`, and `{task_id}`. Example shape only:

`FLIPPCHILL_BOT_COMMAND="your-bot-command {prompt_file}"`

The dispatcher deliberately requires an explicit local command instead of assuming a specific OpenCode CLI syntax.
