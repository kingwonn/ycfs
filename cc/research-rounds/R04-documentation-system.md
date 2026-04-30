# R04 - 文档体系

Date: 2026-04-30
Timebox: accelerated run using the 60-minute protocol
Question: 官方如何教育用户形成新工作法？
Working hypothesis: Claude Code 文档本质上是 adoption infrastructure，不只是 API reference。

## Sources Checked

| Source | Type | URL | Evidence Level | Notes |
|---|---|---|---|---|
| Overview | Official docs | https://code.claude.com/docs/en/overview | S | Product entry point |
| Best practices | Official docs | https://code.claude.com/docs/en/best-practices | S | Work method |
| Common workflows | Official docs | https://code.claude.com/docs/en/common-workflows | S | Use case guidance |
| Hooks | Official docs | https://code.claude.com/docs/en/hooks | S | Automation point |
| Skills | Official docs | https://code.claude.com/docs/en/skills | S | Reusable workflows |

## Facts

- [Fact][Confidence: High] The documentation includes product overview, quickstart, common workflows, memory, hooks, MCP, skills, subagents, security, analytics, and enterprise topics.
- [Fact][Confidence: High] The docs teach how to structure Claude Code usage, not merely how to install it.
- [Fact][Confidence: High] Reusable instructions and automation points are first-class doc concepts.

## Inferences

- [Inference][Confidence: High] Documentation is part of the product: it shapes the user into an effective agent manager.
- [Inference][Confidence: High] The docs convert tacit team practices into public rituals: plan, verify, use memory, create repeatable commands.
- [Inference][Confidence: Med] The product likely depends on user education more than traditional devtools because agent outcomes are prompt/process-sensitive.

## Contradictions / Risks

- [Risk] Docs may lag actual product behavior.
- [Risk] Users may cargo-cult advanced features before mastering the core loop.

## Impact On Our Playbook

Keep: Document the work method, not just the tool.

Change: Our docs should be operational templates with exact inputs/outputs.

Add: A “start here” path: task intake -> plan -> execute -> verify -> PR -> learn.

Remove: Long unstructured essays as primary onboarding.

## Next Questions

1. What do official best practices converge on?
2. Which doc features should become mandatory in our workflow?
3. How do hooks/skills/memory interact with quality?
