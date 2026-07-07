# R09 - 权限与安全

Date: 2026-04-30
Timebox: accelerated run using the 60-minute protocol
Question: 自动执行如何控制风险？
Working hypothesis: Automation only scales when permissions are explicit, observable, and bounded by environment.

## Sources Checked

| Source | Type | URL | Evidence Level | Notes |
|---|---|---|---|---|
| Claude Code auto mode | Official engineering | https://www.anthropic.com/engineering/claude-code-auto-mode | S | Permission automation |
| Claude Code Security | Official product | https://claude.com/solutions/claude-code-security | S | Security offering |
| Enterprise product page | Official product | https://claude.com/product/claude-code/enterprise | S | Admin controls |
| Hooks docs | Official docs | https://code.claude.com/docs/en/hooks | S | Automation hooks |
| Security docs | Official docs | https://code.claude.com/docs/en/security | S | Safe use guidance |

## Facts

- [Fact][Confidence: High] Claude Code exposes permissioning and automation concepts as product and documentation concerns.
- [Fact][Confidence: High] Enterprise/security pages emphasize controls such as admin governance, observability, and safer deployment.
- [Fact][Confidence: High] Auto mode exists because repeated manual permission approvals create friction and fatigue.

## Inferences

- [Inference][Confidence: High] The correct model is not “always manual” or “always autonomous,” but risk-tiered execution.
- [Inference][Confidence: High] Hooks and allowlists should enforce organization policy before dangerous commands run.
- [Inference][Confidence: Med] Security positioning is central to enterprise adoption, not a later compliance add-on.

## Contradictions / Risks

- [Risk] Auto permission classifiers can fail under prompt injection or unusual tools.
- [Risk] Excessive friction can push users to unsafe bypasses.

## Impact On Our Playbook

Keep: Human approval for high-risk changes.

Change: Define three modes: explore-only, human-approved execution, bounded auto mode.

Add: Permission matrix by tool/action/environment.

Remove: Ad hoc approvals without logging.

## Next Questions

1. What enterprise controls are required for teams?
2. Which commands are safe to auto-run?
3. How should audit logs be reviewed?
