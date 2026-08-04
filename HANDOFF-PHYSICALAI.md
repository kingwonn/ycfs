# HANDOFF — 数采设备项目移交 physicalai 仓库

> 分拆决定:**physicalai = 战场**(UMI 力觉数采,目标外部、裁判外部);
> **ycfs = 法律库**(言出法随,只通过判例回流生长,gate 冻结在核心诚实腿)。
> 顺序:①本文+脚本入 ycfs(不删任何东西,ycfs 保持全绿)→ ②新 session 在
> physicalai 跑迁移、验绿、推送 → ③确认后回 ycfs 做清理提交(删设备资产+裁腿)。
> 两仓接口 = 判例回流:physicalai 打完仗,把"哪条纪律有用/哪条是仪式"一行写回
> ycfs 的 PRECEDENTS/REALITY;不回流资产。

---

## 一、迁移清单(ycfs → physicalai,保持相对路径)

**产品文档**:PRODUCT.md · PRODUCT-MATRIX.md · PRODUCT-SPEC.md · FUNCTION-SPEC.md ·
TECH-STACK.md · ROADMAP.md · VENDOR-LANDSCAPE.md · WATCHLIST.md · PROFILES.md ·
PROFILE-DIMENSIONS.md · FIRST-PRINCIPLES.md · WHAT-IS-VERIFIED.md

**数据与引擎**:`m0/` 全部(functions/techstack/roadmap/watchlist/profiles/bom 各 json、
cert.py、tradeoff.py、build_*.py、fixtures)· `m2/` 全部(ablation 框架+数据可得性)·
`practice/` 全部(research 路线调查+routes 评分)

**站点与发布**:`site/` 全部(index/product/spec/techstack/roadmap/watchlist/prompts)·
`.github/workflows/pages.yml`(注意:workflow 里触发分支要改成 physicalai 的分支名)

**验证器实例(设备腿,11 条)**:`runtime/gate.py` + `runtime/legs/` 中
leg_pipeline / leg_tradeoff / leg_dashboard / leg_ablation / leg_bom / leg_provenance /
leg_functions / leg_spec / leg_techstack / leg_techstack_html / leg_roadmap /
leg_roadmap_html + `runtime/negative_controls.json` 中对应条目 + 核心四腿一并带走
(outbound/choke-point/secret-scan/no-self-certification 是通用诚实件,设备仓照用),
即 **runtime/ 整目录复制**,设备仓落地即 16/16 绿,之后按需增删。
floor.lock.json 一并带走(棘轮基线延续);gate_history.jsonl 可不带(从零记)。

**不迁移**:PRECEDENTS.md、GATES/、DIGEST.md、BACKLOG.md、docs/(方法论,留 ycfs)。

## 二、迁移脚本(在新 session 里跑)

```bash
# 前提:两仓都在本地(ycfs 只读即可),physicalai 已开好工作分支
SRC=/path/to/ycfs      # 例 /workspace/ycfs 或克隆处
DST=/path/to/physicalai

cd "$DST"
for p in PRODUCT.md PRODUCT-MATRIX.md PRODUCT-SPEC.md FUNCTION-SPEC.md \
         TECH-STACK.md ROADMAP.md VENDOR-LANDSCAPE.md WATCHLIST.md \
         PROFILES.md PROFILE-DIMENSIONS.md FIRST-PRINCIPLES.md \
         WHAT-IS-VERIFIED.md m0 m2 practice site runtime; do
  cp -r "$SRC/$p" "$DST/"
done
mkdir -p .github/workflows && cp "$SRC/.github/workflows/pages.yml" .github/workflows/
rm -f runtime/gate_history.jsonl        # 历史从零记
# 手工两处:1) pages.yml 的 branches 改成本仓分支;2) 如与本仓已有 CLAUDE.md 冲突,合并说明
pip install numpy scikit-learn
python3 runtime/gate.py && python3 runtime/gate.py --selftest   # 必须 16/16 + 对照全绿
```

## 三、新 session 开场 prompt(直接粘贴)

```
本仓(physicalai)从本轮起以「UMI 力觉数采设备/数据业务」为唯一目标。
产品全部资产已按 kingwonn/ycfs 仓 HANDOFF-PHYSICALAI.md 迁入(若未迁,先按该文件
第二节脚本迁移并验证 gate 16/16 绿)。

读三份文件建立上下文,按优先级:
1. FIRST-PRINCIPLES.md —— 公理→定理→行动;当前在 Step 0。
2. WHAT-IS-VERIFIED.md —— 诚实账本:每条主张的证据等级与外部裁判;禁止把
   内部一致说成已验证。
3. PROFILES.md / WATCHLIST.md —— 75 家竞品/客户/供应商七维深扒。

当前最高优先任务 = FIRST-PRINCIPLES Step 0(一张 GPU 卡,2-4 周):
① M2a 复现:RDP(github.com/xiaoxiaoxh/reactive_diffusion_policy)/DexUMI 公开
  数据+代码,复算「含力 vs 关力」;裁判=他们的代码;复现不出→力有用存疑,停。
② 标定 vs 相对信号消融(全行业无人做过):在 RDP/RH20T 带力数据上对比
  (a)标定牛顿通道 (b)逐台加随机增益/偏置/非线性的「未标定」版
  (c)相对信号+per-device 适配器 的下游策略性能与跨设备汇聚性;
  裁判=固定协议;(c)≈(a)→标定溢价不成立,产品退回触觉阵列定位。
并行零硬件任务 = Step 1:LeRobot force/tactile 模态扩展 RFC + 参考实现 +
RLDS/HDF5 双向转换器。

纪律(从 ycfs 继承的三条,不多带):
- P14:引用他家必带出处+批判;推演必标理论依据;
- 证据分级:每条主张标【实】/【口】/【推】;
- 外部裁判:每步带裁判(非自己)与杀死条件;内部一致≠正确。
打完每一仗,把「哪条纪律起了作用/哪条是仪式」以一行判例回流 ycfs 的
PRECEDENTS/REALITY。
```

## 四、ycfs 侧清理(移植确认后,回 ycfs 做)

1. 删除已迁移的设备资产(上表全部);
2. `runtime/gate.py` LEGS 裁回核心四腿(outbound/choke-point/secret-scan/
   no-self-certification);`negative_controls.json` 同步删设备条目;
   `floor.lock.json` 删除对应腿条目——**这是结构性下调,必须在同一提交里
   与资产删除绑定,git 历史留痕**(符合"下调只能人手改且留痕"的铁律);
3. BACKLOG 清掉 M0/M2 卡(随战场走);DIGEST 记一行"分拆"判例;
4. ycfs 从此的生长方式 = 判例回流;成功标准 = "有这套纪律 vs 没有,外部项目
   的裁判通过更快、错误被抓更多吗"(可判决)。

## 五、风险与防线

- **窗口期数据丢失**:清理(第四节)必须等新仓 gate 验绿+推送确认后再做;
- **ycfs 复发自指**:宪法一条——ycfs 不再为自己新增任何腿/仪式,只收判例;
- **观察列表断更**:watchlist/profiles 随战场迁走,月度刷新在 physicalai 做。
