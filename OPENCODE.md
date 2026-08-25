# OpenCode — Flipp&Chill shared-state protocol

Before making any change in this repository:

1. Read `sync/CRM_SOURCE_OF_TRUTH.json`.
2. Read `sync/CRM_SYNC.md`.
3. Read `BACKLOG.md`.
4. Inspect open P0/P1 GitHub Issues.
5. Treat the repository state as authoritative over conversational memory.

Rules:

- Never introduce a second copy of a business rule if the same rule already exists in the source-of-truth manifest or central application config.
- If a user request conflicts with the manifest, implement the newest explicit user request and update the manifest in the same commit.
- Every completed feature must have: implementation, test or deterministic verification, backlog update, and sync-state update when relevant.
- Do not promote a BEST release while CI is red.
- `main` is stable; normal development happens on `develop` or feature branches.
- The CRM Baza mieszkań view and financial calculator must consume the same transaction/status/financial semantics.

At the end of each work cycle output a compact SYNC PACKET:

- CHANGESET
- BUSINESS DECISIONS
- P0/P1 BLOCKERS
- CRM BAZA MIESZKAŃ IMPACT
- TEST RESULTS
- COMMIT SHA

This packet is intended to be reusable in other ChatGPT/OpenCode work threads without re-explaining the project.
