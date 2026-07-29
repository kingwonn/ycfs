# WATCHLIST — 具身 / Physical AI 观察列表

> 75 家中美主要玩家,由 `m0/watchlist.json` 生成(可筛选版见 `site/watchlist.html`)。
> 数据 2026-07,会变——这是观察清单不是定论。关系:客户候选/竞品/供应商/相邻/生态。
> 带'口径/未找到'的按标注理解;不接门禁、不自评,靠外部公开信息。

## 大脑 / 基座模型（20）

| 名称 | 国 | 观察什么 | 状态 | 关系 | 来源 | 关键批判 |
|---|---|---|---|---|---|---|
| Physical Intelligence | 美 | π0/π0.5/π0.6 VLA,开源 openpi | B轮$6亿,估值~$24亿 | 客户 | pi.website | 理想数据消费方,openpi 原生吃 LeRobot/DROID/OXE;自采1万小时已强,只在缺的模态有议价 |
| NVIDIA（英伟达） | 美 | Isaac GR00T N1.5/N1.6 + DreamGen 合成 | 上市巨头 | 生态 | developer.nvidia.com/isaac | 定标准者(扩展版LeRobot+modality.json);但战略'仿真替代真机'是数据卖方结构威胁 |
| Google DeepMind | 美 | Gemini Robotics + ALOHA 生态 | Alphabet 内部 | 生态 | deepmind.google | 自家 ALOHA2 遥操封闭,几乎不外购;ALOHA 格式是事实标准之一 |
| Toyota Research Institute（丰田TRI） | 美 | Large Behavior Models + Diffusion Policy | 丰田资助 | 客户 | tri.global | ★最强背书:旗舰 LBM 训练已混入 32h UMI 数据;明确主打触觉/力遥操;但仅补充料、可自采 |
| Genesis AI | 美 | GENE 基座 + 高保真仿真 | 种子$1.05亿(Khosla/Schmidt) | 供应商 | genesis.ai | 重仿真、弱真机需求;名字与 Generalist 混淆源(genrebot 歧义) |
| Skild AI | 美 | Skild Brain omni-bodied | ~$14亿/估值>$140亿(软银) | 竞品 | skild.ai | 仿真+网络视频优先、真机最小化——数据卖方眼中的坏客户 |
| Dyna Robotics | 美 | DYNA-1(双臂,99.4%无干预) | A轮$1.2亿 | 客户 | dyna.co | 商用落地、数据规模小,理论有外购特定场景空间;更可能自采 |
| Field AI | 美 | Field Foundation Models(导航自主) | ~$4.05亿 | 相邻 | fieldai.com | 做导航非操作,与手持力觉数据几乎不重叠 |
| Covariant | 美 | RFM-1(核心团队并入亚马逊) | 被亚马逊逆向收购 | 相邻 | covariant.ai | 决策权转亚马逊;自有海量数据,几乎不外购 |
| 智元机器人（AgiBot） | 中 | GO-1 基座 + AgiBot World 百万数据 + AIDEA 采集 | 估值超百亿,已孵化觅蜂 | 竞品 | agibot.com | 全栈自给还外卖数据;数据用 LeRobot;是对手生态不是买家 |
| 银河通用（Galbot） | 中 | GraspVLA(纯合成数据预训练) | 累计>24亿/估值~200亿(宁德领投) | 竞品 | galbot.com | 叙事就是'合成数据绕开真机采集',理念对立 |
| 星动纪元（Robot Era） | 中 | ERA-42 五指灵巧手大模型 + XHand1 | 近10亿+2026超$2亿(顺丰) | 客户 | robotera.com | 全模态含触觉,路线契合;但已自研数采设备,拼精度/成本 |
| 自变量机器人（X Square） | 中 | WALL-A/WALL-OSS 操作大模型 | A++轮10亿(字节/红杉)/估值>200亿 | 客户 | x2robot.com | '以真实数据为主'=天然买方;但已建数采工厂,需摸清自建还是外采 |
| 千寻智能（Spirit AI） | 中 | Spirit VLA + 全力控 Moz1(26DoF) | 3月约50亿/百亿独角兽(京东) | 客户 | spirit-ai.com | 力控+遥操作数采是核心;同样自研数采设备,拼力控精度 |
| 星海图（Galaxea） | 中 | G0 VLA + GOD 开源数据集(500h/10TB) | B+约20亿/估值200亿 | 客户 | galaxea-ai.com | ★强候选:旗帜押真实数据VLA,最缺数据;需确认自采还是外采硬件 |
| 穹彻智能（Noematrix） | 中 | '力为中心'具身大脑 + CoMiner 采集 | 1年3轮累计>10亿(阿里) | 竞品 | noematrix.ai | 以力立身且自研 CoMiner 采集系统,功能直接重叠 |
| 灵初智能（Psi Robot） | 中 | Psi R 系列 + Psi-SynEngine 外骨骼手套 | 1年20亿(高瓴/智元) | 竞品 | psibot.ai | 自研外骨骼数采引擎、10万+小时;且是觅蜂跟投方 |
| 智源研究院（BAAI） | 中 | 悟界 RoboBrain 2.0 + RoboOS 跨本体 | 非营利研究院 | 生态 | baai.ac.cn | 开源方/标准制定者,不采购硬件;格式被其生态采纳=战略杠杆 |
| 清华 RDT 团队（TSAIL） | 中 | RDT-1B/RDT2(开源双臂扩散基座) | 学术团队 | 生态 | github.com/thu-ml/RoboticsDiffusionTransformer | ALOHA 自采;非商业客户,但格式若成标准需兼容;RDT2 强绑 UMI 手持采集 |
| 有鹿机器人 | 中 | LPLM-10B 通用大脑(阿里系,清洁场景) | >1亿天使(创新工场/百度) | 相邻 | — | 清洁设备'大脑'外挂,操作数采需求薄 |

