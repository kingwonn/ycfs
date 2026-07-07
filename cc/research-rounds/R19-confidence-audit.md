# R19 - 置信度审计

Date: 2026-04-30
Timebox: accelerated run using the 60-minute protocol
Question: 哪些判断证据强，哪些只是推断？
Working hypothesis: The core workflow claims are high-confidence; internal org structure and private metrics are low-confidence.

## Sources Checked

| Source | Type | URL | Evidence Level | Notes |
|---|---|---|---|---|
| R01-R18 cards | Internal synthesis | `cc/research-rounds/` | A | Audit corpus |
| Official docs/engineering/blog | Primary sources | https://code.claude.com/docs/en/overview | S | Product/method facts |
| NPM metadata | Registry | https://www.npmjs.com/package/@anthropic-ai/claude-code | A | Release cadence |
| HN/GitHub/arXiv | External sources | Multiple | A/B | Community and academic signals |

## Facts

- [Fact][Confidence: High] Product surface, docs, changelog, engineering posts, enterprise pages, and NPM metadata are public and directly verifiable.
- [Fact][Confidence: High] Community and academic sources support the need for eval, governance, bug taxonomy, and community canaries.
- [Fact][Confidence: High] Public sources do not expose exact Claude Code internal team size, private roadmap process, or eval thresholds.

## Inferences

- [Inference][Confidence: High] High-confidence claims: workflow completion loop, high release cadence, need for eval, need for long-running harness, need for permissions/governance.
- [Inference][Confidence: Med] Medium-confidence claims: small senior early team, dogfood shaping roadmap, community canary influencing process.
- [Inference][Confidence: Low] Low-confidence claims: exact org chart, exact team cadence, exact customer productivity deltas.

## Contradictions / Risks

- [Risk] Competitor landscape and product features change weekly.
- [Risk] Some sources are curated marketing or user anecdotes.
- [Risk] Our SOP may need adjustment after real internal trials.

## Impact On Our Playbook

Keep: Only high-confidence claims become hard rules.

Change: Medium-confidence claims become experiments.

Add: Confidence column to all operating model decisions.

Remove: Unverified claims about Anthropic internals.

## Next Questions

1. What final decision should we make now?
2. What should the first 30 days implement?
3. What should stay open for future research?
