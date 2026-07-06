# 开源复用短名单 · adopt / trial / assess / avoid

> 落实要求#7:尽量 follow 好用的开源方案,不到万不得已不重复造轮子。
> 分级:**adopt** 直接采用 · **trial** 试点/轻量起步 · **assess** 待决策解锁后评估 · **avoid** 不推荐(形状不符或 license 陷阱)。
> **唯一自建**的是「YCFS 治理层」(验证器裁决 / 被测不能自证 / 门槛只紧不松 / 真值出生证 / 裁判物理分离 / 门禁结构缺失边)——没有任何现成 agent/eval 框架内建这些不变量。

## ✅ ADOPT — 直接采用

| 方案 | 类别 | License | 说明 |
|---|---|---|---|
| [OpenHands Software Agent SDK (V1)](https://github.com/OpenHands/software-agent-sdk) | 执行脊柱 | MIT | MIT,事件溯源=YCFS『可追索/可审计』原生实现,自带 REST/WebSocket 契合 BS,MCP 工具系统可挂自建验证器/门禁;生产化程度最高。 |
| [SWE-ReX](https://github.com/SWE-agent/SWE-ReX) | 沙箱抽象 | MIT | MIT,agent 代码不变而底层在 Docker/云/本地间切换;把『在哪跑固件 CI』与 agent 逻辑解耦,未来换隔离档不动 agent。 |
| [Renode](https://github.com/renode/renode) | 固件仿真(L-sim/L3) | MIT | MIT,跑未修改二进制,ChromeOS EC 生产验证;确定性契合『门禁全绿』。硬边界:无电机/逆变器物理模型,plant model=地图,结果须打『map, not territory』标签,永不代替真机。 |
| [Ceedling + Unity + CMock](https://github.com/ThrowTheSwitch/Ceedling) | L2 单元测试腿 | MIT | MIT,嵌入式 C 无硬件单测标准栈,gcov 覆盖率;输出可被 v_min(断言下限+零失败)解析,天然防『测试静默变少』。 |
| [cppcheck (MISRA addon) + clang-tidy-misra](https://github.com/rettichschnidi/clang-tidy-misra) | L2 静态分析腿 | cppcheck GPL-3.0 / clang-tidy Apache-2.0 | 开源 MISRA 基座,无硬件易 CI。注意:开源覆盖率低于商业工具(Helix QAC/Polyspace/LDRA),MISRA 全绿≠功能安全,只保证 C 安全子集;认证审计需商业背书,门槛只紧不松、不足规则不得静默放宽。 |
| [厂商 IEC 60730 Class B 自检库(ST X-CUBE-STL / Renesas / Microchip / Infineon)](https://www.st.com/en/embedded-software/x-cube-stl.html) | L0 真值 / L2 自检腿 / 功能安全 | 厂商专有(随 MCU 免费) | 把『表格自测』锚到权威真值(标准条款+认证库,非被测自证)的现成素材,覆盖 CPU 寄存器/RAM-March/Flash-CRC/时钟/看门狗,分 POST/BIST。自研 March/CRC 需重走认证。MCU 厂商绑定。 |
| [STM32CubeMX-CMake 模板 + arm-none-eabi-gcc + Docker 镜像](https://github.com/windsorschmidt/stm32cubemx-cmake) | 交叉编译门禁(L0/L1) | 社区 MIT / GCC 工具链 GPL(产物不受限) | 『可编译通过』的 headless 落地路径,Docker/GitHub Actions 可复现构建,产 .elf/.map/size 作验收物。前提:目标 MCU 用开源 GCC;若厂商强制 IAR/Keil 专有编译器则此路受阻(待访谈头号问题)。 |
| [pdfplumber / Camelot](https://github.com/jsvine/pdfplumber) | L1 溯源解析核验 | MIT | 承载 L1 关键升级:把溯源核验从『LLM 自证有引用』改为确定性解析被引页/表、确认数值字面出现,封死伪造引用红队路径。必须覆盖中英双语防单语言盲区。 |
| [Doorstop / StrictDoc / OpenFastTrace](https://github.com/doorstop-dev/doorstop) | 需求追溯 RTM 骨架 | Doorstop LGPL-3.0 / OpenFastTrace GPL-3.0 | 需求即代码,YAML 版本化、可机器校验链路完整性,直接成为 L1/L4 骨架与要求#6 可追索抓手;不必自造 Markdown 合规矩阵。二选一避免重复。 |
| [OTel GenAI semconv + OpenLLMetry](https://github.com/traceloop/openllmetry) | 可观测仪表化标准 | Apache-2.0 | Apache-2.0,厂商中立线格式,避免锁定单一观测后端,可从 Langfuse 平滑切 Phoenix/自建。代价:多数属性仍 experimental,需固定版本。 |
| [assistant-ui / Vercel AI SDK + AI Elements](https://github.com/assistant-ui/assistant-ui) | 前端原语底座(BS) | MIT / Apache-2.0 | MIT/Apache-2.0,generative UI+inline human approval+streaming,可接任意自建 HTTP 后端;AI Elements 的 Source/inline-citation 组件正对应 L1 溯源呈现。UI 层不得把『gate 绿』展示为 verified,状态标签须结构性区分『待真机』。 |
| [shadcn/ui + Tremor + Monaco/react-diff-view](https://ui.shadcn.com/) | 自建专属视图积木 | MIT / Apache-2.0 | MIT/Apache-2.0,红绿墙=状态矩阵(Tremor/shadcn)、diff review=Monaco/react-diff-view、卡看板=shadcn;避免自绘控件。 |

## 🔬 TRIAL — 试点/轻量起步

| 方案 | 类别 | License | 说明 |
|---|---|---|---|
| [mini-SWE-agent](https://github.com/SWE-agent/mini-swe-agent) | 执行脊柱(轻量备选) | MIT | MIT,~100 行线性轨迹极易审计,契合『越简单越好审计』;Princeton 当前主力方向。代价:UI/服务/沙箱编排要自补。作先起步、成熟后迁 OpenHands 的路径。 |
| [Langfuse](https://github.com/langfuse/langfuse) | 可观测/审计后端 | MIT(ee 目录商用) | 核心 MIT 可自托管,session replay+datasets+scores 承载 L0 真值集与 L4 覆盖增长。LLM-judge 不强制裁判≠被测(治理约束须自建于其上);2026-01 被 ClickHouse 收购有路线图风险,故埋点走 OTel 保持可替换。 |
| [AG-UI Protocol](https://github.com/ag-ui-protocol/ag-ui) | 前后端事件契约 | MIT | MIT,~16 种事件(文本/tool call/state/HITL)over SSE/WS;门禁=HITL 事件、DIGEST/验证器=state 事件,前端随之可替换解耦。是否采用取决于后端语言与解耦诉求。 |
| [in-toto / SLSA](https://in-toto.io/) | 审计出生证/供应链证明 | Apache-2.0 | Apache-2.0,把 who/when/被谁接受/toolchain 固化为不可抵赖证明,承载 L0『真值出生证』与要求#6 可审计;适配固件构件审计链。 |
| [Robot Framework](https://github.com/robotframework/robotframework) | 测试编排 | Apache-2.0 | Apache-2.0,Renode 官方集成,可统一编排仿真/HIL/真机测试步骤,输出结构化结果供验证器裁决与审计追溯。 |

## 🕒 ASSESS — 待决策解锁后评估

| 方案 | 类别 | License | 说明 |
|---|---|---|---|
| [X-CUBE-MCSDK / TI InstaSPIN / Infineon iMOTION](https://www.st.com/en/embedded-software/x-cube-mcsdk.html) | 电机控制 SDK/参考实现 | 厂商专有(免费) | 平台强相关,由方向门禁选型决定:选 STM32+MCSDK 则 agent 产出变为 workbench 配置+应用层、CI 要核对生成物;选 iMOTION 固定引擎则电机 coding 表面积几乎清零。作参考语义(spec-by-example),MISRA 合规需向厂商确认。待访谈解锁。 |
| [STM32CubeMX (.ioc)](https://www.st.com/en/development-tools/stm32cubemx.html) | 配置与代码生成/机器可验证杠杆 | ST 专有(免费) | 最强机器可验证杠杆:引脚/外设/时钟树/功耗预算可从 .ioc 自动导出并反向校验、引脚冲突/通道超订确定性检查。前提目标 MCU 在 STM32 生态;国产 MCU(GD32/AT32 等)需确认有无等价配置源。 |
| [Libre Solar / 厂商预验证 BMS 固件(TI BQ769x2, Renesas R-BMS)](https://libre.solar/software/bms.html) | BMS 电池子系统 | Libre Solar 开源 / 厂商专有 | 无绳吸尘器电池子系统可复用起点;若用固定固件 BMS,agent 活缩成参数化+集成测试。电池安全另有 IEC 62133 合规面,需独立卡 lane。仅吸尘器线相关。 |
| [Claude Agent SDK (PreToolUse hooks)](https://code.claude.com/docs/en/agent-sdk/hooks) | 门禁范式参考 | SDK 可嵌但运行耦合 Anthropic API | PreToolUse hook 是最顺手的『数据门禁 denylist 硬停在不可逆操作前』实现范式,子 agent 不继承权限。但运行耦合 Anthropic 云 API,若要求气隙/本地模型则不适合作脊柱,仅借鉴 hook 权限模型。 |
| [Arize Phoenix](https://github.com/Arize-ai/phoenix) | 可观测备选 | Elastic License v2 | OTel-native trace timeline,自托管内部审计可用。硬约束:Elastic License v2 禁止作托管服务对第三方转售——白标/SaaS 场景不能用。 |

## ⛔ AVOID — 不推荐

| 方案 | 类别 | License | 说明 |
|---|---|---|---|
| [Open WebUI / Lobe Chat / Dify](https://github.com/open-webui/open-webui) | 前端底座(不推荐) | BSD-3+条款 / LobeHub Community(非OSI) / 改版 Apache-2.0 | 形状是终端 ChatGPT 客户端/app builder,不建模 YCFS 审计对象;且 license 陷阱:Open WebUI 品牌保护条款、Dify 多租户/logo 条款、Lobe 自定义非 OSI 许可,白标/产品化不可接受。仅作交互参考。 |

---

> **溯源提示(自我应用 L1)**:上表 URL 与 license 由调研 agent 产出。知名项目(Renode / pdfplumber / Ceedling / shadcn / Langfuse / Robot Framework / OpenLLMetry / assistant-ui)可信;个别快速演进的项目(OpenHands Agent SDK / mini-SWE-agent / AG-UI)的确切仓库路径与 license 条款,在真正 `adopt` 前需**逐一二次核实**并落到卡的验收里——这本身就是本系统「每个对外值必须溯源」铁律对它自己文档的应用。license 陷阱(Phoenix ELv2 禁转售、Open WebUI 品牌条款、Lobe 非 OSI)与最终交付形态(内部工具 vs 白标/SaaS,见 PENDING_HUMAN Q6)强相关,选定前必过法务门禁。
