# VENDOR-LANDSCAPE — 中美厂商全景(数采设备的客户 / 竞品 / 供应商 / 相邻)

> 配套 `PRODUCT-SPEC.md`。这里把市面玩家按**和我们产品的关系**分类,中美并列,每家带真规格/真事实 + 批判 + 来源 URL。
> 调研 2026-07。**可靠性说明**:多数一手 PDF(arxiv/HF/厂商)被本环境出口策略拦截,标"[二手]"的数字来自 WebSearch 对原文/媒体的引用;国产厂商量程/分辨率/价格多未公开(标"未找到"),不臆测。上线前关键数字请在能访问 arxiv/HF 的环境复核。

---

## 0 · 三个识别/订正(诚实置顶)

1. **"genrebot" = GenRobot / 简智新创**(北京,2025.7)——精确域名匹配 genrobot.ai。**纯数采公司**,可穿戴 Gen DAS:头戴 DAS Ego(270°六路/mm级/350g/24h)、DAS Fingers(**0.05N 触觉/1ms 延迟**)、DAS Gripper(8 传感器)。订单破万台,累计融资 ¥2.4 亿(顺为/初心/百度风投)。**若你指的是美国公司,最接近的是 Generalist AI**(手套式 data hands,GEN-0 已 >50 万小时,融资 >5 亿,李飞飞背书)。[来源:新浪财经 inhzzqck3071485;forbes 2026/04;generalist.ai]
2. **"觅蜂蜂" = 觅蜂科技(Beehive)**(智元旗下,2026.2,CEO 姚卯青)——To B 数据服务 + MEgo 无本体采集(头+腕双视角、**号称亚毫秒同步**),背靠智元+红杉,喊 2026 千万小时产能。[来源:澎湃 33399250;机器人大讲堂 8091]
3. **X-Trainer 是越疆 Dobot 的桌面双臂平台,不是智元**——我早前记错。智元真正的采数栈是 **AIDEA / AgiBot World**。[来源:github embodied-dobot/x-trainer]

---

## A · 客户候选:大脑/整机厂商(谁可能买数据)

**判据**:真实数据派、最缺真机数据 = 强买家;仿真优先派 / 自建采集闭环 = 弱买家或对立。

