# BACKLOG — swe-agent 任务卡(唯一计划真源)

> 无时间线。只有优先级(自上而下)、状态、依赖、机器可查的验收。
> 首批 11 卡由盲点扫描合成。2026-07-07 立法(D-001/003/004,见 docs/DECISIONS.md)后:F1/G1/H1 解锁;B2 等 Q2 样例;D2 等 Q5;E2 等 Q4b/Q6。

状态:`ready` 可做 | `in-progress` 进行中 | `blocked-on-human` 等人 | `done` 验收已过 | `dropped` 放弃(留理由)

---

## Lane A · 执行核心(决策无关)

### A1 · 执行脊柱 + 沙箱抽象 + 事件溯源骨架
- 状态:`blocked-on-human`(Q7/D-005 执行脊柱签字;原 OpenHands 路线经六方重审后拟改为 opencode 主 + 可插拔适配层,见 docs/spine-comparison.md)
- 原话:"系统可以先考虑BS架构" + "做成可观测,可追索,可审计,可验证的开发助手" + "我感觉不好,我希望考虑openai 或者anthropic agentsdk,vercel 的案例以及CF的" + "还有opencode+加上其沙箱功能是否也是一个好方案?"
- 翻译:待 D-005 签字后:opencode server 经适配层嵌入 BS 后端,事件流(SSE)落**不可变**存储确定性回放;适配层保留换装 Claude Agent SDK/Codex。
- 依赖:Q7 签字
- 验收(机器可查):
  - `agent_server` 起 REST/WebSocket 并通过健康检查(exit 0)
  - 跑一次样例任务产出事件流文件,重放脚本对同一事件流两次执行**输出字节级一致**
  - CI 断言事件流 **append-only**(写后哈希不变)
- 证伪/回退:若 OpenHands SDK 过重拖慢迭代 → 退到 mini-SWE-agent(~100 行,线性轨迹),回退成本低,事件流 schema 保持不变。

---

## Lane B · 验证门禁(决策无关)

### B1 · gate 运行器 + v_min 单调地板
- 状态:`ready`
- 原话:"验证方案考虑可编译通过,可以完成一些表格自测" + "可验证"
- 翻译:实现一条命令 N 腿全绿的门禁运行器,断言数 / 自检项数 / MISRA 抑制项列表落文件,**门槛只紧不松**(下降即红)。本目录 `gate.py` 是其骨架起点。
- 依赖:无
- 验收(机器可查):
  - gate 运行输出结构化 JSON(每腿 red/green + 计数)
  - 人为删一条断言后 CI 检测到计数**低于地板**并返回非零退出码
  - 抑制项列表新增条目触发红
- 证伪/回退:若某腿地板被证明本就过严(误伤真值)→ 只能在 PENDING_HUMAN 走 direction 门禁人批后调整,且记录出生证;**AI 不得自行放宽**。

## Lane B · 验证门禁(阻塞于 Q2/Q4)

### B2 · IEC 60730 Class B 自检覆盖表 L0
- 状态:`blocked-on-human`(等 Q2 老项目自测表样例——原话"会有测试表格以后说";Q4 已立法 D-004:全球市场,合规矩阵按最宽立)
- 原话:"可以完成一些表格自测"
- 翻译:把 Annex H 表 H.11.12.7 编码为规格符合性对照表,真值锚取**标准条款 + 厂商认证 STL**,真值列与被测生成物**物理隔离**。
- 依赖:Q2、Q4;L0 真值管道(A1 事件流)
- 验收(机器可查):
  - 每项自检的 POST/BIST 分类 + 故障类型 + 实现与否**机器可查**
  - 真值列 provenance 指向标准编号/条款/认证库,**而非被测自出**
  - **字节对比证明期望列与被测生成产物非同源**(常备证伪探针)
- 证伪/回退:若期望列被发现与被测生成物字节同源 → 该自检守护零信息,整卡重构(最高优先封死的污染入口)。

---

## Lane C · 状态机治理(决策无关)

