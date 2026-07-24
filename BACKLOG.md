# BACKLOG — 任务卡(唯一计划真源)

> 无时间线。只有优先级(自上而下)、状态、依赖、机器可查的验收。

状态:`ready` 可做 | `in-progress` 进行中 | `blocked-on-human` 等人 | `done` 验收已过 | `dropped` 放弃(留理由)

---

## Lane R · 把方法论落成可跑的运行时(源自 docs/tech-radar-2026.md 路线图)

### R1 · 对外单点 + deny-by-default hook 层
- 状态:`done`(R1 轮。`python3 runtime/gate.py` 3 腿全绿:行为 50/0、结构 14/0、密钥扫描 16 文件 0 命中;hook 冒烟 4 拒 1 放全部符合预期。关键决策:执法层源码含检测样本串,静态扫描豁免 legs/hooks 并把豁免集合本身锁进断言——改宽即腿红。)
- 原话:"我希望能帮助我快速完成AI native的言出法随" / "能否做到"
- 翻译:把雷达路线图①做成仓库内可跑的参考实现:对外动作唯一 choke-point(状态机上不存在绕过人审的边)+ Claude Code PreToolUse deny-by-default hook + 一条命令可跑的 gate。
- 依赖:无
- 验收(机器可查):
  - `python3 runtime/gate.py` 全绿退出 0,任一腿红退出非零
  - 对外状态机测试:N 条被篡改载荷**必全判红**、N 条已审批真载荷**零误伤**;无审批文件即硬阻断
  - 静态腿:choke-point 唯一(全仓库仅一个 `release`);`outbound.py` 无任何时间基放行(无 `time`/`sleep`);policy `default=deny`
  - hook 拒绝:agent 写 `GATES/APPROVALS/`、改 `runtime/policy.json`(法只能人改)、跑对外命令/自批 `approve`
- 证伪/回退:若存在一条到对外、不穿 choke-point 的路径,或存在自动放行 → 本卡方案证伪;回退成本近零(纯新增文件,删目录即回退)。

### R2 · 生成者 ≠ 批准/合并者 分支保护不变量
- 状态:`ready`
- 翻译:分支保护规则 + CI 检查:PR 作者身份 ≠ 合并者身份;agent 身份无 merge 权;提交前密钥扫描硬停(gate 已含腿,需接 CI)。
- 依赖:R1;仓库托管方分支保护配置(需人操作,见 GATES)
- 验收:CI 上模拟"作者=合并者"的合并请求被拒退非零。

### R3 · L1 出口双门:确定性数字校验 + 异模蕴含核验
- 状态:`ready`
- 翻译:对外数字与确定性重算(代码/SQL 对源)不符即硬阻断;承重句+溯源 chunk 过本地异模核验器,低于阈值转 PENDING_HUMAN。
- 依赖:R1(核验挂在 choke-point 上);需要一个真实项目的真源(见 GATES 事实核实)
- 验收:property 对抗集 N 条篡改全判红、N 条真值零误伤;阈值只紧不松写进常量。

### R4 · EARS 验收字段 + strict schema 门禁
- 状态:`ready`
- 翻译:BACKLOG 卡验收字段 lint:必须 EARS 句式且能派生确定性测试,否则 gate 拒收;人签字后才作真值锚。
- 依赖:无
- 验收:gate 新增 backlog-lint 腿;含一条非 EARS 验收的卡时 gate 红。

### R5 · L5 校准统计化 + human-human 归一化
- 状态:`ready`
- 翻译:judge 一致率带 95% CI + 聚类标准误;对 human-human 一致率归一化;面板聚合取最严。
- 依赖:R3;需要真人盲标基线(人力,见 GATES)
- 验收:校准脚本对给定标注集输出 CI;CI 下界跌破阈值退非零。

---

## 卡片纪律

- 一张卡 = 一小块**可验证**增量。做不完拆小,别攒大卡。
- 验收必须机器可查。写不出机器验收的卡,先想清楚"怎么算做对了",再落卡。
- `blocked-on-human` 的卡不空转等待:跳过做下一张,每轮 DIGEST 持续报告卡点未解除。
- 完成才标 `done`;验收没 100% 过不标 done,不放宽验证器、不造数据。
