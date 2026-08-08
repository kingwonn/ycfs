# AI-Native Codex Research Plan

This plan structures a 20-round research cycle for studying OpenAI Codex, Symphony, and adjacent AI-native development practices. Each round is designed as a one-hour research block with evidence capture and synthesis.

## Research Objective

Develop a critical, implementation-oriented understanding of Codex-enabled development and synthesize a state-of-the-art AI-native software engineering operating model.

## Research Skills And Tools

- `smart-search`: External research, community signals, comparisons, and non-OpenAI sources.
- `openai-docs`: Official OpenAI Codex, Agents SDK, Responses API, Evals, and platform documentation.
- `browser-use` or `playwright`: Browser-visible verification for UI and local development workflows.
- `systematic-debugging`: Failure analysis for agentic coding, CI repair, and regression workflows.
- `writing-plans`: Convert final research findings into an executable implementation roadmap.

## 20-Round Schedule

1. Codex product map: CLI, app, cloud tasks, App Server, and workflow boundaries.
2. Codex agent loop: planning, tool use, observation, editing, and verification.
3. Harness Engineering: how OpenAI frames agent-first development environments.
4. `AGENTS.md` and skills: repo-local instructions, reusable capabilities, and context design.
5. Worktrees and parallelism: isolated implementation, conflict handling, and branch hygiene.
6. Codex App Server: headless orchestration, event streams, approvals, and JSON-RPC control.
7. Symphony architecture: issue tracker to isolated agent run to PR.
8. Symphony critique: task quality, permissions, verification, review, and organizational limits.
9. AI-native engineering teams: role shifts, planning flows, ownership, and human gates.
10. Evals and quality gates: converting engineering quality into measurable pass/fail criteria.
11. Review agents: correctness review, security review, architecture review, and maintainability review.
12. Debugging agents: reproduction, logs, CI repair, regression tests, and root-cause analysis.
13. Browser verification: local UI validation, screenshots, interaction replay, and runtime evidence.
14. MCP and tool integration: GitHub, Linear, Slack, docs, browser, database, and internal systems.
15. Agents SDK: handoffs, guardrails, traces, tools, memory, and production agent patterns.
16. Responses API computer use: shell, containers, filesystems, network policy, and long-running tasks.
17. Enterprise AI coworkers: shared context, identity, permissions, governance, and feedback learning.
18. Competitor comparison: Claude Code, Cursor, Devin, Amp, Factory, Cognition, and similar tools.
19. Failure-mode library: context pollution, bad edits, hallucinated APIs, overbroad permissions, and weak verification.
20. SOTA synthesis: AI-native development operating system, adoption path, and implementation playbook.

## Per-Round Output Format

```md
# Round N: <topic>

## Research Question
- What must this round answer?

## Core Findings
- Finding 1
- Finding 2
- Finding 3

## Evidence
- Source:
- Source type: official / primary / secondary / inferred
- Confidence:

## Critical Evaluation
- Strengths:
- Gaps:
- Risks:
- Applicability:

## Reusable Pattern
- Pattern:
- Anti-pattern:
- Practical action:

## Next-Round Questions
- What should the next hour investigate?
```

## Final Report Format

```md
# AI-Native Development SOTA Report

## 1. Executive Summary
## 2. Codex Development Process
## 3. Symphony Critical Analysis
## 4. Adjacent OpenAI Systems
## 5. Key Development Patterns
## 6. Failure Modes And Governance
## 7. SOTA Methodology
## 8. Team Adoption Roadmap
## 9. Skills, Tools, And Documentation Structure
## 10. References
```

## Operating Rules

- Separate facts, sources, judgments, inferences, and recommendations.
- Prefer official OpenAI sources for Codex-specific claims.
- Use primary sources where possible for competitor and community analysis.
- Capture evidence every hour; do not defer source tracking to the final report.
- Run synthesis checkpoints after rounds 5, 10, 15, and 20.
- Treat every failure or ambiguity as a signal to improve the research harness.
