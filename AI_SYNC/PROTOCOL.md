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
- `action=RUN_FIX`, `status=READY`: watcher/supervisor may launch the bot named by `target_agent` for `task_id`.
- watcher changes local state to `CLAIMED` before execution.
- bot runs the requested checks and writes outcome back to queue/audit state.
- after a successful verified cycle, trigger becomes `IDLE` or points to the next READY task.

A report can therefore create work by publishing a READY queue item and setting the trigger to RUN_FIX.

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

## Local self-dispatch

Run `python scripts/agent_dispatch.py --watch` from the repository root. The dispatcher polls `AI_SYNC/TRIGGER.json`. When `RUN_FIX + READY` appears, it builds `AI_SYNC/BOT_INBOX.md` from the task and invokes the command configured in `FLIPPCHILL_BOT_COMMAND`.

The command template may contain `{prompt_file}`, `{agent}`, and `{task_id}`. Example shape only:

`FLIPPCHILL_BOT_COMMAND="your-bot-command {prompt_file}"`

The dispatcher deliberately requires an explicit local command instead of assuming a specific OpenCode CLI syntax.
