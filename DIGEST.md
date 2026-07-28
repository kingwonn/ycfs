# DIGEST — 每轮一行(人的唯一必读)

| 轮 | 卡 | 做了什么 | 验收 | 卡点/下一步 |
|---|---|---|---|---|
| R0 | — | 技术雷达 2026:8 视角互盲调研+敌对验证,落 docs/tech-radar-2026.md,派生 R1-R5 卡 | 敌对验证 8/8 过审(剔 2 条、订正 7 处) | 下一步 R1 |
| R1 | R1 | 对外门禁参考实现:choke-point 状态机 + deny-by-default policy + PreToolUse hook + 可跑 gate | ✅ gate 3 腿全绿(50/0 + 14/0 + 16 文件 0 命中) | R2 需人配分支保护(见 GATES);R3 需真实项目真源 |
| R2 | 接手 | 交接会话2.5h零推送判异常,本会话接手产出 spec-v0.md(设备规格,每项带机器验收,直面P13三条证伪)+ outreach.md(两问脚本+6触点名单) | ✅ gate 4/4;证伪条件3条各直面 | 交接失败已入REALITY;下一步领土接触(Q1力/触觉买家 Q2卡格式还是质量) |
| R3 | 纠偏 | 用户判 spec-v0 敷衍(决策全推给验证)。产出 product-definition.md:三押注押明(力/触觉在配/硬同步≤1ms/双格式交付)+ 数据价值五项量化 + BOM ¥7.3k + 剃刀刀片模式 + 12周路线图 + North-star 验收 | ✅ gate 4/4;每押注带证伪与退路 | M0 样机 8 周;M2 领土验证并行不阻塞 |
| R4 | 定义 | data-product-spec.md:大脑第一性(N1-N6)→UMI 根本需求(R1-R5)→数据 schema(每字段带为什么)→设备参数表(每参数带服务对象与不达标后果)+ 参数否决线 4 条 + 原因分析总图;M0 拆 5 卡入 BACKLOG | ✅ gate 4/4;每参数可向上追责 | 下一轮 M0-1 同步总线 + M0-4 管线骨架(可并行) |
| R5 | M0-4 | 调查 4 路并行出发(力觉买家/采集运营/形态与在位者/采购行为);同时落 m0/ 管线骨架:证书计算器十项(好批必过/坏批必被抓,同步指标区分0.5ms与25ms差一个量级)+ LeRobot v3 形状打包器 + pipeline 腿接入 gate | ✅ gate 5/5;阴性对照 5/5(新对照:偷偷放宽同步阈值→必红) | loader 验收待样机环境;调查回来后合成完整产品定义 PRODUCT.md |
| R6 | PRODUCT | 四路调查全合成为 PRODUCT.md:七步推理链+三押注(计量标定力/可审计证书/部署傻瓜化,各带证伪退路)+ 参数表按调查更新(可靠性升一级/VIO傻瓜化/力计量标定)+ 风险总账6条+North-star具体化 | ✅ gate 5/5;三处纠错入台账 | 最致命风险=跨本体力迁移,M2-1 先于造设备验(不需硬件) |
| R7 | 矩阵 | 6 路技术路线穷举调查并行(触觉/力测量/位姿+同步/动作标签+视觉);同时落 m0/tradeoff.py 选型决策矩阵引擎(7维加权、缺项记null不蒙混、三档权重flagship/volume/dexterous)+ leg_tradeoff 接gate | ✅ gate 6/6;阴性对照6/6(新:忽略权重必红) | 调查回来填 practice/routes/*.json,自动出产品矩阵 |
| R8 | 矩阵 | 4路技术路线穷举全回库(触觉8条/力9条/位姿7+同步4/动作5+视觉5),各落 practice/research/route-0*.md;填 practice/routes/*.json 喂决策矩阵;跑出三档产品选型;合成 PRODUCT-MATRIX.md(3机型×4模态+roadmap) | ✅ gate 6/6;tradeoff腿164断言;4处纠错入台账 | 铺量档Go先做(M0);M2跨本体力迁移仍是最致命验证 |
| R9 | HTML | 产品定义可视化:m0/build_dashboard.py 从 routes/*.json 经引擎实时算出→site/product.html(三档产品+模态得分条+roadmap+风险表,自包含明暗自适应);dashboard腿绑死HTML与引擎。阴性对照抓到首版"每次重生成=验不出陈旧"缺陷并修正 | ✅ gate 7/7;阴性对照7/7 | M2跨本体力迁移脚手架 |
| R10 | M2 | 跨本体力迁移验证骨架:m2/ablation.py 力消融框架(同/跨本体×有力/无力,合成contact世界力+0.10跨本体保留、null世界-0.01正确识别噪声)+ leg_ablation接gate锁判别力;m2/README写死判决规则与诚实边界;数据可得性调查并行 | ✅ gate 8/8;阴性对照8/8 | 等调查确认公开真机力数据集,接入替换合成 | 
| R11 | M2裂 | 数据可得性调查回库:M2劈成两半——M2a力有没有用(RDP/DexUMI公开可验,多篇+33~54pp一致)/ M2b力能否跨本体(硬缺口:最大跨本体数据全纯视觉无力,唯DexUMI双手小规模)。产品头号风险恰落在验不了那半。更新PRODUCT风险表+North-star,BACKLOG拆M2a/M2b卡 | ✅ gate 8/8 | M2a可立即做(下RDP);M2b需自采强证据=与"要不要造设备"绑定 |
| R12 | M0-1+P14 | M0-1同步总线设计+可下单BOM(¥120≤150预算,leg_bom 16断言);P14引用纪律落判例+leg_provenance(承重文档必标来源、引用他家必带批判),首跑抓9处自己违规(路线文档丢链接)已补;删重复文档;fixture化阴性对照 | ✅ gate 10/10;阴性对照10/10 | M0-1可下单;M2a待算力 |
| R13 | 功能定义 | FUNCTION-SPEC.md产品功能定义(10功能:4第一性推演N1-N6+6参考他家,各带出处+批判)→核心参数(13项,每个溯源到功能+值+来源+批判);结构化真源functions.json;leg_functions 107断言(功能有源/参考必批判/参数无孤儿/值不悖cert);FUNCTION-SPEC入provenance | ✅ gate 11/11;阴性对照11/11(孤儿参数必红) | 全程P14合规;下一步M0-2相机VIO选型 |
| R14 | review+HTML | 参数完整性review:补12参数(力分辨率/夹爪行程/编码器/IMU率/续航/存储/开机/标定偏差/照度/语言标注/带宽/触觉/知情同意)+2功能(F11现场运行/F12合规),标新增与仍out-of-scope理由供Codex审;spec.html(功能参数表+完整性review+每轮prompt折叠日志R0-R29);leg_functions 188断言+leg_spec绑死HTML与真源 | ✅ gate 12/12;阴性对照12/12 | 供Codex批判性分析 |
| R15 | 选型+发布 | 平台/技术栈选型:10子系统S1-S10(固件Zephyr/算力分档/VIO OpenVINS/管线LeRobot/IK Pinocchio/协议USB-COBS/质检numpy/App CLI→Tauri/传感CoinFT·PaXini/CI ycfs-gate),各🧬第一性或📎参考+出处+批判(P14),serves溯源到真实功能;techstack.json+TECH-STACK.md+techstack.html;leg_techstack 130断言+leg_techstack_html绑死。直面"为何没做Artifact/Pages":此前只SendUserFile发文件;新增.github/workflows/pages.yml(先跑gate红则不发→重生成无diff→仅main部署)+site/index.html总览页 | ✅ gate 14/14;阴性对照14/14 | Pages启用待人配(PENDING_HUMAN #7);Artifact本轮发布 |
| R16 | 三代roadmap | 代际=时间层(区别于并发SKU):G1立足(铺量Go,消R_COMMERCIAL,📎)→G2差异化(旗舰Pro+自采跨本体力,消致命R_XEMBODIMENT,🧬N6,含北极星)→G3平台/服务(消R_SCALE,🧬N3,**按G2力迁移判决分叉**Fork A通用库+灵巧手/Fork B现采现标)。每代押注+证伪+退路(不骑墙)+准入依赖上代出口;roadmap.json+ROADMAP.md+roadmap.html;leg_roadmap 93断言(守代际递进/证伪≠退路/de_risks无孤儿/G3必分叉)+leg_roadmap_html绑死;index加第4卡 | ✅ gate 16/16;阴性对照16/16 | G2的M2b自采验证是生死手,与"造设备"绑定 |
