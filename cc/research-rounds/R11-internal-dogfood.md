# R11 - 内部 Dogfood

Date: 2026-04-30
Timebox: accelerated run using the 60-minute protocol
Question: Anthropic 内部哪些团队怎么用 Claude Code？
Working hypothesis: Claude Code 的产品定义来自跨职能 dogfood，而不仅是工程团队写代码。

## Sources Checked

| Source | Type | URL | Evidence Level | Notes |
|---|---|---|---|---|
| How Anthropic teams use Claude Code | Official blog | https://claude.com/blog/how-anthropic-teams-use-claude-code | S | Internal use cases |
| Best practices | Official docs | https://code.claude.com/docs/en/best-practices | S | Internalized usage pattern |
| Routines announcement | Official blog | https://claude.com/blog/introducing-routines-in-claude-code | S | Automation beyond coding |
| Claude Code in Slack | Official docs | https://code.claude.com/docs/en/slack | S | Team collaboration |

## Facts

- [Fact][Confidence: High] Anthropic publicly describes multiple internal teams using Claude Code, including engineering, data, security, product design, legal, and growth-related functions.
- [Fact][Confidence: High] Use cases include code navigation, testing, debugging, prototyping, data analysis, automation, documentation, and repetitive workflow execution.
- [Fact][Confidence: High] Collaboration surfaces such as Slack and routines indicate internal use is not limited to local terminal sessions.

## Inferences

- [Inference][Confidence: High] Dogfood broadens product definition from “developer coding assistant” to “software-mediated work assistant.”
- [Inference][Confidence: High] Non-engineering teams expose workflow gaps that pure coding benchmarks miss.
- [Inference][Confidence: Med] The fastest feedback loop is internal daily usage by people close enough to product to report precise failures.

## Contradictions / Risks

- [Risk] Official dogfood examples are curated success cases.
- [Risk] Internal adoption intensity and failure rate are not public.

## Impact On Our Playbook

Keep: Internal-first usage before external methodology claims.

Change: Dogfood should include PM, design, data, growth, support, and ops, not only engineers.

Add: Weekly dogfood report with workflow, outcome, failure, rule/eval update.

Remove: Treating product feedback as only customer interviews.

## Next Questions

1. Which public members shaped Claude Code?
2. How should our own non-engineering roles use agents?
3. What dogfood metrics should be required?
