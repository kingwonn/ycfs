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
| R8 | K1 | agent 评测基准落地 bench/:2 道埋 bug 修复题(构造即真值,host gcc 可判)+6 道 spec_qa(真值锚本会话核实事实带 URL)+run_bench 自检(参考必绿/buggy 必红/出生证/哈希锁/题数下限);gate 新增 bench-self-check 腿 | ✅ gate 5/5 绿(bug_fix=2, spec_qa=6);负向自测 2/2(篡改触红/同源探针触红) | K1 done。零依赖 ready 卡告罄——M1 等 Q7 签字,其余等 Q2/Q4b/Q5/Q6/Q8/Q9。写权限仍未开(8 提交待推)。 |

写法:
- **一行讲清一轮**:做了什么、验收结果(带数字)、有没有卡点。
- 验收带**机器数字**(腿数 / 断言数 / 卡数),不写「跑通了」这种没法查的话。
- 踩到的坑、抓到的真 bug、被推翻的决策,一句话记在「卡点/下一步」——它是项目记忆。