### 中国
| 公司 | 定位/主打 | 力·触觉 | 数采现状 | 买家可能性 + 批判 |
|---|---|---|---|---|
| **星海图 Galaxea** | G0 VLA + GOD 开源数据集(500h/10TB) | 未主打 | 真实数据路线,GOD 全真实场景 | **强候选**——旗帜押真实数据 VLA,最缺数据;但需确认自采还是外采 [galaxea-ai.com] |
| **自变量 X Square** | WALL-A/WALL-OSS,估值超 200 亿 | 未找到 | "以真实数据为主",已建数采工厂 | 中候选/两面——真实数据=天然买方,但已自建工厂可能自研设备 [x2robot.com] |
| **星动纪元 Robot Era** | ERA-42 五指灵巧手大模型 | **是**(全模态含触觉) | 遥操作+自研数采设备 | 潜在客户(有摩擦)——路线契合,但已自研数采,拼精度/成本 [robotera.com] |
| **千寻智能 Spirit AI** | Spirit VLA + 全力控 Moz1 | **是**(26 自由度力控) | 遥操作+自研数采 | 潜在客户(有摩擦)——力控数采是核心,拼你的力/触觉精度 [spirit-ai.com] |
| **智元 AgiBot** | GO-1 基座 + AgiBot World 百万数据 | **是**(视触觉+力) | 4000㎡ 数采工厂,LeRobot 格式;**已孵化觅蜂做 To B 数据** | **竞品倾向**——自给自足还外卖数据,是对手生态 [agibot.com] |
| **银河通用 Galbot** | GraspVLA(纯合成数据),估值 ~200 亿 | 未主打 | **仿真合成数据优先,刻意弱化真机** | 弱/对立——叙事就是"合成绕开真机采集" [news.cn] |
| **穹彻智能 Noematrix** | "力为中心"具身大脑(非夕孵化) | **是**(以力立身) | 自研 CoMiner 采集系统 | **竞品倾向**——以力立身且自研采集,功能重叠 [tmtpost 7735591] |
| **灵初智能 Psi** | Psi R 系列(端到端 RL) | **是**(灵巧手) | 自研 Psi-SynEngine + 外骨骼手套,10 万+小时 | **竞品倾向**——自研外骨骼数采,且是觅蜂跟投方 [psibot.ai] |
| **逐际动力 LimX** | FluxVLA + COSA OS,推进 IPO | 未主打 | 偏运控/OS | 潜在(需验证)——操作数采需求强度不明 [limxdynamics.com] |
| **宇树 Unitree** | G1(9.9万起)+ UnifoLM | 力矩关节,触觉弱 | **卖 G1-D 数采全栈**,数据集**原生 LeRobot** | 竞品+平台两面——G1-D 与你竞争,但拥抱 LeRobot 可蹭生态 [unitree.com/G1-D] |
| **优必选 UBTech** | Walker S2 + 多模态规划 | **是**(36 力反馈关节) | **中标广西数采中心 ¥1.26 亿,用 Walker 自采** | **竞品倾向(危险)**——政企资源进你赛道 [ubtrobot.com] |
| 星动/众擎/加速进化 | 人形整机(偏运控/科教) | 力控关节 | 操作数采需求弱 | 弱客户/待观察 |
| 智源 BAAI / 清华 RDT | 开源大脑/学术(RoboBrain/RDT-1B) | 非重点 | 开源框架/学术自采 | 非商业客户——但格式若成标准需兼容 |
| 有鹿机器人 | LPLM 通用大脑(阿里系,清洁场景) | 未主打 | 垂直清洁 | 弱/垂直客户 |

### 美国/西方
| 公司 | 定位/主打 | 力·触觉 | 数据策略 | 买家可能性 + 批判 |
|---|---|---|---|---|
| **TRI(丰田)** | Large Behavior Models + Diffusion Policy | **明确主打**(触觉/力遥操) | 468h 双臂 + **32h UMI 数据** + 1150h OXE | **最强背书**——UMI 数据已进旗舰 LBM,是你唯一的顶级实验室实锤;但仅 32h 补充料、能力上可自采 [tri.global] |
| **Physical Intelligence** | π0/π0.5/π0.6,开源 openpi | 触觉研究中(非默认) | 自采 1 万小时;openpi 原生吃 **LeRobot/DROID/OXE** | 理想数据消费方——格式对口;但自采已强,只在缺的模态(触觉/新本体)有议价 [pi.website] |
| **NVIDIA(GR00T)** | Isaac GR00T N1.5,全栈卖铲子 | 非主打 | 真机+合成(**DreamGen** 世界模型),**扩展版 LeRobot+modality.json** | 定标准者+结构威胁——格式入场券,但战略是"仿真替代真机采集" [developer.nvidia.com/isaac] |
| **Generalist AI** | GEN-0/GEN-1,physical AGI | **data hands**(视觉+夹爪位姿,力深度存疑) | **自研手套采集**,GEN-0 >50 万小时,融资 >5 亿 | **直接竞品(最危险)**——同赛道放大版,李飞飞背书;你只能压"力/触觉精度" [generalist.ai] |
| **Figure AI** | 人形 Figure 03 + Helix,估值 390 亿 | **是**(指尖触觉 3g) | 自建 BotQ,1000h 人类+500h 遥操,全自采 | 非买家(自闭环)——但证明触觉有价值 [figure.ai] |
| **Skild AI** | omni-bodied 大脑,估值 >140 亿 | 未主打 | **仿真+网络视频优先,真机最小化** | 坏客户——叙事就是仿真替代采集 [skild.ai] |
| **Genesis AI** | GENE 基座 + 高保真仿真,种子 1.05 亿 | 未找到 | 重仿真 + 少量真机锚定 | 弱买家——仿真优先;名字与 Generalist 混淆源 [genesis.ai] |
| **Google DeepMind** | Gemini Robotics + ALOHA | 未主打 | 自家 ALOHA 2 遥操,封闭 | 非买家(巨头自闭环) [deepmind.google] |
| **1X / Tesla / Apptronik / Agility / Boston Dynamics / Covariant** | 人形/工业整机 | Tesla/Figure 有指尖力 | 全自采闭环(遥操回流/Robot Park/RL 仿真) | 基本非买家——垂直整合,几乎不外购 |
| **Sanctuary AI**(加) | Phoenix + 触觉 5mN | **是** | 自建触觉遥操 | 理念契合但自采+非美国 |
| **Dyna / Field AI** | 商用落地 / 导航自主 | 无 | 场景自采 / 导航数据 | 弱或无关(Field AI 不做操作) |

