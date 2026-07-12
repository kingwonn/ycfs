# opencode 平台设计与资源清单(R19,回答「如何设计和使用,需要什么资源」)

> 事实全部经核实(opencode.ai 被本环境代理拦截,改从同源仓库 anomalyco/opencode 的文档源码核实,
> 版本 v1.17.18,MIT)。本文档 = A1 卡的设计输入;**Q7(D-005)签字后按此实施**。

## 一、总体设计(在我们架构里的位置)

```
浏览器(Next.js + Vercel AI SDK/AI Elements)
    │  骨架直接抄 vercel-labs/coding-agent-template(原生支持 opencode)
    ▼
我们的 BS 后端(多租户 · YCFS 治理层 · 审计)          ←← 自建薄层(核心 IP)
    │  每任务/租户一个 opencode server 实例(无状态容器,可随时重启)
    ▼
opencode server(Bun 单文件二进制,--port 4096)
    │  REST(OpenAPI 3.1 @ /doc)+ SSE 事件流
    │  插件钩子 → 调我们的 data_gate/门禁内核裁决
    ▼
自建 Docker 固件沙箱(F1 已验证:arm-none-eabi-gcc 13.2.1 + cmake + cppcheck)
```

**关键设计决定**:opencode **无多用户概念**——多租户由我们 BS 后端包(每租户/每任务独立 server 实例);
它有内存泄漏与存储膨胀的未根治 issue(#11399/#16777,长跑可达数 GB)——**按「可随时重启的无状态容器」设计**,
会话真相落我们的审计存储而非依赖其本地存储。

## 二、安装与启动

```bash
# 任选:官方脚本 / npm / Docker 镜像
curl -fsSL https://opencode.ai/install | bash        # 或 npm i -g opencode-ai
# 纯 server(无 TUI),默认只绑本机:
opencode serve --port 4096 --hostname 127.0.0.1
# OpenAPI 规范: GET /doc
```
发行物是 Bun 编译的单文件二进制,**目标机无需预装 Node/Bun**;官方 Docker 镜像 `ghcr.io/anomalyco/opencode`。

## 三、配置(opencode.json,项目级覆盖全局)

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-5",          // SOTA 按 D-003;key 走 ANTHROPIC_API_KEY 环境变量
  "permission": {                                   // ⚠ 默认全 allow——上线前必须显式收紧
    "bash": { "git *": "allow", "cmake *": "allow", "rm *": "deny", "*": "ask" },
    "edit": "allow", "webfetch": "ask"
  },
  "plugin": []                                      // 治理插件见 §五
}
```
server 自带认证仅 HTTP Basic(`OPENCODE_SERVER_PASSWORD`)——**生产必须反代 TLS + 我们自己的鉴权**。

## 四、SDK 集成(方法名已核实,适配层就写这些)

```ts
import { createOpencodeClient } from "@opencode-ai/sdk"
const client = createOpencodeClient({ baseUrl: "http://localhost:4096" })

const s = await client.session.create({ body: { title: "G4-foc-param-pack" } })
await client.session.prompt({ path: { id: s.id }, body: { parts: [{ type: "text", text: task }] } })
// 异步任务: POST /session/:id/prompt_async
for await (const e of (await client.event.subscribe()).stream) { /* SSE:审计落库+前端转发 */ }
// 人审应答(PENDING_HUMAN UI 的提交动作):
await client.postSessionByIdPermissionsByPermissionId({ path: { id, permissionID }, body: { response: "always"|"once"|"reject" } })
```
事件流即我们「可追索」的原料:适配层把每个事件**append-only 落审计 sink**(E1),不依赖 opencode 本地存储。

## 五、治理接线(H1 数据门禁的执行点——签名已从源码核实)

插件放 `.opencode/plugins/`,启动自动加载:

```ts
import type { Plugin } from "@opencode-ai/plugin"
export const YcfsGate: Plugin = async ({ project, client }) => ({
  // 钩子1:工具执行前——throw 即硬阻断
  "tool.execute.before": async (input, output) => {
    const verdict = await ycfsDataGate(input.tool, output.args)   // 调 governance/data_gate 内核
    if (!verdict.allow) throw new Error(`YCFS 数据门禁硬停: ${verdict.reason}`)
  },
  // 钩子2:权限询问——置 deny 即拒;needs_named_approval 时保持 "ask" 走人审闭环
  "permission.ask": async (perm, output) => {
    const v = await ycfsDataGate(perm.type, perm)
    if (!v.allow && !v.needs_named_approval) output.status = "deny"
  },
})
```
双保险:config 的 permission 块(静态收紧)+ 插件钩子(动态裁决,概括授权无效/approval 消耗式由内核保证)。

## 六、资源清单(回答「需要什么资源」)

| 项 | 结论 |
|---|---|
| **GPU** | **不需要**——推理全走云 API(D-003) |
| 服务器 | **起步 4C8G VPS/容器主机**:opencode server(启动数百 MB)+ Next.js 前端 + Postgres/SQLite + 固件 CI 容器;编译并发大再升 8C16G |
| API 预算 | 官方价:Sonnet $3/$15、Opus $5/$25 每百万 token(缓存读≈0.1×);社区量级:bug 修复 ≈$0.5–0.9/次,feature 级 ≈$2.3–3.8/次,企业均值 ~$13/人/活跃日 → **轻用 $20–80/月,重用 $150–300/人/月** |
| 存储 | 审计 sink(Postgres/对象存储)为真相源;opencode 本地存储当缓存,容器重启即弃 |
| **人力** | TS 全栈 1 人 × **1–3 人周**(以 coding-agent-template 为骨架:替换 Vercel Sandbox→自建 Docker、接 opencode server、挂 YCFS 治理插件) |
| 密钥 | ANTHROPIC_API_KEY(主)+ 备选 provider key;经我们后端注入,不进前端 |

## 七、风险与对策(核实过的坑)

1. **权限默认全 allow** → 上线前 permission 块写死 + 插件钩子双保险(§五);
2. server 仅 Basic Auth、明文 HTTP → 反代 TLS + 自建鉴权,server 永远只绑 127.0.0.1;
3. 内存泄漏/存储膨胀未根治 → 无状态容器 + 内存上限 + 定期重启;真相在我们审计层;
4. 迭代极快(已迁 anomalyco 组织) → **适配层钉版本**(v1.17.x),升级走门禁;
5. 官方无 CPU/内存基准、无多租户方案 → 上述规格系社区 issue 推断,**A1 开工首周先 PoC 实测**(已列进 A1 验收的证伪条件)。
