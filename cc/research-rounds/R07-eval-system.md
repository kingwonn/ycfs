# R07 - Eval 体系

Date: 2026-04-30
Timebox: accelerated run using the 60-minute protocol
Question: Claude Code 如何判断 agent 行为变好或变坏？
Working hypothesis: Agent eval 必须评价最终环境 outcome、工具调用轨迹和人工感知质量，不能只看单一 benchmark。

## Sources Checked

| Source | Type | URL | Evidence Level | Notes |
|---|---|---|---|---|
| Demystifying evals for AI agents | Official engineering | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | S | Eval methodology |
| Infrastructure noise in agentic coding evals | Official engineering | https://www.anthropic.com/engineering/infrastructure-noise | S | Benchmark reliability |
| April 23 postmortem | Official engineering | https://www.anthropic.com/engineering/april-23-postmortem | S | Regression detection |
| Daily benchmark tracker | Community | https://marginlab.ai/trackers/claude-code/ | B | External tracking signal |

## Facts

- [Fact][Confidence: High] Anthropic publicly discusses agent eval design and warns that infrastructure constraints can distort benchmark results.
- [Fact][Confidence: High] The April quality incident led Anthropic to broaden eval coverage and review prompt/model behavior changes more carefully.
- [Fact][Confidence: High] Community benchmark trackers exist, which indicates external demand for regression visibility.

## Inferences

- [Inference][Confidence: High] Our eval bank should include task success, tests, diff quality, tool calls, cost, latency, and human review labels.
- [Inference][Confidence: High] Any prompt/system/model/tool change must run through a regression task set.
- [Inference][Confidence: Med] Eval failure taxonomy is more valuable than aggregate score alone.

## Contradictions / Risks

- [Risk] LLM judge scores can drift or mask real developer frustration.
- [Risk] Benchmarks may not reflect our codebase and team workflows.

## Impact On Our Playbook

Keep: Verification before completion.

Change: Replace informal “looks good” with eval records.

Add: `codex/eval-bank-template.md` with task fixtures, expected checks, metrics, and failure taxonomy.

Remove: Any release process that cannot answer “which tasks got worse?”

## Next Questions

1. What did the quality incident reveal about release gates?
2. Which eval tasks should be first in our bank?
3. How do we integrate community canary feedback?