---

## B · 直接竞品:手持无本体数采(同赛道同形态)

| 产品 | 国别 | 相机/位姿 | 力·触觉 | 格式 | 价格/开源 | 批判 |
|---|---|---|---|---|---|---|
| **原版 UMI** | 美/Stanford | GoPro 155°鱼眼+侧镜,离线 ORB-SLAM3 | **无**(软指) | Zarr,可并 OXE | 开源,BOM **~$370** | 鼻祖;无力觉、SLAM 脆、吞吐低 |
| **鹿明 FastUMI Pro** | 中 | 纯视觉 3mm,背包 RGB 鱼眼+深度+8h | **无**(主打视觉+深度) | 未找到(自有) | 未找到,拟上京东 | 商用最激进;**无力觉**、纯视觉 contact-rich 受限;"万台/百万小时"是产能叙事 |
| **GenRobot 简智新创** | 中 | DAS Ego 头戴 270°六路/mm级 | **是**(DAS Fingers 0.05N/1ms) | 未找到 | 未找到,订单破万台 | **最像你的对手**;触觉参数亮眼,4 月连融数亿 |
| **觅蜂科技 MEgo** | 中(智元系) | 头+腕双视角,亚毫秒同步[厂商口径] | 夹爪采集,触觉未强调 | 未找到 | 未找到 | **弹药最足**;智元+红杉,产能目标激进 |
| **Generalist AI data hands** | 美 | 手套式人手采集 | 接触/力信号(深度存疑) | 未找到(自有) | 自建 50 万+小时 | 头部竞品;力觉深度是你的突破口 |
| **UMI-FT** | 美/Stanford | iPhone ARKit | **是**(每指 CoinFT 六轴) | 建于 UMI | 未找到量产 | **带力,但学术原型**;CoinFT 量产标定未知 |
| **DexUMI** | 美/Stanford | OAK-1 150°+Record3D | **是**(FSR/电磁,外骨骼) | 开源 | 开源,未量产 | 灵巧手方向;每种手需专造外骨骼 |
| **DEXOP** | 美 | 被动手外骨骼+编码器 | **是**(触觉+接触力) | 未找到 | 未找到 | 无源低成本;被动限可达构型 |
| **DexCap** | 美/Stanford | Rokoko 手套+T265 | **无**(电磁测位置非力) | 未找到 | 开源 | 40min 续航短、笨重、易磁干扰 |

**白地**:已量产的手持竞品(UMI/FastUMI/GenRobot/觅蜂/Generalist)**力觉基本缺失或深度存疑**;唯三真带力的(UMI-FT/DexUMI/DEXOP)**全是未量产学术原型**。→ **"已量产 + 手持在野 + 真六轴力 + LeRobot 原生"目前是空的。**

---

## C · 相邻路线:遥操作/本体数采