## 整机 / 人形（12）

| 名称 | 国 | 观察什么 | 状态 | 关系 | 来源 | 关键批判 |
|---|---|---|---|---|---|---|
| Figure AI | 美 | Figure 03 + Helix VLA,指尖触觉3g | C轮>$10亿/估值$390亿 | 竞品 | figure.ai | 自建 BotQ 全自采;证明触觉有价值但不外购 |
| 1X Technologies | 其他 | NEO + 1X World Model | 传闻募$10亿/估值~$100亿 | 竞品 | 1x.tech | 挪威;'卖机器人进家→遥操回流数据'的数据飞轮,自给 |
| Tesla Optimus（特斯拉） | 美 | Optimus Gen3,22DoF手/指尖力 | 特斯拉内部 | 竞品 | tesla.com/optimus | 重视手部力反馈(利好触觉叙事);自建随身采集,永不外购 |
| Sanctuary AI | 其他 | Phoenix + Carbon,触觉5mN | >$1.4亿 | 客户 | sanctuary.ai | 加拿大;极重视触觉数据,理念契合;但自采+非美国 |
| Boston Dynamics | 美 | Atlas(电动)+ TRI 的 LBM | 现代持有 | 相邻 | bostondynamics.com | 数据路线随 TRI,UMI 数据可经 TRI 间接触达;自身数据能力强 |
| Agility Robotics | 美 | Digit v5 + NVIDIA 全身控制 | C轮$4亿/估值~$21亿 | 相邻 | agilityrobotics.com | 物流搬运对灵巧/触觉要求不高,非天然买家 |
| Apptronik | 美 | Apollo(用 Gemini Robotics 脑) | A轮累计$9.35亿/估值~$55亿 | 竞品 | apptronik.com | 自建 Robot Park 采集喂 DeepMind;外购位置窄 |
| 逐际动力（LimX Dynamics） | 中 | FluxVLA + COSA OS,推进IPO | 近$2亿Pre-IPO/估值150亿 | 客户 | limxdynamics.com | 偏运控/OS,操作数采需求强度不明,需验证 |
| 宇树科技（Unitree） | 中 | G1(9.9万) + G1-D 数采全栈 + UnifoLM | Pre-IPO级龙头 | 竞品 | unitree.com | 卖 G1-D 数采方案与你竞争;但数据集原生 LeRobot,可蹭生态 |
| 优必选（UBTech） | 中 | Walker S2 + 多模态规划,36力反馈关节 | 港股上市,Walker订单>6.3亿 | 竞品 | ubtrobot.com | ★危险:中标广西数采中心¥1.26亿、用自家机器人采数据,政企资源进你赛道 |
| 众擎机器人（EngineAI） | 中 | 人形整机+高功率密度关节 | 近10亿两轮/估值100亿(小鹏/京东) | 客户 | engineai.com.cn | 以运控见长,大模型/操作数据早期,采购时机未到 |
| 加速进化（Booster Robotics） | 中 | Booster T1/K1 开发平台 | 新一轮近10亿(IDG),出货>千台 | 相邻 | booster.tech | 偏运动/科教本体,操作数采需求弱 |

