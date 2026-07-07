# 参考轮子:OpenHands(端到端)与 mini-swe-agent(极简可读)

> YCFS「参考」步骤:说不清想要什么时,最好的规范是源代码。本文档记录 2026-07-07 核实过的事实
> (WebFetch 逐项核对仓库页,非记忆),作为 A1 执行脊柱与前端工作台的参考语义来源。

## 主参考:OpenHands — 最接近我们要造的东西的完整轮子

**是什么**:开源「AI 软件工程师」完整应用。**79.8k★,MIT,活跃**(107 releases,2026 年仍高频提交)。

**为什么是它**:它就是一个已经造好的「BS 架构 + 沙箱执行 + 事件溯源 + 可回放」的 coding agent 系统——正是我们 7 组件里 #1(前端)、#2(执行核心)、#5(沙箱)、部分 #6(轨迹)的现成组合:

| OpenHands 里的东西 | 对应我们的组件 | 能直接抄什么 |
|---|---|---|
| `frontend/` + `openhands-ui/`(React/TS) | #1 前端工作台 | 会话工作台布局、流式输出、diff 视图、等待人确认的交互形态 |
| `openhands/` Python 后端(Agent Server REST + 事件/调度) | #2 Agent 后端 | Action/Observation 事件流、会话管理、REST/WS 服务形态 |
| `containers/` Docker runtime | #5 固件 CI 沙箱 | 沙箱隔离执行的工程化做法(我们换成装 arm-none-eabi-gcc 的镜像) |
| trajectory 记录与回放 | #6 可观测审计 | 事件溯源持久化格式、回放语义 |

**10 分钟上手感受它**(本地 Docker 一条命令):

```bash
export PROJECTS_PATH="$HOME/projects"; mkdir -p "$PROJECTS_PATH" "$HOME/.openhands"
docker run -it --rm -p 8000:8000 \
  -v "$HOME/.openhands:/home/openhands/.openhands" \
  -v "$PROJECTS_PATH:/projects" \
  ghcr.io/openhands/agent-canvas:1.0.0-rc.11
# 浏览器开 http://localhost:8000,配一个 LLM API key 即可用
```

**嵌入我们系统的方式不是 fork 整个应用,而是用它的 SDK**(A1 卡既定路线):
`OpenHands/software-agent-sdk` — MIT,v1.32.0(2026-07),核心抽象 `Agent / Conversation / Tool / Workspace`,
自带 `openhands-agent-server` 子包(REST + WebSocket,天然契合 BS):

```python
# pip install openhands-sdk
from openhands.sdk import LLM, Agent, Conversation, Tool
from openhands.tools.terminal import TerminalTool

agent = Agent(llm=llm, tools=[Tool(name=TerminalTool.name)])
conversation = Conversation(agent=agent, workspace=cwd)
conversation.send_message("Write facts into FACTS.txt")
```

## 副参考:mini-swe-agent — 100 行读懂 agent 循环

**5.6k★,MIT,活跃**(v2.4.5,2026-07)。agent 类核心 ~100 行 Python:**线性消息历史、只用 bash、
每步 `subprocess.run` 独立执行**,却在 SWE-bench verified 拿 >74%。
读它的价值:一小时内看穿「agent 循环到底有多简单」,以及**线性轨迹天然易审计**——这正是我们
「可追索」的最小实现参照。快速试用:`pip install uv && uvx mini-swe-agent`。

## 这个轮子缺什么(= 我们真正要造的部分)

对照走一遍 OpenHands 就会看到,它**没有也不打算有**:

1. **验证器裁决**:它的"完成"由 agent 自己宣布;没有 gate N 腿全绿、门槛只紧不松的棘轮。
2. **被测不能自证**:没有真值出生证、没有异模裁判、没有「gate 绿 ≠ verified」的状态机结构边。
3. **三门禁**:有基本的用户确认,但没有方向/数据/对外的具名签字机制,更没有「真机签字是 verified 唯一路径」。
4. **固件域一切**:交叉编译门禁、60730 自检表、规格书溯源(L1)、Renode 仿真——通用 coding agent 零覆盖。
5. **逐值溯源**:输出不带「这个数字来自规格书第 X 页」的确定性证据链。

**结论(与 ARCHITECTURE.md 一致)**:轮子负责「AI 怎么干活 + 人怎么看它干活」,我们只造薄治理层
(#3 验证门禁引擎、#4 知识库溯源、#7 人核接口)+ 固件 CI 内容物。这是 adopt 一个 79.8k★ 活跃项目
的 SDK,而不是自己从零写 agent 循环的全部理由。

---
*事实核实时间 2026-07-07;数字(star/版本)会漂移,采用前按 L1 纪律重新核对仓库页。*
