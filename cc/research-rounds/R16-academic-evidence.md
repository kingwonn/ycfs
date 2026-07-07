# R16 - 学术研究

Date: 2026-04-30
Timebox: accelerated run using the 60-minute protocol
Question: 论文如何评价 agentic coding 的缺陷和真实效果？
Working hypothesis: Academic evidence supports both promise and governance risk: many tasks work, but configuration, bugs, attribution, and evaluation remain immature.

## Sources Checked

| Source | Type | URL | Evidence Level | Notes |
|---|---|---|---|---|
| Dive into Claude Code | arXiv | https://arxiv.org/abs/2604.14228 | A | Design space analysis |
| Decoding configuration | arXiv | https://arxiv.org/abs/2511.09268 | A | Claude Code project config |
| Engineering Pitfalls in AI Coding Tools | arXiv | https://arxiv.org/abs/2603.20847 | A | Bug taxonomy |
| On the Use of Agentic Coding | arXiv | https://arxiv.org/abs/2509.14745 | A | PR-level empirical study |
| Fingerprinting AI Coding Agents | arXiv | https://arxiv.org/abs/2601.17406 | A | Attribution/governance |

## Facts

- [Fact][Confidence: High] Recent arXiv results include direct Claude Code design/configuration studies and broader AI coding tool empirical work.
- [Fact][Confidence: Med] Papers report configuration practices, bug categories, PR outcomes, and agent fingerprinting risks.
- [Fact][Confidence: High] Academic work treats agentic coding as a system-level phenomenon, not only model output quality.

## Inferences

- [Inference][Confidence: High] Our operating model should include configuration versioning, bug taxonomy, and AI contribution governance.
- [Inference][Confidence: Med] The academic field is moving quickly, so papers should inform eval questions but not freeze practice.
- [Inference][Confidence: Med] AI-generated PRs can be productive, but human review remains necessary for quality and responsibility.

## Contradictions / Risks

- [Risk] Preprints may change and can lag fast product evolution.
- [Risk] Results may not generalize across teams, languages, and task types.

## Impact On Our Playbook

Keep: Use papers for risk taxonomy and eval design.

Change: Add governance and attribution questions to PR review.

Add: AI coding bug taxonomy: API/integration/config, terminal/command failure, incorrect behavior, overengineering, unsafe permission.

Remove: Treating merged PR rate as sufficient success metric.

## Next Questions

1. How does Claude Code differ from competitor agent tools?
2. Which competitor practices should we borrow?
3. Which benchmarks map to our actual tasks?
