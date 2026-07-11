# G2 · 吹风机电机驱动路线核实报告(2026-07-07,事实均经联网核实)

> 触发:首席工程师 review A1 质疑 D-001(MCSDK 面向三相,Dyson 吹风机是单相)。
> 结论先行:**质疑部分成立但不致命——Dyson 单相是专利孤岛,国产/ODM 供应链已趋同三相高速 PMSM;
> 若电机选三相,D-001 在吹风机线依然成立。**

## 核实事实

1. **MCSDK 拓扑与转速覆盖**:官方仅支持三相 PMSM/BLDC(FOC/六步),无单相支持(产品页+6.1.2 Release Notes)。
   高速能力:ST 社区确认 **HSO 观测器已测试至 5kHz 电气频率**,需 40–50kHz PWM(≥10 采样/电周期)。
   100k RPM 按 1–2 对极 = 1.7–3.3kHz 电频,**在已验证范围内**。
   (community.st.com/t5/stm32-mcus-motor-control/does-the-hso-support-high-speed-motors…/td-p/849259)
2. **国产供应链主流 = 三相高速无感 FOC**:
   - 峰岹 FU68xx(8051+ME 硬件 FOC 引擎,PWM ≤40kHz),FU6812L 有 11 万转风筒方案板(fortiortech.com;知乎 p/558737873);
   - 灵动 MM32SPIN0280 官方高速吹风机方案:三相无感 FOC、100k RPM、400ms 到顶速(mindmotion.com.cn);
   - 电机 ODM 件均三相。
3. **大厂参考设计**:ST 无吹风机专用 STEVAL/AN(仅通用三相板);**Infineon 有 REF-HAIRDRYER-C101-6ED**:
   IMC101T 无感 FOC,明确标注 "up to 100kRPM" 吹风机参考设计(infineon.com)。
4. **Dyson 单相 = 专利孤岛**:V9 单相无感 BLDC、115k RPM、2-FET,核心专利 US8988021(换相时序)/US9515588B2(无感控制)等,Dyson 电机类申请 535 件(2005–2026,PatSnap)。~~US10110102~~(**R15 溯源更正**:该专利同族证据指向 Johnson Electric 而非 Dyson,详见 single-phase-primer.md §四——但 Johnson Electric 同样在单相吹风机电机布防,「专利孤岛」结论不变且更强)
   (Electronics Weekly 2016;USPTO)。国产量产高速风筒无一采用。

## 三条路线

| 路线 | 内容 | agent coding 表面积 | 利 | 弊 |
|---|---|---|---|---|
| **A(推荐)** | STM32G4 + MCSDK 三相高速 PMSM | **大**(生成全开源 C 代码,应用层/保护/自检全归 agent) | HSO 实测 5kHz 电频覆盖 100kRPM;文档/wiki 丰富;与吸尘器线共平台共工具链 | 高速启动/调参周期长;BOM 略贵 |
| B | 峰岹 FU68xx 类内置 FOC 引擎 | **小**(寄存器式参数化) | 量产生态最成熟、上市最快 | 8051 闭源工具链(打破 F1 的 GCC 容器化 CI);差异化弱 |
| C | Dyson 式单相自研 | 最大 | BOM 最省(2-FET) | 专利壁垒 + 算法全自研,风险/周期最高,**不建议** |

## D-001 修订案(待立法者签字)

> D-001 增补前提条件:**吹风机线电机锁定三相高速(slotless)PMSM、极频 ≤5kHz、MCU 用 STM32G4 级**——
> 满足则 D-001 全线成立(路线 A);若客户坚持 Dyson 式单相或指定峰岹类专用芯片,吹风机线单独立决策(B/C 路线,
> CI 与领域包按 B/C 分叉)。

## 需要客户/立法者回答(定案的最后两问,已入 PENDING_HUMAN Q9)

1. 吹风机电机是**外购三相 ODM 件**还是坚持 Dyson 式单相定制?
2. 目标转速与极对数是多少?(决定电频是否 ≤5kHz、HSO 是否够用)
