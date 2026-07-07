# R15 - 生态与插件及第三阶段汇总

Date: 2026-04-30
Timebox: accelerated run using the 60-minute protocol
Question: 社区围绕 Claude Code 造了哪些工具？
Working hypothesis: Claude Code 的生态扩张围绕配置、hooks、skills、IDE/editor integration、monitoring、security skills 和 guides。

## Sources Checked

| Source | Type | URL | Evidence Level | Notes |
|---|---|---|---|---|
| GitHub search: Claude Code Anthropic | Public repos | https://github.com/search?q=Claude+Code+Anthropic&type=repositories | A | Ecosystem map |
| ZacheryGlass/.claude | Public repo | https://github.com/ZacheryGlass/.claude | A | Personal config patterns |
| Security skills repo | Public repo | https://github.com/Security-Phoenix-demo/security-skills-claude-code | A | Security skills |
| Rules Claude | Public repo | https://github.com/buildbuddy-io/rules_claude | A | Hermetic/Bazel integration |
| Clancy | Public repo | https://github.com/bazumo/clancy | A | Agent traffic proxy/monitoring |

## Facts

- [Fact][Confidence: High] GitHub search shows community work on configs, best-practices guides, skills, hooks, monitoring proxies, editor integrations, Bazel rules, and security workflows.
- [Fact][Confidence: High] Ecosystem projects often reinforce official primitives: rules, hooks, skills, MCP-like connectors, and execution wrappers.
- [Fact][Confidence: Med] Some projects mirror, analyze, or reconstruct Claude Code behavior, indicating high curiosity and trust scrutiny.

## Inferences

- [Inference][Confidence: High] A healthy agentic coding ecosystem forms around reusable context and guardrails, not just prompts.
- [Inference][Confidence: Med] Monitoring and hermetic execution are emerging needs for serious teams.
- [Inference][Confidence: Med] Security teams will build specialized skills faster than central product teams can cover every domain.

## Contradictions / Risks

- [Risk] GitHub stars are weak adoption proxies.
- [Risk] Some repos may be stale, unsafe, or based on leaked internals.

## Impact On Our Playbook

Keep: Build reusable skills and project configs.

Change: Evaluate community tools through safety and maintainability filters.

Add: `third-party-agent-tool-review.md` checklist before adopting tools.

Remove: Copying configs without understanding permissions and context load.

## Phase 3 Summary

Initial belief reinforced: community is part of the product's feedback and distribution system.

Initial belief corrected: negative feedback and external tooling are not peripheral; they expose production risks.

Still missing: Quantitative adoption by enterprise teams and real productivity deltas.

Playbook update: add community canary tracking, ecosystem review, and curated use case library.

## Next Questions

1. What does academic work say about agentic coding?
2. How does Claude Code compare to Codex/Cursor/Copilot/Devin/Gemini CLI?
3. What should our final SOP include?
