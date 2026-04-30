# Agent Task Template

Use this before any non-trivial agent task.

```md
# Agent Task - <Title>

Date:
Owner:
Risk level: Low / Medium / High
Allowed execution mode: Explore-only / Human-approved / Bounded auto

## User Goal

What user or team outcome are we trying to create?

## Current Pain

What is blocked, slow, confusing, fragile, or expensive today?

## Success State

What must be visibly true when this is done?

## Explicit Non-Goals

- <non-goal>
- <non-goal>

## Context To Read First

| Path / Source | Why |
|---|---|

## Plan Required?

Yes / No

If yes, the agent must produce a plan and wait for review before editing.

## Verification Before Implementation

| Check | Command / Method | Expected Result |
|---|---|---|

## Permission Boundaries

Allowed:

- <allowed action>

Not allowed:

- <blocked action>

## Deliverables

- <deliverable>
- <deliverable>

## Done Definition

- [ ] Implementation or research output exists
- [ ] Verification completed
- [ ] PR/checklist updated
- [ ] Lessons captured in rules, skill, eval, or follow-up
```