## 数据采集(竞品/相邻)（14）

| 名称 | 国 | 观察什么 | 状态 | 关系 | 来源 | 关键批判 |
|---|---|---|---|---|---|---|
| Generalist AI | 美 | GEN-0/GEN-1 + 手套式 data hands 采集 | $4亿/估值~$20亿,李飞飞背书 | 竞品 | generalist.ai | ★直接竞品:手套采集卖基座,GEN-0>50万小时;力觉深度存疑=你的突破口 |
| GenRobot（简智新创） | 中 | Gen DAS:DAS Ego头戴/DAS Fingers(0.05N/1ms)/DAS Gripper | 累计¥2.4亿/订单破万台(顺为/百度) | 竞品 | genrobot.ai | ★最像你的对手:可穿戴带触觉无本体数采,4月连融数亿(即'genrebot') |
| 觅蜂科技（Beehive） | 中 | MEgo View/Gripper 无本体采集,亚毫秒同步[口径] | 数亿天使(红杉,智元旗下) | 竞品 | — | ★弹药最足:智元+红杉,喊2026千万小时产能(即'觅蜂蜂') |
| 鹿明机器人（FastUMI Pro） | 中 | 手持600g/负载2kg,纯视觉3mm,拟上京东 | 拟投万台/百万小时 | 竞品 | fastumi.com | 商用最激进但无力觉、纯视觉 contact-rich 受限;'万台'是产能叙事 |
| 原版 UMI（Universal Manipulation Interface） | 美 | GoPro 155°+离线SLAM,开源BOM~$370 | Stanford 开源鼻祖 | 竞品 | umi-gripper.github.io | 无力觉、SLAM脆、吞吐低;是整个品类的原型 |
| UMI-FT | 美 | iPhone ARKit + 每指 CoinFT 六轴力 | Stanford 学术,未量产 | 竞品 | umi-ft.github.io | ★带真力但学术原型;CoinFT 量产标定/耐久未知——你要量产化这条 |
| DexUMI | 美 | 手外骨骼 + FSR/电磁触觉,Inspire/XHand | Stanford,CoRL'25,开源未量产 | 竞品 | dex-umi.github.io | 灵巧手方向;每种手需专造外骨骼,泛化差 |
| DEXOP | 美 | 被动手外骨骼+编码器+触觉 | 学术,未量产 | 竞品 | dex-op.github.io | 无源低成本;被动限制可达构型 |
| DexCap | 美 | Rokoko手套+T265+RGB-D LiDAR | Stanford 开源 | 相邻 | dex-cap.github.io | 无接触力(电磁测位置);40min续航短、笨重 |
| 松灵机器人（AgileX） | 中 | Cobot Magic($48k)/PiPER臂($1,999) | 被 RoboMIND 等采数用 | 相邻 | global.agilex.ai | 遥操作/本体数采;PiPER 便宜是卖点,无内置力觉 |
| 越疆 Dobot | 中 | X-Trainer 桌面双臂(0.05mm),开源 | 上市公司 | 相邻 | dobot.cn | 桌面级 VLA 采数;(订正:X-Trainer 是越疆不是智元) |
| ALOHA / Mobile ALOHA | 美 | 双臂主从遥操,HDF5,$20–32k | Stanford 开源标准 | 相邻 | aloha-2.github.io | 需真机、贵、不便携、无力觉;遥操采数事实标准之一 |
| GELLO | 美 | 廉价 leader 臂 ~$300–500 | Berkeley 开源 | 相邻 | wuphilipp.github.io/gello_site | 仍需 follower 真机;无力反馈(FACTR 扩展加力) |
| Open-TeleVision | 美 | VR 沉浸式立体遥操 | UCSD+MIT 开源 | 相邻 | robot-tv.github.io | 解决'看'不解决'感',无力反馈 |

