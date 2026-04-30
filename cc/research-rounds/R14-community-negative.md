# R14 - 社区负反馈

Date: 2026-04-30
Timebox: accelerated run using the 60-minute protocol
Question: 用户最敏感的退化、抱怨和替代方案是什么？
Working hypothesis: Negative feedback clusters around quality regression, source/package trust, pricing/plan changes, and loss of autonomy.

## Sources Checked

| Source | Type | URL | Evidence Level | Notes |
|---|---|---|---|---|
| HN search: Claude Code | Community index | https://news.ycombinator.com | A | Negative and positive posts |
| GitHub issue #42796 | Public issue | https://github.com/anthropics/claude-code/issues/42796 | A | Complex task regression |
| April 23 postmortem | Official engineering | https://www.anthropic.com/engineering/april-23-postmortem | S | Official response |
| Source leak discussion | Community/blog | https://alex000kim.com/posts/2026-03-31-claude-code-source-leak/ | B | Trust/security discourse |
| Benchmark tracker | Community | https://marginlab.ai/trackers/claude-code/ | B | Degradation tracking |

## Facts

- [Fact][Confidence: High] HN results show high-engagement negative stories on quality regression, source leak concerns, plan restrictions, and benchmark tracking.
- [Fact][Confidence: High] Anthropic publicly acknowledged quality reports and changed process.
- [Fact][Confidence: Med] Users describe degradation using workflow metrics such as edit/read ratios, planning depth, and command compliance.

## Inferences

- [Inference][Confidence: High] Power-user complaints are a valuable source of eval tasks because they describe real workflow failures.
- [Inference][Confidence: High] Agent products need trust management across quality, packaging, security, and pricing.
- [Inference][Confidence: Med] Fast-moving agent products face unusually high user sensitivity to small behavior changes.

## Contradictions / Risks

- [Risk] Community outrage may conflate unrelated incidents.
- [Risk] Source-leak analysis may be incomplete or adversarial.

## Impact On Our Playbook

Keep: Treat external complaints as canary signals.

Change: Convert negative feedback into reproducible eval cases before changing product behavior.

Add: Risk radar with categories: quality, trust, cost, safety, autonomy, packaging.

Remove: Dismissing negative sentiment as “just vibes.”

## Next Questions

1. Which ecosystem tools show real adoption?
2. Which community projects should we learn from?
3. How do we prevent unsafe community cargo-culting?
