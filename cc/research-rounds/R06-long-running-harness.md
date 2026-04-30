# R06 - 长任务 Harness

Date: 2026-04-30
Timebox: accelerated run using the 60-minute protocol
Question: 长时间 agent 任务如何不断片？
Working hypothesis: 长任务成功依赖外部化状态，而不是依赖单次上下文窗口。

## Sources Checked

| Source | Type | URL | Evidence Level | Notes |
|---|---|---|---|---|
| Effective harnesses for long-running agents | Official engineering | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | S | Task harness pattern |
| Harness design for long-running apps | Official engineering | https://www.anthropic.com/engineering/harness-design-long-running-apps | S | Planner/generator/evaluator framing |
| Building a C compiler | Official engineering | https://www.anthropic.com/engineering/building-c-compiler | S | Parallel long-running project |
| Agent teams docs | Official docs | https://code.claude.com/docs/en/agent-teams | S | Coordination surface |

## Facts

- [Fact][Confidence: High] Anthropic describes explicit harness design for long-running agents, including initialization, progress tracking, feature lists, and verification loops.
- [Fact][Confidence: High] The C compiler case used many Claude Code sessions and parallel work, demonstrating that large tasks require orchestration beyond a single prompt.
- [Fact][Confidence: High] Official docs now treat agent teams as a product-level coordination concept.

## Inferences

- [Inference][Confidence: High] Long tasks need durable files: `feature_list.json`, `progress.md`, `init.sh`, eval scripts, and commit boundaries.
- [Inference][Confidence: High] Every agent turn should start by reading state and end by updating state.
- [Inference][Confidence: Med] The harness is the real product moat for long work, because models alone forget or overrun scope.

## Contradictions / Risks

- [Risk] Harness overhead is wasteful for tiny tasks.
- [Risk] If progress files are not reviewed, they become stale fiction.

## Impact On Our Playbook

Keep: Commit frequently after coherent progress.

Change: Multi-hour work must be state-machine driven.

Add: Required long-running harness template with feature list, progress log, init script, evals.

Remove: Long unsupervised tasks without checkpoint files.

## Next Questions

1. What eval bank should monitor these long-running tasks?
2. How should failures be classified?
3. How much parallelism is worth the cost?
