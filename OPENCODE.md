# OpenCode — Flipp&Chill shared-state protocol

Before making any change in this repository:

1. Read `sync/CRM_SOURCE_OF_TRUTH.json`.
2. Read `AI_SYNC/PROTOCOL.md`.
3. Read `AI_SYNC/LATEST_AUDIT.json`.
4. Read `AI_SYNC/BOT_QUEUE.json`.
5. Read `AI_SYNC/TRIGGER.json`.
6. Read `sync/CRM_SYNC.md`.
7. Read `BACKLOG.md`.
8. Inspect open P0/P1 GitHub Issues and current CI state.
9. If a queue task is assigned to your role and is `READY`, claim only that task before implementation.

Treat repository state as authoritative over conversational memory.

## Agent roles

- `PRIMARY` — implementation/integration on `develop` or feature/fix branches.
- `SECOND_AUDIT` — independent regression, data-integrity and financial verification.
- `THIRD_UI` — UI/UX, responsive, accessibility and visual-regression verification.

Do not take a task locked by another agent unless the queue explicitly reassigns it.

## Rules

- Never introduce a second copy of a business rule if the same rule already exists in the source-of-truth manifest or central application config.
- If a user request conflicts with the manifest, implement the newest explicit user request and update the manifest in the same commit.
- Every completed feature/fix must have: implementation, test or deterministic verification, backlog/issue update when relevant, and sync-state update.
- Do not promote a BEST release while CI is red.
- `main` is stable; normal development happens on `develop` or feature/fix branches.
- The CRM Baza mieszkań view and financial calculator must consume the same transaction/status/financial semantics.
- Automatic audit work NEVER increments BEST56. Audit artifacts are named `BEST56 BAZA MIESZKAŃ AUDYT`.
- If a task cannot be verified, mark it `BLOCKED`; never fabricate PASS.

## Machine handoff / dispatch

`AI_SYNC/TRIGGER.json` is the dispatch signal.

When `action=RUN_FIX` and `status=READY`, the watcher/supervisor may start the target agent for the referenced queue task. The bot must read the queue task, work only in its scope, run required checks, then update:

- `AI_SYNC/LATEST_AUDIT.json`
- `AI_SYNC/LATEST_AUDIT.md`
- `AI_SYNC/BOT_QUEUE.json`
- `AI_SYNC/TRIGGER.json`
- `sync/CRM_SYNC.md` when shared state changes
- `BACKLOG.md` / GitHub issue when blocker status changes

The full lifecycle and locking rules are in `AI_SYNC/PROTOCOL.md`.

A local watcher can be started with:

`python scripts/agent_dispatch.py --watch`

The local bot command is configured via `FLIPPCHILL_BOT_COMMAND`; the dispatcher does not assume a specific OpenCode CLI syntax.

## End-of-cycle SYNC PACKET

Output and persist:

- CHANGESET
- BUSINESS DECISIONS
- P0/P1 BLOCKERS
- CRM BAZA MIESZKAŃ IMPACT
- TEST RESULTS
- COMMIT SHA / PR
- NEXT READY TASK
- TARGET AGENT
- TRIGGER STATUS

This packet is intended to be reusable by all three bots and by ChatGPT/OpenCode threads without re-explaining the project.
