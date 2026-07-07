# R18 - 可行套路设计

Date: 2026-04-30
Timebox: accelerated run using the 60-minute protocol
Question: 我们自己的 SOP 应该继承哪些，删除哪些？
Working hypothesis: The SOP should copy the loop, not the brand: intake, evidence, plan, harness, eval, PR, incident response, and memory.

## Sources Checked

| Source | Type | URL | Evidence Level | Notes |
|---|---|---|---|---|
| R01-R17 cards | Internal synthesis | `cc/research-rounds/` | A | Evidence base |
| Best practices | Official docs | https://code.claude.com/docs/en/best-practices | S | Core method |
| Long-running harness | Official engineering | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | S | Execution structure |
| April 23 postmortem | Official engineering | https://www.anthropic.com/engineering/april-23-postmortem | S | Quality response |
| Enterprise/security docs | Official docs/product | https://claude.com/product/claude-code/enterprise | S | Governance |

## Facts

- [Fact][Confidence: High] The research base consistently points to the same core loop: real task, context, plan, action, verification, PR, learn.
- [Fact][Confidence: High] Long tasks require durable state and verification artifacts.
- [Fact][Confidence: High] Quality and security need explicit gates.

## Inferences

- [Inference][Confidence: High] Our first SOP should be lightweight but enforceable through templates.
- [Inference][Confidence: High] The minimum artifact set is task template, PR checklist, eval bank template, long-running harness, incident template, product method, and operating model.
- [Inference][Confidence: Med] A weekly review cadence will convert individual wins into organizational learning.

## Contradictions / Risks

- [Risk] Too much process can slow early experimentation.
- [Risk] Templates without enforcement become theater.

## Impact On Our Playbook

Keep: The Claude-style loop.

Change: Make every stage produce a file or explicit signal.

Add: Seven concrete templates and a 30-day rollout.

Remove: Untracked agent work and undocumented “magic prompts.”

## Next Questions

1. Which claims have high confidence?
2. Which remain uncertain?
3. What final operating model should be committed?
