# R02 - 官方产品面

Date: 2026-04-30
Timebox: accelerated run using the 60-minute protocol
Question: Claude Code 当前公开能力边界是什么？
Working hypothesis: Claude Code 是跨 terminal、IDE、web、mobile、Slack、GitHub Actions 的 agentic coding surface，而 CLI 是核心入口。

## Sources Checked

| Source | Type | URL | Evidence Level | Notes |
|---|---|---|---|---|
| Claude Code product page | Official product | https://claude.com/product/claude-code | S | Product positioning and access |
| How Claude Code works | Official docs | https://code.claude.com/docs/en/how-claude-code-works | S | Agent loop |
| GitHub Actions docs | Official docs | https://code.claude.com/docs/en/github-actions | S | PR/CI surface |
| Slack docs | Official docs | https://code.claude.com/docs/en/slack | S | Collaboration surface |
| NPM package metadata | Registry | https://www.npmjs.com/package/@anthropic-ai/claude-code | A | Distribution and versioning |

## Facts

- [Fact][Confidence: High] Claude Code is distributed as `@anthropic-ai/claude-code`; registry metadata describes it as a terminal assistant that understands codebases, edits files, runs terminal commands, and handles workflows.
- [Fact][Confidence: High] Official surfaces include CLI, IDE integrations, GitHub Actions/CI, Slack, and broader Claude app surfaces.
- [Fact][Confidence: High] Product documentation centers the loop of context collection, action, and verification.

## Inferences

- [Inference][Confidence: High] The CLI gives the product privileged access to the real developer environment: repo, shell, tests, build tools, Git, and local conventions.
- [Inference][Confidence: High] The expansion from CLI to collaboration surfaces is a deliberate route from solo productivity to team operating system.
- [Inference][Confidence: Med] The product boundary is moving from “coding tool” toward “software work orchestration layer.”

## Contradictions / Risks

- [Risk] Public pages blur boundaries between Claude Code, Claude app, Cowork, Routines, and enterprise products.
- [Risk] Some features may be plan-gated or region-gated; public availability does not imply every team can use them immediately.

## Impact On Our Playbook

Keep: Start where developers already work: repo, terminal, GitHub, Slack.

Change: Define product surface as workflow completion, not interface count.

Add: Our SOP must distinguish core loop, collaboration surface, and enterprise control plane.

Remove: Any single-surface assumption such as “CLI only.”

## Next Questions

1. How fast has this surface changed over time?
2. Which features caused adoption jumps?
3. Which surfaces are essential for our own first version?
