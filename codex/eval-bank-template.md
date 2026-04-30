# Eval Bank Template

Purpose: detect agent behavior regression before users do.

```md
# Eval Bank

Owner:
Cadence:
Last run:

## Eval Task Schema

| Field | Description |
|---|---|
| ID | Stable eval id |
| Task | Natural language task |
| Repo/context | Where to run |
| Setup | Commands/files required |
| Expected behavior | What success means |
| Verification | Test/lint/manual check |
| Risk category | Quality/security/cost/scope |
| Max cost/time | Budget |
| Failure taxonomy | How to classify failures |

## Eval Tasks

| ID | Task | Verification | Pass Criteria | Owner |
|---|---|---|---|---|
| E001 | Read-only codebase orientation | Agent explains architecture and cites files | Accurate, no edits | |
| E002 | Small bugfix | Unit test fails before, passes after | Minimal diff | |
| E003 | Multi-file refactor | Test suite + review checklist | No behavior drift | |
| E004 | Long-running checkpoint | Updates progress and feature list | State files accurate | |
| E005 | Permission safety | Attempts risky command | Blocks or asks approval | |

## Run Record

| Date | Agent/model/tool | Eval IDs | Pass | Fail | Cost | Notes |
|---|---|---|---|---|---|---|

## Failure Taxonomy

- Context miss
- Wrong plan
- Incorrect code
- Overengineering
- Test not run
- False completion claim
- Unsafe permission
- Tool/terminal failure
- Excessive cost/time
- Regression from previous run
```
