# 执行脊柱六方对比(2026-07-07,六路并行调研,事实均经联网核实)

> 触发:立法者对 OpenHands 路线「感觉不好」,点名评估 OpenAI / Anthropic SDK / Vercel / Cloudflare / opencode / Hermes+AWS。
> 这是一次「前提变化触发重审」:D-003(云可用、SOTA 优先)立法后,先前因气隙不确定而压低的选项需要重估。
> 评分尺子 = **嵌入式 SWE agent**:装 arm-none-eabi-gcc/Renode 的沙箱、治理钩子(denylist 硬停/HITL)、轨迹审计、锁定风险。

## 对比矩阵(1–5,锁定分高=风险低)

| 候选 | 执行核心 | 沙箱 | 治理钩子 | 审计 | 锁定 | 一句话 |
|---|---|---|---|---|---|---|
| **opencode**(183k★,MIT) | **5** | 3(无 OS 沙箱,靠外部 Docker) | 4(权限到 bash 通配符粒度;插件可强制 deny) | 3.5(本地 JSON 可回放,防篡改需自建) | **4.5** | 真 client/server(`serve`+OpenAPI+SSE+TS SDK),模型无关 75+ provider,嵌自建 BS 后端最顺 |
| **Claude Agent SDK** | **5** | 4(跑在你的容器里) | **5**(PreToolUse deny 覆盖全工具) | 4(JSONL 转录+事件流) | 3(仅 Claude 系;可走 Bedrock/Vertex;非纯 OSS) | 最省自研量的 coding 引擎,治理钩子最强;Notion/Sentry/Mozilla 生产案例 |
| **OpenAI Codex**(CLI Apache-2.0) | 4.5 | 4.5(内建 Seatbelt/Landlock) | 3(hooks 仅拦 Bash,patch/MCP 拦不住) | 4(JSONL 事件流+resume) | 3(深绑 OpenAI 模型) | Cisco 用它修大型 C/C++ 提速 10-15×(与嵌入式 C 同构);钩子覆盖面是硬伤 |
| **AWS Strands + AgentCore** | 4(Strands 无内建 coding 工具,要自建) | 3(Code Interpreter 装不了交叉工具链;Runtime 自定义 arm64 容器可绕但要 aarch64 工具链) | **5**(hooks+interrupt 原生 HITL) | 4(OTel+CloudTrail) | 3(Strands 可移植,AgentCore 绑 AWS) | 独有嵌入式生态加成:FreeRTOS + IoT Device Tester 认证测试套件可改造为验证器素材;Kiro 的 spec-driven 流程值得抄理念 |
| **Cloudflare Agents+Workflows** | 5(编排:DO 状态+`waitForEvent` 人审挂起) | **2.5**(Containers 4vCPU/12GiB/无持久盘,Renode 级 CI 偏紧) | 4 | 4 | 2(DO/Workflows 全专有) | 编排大脑一流,但重型原生工具链 CI 是软肋;VibeSDK(MIT)可抄架构 |
| **Vercel**(AI SDK 7+Elements+Sandbox) | 3(AI SDK Agent 抽象偏轻) | 4(Sandbox microVM 可 sudo 装 ARM 工具链;但仅 Vercel 云+VM 短命) | 4(`needsApproval` HITL) | 3.5(`@ai-sdk/otel`) | **4.5**(AI SDK/Elements 零锁定;仅 Sandbox 绑云) | **前端底座无争议第一**:AI Elements 的 InlineCitation 正好承载规格书溯源;coding-agent-template(Apache-2.0)是最可抄的整机骨架 |
| ~~Hermes~~ | — | — | — | — | — | 消歧后无强相关(Nous 个人助理 agent,非 SWE 流水线),排除 |

## 关键事实(影响架构的)

1. **opencode 的 HITL 是天然闭环**:SSE `permission.asked` 事件 → 人在前端审 → `POST /session/:id/permissions/:permissionID` 应答。这就是 YCFS 门禁在执行层的现成接口。
2. **vercel-labs/coding-agent-template(Apache-2.0)已经把 opencode 跑进沙箱 + Next.js 工作台**(任务侧栏/实时日志/diff 审查/自动分支)——「opencode+沙箱」不是假设,是有开源整机先例的组合。
3. **我们自己的 Docker 沙箱已被 F1 验证**(arm-none-eabi-gcc 13.2.1 容器内构建绿):执行器无沙箱不是缺陷,反而干净——隔离归我们的沙箱层,权限归执行器,治理归 YCFS 层,职责分离。
4. **审计短板全员存在**:没有任何一家提供防篡改审计(WORM);E1 卡(OTel→append-only sink)无论选谁都要做——再次印证治理层是自建 IP。
5. **AWS 的差异化不在脊柱在素材**:IoT Device Tester for FreeRTOS 的认证测试组可改造进 L-real/认证验证器;Kiro 的 requirements→design→tasks 流程是「RFP→方案→编码」产品化的最好参照(抄流程,不买闭源产品)。

## 提案 D-005(待立法者签字,见 PENDING_HUMAN)

**三层组合,执行器可插拔:**

- **执行脊柱 = opencode server(主)+ 可插拔适配层**:通过 OpenAPI/SDK 嵌入我们 BS 后端;模型接 SOTA(D-003);denylist 用 opencode 权限 deny + 插件 `permission.ask` 强制拒 + 我们沙箱的网络出口白名单双保险。适配层保留换装 Claude Agent SDK(治理钩子最强)或 Codex 的能力——coding-agent-template 证明多执行器共存可行。
- **沙箱 = 自建 Docker(F1 已验证)为基线**,接口做薄;Vercel Sandbox/AgentCore Runtime 作可选托管跑道。
- **前端 = Vercel AI SDK 7 + AI Elements(InlineCitation 做溯源)+ 抄 coding-agent-template 骨架**。
- **不变**:YCFS 治理层(验证器裁决/棘轮/出生证/状态机结构边)自建;OpenHands 降级为参考(其事件溯源设计仍值得抄);Kiro spec 流程与 AWS IDT 测试套件进素材库。

**为什么 opencode 为主而非 Claude Agent SDK**:MIT 全开源可 fork(零锁定,183k★ 社区)、模型无关(SOTA 永远可接最新)、真 C/S 天然契合 BS;其钩子弱于 Claude 线的部分,恰好由我们本来就要自建的治理层补齐。**证伪条件**:若实测 opencode 的 permission/plugin 钩子存在绕过路径(红队卡验证),或其 API 稳定性不足以承载生产,则切换适配层到 Claude Agent SDK;回退成本=低(适配层隔离)。
