# Claude Code 20 轮逐小时 Research 计划

目标：用 20 个一小时研究回合，把 Claude Code 团队、产品、研发、协作、发布、安全、社区反馈和可复用套路调查到可决策状态。

每轮固定节奏：

- 00-05 分钟：确认本轮问题、假设和输出物
- 05-15 分钟：列来源清单，优先官方/一手来源
- 15-40 分钟：检索、阅读、摘证据
- 40-50 分钟：归纳事实、推断、风险、遗漏
- 50-60 分钟：写本轮研究卡，更新总表和下一轮问题

每轮输出：

- 一张 `research card`
- 5-10 条证据，带来源链接
- 3 条确定事实
- 3 条合理推断
- 1-3 条仍不确定的问题
- 对“我们的可行套路”的修正建议

## 20 轮计划

| 轮次 | 主题 | 核心问题 | 首选来源 | 本轮产物 |
|---|---|---|---|---|
| 01 | 问题定义与证据标准 | 我们到底要学习 Claude Code 的什么？哪些结论算可证实？ | 现有两份报告、官方 docs | 研究问题树、证据等级表 |
| 02 | 官方产品面 | Claude Code 当前公开能力边界是什么？ | claude.com、code.claude.com | 功能地图 |
| 03 | 发布节奏 | 它迭代有多快？哪些阶段变化最大？ | changelog、NPM registry | 时间线和发布密度 |
| 04 | 文档体系 | 官方如何教育用户形成新工作法？ | docs、academy、best practices | 文档架构图 |
| 05 | 工程方法 | 官方 best practices 的共同模式是什么？ | best practices、workflows | 工程流程提炼 |
| 06 | 长任务 harness | 长时间 agent 任务如何不断片？ | long-running agents、harness design | 长任务执行协议 |
| 07 | Eval 体系 | 他们如何判断 agent 行为变好或变坏？ | eval engineering posts、benchmarks | eval bank 模型 |
| 08 | 质量事故 | 质量下降事件暴露了哪些门禁缺口？ | April 23 postmortem、HN、GitHub issue | 事故复盘模板 |
| 09 | 权限与安全 | 自动执行如何控制风险？ | auto mode、security、enterprise docs | 权限矩阵 |
| 10 | 企业化 | Team/Enterprise 如何支撑组织采用？ | enterprise、admin、analytics、OpenTelemetry | 企业治理清单 |
| 11 | 内部 dogfood | Anthropic 内部哪些团队怎么用？ | How Anthropic teams use Claude Code | 内部场景矩阵 |
| 12 | 核心成员与角色 | 公开可证实的关键人物和分工是什么？ | webinars、podcasts、官方活动页 | 人物/角色表 |
| 13 | 社区正反馈 | 用户真正觉得好在哪里？ | HN、Reddit、blogs、GitHub repos | 高价值用例库 |
| 14 | 社区负反馈 | 用户最敏感的退化、抱怨和替代方案是什么？ | HN、GitHub issues、benchmark trackers | 风险雷达 |
| 15 | 生态与插件 | 社区围绕 Claude Code 造了哪些工具？ | GitHub search、awesome lists、NPM | 生态地图 |
| 16 | 学术研究 | 论文如何评价 agentic coding 的缺陷和真实效果？ | arXiv、papers、benchmarks | 学术证据摘要 |
| 17 | 竞品对比 | Codex、Cursor、Copilot、Devin、Gemini CLI 的差异是什么？ | 官方 docs、公开评测、社区反馈 | 竞品定位表 |
| 18 | 可行套路设计 | 我们自己的 SOP 应该继承哪些，删除哪些？ | 前 17 轮结果 | SOP v1 草案 |
| 19 | 置信度审计 | 哪些判断证据强，哪些只是推断？ | 全部 research cards | 证据/置信度矩阵 |
| 20 | 汇总与决策 | 最终应该执行哪套组织工作法？ | 全部材料 | 总报告、路线图、模板清单 |

## 证据等级

- S 级：官方文档、官方工程文章、官方 changelog、一手访谈原文、可复现数据
- A 级：GitHub issue、HN 高质量讨论、NPM 元数据、公开 repo、论文
- B 级：媒体转述、播客摘要、个人博客实战经验
- C 级：社交媒体碎片、未给出处的二手总结

结论必须标注：

- `Fact`：来源直接支持
- `Inference`：多个事实推导
- `Hypothesis`：待验证假设
- `Risk`：可能推翻当前判断的证据

## 每 5 轮做一次阶段汇总

- 第 05 轮：产品与官方方法阶段汇总
- 第 10 轮：工程、eval、安全、企业化阶段汇总
- 第 15 轮：内部/社区/生态阶段汇总
- 第 20 轮：最终综合报告

每次阶段汇总都要回答：

1. 我们之前的判断哪里被强化？
2. 哪里被推翻或需要降级？
3. 哪些信息仍然缺？
4. 我们自己的套路要新增、删除或改写什么？

## 完成标准

20 轮结束后应得到：

- `cc/final-claude-code-operating-model.md`
- `codex/agent-task-template.md`
- `codex/pr-checklist.md`
- `codex/eval-bank-template.md`
- `codex/long-running-agent-harness.md`
- `codex/quality-incident-postmortem-template.md`
- `claw/product-method.md`
