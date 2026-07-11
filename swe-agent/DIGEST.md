# DIGEST — swe-agent 每轮一行(人的唯一必读)

> 一轮 loop 做完,追加一行。扫这个文件就知道进展与卡点,不必读代码、不必读长报告。

| 轮 | 卡 | 做了什么 | 验收 | 卡点/下一步 |
|---|---|---|---|---|
| R1 | 建库 | 5 视角互盲盲点扫描 + 开源生态调研 + 架构合成;落 v0 脚手架(架构/固件验证器/复用短名单/未知地图 4 文档 + BACKLOG 11 卡 + DIGEST + PENDING_HUMAN 6 问 + 可跑 gate) | ✅ gate 绿(scaffold-integrity 腿:11 卡字段完整 / 4 文档齐 / DIGEST 有行);其余门禁腿诚实标 BLOCKED 不伪绿 | 6 个架构级问题待人答(见 PENDING_HUMAN Q1–Q6);5 张决策无关卡(A1/B1/C1/D1/E1/F1)ready 可开工。**关键未知**:Q1 MCU/工具链(手写 vs 生成边界)、Q3 数据出域(云 vs 气隙)是最大分叉。 |
| R2 | 立法+F1 | 人立法 Q1=STM32+MCSDK+GCC / Q2=样例后置 / Q3=云可用 SOTA 优先 / Q4=全球市场,落 docs/DECISIONS.md(D-001~004,带原话出生证);解锁 F1/G1/H1;实现 F1:STM32G474 种子工程(裸机启动+保护状态机)+headless 构建+gate cross-compile 腿激活(版本锁+size 断言) | ✅ gate 3/3 绿(cross-compile: gcc=13.2.1 text=856B);负向自测 2/2(版本篡改→红,text 下限→红) | 推送仍被 403 挡(等仓库写权限);Q2 样例、Q4b 签字人/HIL、Q5 老资料、Q6 前端受众待答。下一张:A1 执行脊柱或 D1 溯源核验。 |
| R3 | 参考轮子 | 核实并落库 docs/reference-wheel.md:OpenHands(79.8k★/MIT)整机导览+映射我们 7 组件;mini-swe-agent(5.6k★)极简参照;明确轮子缺的正是 YCFS 治理层 | ✅ gate 3/3 绿 | 立法者对 OpenHands 路线「感觉不好」,点名六方重审 → R4 |
| R4 | 六方重审 | 6 路并行调研(Anthropic/OpenAI/Vercel/CF/opencode/Hermes+AWS)按嵌入式尺子打分,落 docs/spine-comparison.md;提案 D-005:opencode 主+可插拔适配层;A1 卡转 blocked-on-human(Q7 签字);Hermes 排除,AWS 取 IDT/Kiro 素材 | ✅ gate 3/3 绿;6 路事实全部带 URL 溯源 | D-005 等 Q7 签字;opencode 钩子绕过路径列为红队卡素材 |
| R5 | 首席review落卡 | 首席工程师视角 review 全蓝图,17 项补充落 docs/chief-review.md;新增 10 卡(G2 吹风机路线核实/B3 资源预算腿/B4 故障注入/B5 MISRA 登记册/I1 DVP&R/I2 BOM-WCCA/I3 声学-ErP/J1 OTA占位/J2 标定-EOL/J3 台架/K1 agent 基准);D-001 加审查附注(吹风机线待核实);PENDING_HUMAN 增 Q8 | ✅ gate 3/3 绿(卡数 12→22,字段完整性全过) | 等人:Q7(D-005 签字,卡 M1)、Q8(资源)、Q2/Q4b/Q5/Q6;写权限仍未开(5 提交待推)。下一张建议:G2 或 B3。 |
| R6 | B3 | 资源预算腿激活:nm 封禁动态分配符号(6 项)/-fstack-usage 栈帧≤256B 且禁 VLA/静态 RAM≤4096B/isr-budget.md 骨架;推送错误层级变化(代理 403→GitHub 端 denied),权限差最后一步 | ✅ gate 4/4 绿(max_frame=32B, static_ram=8B);负向自测 3/3 | B3 done。等人项不变(Q7 最紧);下一张:K1 agent 基准 或 G2 吹风机路线调研。 |
| R7 | G2 | 吹风机驱动路线核实完成,报告落 docs/g2-hairdryer-drive.md:MCSDK 仅三相但 HSO 实测 5kHz 电频覆盖 100kRPM;Dyson 单相=专利孤岛(US10110102),国产供应链趋同三相高速 PMSM(峰岹 11 万转方案/灵动 100kRPM 方案/Infineon 100kRPM 参考设计);D-001 修订案:补「三相+极频≤5kHz」前提则全线成立 | ✅ 结论全部带厂商溯源;gate 4/4 绿 | review A1 从「决策危机」降级为「加前提条件」。等 Q9 两问(电机拓扑/转速极对数)+ D-001 修订签字;Q7(D-005)仍是 M1 闸门。下一张:K1。 |
| R8 | K1 | agent 评测基准落地 bench/:2 道埋 bug 修复题(构造即真值,host gcc 可判)+6 道 spec_qa(真值锚本会话核实事实带 URL)+run_bench 自检(参考必绿/buggy 必红/出生证/哈希锁/题数下限);gate 新增 bench-self-check 腿 | ✅ gate 5/5 绿(bug_fix=2, spec_qa=6);负向自测 2/2(篡改触红/同源探针触红) | K1 done。~~零依赖 ready 卡告罄~~(**R9 更正:错报**——C1/D1/I1/J1/H1 仍 ready)。 |
| R9 | C1 | 「待真机」结构性终态断言落地 governance/:转移白名单无任何 (*,verified) 边;唯一入口要求 done+有效真机签字(非空证据/卡号匹配/概括授权无效);audit 抓伪造 verified(P0)+枚举待真机队列;gate 第 6 腿 state-machine(断言下限 10) | ✅ gate 6/6 绿(asserts=10/10);gate_green 开不了 verified 的门被单测证明 | C1 done(YCFS 最承重不变量落地)。剩余零依赖 ready:D1(L1 溯源)/I1(DVP&R)/J1(OTA 占位)/H1。等人:Q7/Q9 最紧;写权限(9 提交待推)。下一张:D1。 |
| R10 | 吹风机规划 | 4 路并行调研(Dyson 拆解对标/高速 FOC/加热温控安规/可移植架构)合成 docs/hairdryer-tech-plan.md:戴森级量化基线(110k rpm/13L·s×3/77dBA 移频/≤100°C·40 次秒)、功率架构(电机仅 60-105W,大头加热丝)、软件分层(bsp ops 表/MCSDK 参数包切面/platform+products)、FOC 规划(三电阻/PWM 40-50k/HSO 直闭环+I/F 后备)、三环 PID+温度前馈、电机-加热联锁(专利语义);**人立法 D-006 裸机优先**(原话落 DECISIONS);落卡 G3(ready)/G4(等 Q9)/G5(ready) | ✅ 调研 4/4 带 URL 溯源;诚实空白 4 处标注(死区补偿/20vs40Hz/控制律无公开/400ms 系厂商宣称);gate 6/6 绿(卡 23→26) | 等 Q9(电机拓扑两问)解锁 G4;小白讲解版 artifact 随后发布。 |
| R11 | G3 | 软件框架骨架落地:firmware/ 重构为 bsp/platform/products/tests/tools 分层(git mv);裸机任务表调度器(过载计数/防雪崩/回绕安全)+OSAL 接缝;board const-ops 表;gate 新增 host-unit-test(9 断言)与 layer-deps(6 文件)两腿;修复 .su 过滤器与 bench 路径连带 | ✅ gate 8/8 绿;host 单测 9/9;负向自测过 | G3 done。G5(温控联锁)ready 可继续;G4 等 Q9;D1/I1/J1/H1 仍 ready。11 提交待推。 |
| R12 | G5 | 温控 PI+前馈(条件积分抗饱和+115°C 硬顶)与电机-加热联锁(三态/闩锁/恢复需风量+冷却双条件/无效读数即切)落地并接入 50Hz 任务;bench 增联锁埋 bug 题(恢复缺冷却确认),run_bench 泛化每题自带被测/判题;**-Werror 抓出真域宽 bug:speed_rpm uint16 在 110k RPM 回绕会骗过联锁,全链改 uint32** | ✅ gate 8/8 绿(host 25 断言含炉温仿真过冲≤5°C;bench 3 题;text=1660B) | G5 done(done≠verified,60335-2-23 异常工况待真机)。PID 拼图:温度环✅/电流+速度环随 G4 等 Q9。12 提交待推。 |
| R13 | D1 | L1 溯源核验落地 provenance/:「引用解析得到该值」语义(非「有引用」),NFKC 归一化中英等强;单测 16/16——真值 16 放行零误伤、篡改 16/16 拦截且 EN=CN、伪造页/缺出处硬阻断、真 PDF 回环(reportlab STSong 中文→pdfplumber);gate 第 9 腿激活 | ✅ gate 9/9 绿(provenance=16);BLOCKED 剩 3 | D1 done——零编造护栏立起。零依赖 ready 剩 I1(DVP&R)/J1(OTA 占位)/H1;等人:Q7/Q9/写权限(13 提交)。 |
| R14 | Q9立法+G2结案+I1/I3 | 人立法:吹风机电机**确认三相**(原话入 DECISIONS),D-001 修订案生效、G2 done、G4 阻塞收窄为 Q9b(转速/极对数/R-L-Ke);单相认知 primer 调研后台进行。I1/I3 落地 dvpr/:DVP&R 15 行(限值全带出处或诚实 PLACEHOLDER,含声学 77dBA/ErP 0.5W/闪变 61000-3-3 行)+DFMEA 6 条,check_dvpr 校验高 RPN 必有验证链接、L-real 有证据必须有签字;gate 第 10 腿 | ✅ gate 10/10 绿(rows=15,dfmea=6);负向自测 3/3 | 零依赖 ready 剩 J1(OTA 占位)/H1。等人:Q9b、Q7、写权限(15 提交)。 |
| R15 | 单相primer+溯源更正 | 单相认知储备落 docs/single-phase-primer.md(电机构造低极数上高速/2-4FET 换相/死点-脉动-无感三难题与解法/利弊/对三相 4 点启示);**溯源更正:US10110102 同族证据指向 Johnson Electric 非 Dyson**——g2 报告与 bench spec_qa/005 引用已更正(替换为 US8988021/US9515588B2),哈希锁重签;「专利孤岛」结论不变且更强(Dyson 535 件+Johnson Electric 布防) | ✅ gate 10/10 绿;更正走 L1 纪律留痕 | 认知任务闭环。等人:Q9b(G4 参数)、Q7(D-005)、写权限(16 提交)。 |

写法:
- **一行讲清一轮**:做了什么、验收结果(带数字)、有没有卡点。
- 验收带**机器数字**(腿数 / 断言数 / 卡数),不写「跑通了」这种没法查的话。
- 踩到的坑、抓到的真 bug、被推翻的决策,一句话记在「卡点/下一步」——它是项目记忆。
