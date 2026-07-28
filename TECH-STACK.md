# TECH-STACK — 平台与技术栈选型

> **这是叙事层**;结构化真源在 `m0/techstack.json`,渲染页在 `site/techstack.html`,
> 由 `techstack` / `techstack-html` 两条门禁腿守住(改选型不重生成 HTML 即红)。
> 选型只回答"用什么实现**已定义**的功能(FUNCTION-SPEC / functions.json 的 F1-F12)",
> **不新增需求**。每条选型按 P14 标注:🧬第一性/方法论推演给理论依据,📎参考他家给出处 + 批判。
>
> 推导链:六条第一性数据要求 N1-N6 → 12 功能 → 27 参数 → **10 个实现子系统 S1-S10** → `ycfs gate` + CI 守。

---

## 选型的第一性约束(为什么栈长这样)

不是先挑喜欢的语言,而是先认约束,栈是被约束逼出来的:

1. **确定性采样与统一时基必须在无 OS 抖动的层做**(推演自 N1 时间对齐;来源:实时系统常识——Linux 用户态调度抖动进标签噪声)。→ 逼出 S1(RTOS 固件)、S6(带 µs 戳的固件↔主机协议)。这两块**不能**用 Python/Linux 用户态实现,是硬约束。
2. **最适配 = 客户零接入工程**(推演自 N2 数据可用性 / P13 客户是具身大脑厂商)。→ 逼出 S4 原生 LeRobot 而非"给个转换脚本"。语言层被买方生态(PyTorch/HuggingFace)钉死。
3. **傻瓜化 = 开机即采、当场质检**(参考 route-03 对原版 UMI"离线采完才知成败"的批判)。→ 逼出 S2 板载算力分档、S3 实时增量 VIO(非离线 SLAM)、S8 操作端 App、S7 机上质检。
4. **被测不能自证**(YCFS 铁律)。→ 逼出 S10:整套定义靠验证器守,CI 在受保护面重跑门禁。

选型 = 在每条约束下,列候选、比、给出被否的备选。**没有备选的选型是"钦定",`techstack` 腿要求每个子系统 ≥2 候选。**

---

## 🧬 从第一性/方法论推演的选型

### S1 · MCU 固件(采样与时基)→ **C/C++ + Zephyr RTOS**(备选裸机 HAL)
- **候选**:裸机 STM32 HAL(最简,时序手控)/ Zephyr RTOS(多传感器调度+设备树+USB 栈)/ Arduino(生态大但实时性差)。
- **理由**:统一时基不能在有调度抖动的层做(N1)。RTOS 给多传感器并发调度 + 成熟 USB CDC 栈,优于裸机手撸;Arduino 实时性不够,排除。
- **来源**:推演自 N1;Zephyr 是开源 RTOS 事实标准之一(嵌入式实时惯例,理论依据=确定性调度)。
- **⚠ 批判**:Zephyr 学习曲线陡;若最终时序极简,裸机 HAL 反而更可控——**这是一条会随样机实测翻案的选型**,不是定论。

### S6 · 固件↔主机协议 → **USB CDC + COBS 带戳帧**(备选 protobuf/nanopb)
- **候选**:USB CDC + 自定义 COBS 帧(轻,带 MCU µs 戳)/ protobuf/nanopb(结构化但开销)/ 以太网+PTP(精度高但笨重)。
- **理由**:多流带统一时基戳传主机(N1);COBS 成帧轻、可靠、易解析。
- **来源**:推演自 N1;COBS 是串行成帧标准做法。
- **⚠ 批判 / 未解**:**P24 是未解风险**——力 500Hz×2 指 + IMU 1kHz + 相机 60fps 并发,USB 带宽够不够**必须样机实测**;以太网+PTP 能到 µs 级但违背便携。这是全栈里最可能推翻当前选型的一处。

### S7 · 质检/证书计算 → **Python + numpy**(已实现 `m0/cert.py`)
- **候选**:Python+numpy(已实现,十项证书)/ Rust(快但生态薄)/ C++(快但开发慢)。
- **理由**:证书是产品的一半(推演自 N4:同批一致性=模型可用性天花板);十项指标确定性可复算,numpy 足够;**已跑通并过 gate(pipeline 腿 31 断言)**。
- **来源**:推演自 N4;`m0/cert.py` 已实现。
- **⚠ 批判**:机上实时质检(F6)若跑在低算力板,numpy 可能要降采样或 C 重写;离线打包 numpy 绰绰有余。