### C1 · 「待真机」结构性终态断言
- 状态:`done`(第 R9 轮。governance/statemachine.py:转移白名单**结构上不含任何 (*,verified) 边**;唯一入口 `transition_verified(signoff)` 要求 done 态 + 有效 RealMachineSignoff(签字人/角色/日期/声明/**非空证据引用**,卡号必须匹配——概括授权无效);gate_green 被单测证明开不了门。audit() 扫描伪造 verified(直改存储绕过转移函数)即报 P0,并枚举 done 卡为待真机队列。单测 10/10;gate 新增 state-machine 腿(断言数下限 10 防静默变少)。签字 schema 为最小集,E2 按 Q4b 扩展只加不减。)
- 原话:"然后由人来上真机测试"
- 翻译:状态机上删除「gate 全绿 → verified」直达边,verified 唯一入口携带人-真机签字。
- 验收记录:gate 6/6 绿(state-machine asserts=10);伪造 verified 被审计抓(T8)。

---

## Lane D · 知识库(决策无关)

### D1 · 确定性规格书解析 + L1 引用解析核验(中英等强)
- 状态:`done`(第 R13 轮。provenance/verify.py:核验语义=「引用解析得到该值」而非「有引用」——无出处/无页码/页不解析/值未见于被引页一律硬阻断;归一化 NFKC(全角→半角)+去千分位+去空白+小写,匹配层语言无感。单测 16/16:真值 EN/CN 各 8 全放行、篡改 EN/CN 各 8 拦截 100% 且**两语言拦截率相等**、伪造页/缺出处硬阻断、**真 PDF 回环**(reportlab 生成 STSong 中文 CID 页→pdfplumber 抽取→同核验器)。gate 第 9 腿 provenance-check 激活(下限 16),BLOCKED 剩 3。表格抽取(Camelot)与 errata/版本绑定随知识库摄取管道(D2/后续卡)扩展。)
- 原话:"根据产品规格和原理图以及器件和MCU规格书"
- 翻译:确定性解析被引页、确认数值字面出现;中英等强;溯源缺失硬阻断。
- 验收记录:gate 9/9 绿(provenance asserts=16);拦截率 EN=CN=100%,零误伤。

## Lane D · 知识库(阻塞于 Q5)

### D2 · 老项目资料「参考非真值」隔离入库
- 状态:`blocked-on-human`(Q5 老资料形态与背书/权属)
- 原话:"会提前给一些老项目资料"
- 翻译:老代码带出处 + 勘误/已知坏点标签,溯源终点落规格书页而非「旧项目用过」;区分规范性引用与仅供参考。
- 依赖:Q5;D1 溯源管道
- 验收(机器可查):
  - 任一值**唯一 provenance 为老代码即硬阻断/标红**并要求重锚回规格书
  - 许可证扫描报告 GPL/受限第三方代码
  - 规范性 vs 仅参考标注完整性校验通过
- 证伪/回退:若把某个仅老项目出现的值当真值放行 → 历史 bug 复利风险成立,回退代价高。承重卡。

---

## Lane E · 观测审计(决策无关)

### E1 · OTel 埋点 → append-only 审计 sink
- 状态:`ready`
- 原话:"做成可观测,可追索,可审计"
- 翻译:仪表化走 OTel GenAI semconv/OpenLLMetry,每步 diff + 决策 + **模型署名**进 trace,落 Langfuse + 外部只读存证。
- 依赖:A1 事件流
- 验收(机器可查):
  - 跑一次任务后 trace 含每步 diff 与模型署名字段
  - 审计 sink **写后修改尝试被拒**(WORM 校验通过)
  - 埋点后端可从 Langfuse 切到备选而 span schema 不变(迁移冒烟测试绿)
- 证伪/回退:埋点绑 OTel 而非专有 SDK,故 Langfuse 路线图风险(2026-01 被 ClickHouse 收购)可平滑切 Phoenix/自建,回退成本低。

## Lane E · 观测审计(阻塞于 Q4/Q6)

### E2 · 真机测试证据结构化回流
- 状态:`blocked-on-human`(Q4b 签字人/HIL 资源未答;Q6 审计面是否物理分离未答)
- 原话:"然后由人来上真机测试"
- 翻译:真机报告(示波器截图/量测数据/签字表)按 schema 结构化进 trajectory,成为 `verified` 唯一真值锚。
- 依赖:Q4、Q6;C1 状态机
- 验收(机器可查):
  - 签字产物 schema 落地并校验必填字段
  - 缺证据的卡 `verified` 转移被状态机拒绝
  - 审计链可从 `verified` 卡**反向追溯**到具体真机证据文件
- 证伪/回退:真机在平台外发生,证据不回流则审计链在最高仲裁处断裂——这是要求#4 能否落成状态机约束的关键。承重卡。

---

## Lane F · 固件 CI 沙箱(D-001 已解锁:STM32+GCC)

### F1 · arm-none-eabi headless 交叉编译门禁
- 状态:`done`(第 R2 轮。STM32G474 种子工程:最小裸机启动+链接脚本+**应用层保护状态机** protection.c(过温降额/跳闸闩锁/堵转/读数无效即 TRIP——D-001 划定的 agent coding 表面积样例);`build.sh` 一条命令 headless 构建产 .elf/.map/size;gate `cross-compile` 腿激活:toolchain.lock 版本校验+text 下限+flash 预算;负向自测×2 证明非空绿(版本篡改→红,text 下限→红)。阈值全标 PROVENANCE: PLACEHOLDER,待 D1 溯源管道。CI 工作流接线拆到新卡 F2。)
- 原话:"coding后CI,验证方案考虑可编译通过"
- 翻译:固定 toolchain 版本,CMake headless 构建 STM32G4 工程产 .elf/.map/size 报告,gate 交叉编译腿激活。
- 验收记录:gate 3/3 绿,cross-compile 腿 gcc=13.2.1 text=856B data=8B;负向自测 2/2。

### F2 · GitHub Actions CI 接线(gate 上云)
- 状态:`ready`
- 原话:"coding后CI"
- 翻译:workflow 装 arm-none-eabi-gcc(版本与 toolchain.lock 一致)+ 跑 `python3 swe-agent/gate.py`,任一腿红即 CI 红;后续腿(静态分析/单测)加进来自动生效。
- 依赖:F1(done);仓库写权限(推送后才能触发)
- 验收(机器可查):
  - PR 上 CI 状态检查出现且绿;人为制造一次红(如改 toolchain.lock)CI 变红后还原
- 证伪/回退:无架构风险;纯接线。

---

## Lane G · 电机领域包(D-001 已解锁)

### G1 · 电机控制拓扑分叉卡结构(热安全包 / 电池-BMS 包)
- 状态:`ready`(D-001:STM32G4+MCSDK 生成路线 → 验证器审 workbench 配置/生成物 diff + 应用层保护状态机)
- 原话:"吹风机和吸尘器类产品,产品level follow 顶级品牌"
- 翻译:按 Q1 结果建对应验证器包:**吹风机热安全包**(温度闭环/OTP 阈值/热熔断逻辑/加热丝 PWM 上限)与**吸尘器电池包**(BMS 状态机/OV-UV-OC-OT 窗口/均衡/握手协议)。两套不同拓扑与合规面,不用一套通用模板通吃。
- 依赖:Q1;D1 溯源
- 验收(机器可查):
  - MCU 平台与拓扑锁定后,生成物 diff 核对(MCSDK/.ioc)**或**算法审各出一套断言
  - 选型理由/DFMEA 条目/合规矩阵行按领域包分叉,**单一通用模板被拒**
- 证伪/回退:若用一套「通用电机 agent」模板 → 吹风机单相高速 2-FET 与吸尘器三相 PMSM+BMS 的差异被抹平,埋隐患。承重卡。

### G2 · 吹风机电机驱动路线核实(单相高速拓扑 vs MCSDK)
- 状态:`blocked-on-human`(调研已完成,报告落 docs/g2-hairdryer-drive.md;等 Q9 两问定案 + D-001 修订案签字)
- 原话:"fable5 站在顶级品牌首席工程师重新review下,假如需要补充列出来"(review 发现 A1)
- 翻译:核实完成——MCSDK 仅三相但 HSO 实测 5kHz 电频覆盖 100kRPM;Dyson 单相为专利孤岛,国产/ODM 趋同三相高速 PMSM;三路线 A(G4+MCSDK 三相,推荐)/B(峰岹类引擎)/C(单相自研,不建议)带利弊与 coding 表面积影响。
- 依赖:Q9(电机拓扑与转速/极对数两问)
- 验收(机器可查):
  - ✅ 调研报告落 docs/,结论带厂商文档溯源(ST 社区/峰岹/灵动/Infineon/USPTO)
  - ✅ 路线选项 3 个带利弊与工具链影响
  - ⏳ D-001 修订案经人签字后更新 DECISIONS.md
- 证伪/回退:若客户答复电机为单相定制 → 走 B/C 分叉,吹风机线 CI 单独立卡;三相则 D-001 全线成立零改动。

---

## Lane H · 数据治理(D-003 已解锁:云默认 + 可收紧)

### H1 · 数据门禁 denylist:按项目红线可收紧的路由层
- 状态:`ready`(D-003:数据可上云,SOTA 优先;门禁保留——denylist + 逐一具名确认机制仍要建,只是默认路由=云)
- 原话:"Q3,数据都可以,先追求SOTA效果"
- 翻译:路由层默认云(SOTA 模型);保留按项目收紧开关(未来 NDA 严格客户可切本地);denylist 机制照建,**逐一具名确认,概括授权无效**。
- 依赖:无(D-003 已解除)
- 验收(机器可查):
  - 模拟外传敏感文档动作被**硬停**(单测)
  - 一次 blanket allow **不能**放行下一个具名产物
  - 本地/云模型路由配置与 Q3 结论一致的冒烟测试绿
- 证伪/回退:若「都允许」式概括授权能放行后续敏感文档外传 → 数据门禁失效,视为 P0。承重卡。

---

## Lane G · 吹风机领域(R10 规划落卡,方案见 docs/hairdryer-tech-plan.md)

### G3 · 软件框架骨架:platform/products 分层 + 裸机调度(D-006)
- 状态:`done`(第 R11 轮。firmware/ 重构为 bsp(nucleo_g474: board const-ops 表+启动+链接脚本)/platform(core: 裸机任务表调度器 sched.c+薄 OSAL 接缝 osal.h;safety: protection.c 迁入;control 留位)/products(hairdryer: 任务表 1kHz 速度/50Hz 温控/10Hz HMI)/tests/tools,git mv 保留历史。调度器语义:到期跑一次、过载计数、防雪崩重同步、tick 回绕安全,host 单测 9/9(修过一处测试设计错误:过载场景需隔离调度器)。gate 新增两腿:host-unit-test(激活原 BLOCKED,断言下限 9)/layer-deps(芯片头 include 检查+扫描数下限防空转)。修复重构连带:.su 过滤器改分层目录、bench 参考实现路径+重签哈希锁。)
- 原话:"软件框架搭建…多项目兼容,便于移植" + "可能优先要考虑裸机代码实现"
- 翻译:monorepo 分层 + const ops 表 + 裸机任务表调度 + OSAL 接缝;电机无关先行。
- 验收记录:gate 8/8 绿(cross-compile text=1100B;host-unit-test 9/9;layer-deps files=6);负向自测过(芯片头被抓/平台头不误伤)。

### G4 · FOC 集成与启动策略(MCSDK 参数包)
- 状态:`blocked-on-human`(Q9:电机拓扑三相 ODM vs 单相定制、目标转速/极对数)
- 原话:"FOC和PID等算法规划实现…要到戴森顶级级别"
- 翻译:Workbench 工程 + 参数包(pmsm_motor_parameters.h/drive_parameters.h 入版本控制,只经 Workbench 改参);三电阻采样首版;PWM 40–50kHz、FOC=PWM/2;启动首选 HSO 直接闭环、I/F 斜坡后备;弱磁按电机参数评估;开工首日核实死区补偿模块存在性。
- 依赖:Q9;G3
- 验收(机器可查):
  - 生成工程容器内构建绿;参数头文件每值带溯源(规格书/Profiler 报告)
  - 启动策略文档带证伪判据(真机启动成功率/到速时间)
  - [真机线] 400ms 级到 100k rpm 为目标非承诺,实测签字
- 证伪/回退:Q9 答单相 → 本卡换 B/C 路线重写,G3/G5 不动。

### G5 · 温控 PI+前馈 与 电机-加热联锁(软件安全核心)
- 状态:`done`(第 R12 轮。platform/control/thermal_pi.c:PI+风量前馈+条件积分抗饱和+硬顶(测温≥115°C 强制 0,先于联锁);platform/safety/interlock.c:OK/DERATE/CUTOFF 三态,风量丧失持续超时切断、闩锁、**恢复需「风量+冷却」双条件**、读数无效即切;经 board const-ops(heater_permille 存根=TRIAC 过零调功落位)接入 products 50Hz 任务。host 单测 16/16(含一阶炉温仿真:收敛±3°C 且过冲≤5°C);bench 增 case-003(埋 bug=恢复缺冷却确认,run_bench 泛化每题自带 ref/test/includes,BUGFIX_MIN 2→3);HOST_TEST_MIN 9→25。**副产物:-Werror 抓出真域宽 bug——speed_rpm 原用 uint16,110k RPM 会回绕成 44464 骗过联锁,已全链改 uint32**。阈值全标 PROVENANCE 待 D1/真机标定。)
- 原话:"FOC和PID等算法规划实现" + 60335-2-23 联锁要求
- 翻译:温度 PI+前馈纯函数 + 联锁状态机 + TRIAC 接口抽象;151°C 角蛋白锚。
- 验收记录:gate 8/8 绿(host asserts=25;bench bug_fix=3);真机异常工况(60335-2-23)仍待 L-real 签字——本卡 done ≠ verified。

---

## Lane B · 验证门禁(首席工程师 review 追加)

### B3 · 资源预算 gate 腿:栈用量 + 禁动态分配 + CPU 负载表
- 状态:`done`(第 R6 轮。gate 新增 `resource-budget` 腿:nm 符号封禁 malloc/free/sbrk 等 6 项、`-fstack-usage` 单函数栈帧 ≤256B 且非 static 限定(VLA/alloca)即红、静态 RAM data+bss ≤4096B、isr-budget.md 骨架落库(WCET 列+70% 占比规则)。负向自测 3/3:合成 malloc 符号/9999B 栈帧/dynamic 限定均触红。上限常量只紧不松。)
- 原话:首席工程师 review C1/C2(出处 docs/chief-review.md)
- 翻译:`-fstack-usage` 静态最坏栈深断言 + 链接产物符号封禁 + ISR 预算表骨架。
- 验收记录:gate 4/4 绿(max_frame=32B, static_ram=8B);负向自测 3/3。

### B4 · 故障注入:验证自检真的能抓故障
- 状态:`ready`(排期依赖 Renode 腿与 B2 自检表落地)
- 原话:首席工程师 review D1
- 翻译:Renode 注入 flash 位翻转/时钟漂移/RAM 位错,断言 60730 自检代码报警——用机器验证验证器本身。
- 依赖:Renode 腿、B2
- 验收(机器可查):
  - N 类注入故障被自检捕获率 100%,未捕获清单为空或逐条带人签豁免
- 证伪/回退:若 Renode 故障注入能力不足以覆盖关键故障类 → 该部分转真机故障注入计划(进 DVP&R),不放弃验证目标。

### B5 · MISRA 偏差登记册
- 状态:`ready`(排期依赖静态分析腿落地)
- 原话:首席工程师 review C5
- 翻译:每条静态分析抑制/偏差带编号、理由、批准人;登记册与抑制项一一对应,完整性机器可查——认证审计必备工件。
- 依赖:静态分析腿
- 验收(机器可查):
  - 抑制项 ↔ 登记册一一对应校验通过;无登记的抑制触发红
- 证伪/回退:无架构风险。

---

## Lane I · 方案交付物(首席工程师 review 新增)

### I1 · DVP&R 骨架 + DFMEA→测试推导链
- 状态:`ready`
- 原话:首席工程师 review A2/B3
- 翻译:方案交付物增加 DVP&R(设计验证计划与报告)骨架——电气/热/声学/EMC/安规/寿命全项带限值与判据;DFMEA 高 RPN 条目必须牵出 ≥1 条验证项(RTM 上机器查完整性);真机签字对 DVP&R 的行签,60730 自检表挂其软件安全节。
- 依赖:无
- 验收(机器可查):
  - DVP&R 模板落库,行含限值/判据/证据槽/签字槽
  - 完整性校验脚本:高 RPN 条目无验证项即红
- 证伪/回退:若客户评审流程用别的骨架(如企业自有 DVT 模板)→ 换模板不换引擎,成本低。

### I2 · BOM 成本 + 供应链生命周期 + WCCA/降额
- 状态:`blocked-on-human`(Q8:成本/供应链数据源与内部优选器件库)
- 原话:首席工程师 review B1/B2
- 翻译:选型带目标成本、生命周期状态(NRND/EOL 机器可查)、二供;WCCA 降额表 = 规格书限值 × 降额系数 × 工作点,可机器验证。
- 依赖:Q8;D1 溯源管道
- 验收(机器可查):
  - 每个 BOM 行有 lifecycle 状态与出处
  - 降额表全行余量 ≥ 降额政策值,否则红
- 证伪/回退:数据源不可得时降级为人工填报+机器校验完整性,引擎不变。

### I3 · 声学预算 + 待机功耗 ErP 合规项
- 状态:`ready`(并入 I1 的 DVP&R)
- 原话:首席工程师 review B4/C4
- 翻译:方案含声学预算(dB(A)+音品质)与测试计划;ErP Lot 6 待机 <0.5W 为 DVP&R 必查行(D-004 全球市场,欧盟硬法规)。
- 依赖:I1
- 验收(机器可查):
  - DVP&R 含声学与待机功耗行,限值带法规编号出处
- 证伪/回退:无架构风险。

---

## Lane J · 量产与生命周期(首席工程师 review 新增)

### J1 · Bootloader/OTA/安全启动占位设计
- 状态:`ready`
- 原话:首席工程师 review C3
- 翻译:双 bank 升级/回滚/固件签名/RDP 防克隆的占位设计;**先定 flash 分区约束**,防止后补推倒链接脚本(F1 种子工程的 512K 布局要预留)。
- 依赖:无
- 验收(机器可查):
  - 分区约束文档落库;链接脚本含预留分区且构建绿
  - 占位设计经人评审签字
- 证伪/回退:若产品线确认永不联网 → 占位缩为最小 bootloader,预留成本低;反向(后补)成本高——这正是现在占位的理由。

### J2 · 标定数据管理 + EOL/产测占位
- 状态:`blocked-on-human`(Q4b 真机资源;量产流程信息)
- 原话:首席工程师 review D3/D4
- 翻译:电机参数辨识数据/批次参数集/EEPROM 配置版本化(标定数据是资产);工厂模式固件与 ATE 脚本占位——verified 不是终点,量产移交才是。
- 依赖:Q4b
- 验收(机器可查):
  - 标定数据 schema 落库,每个参数集带批次与出处
  - 产测占位清单经人确认
- 证伪/回退:形态依赖客户产线现状,先 schema 后实现,回退成本低。

### J3 · 自动化台架(HIL 前的便宜版)
- 状态:`blocked-on-human`(Q8:预算/场地拍板)
- 原话:首席工程师 review D2
- 翻译:继电器上下电 + 热电偶 + 电流探头 + 串口日志的自动台架,把部分 L-real 变成夜间回归——比等 HIL 务实。
- 依赖:Q8
- 验收(机器可查):
  - 台架清单+预算提交人批
  - 建成后 ≥N 项 L-real 检查夜间自动化并落红绿墙
- 证伪/回退:若 Q4b 答复已有 HIL → 本卡降级或合并,零浪费(清单工作可复用)。

---

## Lane K · agent 自身评测(首席工程师 review 新增)

### K1 · agent 评测基准套件(golden cases)
- 状态:`done`(第 R8 轮。bench/ 落地:2 道埋 bug 修复题(构造即真值:传感器失效乐观假设/堵转计时器不清零,均对应真实事故形态)+ 6 道 spec_qa(真值全部锚定本会话已核实的带 URL 事实);run_bench.py 自检=参考实现必绿+buggy 必红+出生证齐+manifest.sha256 哈希锁防改题凑分+题数下限只紧不松;gate 新增 bench-self-check 腿。负向自测 2/2:篡改真值触红、参考实现冒充 buggy 被同源探针抓。agent 跑分模式待 M1 执行脊柱接入。plan_review 题待 Q2/Q5 素材。)
- 原话:首席工程师 review E1("你怎么证明这个助手是好的?")
- 翻译:埋 bug 修复题 + 规格 QA 题 + 跑分/自检脚本;L4 覆盖增长的校准基线。
- 验收记录:gate 5/5 绿(bug_fix=2, spec_qa=6);负向自测 2/2。

---

## 卡片纪律

- 一张卡 = 一小块**可验证**增量。做不完拆小,别攒大卡。
- 验收必须机器可查。写不出机器验收的卡,先想清楚「怎么算做对了」再落卡。
- `blocked-on-human` 的卡不空转等待:跳过做下一张(A1/B1/C1/D1/E1/F1 均 ready),每轮 DIGEST 持续报告卡点未解除。
- 完成才标 `done`;验收没 100% 过不标 done,不放宽验证器、不造数据。
- **固件域铁律**:任何卡都不能自行标 `verified`——`verified` 唯一路径穿过人的真机签字(C1)。