## 数据集 / 格式标准（7）

| 名称 | 国 | 观察什么 | 状态 | 关系 | 来源 | 关键批判 |
|---|---|---|---|---|---|---|
| Open X-Embodiment（OXE/RT-X） | 美 | 100万+轨迹/22本体,RLDS 事实标准 | Google+34实验室,开源 | 生态 | robotics-transformer-x.github.io | RLDS 定义者;把'无力视觉+位姿'固化为默认schema,频率3–10Hz偏低 |
| DROID | 美 | 76k轨迹/350h/564场景,RLDS | 多校联合,开源 | 生态 | droid-dataset.github.io | 纯视觉、单臂Franka、无力觉,contact天花板低 |
| AgiBot World（智元） | 中 | 100万+/2976h,含触觉,LeRobot v2.0 | 智元 OpenDriveLab,开源 | 生态 | github.com/OpenDriveLab/Agibot-World | 中国版OXE,选LeRobot而非RLDS;锁定智元本体 |
| RoboMIND | 中 | 31万+双臂/6本体,2.0含12k触觉,HDF5 | 国地共建中心,开源 | 生态 | x-humanoid-robomind.github.io | 力觉是2.0补丁非原生;HDF5非主流、互操作成本高 |
| RH20T | 中 | 11万+ contact-rich,6DoF力+指尖触觉+音频 | 上交,开源 | 生态 | rh20t.github.io | ★力觉先行者,但固定台架非在野、装置重难规模化 |
| Galaxea GOD（星海图） | 中 | 500h/10TB 开放场景,LeRobot,下载40万+ | 星海图,开源 | 生态 | galaxea-ai.com | 开放场景强但无力觉、单一本体锁定 |
| LeRobot | 其他 | HuggingFace 数据格式 v2.1/v3(交换标准) | HuggingFace 开源 | 生态 | huggingface.co/lerobot | GR00T原生、π0事实标准;v3有breaking change,openpi贴v2.x→须双版本 |

## 力/触觉传感器(供应商)（18）