### S10 · 构建/质量门/CI → **ycfs gate + GitHub Actions**
- **候选**:ycfs gate(本仓已有:棘轮+阴性对照+溯源)/ 纯 pytest(缺棘轮与自证防护)/ 无 CI(不可持续)。
- **理由**:整套产品定义靠验证器守住(被测不能自证);gate 已 14 腿,GitHub Actions 跑 gate = "门禁自跑门禁"。
- **来源**:推演自 YCFS 方法论(验证器分层 / 被测不能自证,理论依据=本仓 PRECEDENTS)。
- **⚠ 批判 / 已知风险**:**gate 自身住在 agent 可写域内**(见 `GATES/PENDING_HUMAN.md`)——必须由 CI 在受保护分支上跑,才是 agent 够不到的硬边界。当前只是"自己给自己上锁",不算数。

---

## 📎 参考已验证方案的选型

### S2 · 板载算力平台 → **分档:铺量=主机/手机;旗舰=Jetson Orin Nano**
- **候选**:主机 PC/手机(铺量,VIO 跑主机)/ Jetson Orin Nano(旗舰,板载 VIO+质检)/ 树莓派 5(便宜但无 GPU 算 VIO 吃力)。
- **理由**:傻瓜化要板载实时 VIO → 需算力;但铺量档为压成本可把 VIO 放主机/手机。旗舰档板载 Jetson。
- **来源**:参考 FastUMI Ego 板载算力路线(route-03);Jetson 是机器人边缘算力常见选择。
- **⚠ 批判**:Jetson 抬 BOM 与功耗、伤 P18 续航;树莓派 5 算 VIO 帧率不够。**板载 vs 主机正是铺量/旗舰的分界线**,不是一刀切。

### S3 · VIO/位姿软件 → **OpenVINS / VINS-Fusion(开源)起步**
- **候选**:OpenVINS(滤波 VIO,实时好)/ VINS-Fusion(优化 VIO,精度高)/ ORB-SLAM3(原版 UMI 用,离线)/ 商用模组(省事但 T265 已 EOL)。
- **理由**:傻瓜化要实时板载**增量 VIO 非离线 SLAM**(route-03 结论);OpenVINS 滤波式实时性好、开源可改。
- **来源**:OpenVINS(open-vins.github.io)、VINS-Fusion(HKUST-Aerial-Robotics);route-03 对离线 SLAM 的批判。
- **⚠ 批判**:纯 VIO 无回环,长轨迹漂移;鱼眼需改标定模型;商用 T265 已停产不选;**自研 VIO 固件工作量大**(M1 需实测带宽/漂移)。ORB-SLAM3 是原版 UMI 痛点(离线采完才知成败),明确不采。

### S4 · 数据管线语言与格式 → **Python + LeRobot v3 + pyarrow**
- **候选**:Python+LeRobot(买方生态,原生格式)/ Python+RLDS/TFDS(PI 大规模用)/ 自定义格式(灵活但客户要写解析=出局)。
- **理由**:最适配=客户零接入工程,买方训练管线在 LeRobot/PyTorch 生态(F7);要**原生 LeRobot 而非"给转换脚本"**。
- **来源**:LeRobot(HuggingFace;GR00T 原生用);PI 承认大规模用 RLDS(route-04)。
- **⚠ 批判**:PI 明说 LeRobot 可扩展性不足、大规模改用 RLDS → **须同时提供 RLDS 导出**,不能只押一个格式;Python 非实时,只做落盘/打包,**不做采样**(采样归 S1)。

### S5 · 在线 IK/可行性/重定向 → **Pinocchio(C++ 核 + Python 绑定)**
- **候选**:Pinocchio(快,解析导数,60Hz 可达)/ PyBullet(易用但 IK 慢)/ 自研解析 IK(FeasibleCap 路线,最快但每本体手写)。
- **理由**:F5 可行性反馈需 60Hz 在线 IK(P10);Pinocchio 是刚体动力学最快开源库之一,C++ 核满足实时,Python 绑定接管线。
- **来源**:Pinocchio(stack-of-tasks/pinocchio);FeasibleCap 用解析式(route-04)。
- **⚠ 批判**:Pinocchio 需 URDF 且各客户本体不同;自碰撞检查另需 FCL;解析式最快但每本体手写、不通用——**通用性与速度在这里要权衡**。

