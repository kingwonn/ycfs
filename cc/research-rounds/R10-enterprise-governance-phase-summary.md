# R10 - 企业化与第二阶段汇总

Date: 2026-04-30
Timebox: accelerated run using the 60-minute protocol
Question: Team/Enterprise 如何支撑组织采用？
Working hypothesis: Claude Code 的企业化核心是可见性、身份、权限、成本、策略和部署选择。

## Sources Checked

| Source | Type | URL | Evidence Level | Notes |
|---|---|---|---|---|
| Claude Code Enterprise | Official product | https://claude.com/product/claude-code/enterprise | S | Enterprise capabilities |
| Team and Enterprise announcement | Official news | https://www.anthropic.com/news/claude-code-on-team-and-enterprise | S | Business packaging |
| Analytics docs | Official docs | https://code.claude.com/docs/en/analytics | S | Usage observability |
| OpenTelemetry docs | Official docs | https://code.claude.com/docs/en/monitoring-usage | S | Monitoring direction |
| Security docs | Official docs | https://code.claude.com/docs/en/security | S | Controls |

## Facts

- [Fact][Confidence: High] Claude Code has Team/Enterprise-oriented positioning and docs covering admin, analytics, security, and deployment concerns.
- [Fact][Confidence: High] Usage monitoring and telemetry are documented, indicating organizational observability is part of adoption.
- [Fact][Confidence: High] Enterprise adoption requires controls that individual CLI use does not require.

## Inferences

- [Inference][Confidence: High] Team-scale AI coding requires a control plane: identity, policy, spend, logs, allowed tools, and eval dashboards.
- [Inference][Confidence: High] Governance should accelerate adoption by reducing security ambiguity.
- [Inference][Confidence: Med] The team operating model should include a weekly review of usage, incidents, and high-value workflows.

## Contradictions / Risks

- [Risk] Enterprise product pages do not reveal customer implementation details.
- [Risk] Over-governance can destroy the speed advantage.

## Impact On Our Playbook

Keep: Central admin controls and usage visibility.

Change: Treat governance as part of the product loop.

Add: Weekly AI engineering ops review: usage, cost, failures, wins, policy changes.

Remove: Private, invisible personal agent workflows as the default for team-critical work.

## Phase 2 Summary

Initial belief reinforced: speed comes from harness + verification, not prompts alone.

Initial belief corrected: safety and enterprise controls are speed multipliers when designed well.

Still missing: Anthropic's exact internal eval thresholds and enterprise customer net metrics.

Playbook update: add eval bank, quality incident template, permission matrix, and governance review cadence.

## Next Questions

1. How does Anthropic dogfood Claude Code internally?
2. Which roles and members are publicly tied to Claude Code?
3. What external community signals matter most?
