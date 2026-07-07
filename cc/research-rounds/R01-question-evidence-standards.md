# R01 - 问题定义与证据标准

Date: 2026-04-30
Timebox: accelerated run using the 60-minute protocol
Question: 我们到底要学习 Claude Code 的什么，哪些结论算可证实？
Working hypothesis: 要学习的不是工具清单，而是一套可复用的 AI-native 产品和工程操作系统。

## Sources Checked

| Source | Type | URL | Evidence Level | Notes |
|---|---|---|---|---|
| Existing initial report | Internal research | `cc/claude-code-team-research.md` | A | Provides first-pass success model |
| Expanded source assessment | Internal research | `cc/claude-code-expanded-source-assessment.md` | A | Adds missing risk/eval/security dimensions |
| Claude Code docs | Official docs | https://code.claude.com/docs/en/how-claude-code-works | S | Defines product behavior loop |
| Best practices | Official docs | https://code.claude.com/docs/en/best-practices | S | Defines recommended work method |
| April 23 postmortem | Official engineering | https://www.anthropic.com/engineering/april-23-postmortem | S | Shows quality regression and correction mechanism |

## Facts

- [Fact][Confidence: High] Claude Code publicly presents itself as a terminal-native, agentic coding tool that can understand codebases, edit files, run commands, and manage workflows.
- [Fact][Confidence: High] Official docs and engineering posts emphasize context gathering, tool use, verification, permissioning, and iterative task completion rather than pure autocomplete.
- [Fact][Confidence: High] Existing research already identified the correct high-level direction, but underweighted eval, release quality, rollback, enterprise governance, and community canary signals.

## Inferences

- [Inference][Confidence: High] The useful target to copy is an operating model: demand intake, planning, harness, eval, PR review, release, incident response, and organization memory.
- [Inference][Confidence: High] The evidence standard must separate official product facts from community sentiment and from our own extrapolation.
- [Inference][Confidence: Med] The highest leverage research output is not a narrative report, but a reusable SOP and templates that can run inside our own team.

## Contradictions / Risks

- [Risk] Public sources do not expose Claude Code's real internal org chart, launch cadence meetings, or exact eval thresholds.
- [Risk] Community posts are high-signal but noisy; they should be treated as canaries, not ground truth.

## Impact On Our Playbook

Keep: The “agentic harness, not autocomplete” frame.

Change: Every conclusion must carry `Fact / Inference / Hypothesis / Risk`.

Add: Evidence levels S/A/B/C and a confidence audit at the end of every research cycle.

Remove: Any claim about internal team structure unless backed by official pages or direct interviews.

## Next Questions

1. What is Claude Code's actual public product surface today?
2. Which capabilities are core vs adoption/enterprise surfaces?
3. What should become our own minimum operating model?