| 产品 | 国别 | 形态 | 力 | 格式 | 价格 | 批判 |
|---|---|---|---|---|---|---|
| ALOHA / ALOHA 2 | 美/Stanford | 双臂主从遥操 | 无(仅被动力感) | HDF5 | ~$20–32k | 需真机、贵、不便携 |
| Mobile ALOHA | 美/Stanford | 移动双臂 | 无 | HDF5 | ~$32k | 成本/便携仍差 |
| GELLO | 美/Berkeley | 廉价 leader 臂 | 无(FACTR 加力) | 依 follower | 自建 ~$300–500 | 仍需 follower 真机 |
| AgileX Cobot Magic(松灵) | 中 | 移动双臂(Mobile ALOHA 复刻) | 无 | 类 HDF5 | ~$48k | 贵、无力觉 |
| AgileX PiPER(松灵) | 中 | 6 轴臂(采数底座) | 未找到 | N/A | **$1,999** | 便宜但负载/精度有限 |
| 智元 AIDEA/AgiBot | 中 | 全身遥操+WBC | **是**(视触觉+力) | LeRobot | 内部 | 全身遥操门槛高、需自家人形 |
| X-Trainer(越疆 Dobot) | 中 | 桌面双臂(0.05mm) | 未找到 | HDF5 | 未找到 | 桌面级 VLA 采数 |
| Open-TeleVision | 美/UCSD+MIT | VR 沉浸遥操 | 无 | 依本体 | 开源 | 解决"看"不解决"感" |
| 星海图 Galaxea | 中 | R1 Lite 统一本体 | 未找到 | LeRobot | 商用 | 数据锁死单一本体 |

---

## D · 数据集/格式标准(交换格式之争 = 入场券)

| 数据集 | 国别 | 规模 | 力/触觉 | 格式 | 批判 |
|---|---|---|---|---|---|
| **Open X-Embodiment / RT-X** | 美+国际 | 100 万+轨迹,22 本体 | 多数无 | **RLDS**(事实标准) | 把"无力视觉+位姿"固化为默认 schema,频率 3–10Hz 偏低 |
| **DROID** | 美+国际 | 76k/350h,564 场景 | 无 | RLDS(并入 OXE) | 纯视觉、单臂 Franka,contact 天花板低 |
| **AgiBot World**(智元) | 中 | 100 万+/2976h | **有触觉** | **LeRobot v2.0** | 中国版 OXE,选 LeRobot;锁定智元本体 |
| **RoboMIND** | 中 | 31 万+双臂/6 本体 | 2.0 有 12k 触觉 | HDF5 | 力觉是 2.0 补丁非原生;HDF5 非主流 |
| **RH20T** | 中/上交 | 11 万+ contact-rich | **有力+触觉+音频** | 自定义 | **力觉先行者,但固定台架非在野**、装置重 |
| **Galaxea GOD** | 中/星海图 | 500h/10TB,下载 40 万+ | 未找到 | LeRobot | 开放场景强,但无力觉、单本体 |

**格式三分**:美系 **RLDS**(OXE/DROID)、中系新玩家 **LeRobot**(AgiBot World/Galaxea/宇树)、传统 **HDF5**(ALOHA/RoboMIND)。→ **数据要被采纳,必须能无损转这三种,并能映射到 GR00T 的 modality.json。**

---

## E · 供应商:力/触觉传感器(按"能否装夹爪指尖"分)

