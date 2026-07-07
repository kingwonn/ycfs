# R20 - 汇总与决策

Date: 2026-04-30
Timebox: accelerated run using the 60-minute protocol
Question: 最终应该执行哪套组织工作法？
Working hypothesis: Adopt an AI-native engineering operating model centered on verifiable task loops, long-running harnesses, eval banks, PR review, incident response, and organizational memory.

## Sources Checked

| Source | Type | URL | Evidence Level | Notes |
|---|---|---|---|---|
| R01-R19 cards | Internal synthesis | `cc/research-rounds/` | A | Full run |
| Official docs/product/engineering | Primary sources | Multiple | S | Product/method facts |
| NPM/HN/GitHub/arXiv | External sources | Multiple | A/B | Independent signal |

## Facts

- [Fact][Confidence: High] The research run completed the planned 20 topics.
- [Fact][Confidence: High] The strongest evidence supports a workflow system rather than a single-tool practice.
- [Fact][Confidence: High] The required outputs are clear: operating model, task template, PR checklist, eval bank, long-running harness, quality incident template, product method.

## Inferences

- [Inference][Confidence: High] Our team should implement a minimum viable AI-native operating system before scaling agent usage.
- [Inference][Confidence: High] The most important near-term constraint is verification discipline.
- [Inference][Confidence: Med] Once templates are used for one week, we should run a retrospective and convert repeated issues into skills/hooks/evals.

## Contradictions / Risks

- [Risk] The SOP may feel heavy for small tasks; use risk tiers to avoid process drag.
- [Risk] Without team adoption, files alone will not change behavior.

## Impact On Our Playbook

Keep: Evidence-led, verification-led agent work.

Change: Make “done” mean PR + verification + lesson capture.

Add: 30-day rollout with weekly review.

Remove: Untracked, unreviewed, unverifiable agent changes.

## Final Decision

Adopt the following operating model immediately:

1. Every task starts with a one-page task card.
2. Every non-trivial task requires plan review before editing.
3. Every implementation must define verification before code changes.
4. Every long-running task uses a harness with state files.
5. Every PR includes AI-work disclosure, validation, risks, and follow-ups.
6. Every behavior regression gets a postmortem and eval case.
7. Every repeated success or failure becomes organization memory.

## Search Summary For 20-Round Run

- OpenCLI registry/help: checked `hackernews`, `arxiv`, `gemini`, `google`, `reddit`, `youtube` availability.
- OpenCLI Hacker News: query `Claude Code`, 1 call.
- OpenCLI arXiv: query `Claude Code agentic coding`, 1 call.
- NPM registry: package `@anthropic-ai/claude-code`, 1 call.
- GitHub search: query `Claude Code Anthropic`, 1 call.
- Web search/open: official Claude/Anthropic docs, engineering posts, product pages, competitor docs, arXiv pages.
- Skipped OpenCLI Gemini/Google/Reddit/YouTube actual searches because Browser Bridge-dependent paths were unavailable or unnecessary after web fallback.
