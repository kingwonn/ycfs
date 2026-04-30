# R03 - 发布节奏

Date: 2026-04-30
Timebox: accelerated run using the 60-minute protocol
Question: Claude Code 迭代有多快，哪些阶段变化最大？
Working hypothesis: Claude Code 采用高频发布策略，但必须依赖质量门、回滚和社区反馈承压。

## Sources Checked

| Source | Type | URL | Evidence Level | Notes |
|---|---|---|---|---|
| Changelog | Official docs | https://code.claude.com/docs/en/changelog | S | Release notes |
| NPM package metadata | Registry | https://www.npmjs.com/package/@anthropic-ai/claude-code | A | Version timestamps |
| HN search | Community index | https://news.ycombinator.com | A | Community response to releases |
| April 23 postmortem | Official engineering | https://www.anthropic.com/engineering/april-23-postmortem | S | Regression response |

## Facts

- [Fact][Confidence: High] NPM metadata shows package creation on 2025-02-24 and latest observed version `2.1.124` modified on 2026-04-30.
- [Fact][Confidence: High] Version history shows dense release activity, including multiple releases in short windows and major version jumps to `1.0.0` and `2.0.0` during 2025.
- [Fact][Confidence: High] Anthropic publicly acknowledged at least one Claude Code quality incident and described release/process corrections.

## Inferences

- [Inference][Confidence: High] Claude Code's team likely optimizes for shipping fast with live product feedback, not long waterfall cycles.
- [Inference][Confidence: High] High cadence creates compounding learning, but also raises regression risk in model/prompt/tool behavior.
- [Inference][Confidence: Med] Release velocity is a product advantage only if paired with soak tests, evals, and rollback.

## Contradictions / Risks

- [Risk] NPM timestamps prove publishing cadence, not internal development cadence.
- [Risk] High release count may include small bugfixes and packaging changes, not always meaningful feature change.

## Impact On Our Playbook

Keep: Fast ship cycles.

Change: “Ship fast” must become “ship fast with eval, canary, rollback, and public incident response.”

Add: A release ledger tracking version, behavior change, eval result, rollout scope, rollback plan.

Remove: Blind daily shipping without objective behavior checks.

## Next Questions

1. How does documentation teach users to absorb this fast-moving product?
2. What release changes require extra gates?
3. How should our team measure release risk?