| 名称 | 国 | 观察什么 | 状态 | 关系 | 来源 | 关键批判 |
|---|---|---|---|---|---|---|
| 帕西尼（PaXini） | 中 | PX6D霍尔六维力±50N;PX-6AX触觉121点0.1mm;DexH13手 | 商用在售 | 供应商 | paxini.com | ★霍尔非电容(订正);六维力商用SDK但180g重;触觉多与自家手绑定 |
| 戴盟机器人（DAIMON） | 中 | DM-Tac 视触觉,~4万单元/cm²,>800Hz | 商用 | 供应商 | dmrobot.com | 适合指尖;六维力算法推算非标定、官方不公开量程/价 |
| 千觉机器人（Xense） | 中 | G1-WS 视触觉,96点,20×14×4.8mm(为夹爪设计) | 商用 | 供应商 | xensevision.com | ★楔形专为夹爪,XY 0.03mm;力为算法估计、相机光路厚度 |
| 他山科技（Tashan） | 中 | TS-F 电容层析+neuromorphic芯片,0–50N | 商用 | 供应商 | — | 3D力0.01N/1mm;但仅30–100Hz采样不利动态滑觉 |
| 海伯森（Hypersen） | 中 | HPS-FT060 六维力±600/800N,2000Hz,255g | 商用 | 供应商 | hypersen.com | 腕部基座式,太大不适指尖、丢分布 |
| 蓝点触控 | 中 | 六维力150–3000N,>10kHz,国内份额72.6% | 商用龙头 | 供应商 | — | 腕部基座式,φ60–80mm不适指尖 |
| 坤维/宇立/鑫精诚（KUNWEI/SRI/Forsentek） | 中 | 六维力应变,0.03%FS,φ46–82mm | 商用,¥1万–6万级 | 供应商 | kunweitech.com | 腕部基座式;鑫精诚有小三维力可勉强装指端 |
| 汉威/能斯达（Hanwei/Nsd） | 中 | 柔性压阻薄膜,<0.3mm | 商用 | 供应商 | hanwei.com | 单轴法向压力、无剪切;压阻迟滞漂移 |
| GelSight | 美 | Mini 视触觉,$499,25fps,gel厚4.25mm | 商用 | 供应商 | gelsight.com | 测几何非标定力;25fps高速滑觉一般;光路厚度 |
| DIGIT / Digit 360（Meta） | 美 | 视触觉,DIGIT 20g/60fps;360多模态 | 开源+商用 | 供应商 | digit.ml | 输出图像非标定力;适合指尖;360规格未公开 |
| ATI Industrial | 美 | Nano17 六维力~50N,分辨率3.1mN,φ17mm | 商用,~$3–5k | 供应商 | ati.novanta.com | 小巧可勉强装指端根部,但需外部DAQ、贵、测合力非分布 |
| Bota Systems | 其他 | SensONE 六维力+IMU,2000Hz | 瑞士,商用 | 供应商 | botasys.com | 腕部基座式,偏大不适指尖 |
| SynTouch（BioTac） | 美 | 阻抗多模态,0.01N,100Hz–4.4kHz,指尖形态 | 商用(供货存疑) | 供应商 | syntouchllc.com | 需充液维护、易损、力为推算 |
| Contactile | 其他 | PapillArray 光学3轴阵列,3D力+滑移 | 澳,商用 | 供应商 | contactile.com | 为抓取设计,适合指尖;阵列覆盖面有限 |
| CoinFT | 美 | 开源电容六维力,φ20mm/2g,0–14N | Stanford 开源 | 供应商 | coin-ft.github.io | ★UMI-FT 用的;量程小、相位2.5Hz起滞后动态差、需自制标定 |
| AnySkin / ReSkin | 美 | 开源磁性皮,<0.1N,>100Hz,~$几 | CMU/Meta/NYU 开源 | 供应商 | any-skin.github.io | 薄、可包指、便宜可换;相对信号非标定、磁干扰、需ML解码 |
| Tekscan | 美 | FlexiForce A201 单轴FSR,$15–30 | 商用 | 供应商 | tekscan.com | 单轴无剪切;压阻迟滞漂移大、精度低 |
| OnRobot | 其他 | HEX 六维力200N,347g | 丹麦,商用 | 供应商 | onrobot.com | 腕部基座式,大且重不适指尖 |

## 灵巧手(重定向目标)（4）

| 名称 | 国 | 观察什么 | 状态 | 关系 | 来源 | 关键批判 |
|---|---|---|---|---|---|---|
| 因时机器人（Inspire） | 中 | RH56 灵巧手 6主动DoF,260触点(H1) | 商用,~$5.6k | 供应商 | inspire-robots.com | 重定向目标本体;渠道价差大 |
| 傅利叶（Fourier） | 中 | GR-2 手 12DoF,6路阵列触觉 | 商用,价未公开 | 供应商 | fftai.com | 重定向目标 |
| 灵心巧手/强脑（Linker/BrainCo） | 中 | 6–12DoF 灵巧手,部分带触觉 | 商用 | 供应商 | — | 重定向目标,国产梯队 |
| Shadow Robot | 其他 | Dexterous Hand 24DoF,120+传感器 | 英,~$100–150k | 供应商 | shadowrobot.com | 重定向目标上限;DoF从6到24差4倍,触觉语义难从人手迁移 |

