# FlippChill AI_SYNC — 3-agent handoff and self-dispatch protocol

`AI_SYNC/` is the shared mailbox for PRIMARY, SECOND_AUDIT, THIRD_UI, ChatGPT automations, OpenCode and the local watcher/supervisor.

## Read order before any work

1. `sync/CRM_SOURCE_OF_TRUTH.json`
2. `AI_SYNC/LATEST_AUDIT.json`
3. `AI_SYNC/BOT_QUEUE.json`
4. `AI_SYNC/TRIGGER.json`
5. `BACKLOG.md`
6. relevant open GitHub issues

Repository state is authoritative over conversational memory.

## Roles

- `PRIMARY` — implementation/integration on `develop` or a feature branch; never silently promotes `main`.
- `SECOND_AUDIT` — independent audit, regression/data/finance verification; does not take ownership of PRIMARY's implementation task unless reassigned.
- `THIRD_UI` — UI/UX/responsive/accessibility/visual verification; does not rewrite core financial logic unless explicitly assigned.

## Audit output naming

Automation baseline remains `BEST56 BAZA MIESZKAŃ`.
Automatic audit artifacts use `BEST56 BAZA MIESZKAŃ AUDYT` and NEVER increment the BEST number.

## Queue lifecycle

Task states:

`OPEN -> READY -> CLAIMED -> WORKING -> TESTING -> DONE`

Alternative terminal states:

`BLOCKED`, `REJECTED`, `SUPERSEDED`.

Each task has exactly one `owner` while CLAIMED/WORKING/TESTING. `lock.owner` + `lock.claimed_at` prevent two bots from modifying the same scope simultaneously.

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
