# Long-Running Agent Harness

Use this for tasks that span multiple hours, multiple sessions, or multiple agents.

## Required Files

```text
<task-root>/
  init.sh
  feature_list.json
  progress.md
  evals/
  logs/
```

## `init.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "Install dependencies and run the fastest baseline checks here."
```

## `feature_list.json`

```json
[
  {
    "id": "F001",
    "name": "Describe the feature or research outcome",
    "status": "pending",
    "verification": "Exact command or manual check",
    "owner": "agent-or-human",
    "notes": ""
  }
]
```

## `progress.md`

```md
# Progress

## Current State

## Completed

## In Progress

## Blocked

## Next Agent Should Read

## Last Verification
```

## Agent Start Protocol

1. Read `progress.md`.
2. Read `feature_list.json`.
3. Run `./init.sh` or the fastest safe baseline check.
4. Pick one feature only.
5. State plan before edits.

## Agent Stop Protocol

1. Run verification.
2. Update `feature_list.json`.
3. Update `progress.md`.
4. Commit coherent progress.
5. List remaining risks.

## Parallel Work Rule

Parallel agents need non-overlapping file ownership and one explicit integrator.
