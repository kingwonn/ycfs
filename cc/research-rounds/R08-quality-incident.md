# R08 - 质量事故

Date: 2026-04-30
Timebox: accelerated run using the 60-minute protocol
Question: 质量下降事件暴露了哪些门禁缺口？
Working hypothesis: Prompt/model/tool behavior changes can cause real regressions without traditional code failures.

## Sources Checked

| Source | Type | URL | Evidence Level | Notes |
|---|---|---|---|---|
| April 23 quality postmortem | Official engineering | https://www.anthropic.com/engineering/april-23-postmortem | S | Root causes and fixes |
| HN Claude Code results | Community | https://news.ycombinator.com | A | User-reported regression signals |
| GitHub issue #42796 | Public issue | https://github.com/anthropics/claude-code/issues/42796 | A | Workflow-level complaints |
| Claude Code changelog | Official docs | https://code.claude.com/docs/en/changelog | S | Release sequence |

## Facts

- [Fact][Confidence: High] Anthropic publicly identified multiple causes behind user quality complaints, including reasoning effort default changes, cache-related issues, and system prompt verbosity changes.
- [Fact][Confidence: High] Anthropic described corrective actions including broader evals, prompt review, ablations, gradual rollout, and better feedback channels.
- [Fact][Confidence: High] HN and GitHub surfaced quality concerns with high engagement, showing community feedback can outpace internal detection.

## Inferences

- [Inference][Confidence: High] Agent products need incident response for behavior regression, not just uptime incidents.
- [Inference][Confidence: High] Prompt changes should be treated like production code changes with review, tests, and rollback.
- [Inference][Confidence: Med] Community canaries should feed into triage dashboards with severity labels.

## Contradictions / Risks

- [Risk] Official postmortem gives root causes from Anthropic's view; user reports may include unrelated frustration.
- [Risk] Overreacting to loud users can destabilize roadmap.

## Impact On Our Playbook

Keep: Public postmortem discipline.

Change: Quality incidents must include model/prompt/config context.

Add: `codex/quality-incident-postmortem-template.md`.

Remove: Treating agent quality complaints as “subjective only.”

## Next Questions

1. How should permissions and safety mode reduce incident blast radius?
2. What metrics identify regression before users complain?
3. How should we handle contradictory feedback?