### E1 · 适合手持指尖(小/轻/自带感知/测接触分布或剪切,无需刚性基座)
| 传感器 | 国别 | 原理 | 关键规格 | 批判 |
|---|---|---|---|---|
| **千觉 Xense G1-WS** | 中 | 视触觉 | 96 压感点,3D 力分布+六维合力+形状,XY 0.03mm,10ms/帧,**20×14×4.8mm 楔形(为夹爪设计)** | 力为算法估计非标定;相机光路厚度 |
| **戴盟 DAIMON DM-Tac** | 中 | 视触觉 | ~4 万单元/cm²,算六维力+滑移/软硬,>800Hz 采集 | 官方不公开量程/价;六维力算法推算 |
| **帕西尼 PaXini ITPU/PX-6AX** | 中 | 视触觉(霍尔阵列) | 121 三轴点/0.1mm/1MHz;DexH13 手 1140 单元 | 多与自家灵巧手绑定;相机厚度 |
| **CoinFT**(开源) | 美/Stanford | 电容六维力 | φ20mm/2g,法向 0–10~14N/剪切 0–4~5N,力 RMSE 0.11–0.16N | **量程小、相位 2.5Hz 起滞后动态差**、需自制标定 |
| **AnySkin / ReSkin**(开源) | 美 | 磁 | <0.1N、>100Hz、薄皮 2–3mm 可包指、~几美元 | 相对信号非标定力、磁干扰、需 ML 解码 |
| **DIGIT / Digit 360**(Meta) | 美 | 视触觉 | DIGIT 20g/60fps;360 多模态(振动/气压/温度) | 输出图像非标定力;光路厚度 |
| **GelSight Mini** | 美 | 视触觉 | $499,25fps,gel 厚 4.25mm | 测几何非力;25fps 高速滑觉一般 |
| **Contactile PapillArray** | 澳 | 光学 3 轴阵列 | 每 pillar 3D 力+滑移+摩擦,X/Y~4N/Z~11N | 阵列覆盖面有限 |
| **SynTouch BioTac** | 美 | 阻抗多模态 | 0.01N,100Hz–4.4kHz,指尖形态 | 需充液维护、易损、力为推算、供货存疑 |
| **他山 Tashan TS-F** | 中 | 电容层析+neuromorphic | 0–50N,3D 力 0.01N,1mm,**仅 30–100Hz** | **采样率低不利动态滑觉**;5%FS 精度一般 |
| 9DTact(开源) | 学术 | 视触觉暗场 | 32.5mm,3D 形状+6D 力估计 | 研究原型;力为学习估计 |

### E2 · 单轴压力薄膜(能贴指尖但只测法向、无剪切/滑移,数据价值有限)
Tekscan FlexiForce A201(美,$15–30)· 汉威/能斯达柔性薄膜(中,<0.3mm)· 纽迪瑞 NDT MSK(中,消费按键)· PPS DigiTacts(美,电容压力阵列)。**批判**:压阻迟滞漂移大、需频繁标定,捕不到剪切。

### E3 · 腕部/法兰"基座式"六维力(体积重量大,不适指尖,只测合力矢量)
| 传感器 | 国别 | 规格 | 批判 |
|---|---|---|---|
| 海伯森 Hypersen HPS-FT060 | 中 | ±600N/±800N/±15Nm,2000Hz,255g,外径 60mm | 太大、装指尖丢分布 |
| 蓝点触控 | 中 | 150–3000N,>10kHz,φ60–80mm,国内份额 72.6% | 腕部基座式 |
| 坤维 KWR / 宇立 SRI / 鑫精诚 | 中 | 6 轴应变,0.03%FS,φ46–82mm | 腕部基座式(鑫精诚有小三维力可勉强装指端) |
| OnRobot HEX / Bota SensONE | 丹/瑞士 | 6 轴,347g/93mm;Bota 2000Hz+IMU | 腕部基座式 |
| **ATI Nano17** | 美 | 6 轴,~50N,**分辨率 3.1mN**,φ17mm/9g | 小巧可勉强装指端根部,但需外部 DAQ、~$3–5k、测合力非分布 |

**选型判断**:手持指尖采集的正解是 **E1 类**(小视触觉如千觉 G1-WS / 戴盟,或 CoinFT 六维力 + 磁皮 AnySkin);**E3 基座式六维力物理上不适合指尖**(测的是安装法兰处合力矢量,须刚性基座)。这与 `PRODUCT-SPEC.md` §4 的力觉选型一致。

---

## F · 供应商:灵巧手(数据重定向的目标本体,来自前轮调研)
| 手 | 国别 | DoF | 触觉 | 价格 |
|---|---|---|---|---|
| 因时 Inspire RH56 | 中 | 6 主动/12 关节 | 有(RH56H1 260 触点) | ~$5.6k(渠道价差大) |
| 智元/星动 XHand1 | 中 | 12 主动(Pro 21) | 指尖 3D 力+温度 | 未公开 |
| 傅利叶 GR-2 手 | 中 | 12 | 6 路阵列 | 未公开 |
| 灵心巧手 Linker / 强脑 BrainCo | 中 | 6–12 | 部分有 | 未公开 |
| Shadow Hand | 英 | 24 | 120+ 传感器 | ~$100–150k |
| PSYONIC Ability | 美 | 假肢手 | 指尖压力 | 假肢整机 |

