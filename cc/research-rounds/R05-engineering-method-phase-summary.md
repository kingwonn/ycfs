# R05 - 工程方法与第一阶段汇总

Date: 2026-04-30
Timebox: accelerated run using the 60-minute protocol
Question: 官方 best practices 的共同模式是什么？
Working hypothesis: Claude Code 的方法核心是 plan-first、context-first、verification-first、memory-first。

## Sources Checked

| Source | Type | URL | Evidence Level | Notes |
|---|---|---|---|---|
| Best practices | Official docs | https://code.claude.com/docs/en/best-practices | S | Core usage pattern |
| How Claude Code works | Official docs | https://code.claude.com/docs/en/how-claude-code-works | S | Agent loop |
| Subagents docs | Official docs | https://code.claude.com/docs/en/sub-agents | S | Specialized agents |
| Agent teams docs | Official docs | https://code.claude.com/docs/en/agent-teams | S | Coordinated parallel work |
| Introduction to agentic coding | Official blog | https://claude.com/blog/introduction-to-agentic-coding | S | Mental model |

## Facts

- [Fact][Confidence: High] Official guidance repeatedly emphasizes giving Claude context, letting it inspect, planning complex changes, running tests, and iterating.
- [Fact][Confidence: High] Subagents and agent teams are documented as ways to decompose work into specialized agents.
- [Fact][Confidence: High] Claude Code is designed around tool use in the developer's environment.

## Inferences

- [Inference][Confidence: High] The base workflow should be `Explore -> Plan -> Review -> Implement -> Verify -> PR -> Learn`.
- [Inference][Confidence: High] The human role shifts from typing code to setting goals, approving plans, judging tradeoffs, and verifying outcomes.
- [Inference][Confidence: Med] A team without verification discipline will see inconsistent outcomes even with the same model.

## Contradictions / Risks

- [Risk] “Agent teams” can create coordination overhead if tasks are not actually independent.
- [Risk] More automation without stronger verification can increase blast radius.

## Impact On Our Playbook

Keep: Plan-first and verification-first.

Change: Make context gathering an explicit first phase, not an invisible prelude.

Add: A rule that every task must state validation before implementation.

Remove: “Just ask the agent to code” as an acceptable work mode.

## Phase 1 Summary

Initial belief reinforced: Claude Code is a workflow product, not an autocomplete product.

Initial belief corrected: release quality, eval, and governance are as important as the visible UX.

Still missing: exact internal team cadence and private eval thresholds.

Playbook update: first version must include task intake, evidence grading, plan review, verification, and memory capture.

## Next Questions

1. How should long-running tasks persist state?
2. What eval system can detect agent quality regression?
3. How do permissions affect automation safety?
