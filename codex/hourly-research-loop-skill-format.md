# Hourly Research Loop Skill Format

下面是可转成 Codex skill 的格式，用于每小时执行一轮 research。它不是全局安装的 skill，而是本仓库内的可复用协议。

````markdown
---
name: hourly-research-loop
description: Use when running one focused 60-minute research round that must produce cited evidence, confidence labels, and a next-step handoff.
---

# Hourly Research Loop

## Inputs

- Research round number
- Research question
- Working hypothesis
- Required output path
- Source priority
- Search budget

## Source Priority

1. Official primary sources
2. First-hand interviews, changelogs, docs, release notes
3. Public repositories, issues, package registries
4. Academic papers and benchmark reports
5. Community discussions
6. Media summaries and personal blogs

## Workflow

1. Restate the question in one sentence.
2. Define success criteria for this hour.
3. Search sources within the budget.
4. Capture citations immediately.
5. Separate `Fact`, `Inference`, `Hypothesis`, and `Risk`.
6. Score confidence for each key claim.
7. Write a research card.
8. Update the source ledger.
9. Write 1-3 next questions for the next hour.

## Output Schema

Use this exact structure:

```md
# RXX - <Title>

Date:
Timebox:
Question:
Working hypothesis:

## Sources Checked

| Source | Type | URL | Used? | Notes |
|---|---|---|---|---|

## Facts

- [Fact][Confidence: High/Med/Low] ...

## Inferences

- [Inference][Confidence: High/Med/Low] ...

## Risks / Contradictions

- [Risk] ...

## Impact On Our Playbook

- Keep:
- Change:
- Add:
- Remove:

## Next Questions

1.
2.
3.
```

## Stop Conditions

- Stop when 60 minutes ends.
- Stop early if the question is answered with high confidence and write the surplus questions.
- Do not hide uncertainty.
- Do not merge facts and inferences.
````
