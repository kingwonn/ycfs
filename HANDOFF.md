# HANDOFF — 新会话冷启动入口

> 记忆住在仓库里,不住在会话里。新会话读完本文件即可接续,无需旧对话。

## 使命(方向 gate 全部已签,见 PRECEDENTS.md)

- 底层使命:言出法随——人说意图,系统落成机器可裁的法,AI 与验证器随之执行(P12:一切服务客户与产品)。
- **当前产品使命(P13):为具身大脑厂商,做最好、最适配、成本最优的 UMI 数采设备。**
  - 最好 = 数据保真度可量化(质检内建,每批数据带可核查质量报告)
  - 最适配 = 大脑厂商训练管线直接摄取(格式/同步/标注)
  - 成本最优 = 消费级组件 + 软件补偿的成本结构
  - 已裁:做设备(运动员),不做中立标准(裁判)——"被测不能自证"冲突解除

## 冷启动阅读顺序

1. `PRECEDENTS.md` — 人的全部裁决。**P13 带三条未解除的证伪条件,是设计的第一约束。**
2. `practice/critical-review.md` — 六条批判(#1 力数据今天没买家、#5 地图堆积领土为零)
3. `practice/buyer-requirements.md` — 大脑厂商训练管线的硬输入规格(π0 50Hz/亚毫秒同步/LeRobot 格式)
4. `practice/first-principles.md` — 第一性推导(仿真 1% 成本;接触/力是仿真结构盲区)
5. `practice/contact-force-and-fidelity.md` — TacUMI/UMI-FT 实现路径、DIGIT $15 供应链、保真度十项指标
6. `practice/competitive-landscape.md` — 鹿明 FastUMI 三产品线、光轮/无问智科、美国头部自建

## 设计任务的起点(从 P13 三个"最"倒推)

| 约束 | 具体含义 | 未解 |
|---|---|---|
| 最适配 | LeRobot 原生输出;语言标注;时间同步质量给数;**对 50Hz joint-state 鸿沟给出对策** | 动作标签形态选什么(EE pose + 重定向层?) |
| 最好 | 保真度十项指标(时间对齐/漂移/tremble/一致性/多样性/可执行率/溯源)设备内实时算 | 力/触觉上不上(取决于证伪条件②) |
| 成本最优 | 对标:DIGIT BOM $15;鹿明 FastUMI Pro 1mm 精度是精度标杆 | BOM 目标价未定 |

## 交付进度
- spec-v0.md ✅(本会话接手产出,交接会话失败)
- outreach.md ✅(两问脚本+6触点名单)
- review-rubric.md ✅ / value-verdict-independent.md ✅(监督方独立评估)

## 下一步(两件,顺序固定)

1. **领土接触(仍未发生,地图已冻结)**:找真实从业者问两句——
   "你们生产模型今天吃不吃力/触觉数据?" + "你们收外部数据时,卡在格式还是卡在质量?"
   这两个答案分别裁决 P13 证伪条件②与"最适配"的优先级。
2. **规格书 v0**:按 buyer-requirements 的硬数字写设备规格草案(带每项的机器可查验收),
   给人过目——这是"言→法"的第一张卡。

## 运行时(全部可跑)

```
python3 runtime/gate.py            # 门禁:4 腿(含被测不能自证),棘轮只紧不松
python3 runtime/gate.py --selftest # 阴性对照:每条腿证明自己会红
python3 runtime/scale.py           # 修为刻度:内力/法宝/历练/逃逸
python3 runtime/reality.py owed    # 历练台账:现实抓到、还没变成断言的
python3 runtime/loop_audit.py <repo> # 体检自治循环仓库(曾抓到 physicalAI 停摆12天)
```

工作纪律:每次外部现实打脸 → `reality.py record --escaped` → 变成永久断言;
承重判断必带证伪条件;调研引用说"某某报告称"不说"事实是"。

## 等人的事

见 `GATES/PENDING_HUMAN.md`:激活 hook、分支保护、凭证隔离。
physicalAI 仓库 loop 停摆与 confidence 零信息已诊断待修(loop_audit 可复现)。