### S8 · 操作端 App(启停/实时质检显示)→ **CLI 起步 → 本地 Web(Tauri)**
- **候选**:CLI(最快出)/ 本地 Web·Tauri(轻,跨平台,可视化质检)/ 原生 App(体验好但每平台重做)/ Electron(重,内存大)。
- **理由**:F6 实时质检要给采集员看"当场提示重采";CLI 最快验证,Web/Tauri 做可视化;Electron 太重伤便携。
- **来源**:参考通用工具实践;Tauri 比 Electron 轻(Rust 核)。
- **⚠ 批判**:采集员非技术人员 → CLI 体验差,需尽快上可视化;但**过早做 App 会分散硬件精力**,起步 CLI 是务实取舍。

### S9 · 力/触觉采集 → **传感器 SDK(CoinFT 开源 / PaXini 电容)**
- **候选**:CoinFT 每指 6 轴(开源,2g,I2C/SPI)/ PaXini 电容六维(量产一致,商用 SDK)/ 视触觉 GelSight(信号丰富但 25-60fps 慢)。
- **理由**:F2 力/触觉是差异化核心(N6);铺量档 CoinFT 开源省成本,旗舰档 PaXini 电容一致性好(route-01/02 选型)。
- **来源**:CoinFT(coin-ft.github.io)、PaXini(paxini.com);route-01/02 技术路线调查。
- **⚠ 批判 / 订正**:CoinFT 带宽无公开数据、软硅胶低通存疑;PaXini 抬成本;**力标签只到牛顿级、非计量级**(route-02 已订正的物理上限——手持无固定基座测不了计量级)。

---

## 为什么此前没做成 Artifact / GitHub Pages(直面 R30 的追问)

**诚实回答**:此前每轮只用 `SendUserFile` 把 HTML **发文件**给你——那是本地文件,不是**可分享的托管页**,你要下载后本地打开,也没有稳定 URL。这是工具用法的欠缺,不是做不到。

**为什么现在能做,且该做**:
- **Pages**:选型链已经是"数据(`m0/*.json`)→ 生成器(`build_*_html.py`)→ 门禁绑死 HTML 与真源 → 部署"。缺的最后一环是 CI 发布。S10 选型接入 GitHub Actions 后,`.github/workflows/pages.yml` 先跑 `gate`(红则不发,保证发布的页与真源一致),再 build、再 `deploy-pages`。**这正好把"被测不能自证"落到发布面**:能上线的页,必然过了门禁。
  - **需人一次性操作**:仓库 Settings → Pages 把 Source 设为 "GitHub Actions"(管理员权限,agent 够不到)——已记入 `GATES/PENDING_HUMAN.md`。
  - **⚠ 批判**:从**功能分支**部署 Pages 受环境保护限制,正式对外应在受保护主分支发;当前工作流对分支可跑、产物可预览,主分支合入后才是稳定站点。
- **Artifact**:claude.ai 的 Artifact 是**默认私有、可选分享**的托管页,适合把 `spec.html` 这类审阅页直接给一个 URL。本轮同步发布一份 spec 的 Artifact 作为可分享入口;真源仍是仓库,Artifact 是快照视图。

---

## 选型的边界(不吹)

- **未解**:S6 的 USB 并发带宽(P24)——全栈最可能翻案处,待样机实测。
- **会翻案**:S1 裸机 vs RTOS、S3 自研 VIO 工作量,均需 M1 硬件回填数据后复评。
- **不通用**:S5 IK、S9 力标签均随客户本体/量程变化,不是一套打天下。
- **硬边界缺口**:S10 的 gate 现住在 agent 可写域,必须靠 CI + 分支保护(人配)才成硬边界。

> 出处汇总:route-01/02/03/04 技术路线调查(`practice/research/`)、FUNCTION-SPEC.md、`m0/functions.json`、YCFS PRECEDENTS(P13/P14)。推演类均标 N1-N6 / 方法论理论依据;参考类均带出处 + 批判。
