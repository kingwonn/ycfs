# Product Method For AI-Native Agent Tools

This method distills the Claude Code research into a product definition workflow.

## Principle

Define products by completed user workflows, not UI surfaces or model capabilities.

## Product Definition Template

```md
# Product Method - <Feature>

## User Workflow

What complete job does the user need done?

## Current Failure

Where does the current workflow break?

## Agent Role

Should the agent:

- Observe
- Suggest
- Plan
- Execute with approval
- Execute automatically

## Human Role

What decisions must stay human-owned?

## Required Context

What files, docs, systems, memories, or connectors must be available?

## Verification

How does the product know the job is complete?

## Safety Boundary

What can go wrong, and how do we stop or recover?

## Adoption Path

How does the user learn the new workflow?

## Organization Memory

What should become reusable rule, skill, command, eval, or doc?
```

## Feature Prioritization

Prioritize features that satisfy all four:

1. Frequent real task
2. High pain or high leverage
3. Clear verification signal
4. Reusable across team workflows

Deprioritize features that are impressive demos but lack verification or repeated use.
