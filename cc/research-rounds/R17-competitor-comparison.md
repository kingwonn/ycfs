# R17 - 竞品对比

Date: 2026-04-30
Timebox: accelerated run using the 60-minute protocol
Question: Codex、Cursor、Copilot、Devin、Gemini CLI 的差异是什么？
Working hypothesis: Competitors differ by surface: terminal/repo harness, IDE agent, GitHub-native agent, autonomous remote worker, and open-source CLI.

## Sources Checked

| Source | Type | URL | Evidence Level | Notes |
|---|---|---|---|---|
| OpenAI Codex docs/search | Official docs/search | https://developers.openai.com/codex | S | Codex agent surface |
| GitHub Copilot coding agent docs | Official docs | https://docs.github.com/en/copilot/concepts/coding-agent | S | GitHub-native agent |
| Cursor docs | Official docs | https://docs.cursor.com | S | IDE agent/rules/background agents |
| Gemini CLI repo/blog | Official repo/blog | https://github.com/google-gemini/gemini-cli | S | Open-source terminal agent |
| Devin docs/site | Official docs/site | https://docs.cognition.ai | S | Autonomous software engineer positioning |

## Facts

- [Fact][Confidence: High] Competitor products emphasize different primary surfaces: IDE, GitHub PRs, terminal, cloud tasks, and autonomous workspaces.
- [Fact][Confidence: High] Rules/context/configuration appear across multiple products, not only Claude Code.
- [Fact][Confidence: Med] GitHub-native and IDE-native tools have distribution advantages inside existing developer habits.

## Inferences

- [Inference][Confidence: High] Claude Code's strongest differentiator is the combination of terminal harness, rich docs, enterprise controls, and Anthropic model behavior.
- [Inference][Confidence: High] Our playbook should be vendor-neutral: task intake, context, plan, execution, eval, PR, memory.
- [Inference][Confidence: Med] Tool choice should vary by workflow: IDE for local edit loops, terminal for harnessed tasks, GitHub agent for issue-to-PR, autonomous worker for bounded async tasks.

## Contradictions / Risks

- [Risk] Competitor feature sets change quickly; this comparison must be refreshed often.
- [Risk] Public docs do not reveal real-world reliability.

## Impact On Our Playbook

Keep: Claude Code as reference model for harness discipline.

Change: Avoid making SOP dependent on one vendor.

Add: Tool selection matrix by task type, risk level, context needs, and verification path.

Remove: “One agent for everything.”

## Next Questions

1. What final SOP should we adopt?
2. Which practices should not be copied?
3. What should we implement in the next 30 days?
