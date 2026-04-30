# Claude Code Operating Model - Final Synthesis

Date: 2026-04-30
Scope: 20-round accelerated research run based on public sources, prior reports, registries, community signals, and academic sources.
Input rounds: R01-R20

## Executive Conclusion

Claude Code 的可复制核心不是“某个 CLI 工具”，而是一套 AI-native 软件工作操作系统。它把真实任务转成可验证的 agent loop：上下文、计划、执行、验证、PR、复盘和组织记忆。我们应该复制这套系统，而不是复制表层功能或个别 prompt。

## What We Know With High Confidence

| Claim | Evidence | Source Level | Confidence |
|---|---|---|---|
| Claude Code 是 agentic coding harness，而不只是 autocomplete | Product page, docs, best practices | S | High |
| 高频发布是真实存在的 | Changelog, NPM version timestamps | S/A | High |
| 质量回归需要 eval、canary、rollback 和 postmortem | April 23 postmortem | S | High |
| 长任务需要外部状态和 harness | Anthropic long-running agents posts | S | High |
| Team/Enterprise adoption 需要权限、身份、日志、analytics 和策略 | Enterprise/security/docs | S | High |
| 社区负反馈是早期质量信号 | HN, GitHub issue, benchmark trackers | A/B | Med-High |
| 精确内部组织结构不可公开证实 | Absence across public sources | S/A | High |

## What Changed From Our Initial Belief

| Initial belief | Updated view | Why |
|---|---|---|
| 关键是速度和 dogfood | 关键是速度 + eval + rollback + governance | 质量 postmortem 和 enterprise docs 改变权重 |
| 并行 agent 是最高效打法 | 并行只适合可测试、可隔离、高价值任务 | C compiler case shows power and cost |
| CLAUDE.md 足够沉淀组织记忆 | 需要 CLAUDE.md + skills + context repo + evals + incident records | Docs and ecosystem show layered memory |
| 社区反馈只是舆情 | 社区反馈是 canary | HN/GitHub issue caught real degradation concerns |

## Claude Code System Model

### Product Surface

Claude Code 的核心入口是开发者已有环境：terminal、repo、Git、IDE、CI、Slack 和 Claude app surfaces。产品价值来自减少上下文切换，并让 agent 能直接进入真实工具链。

### Agent Harness

Agent harness 包括上下文收集、工具权限、计划、执行、验证和状态持久化。长任务必须有 `feature_list.json`、`progress.md`、`init.sh`、eval scripts 和 commit checkpoints。

### Eval And Verification

每个任务都必须在开始前定义验证。Eval bank 至少覆盖任务成功、测试结果、diff 质量、工具调用、成本、耗时、失败类型和人工 review 标签。

### Release And Rollback

Prompt、model、config、tool、permission policy 的变更都应当像代码一样走 review、ablation、soak、canary 和 rollback。

### Community Feedback

HN、GitHub issues、benchmark trackers、community guides 是 canary 系统。所有高质量负反馈都应该转成 eval case 或 risk radar 条目。

### Enterprise Governance

团队采用需要身份、权限、日志、analytics、成本控制、managed settings、SSO/SCIM、audit 和安全策略。治理不是减速器，而是让大规模使用更快、更安全。

### Team Operating Model

人类角色上移到目标定义、计划审查、风险判断、验收、PR review、事故复盘和规则沉淀。Agent 负责调查、修改、验证、生成 PR 和维护上下文资产。

## Playbook We Should Adopt

### 1. Demand Intake

所有需求使用 `codex/agent-task-template.md`。必须写用户目标、当前痛点、成功样子、验证方式、风险等级、自动化许可和不做范围。

### 2. Research And Planning

复杂任务先跑 research card，再写 plan。计划必须列文件边界、验证命令、风险和回滚路径。

### 3. Agent Execution

小任务单 agent；长任务用 harness；并行任务必须文件边界互不冲突，并有集成人。

### 4. Verification

没有验证，不算完成。验证可以是 tests、lint、build、E2E、browser screenshot、data check、manual checklist，但必须明确。

### 5. PR And Review

每个 PR 必须有 summary、validation、risk、AI contribution、follow-ups。Reviewer 审行为结果和 diff，不只审文字。

### 6. Incident / Quality Response

任何 agent 行为退化都走 postmortem：触发信号、影响面、复现方式、根因、修复、eval case、rollback、预防。

### 7. Organization Memory

重复出现的成功或失败进入 CLAUDE.md、skills、commands、hooks、context docs 或 eval bank。第二次出现同类错误就是系统问题。

## What We Should Not Copy

| Practice | Reason |
|---|---|
| 盲目高频发布 | 没有 eval/rollback 会扩大回归风险 |
| 无边界并行 agent | 容易冲突、烧成本、难集成 |
| 只靠社区模板 | 可能过期、不安全、与本仓库不匹配 |
| 把负反馈当噪音 | 真实 workflow degradation 往往先被 power users 发现 |
| 对小任务强制重流程 | 会造成流程疲劳，应按风险分层 |

## 30-Day Implementation Roadmap

| Week | Outcome | Files / Systems | Verification |
|---|---|---|---|
| 1 | 使用任务模板和 PR checklist | `agent-task-template`, `pr-checklist` | 5 个真实任务跑通 |
| 2 | 建立 eval bank v1 | `eval-bank-template`, 10 个 eval tasks | 每次 agent 变更跑一次 |
| 3 | 长任务 harness 试点 | `long-running-agent-harness` | 1 个多日任务不断片 |
| 4 | 质量与治理复盘 | incident template, weekly ops review | 输出规则更新和下一批 skills |

## Open Questions

1. Anthropic 内部真实组织结构和 eval thresholds 不公开。
2. 企业客户真实净效率指标仍需客户案例或访谈验证。
3. 竞品特性变化快，需要每两周刷新一次比较。

## Source Appendix

| Source | URL | Used in rounds |
|---|---|---|
| Claude Code docs | https://code.claude.com/docs/en/overview | R01-R10 |
| Claude Code changelog | https://code.claude.com/docs/en/changelog | R03 |
| April 23 postmortem | https://www.anthropic.com/engineering/april-23-postmortem | R07-R08 |
| Long-running agents | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | R06 |
| Harness design | https://www.anthropic.com/engineering/harness-design-long-running-apps | R06 |
| Agent evals | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | R07 |
| Infrastructure noise | https://www.anthropic.com/engineering/infrastructure-noise | R07 |
| Auto mode | https://www.anthropic.com/engineering/claude-code-auto-mode | R09 |
| Enterprise | https://claude.com/product/claude-code/enterprise | R10 |
| HN search | https://news.ycombinator.com | R13-R15 |
| NPM package | https://www.npmjs.com/package/@anthropic-ai/claude-code | R03 |
| arXiv Claude Code studies | https://arxiv.org/abs/2604.14228 | R16 |
