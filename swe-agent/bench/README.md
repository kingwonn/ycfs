# bench — agent 评测基准套件(K1)

> 回答首席工程师的灵魂拷问:「你怎么证明这个助手是好的?」
> 这也是 L4 覆盖增长的校准基线:agent 改版后必须重跑,通过率只准升不准降(棘轮)。

## 三类题

| 类型 | 真值从哪来(出生证) | 判定 |
|---|---|---|
| `bug_fix/` 埋 bug 修复题 | **构造即真值**:bug 是我们亲手埋的,判定测试向量在埋 bug 前对参考实现全绿 | 编译 + 确定性测试向量,布尔 |
| `spec_qa.jsonl` 规格/领域 QA | 公开文档事实,**每题带来源 URL 与核实轮次**(本仓库调研留痕) | 字符串/数值精确比对 |
| `plan_review.jsonl` RFP→方案判断题 | 占位:等真实 RFP 素材与人工基线(Q2/Q5) | 待定 |

## 铁律(被测不能自证)

1. **题目真值永不来自被测 agent 的输出。** bug_fix 的真值锚 = 参考实现 + 测试向量;spec_qa 的真值锚 = 公开文档。
2. `run_bench.py --self-check` 含**字节同源探针**:参考答案文件与被测产物同源(哈希相同)即判无效。
3. `manifest.sha256` 锁定全部真值文件哈希——真值被改动时 self-check 变红(防"改题凑分")。
4. 通过率**只准升不准降**:回归即红,不许删题凑分(题数下限写进 gate)。

## 用法

```bash
python3 run_bench.py --self-check   # 题目质量自检(gate 的 bench-self-check 腿跑这个)
python3 run_bench.py --list         # 列出全部题目与出生证
# agent 跑分模式(M1 执行脊柱落地后接入):对每道 bug_fix 题,把 buggy 源交给 agent 修复,
# 用本套件判定;输出通过率 JSON 落 observability。
```

## 自检都查什么

- 每题 manifest 含完整出生证(构造者/日期/真值锚/来源)。
- bug_fix:参考实现 + 测试 = **必须全绿**(题目本身可判);buggy + 测试 = **必须变红**(bug 可检出,不是废题)。
- 真值哈希与 manifest.sha256 一致。
- spec_qa:schema 完整,provenance 的 URL 非空。
