# Quality Incident Postmortem Template

Use when agent output, prompt behavior, eval results, or user feedback shows quality regression.

```md
# Quality Incident - <Title>

Date:
Owner:
Severity: Low / Medium / High / Critical
Status: Investigating / Mitigated / Resolved

## Summary

What happened?

## Trigger Signal

- User report:
- Eval failure:
- CI/check failure:
- Community canary:
- Internal dogfood:

## Impact

Who was affected and how?

## Timeline

| Time | Event |
|---|---|

## Reproduction

Steps:

1.
2.
3.

Expected:

Actual:

## Root Cause

Classify:

- Model behavior
- Prompt/system instruction
- Tool/harness
- Permission policy
- Context/memory
- Eval gap
- Human process

## Fix

What changed?

## Verification

| Check | Result |
|---|---|

## New Eval Case

Eval ID:
Task:
Pass criteria:

## Prevention

- Rule update:
- Skill update:
- Hook update:
- Release gate update:
- Monitoring update:

## Follow-Ups

- [ ]
```