**批判**:目标手 DoF 从 6(Inspire)到 24(Shadow)差 4 倍,驱动/耦合/触觉排布/价格全不同;**触觉语义几乎无法从人手迁移,重定向基本只覆盖运动学**。

---

## G · 战略综合(外部数据逼出来的判断)

1. **赛道已是红海,不是蓝海**:无本体数采在中国已有 **GenRobot、觅蜂(智元系)** 两家专业竞品 + 一批自研采集的大脑厂商(穹彻/灵初/宇树 G1-D/优必选);美国有 **Generalist AI** 同形态放大版。"没人做这把铲子"是错的。
2. **但白地确实存在**:**已量产 + 手持在野 + 真六轴力 + LeRobot 原生**——这个交集目前空着(带力的全是学术原型 UMI-FT/DexUMI/DEXOP,量产的全没真力)。这是唯一站得住的差异化,且和 `PRODUCT-SPEC.md` 的"力做可选旗舰层"一致。
3. **真买家稀少**:多数大脑厂商自采;**仿真优先派**(Skild/Genesis/银河/NVIDIA DreamGen)从根上压低真机数据需求;**现实买家是真实数据派**——星海图、TRI(已用 32h UMI)、自变量、星动/千寻(力控,但多已自研设备)。销售要先筛掉"自采闭环"和"仿真优先"两类。
4. **最强背书 = TRI 已把 32h UMI 数据写进旗舰 LBM**——务必用作第三方实锤(但只占 32h,是补充料)。
5. **格式是入场券**:必须原生出 **LeRobot**,并能无损转 **RLDS(OXE/DROID)、HDF5**,且映射 **GR00T modality.json**——否则进不了主流管线。
6. **差异化只能压两点**:①**力/触觉采集精度**(GenRobot 的 0.05N、觅蜂主打视觉+同步,力深度都存疑;Generalist 的 data hands 力也存疑)——你要用**指尖内联六维力(CoinFT/PaXini)+ IMU 补偿**做出别人没有的**标定过的牛顿级力**;②**LeRobot 原生 + 三格式无损转**。其余(视觉/位姿/傻瓜化)别人已卷平,不构成壁垒。

---

## 来源(逐条已内嵌;关键项)
大脑:pi.website · developer.nvidia.com/isaac · deepmind.google · tri.global · skild.ai · generalist.ai · genesis.ai · figure.ai · agibot.com · galaxea-ai.com · x2robot.com · spirit-ai.com · robotera.com · unitree.com · tmtpost/psibot.ai。
竞品/相邻:umi-gripper.github.io · fastumi.com · dex-umi.github.io · umi-ft.github.io · dex-op.github.io · dex-cap.github.io · aloha-2.github.io · mobile-aloha.github.io · wuphilipp.github.io/gello · global.agilex.ai · dobot.cn · robot-tv.github.io · genrobot.ai · 澎湃 33399250。
数据集:robotics-transformer-x.github.io · droid-dataset.github.io · OpenDriveLab/Agibot-World · x-humanoid-robomind · rh20t.github.io · HuggingFace galaxea。
传感器:dmrobot.com · geekpark(千觉)· paxini.com · hypersen.com · kunweitech.com · srisensor.com.cn · gelsight.com · digit.ml · ati.novanta.com · botasys.com · syntouchllc.com · contactile.com · tekscan.com · coin-ft.github.io · any-skin.github.io · pressureprofile.com。

> 本文不接门禁腿、不自评——靠上面这些外部真实来源。带"二手/厂商口径/未找到"的条目按标注理解,上线前复核。
