#!/usr/bin/env python3
"""腿:被测不能自证 —— 把最重要的那条铁律变成可执行的断言。

出处(历练→内力):本腿由 GATES/REALITY.jsonl 里一条真实逃逸催生 ——
"所谓 6 份人工基线实为旧系统凌晨脚本输出,3000+ 断言本质是一个自等式"。
现实抓到过一次,当时靠人的对抗性提问才发现。现在它变成永久断言。

守四条自证通道(任一打开,污染开始复利):

  1. 自等式:声明为真值锚的文件,不得与被测系统的输出字节相同或互为派生。
     (你的整栈最强结论若只是"复刻了自己某次输出",断言再多也是零信息。)
  2. 空头承诺:REALITY.jsonl 里已 close 的逃逸,其 landed_as 必须指向真实存在的断言。
     否则"已编码"是一句谎,逃逸被悄悄注销。
  3. 自产自销:被测系统不得既生产逃逸信号、又判定它已被解决——
     probe 来源的信号必须有非空 signal,且 close 动作必须留下可查的断言指向。
  4. 篡改趋势:scale_history 的哈希链必须完整。改历史让曲线好看 = 对自己的自证。

输出末行 "结果: N 通过, M 失败"。
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
ANCHORS = ROOT / "runtime" / "anchors.json"
REALITY = ROOT / "GATES" / "REALITY.jsonl"
SCALE = ROOT / "runtime" / "scale_history.jsonl"

PASSED = FAILED = 0


def check(cond, name):
    global PASSED, FAILED
    if cond:
        PASSED += 1
    else:
        FAILED += 1
        print(f"  ✗ {name}")


def jsonl(path):
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            try:
                out.append(json.loads(line))
            except Exception:
                pass
    return out


# ── 1. 自等式检测 ──────────────────────────────────────────────────
def check_tautology():
    if not ANCHORS.exists():
        # 没声明真值锚 → 无法检测自等式。这本身是一个缺陷,不是"通过"。
        check(False, "未声明真值锚(runtime/anchors.json)——自等式无法检测,"
                     "L0 真值没有出生证")
        return
    spec = json.loads(ANCHORS.read_text(encoding="utf-8"))
    anchors = spec.get("truth_anchors", [])
    outputs = spec.get("system_outputs", [])
    check(bool(anchors), "必须声明至少一个真值锚")

    def digest(rel):
        p = ROOT / rel
        return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None

    a_hashes = {rel: digest(rel) for rel in anchors}
    o_hashes = {rel: digest(rel) for rel in outputs}
    for arel, ah in a_hashes.items():
        check(ah is not None, f"真值锚必须存在: {arel}")
        for orel, oh in o_hashes.items():
            check(not (ah and oh and ah == oh),
                  f"自等式!真值锚与被测输出字节相同: {arel} == {orel}")
        check(arel not in outputs,
              f"真值锚不得同时被声明为被测输出: {arel}")

    for rel in anchors:
        meta = spec.get("provenance", {}).get(rel, {})
        for field in ("who", "when", "accepted_by"):
            check(bool(meta.get(field)),
                  f"真值锚缺出生证字段 {field}: {rel}")
        check(meta.get("generated_by_system_under_test") is not True,
              f"真值锚由被测系统生成 = 自等式: {rel}")


# ── 2/3. 逃逸不得空头注销 ──────────────────────────────────────────
def check_escapes():
    rows = jsonl(REALITY)
    check(bool(rows), "历练台账不得为空——零现实信号=无外部锚")

    # 收集全仓真实存在的断言名(腿文件 + 其中的 check 描述)
    # 可执行检查不止住在 legs/:loop_audit.py 这类针对外部仓库的审计器住在 runtime/,
    # 同样是真实断言。扫描面窄会把真编码误判成空头注销(本条由一次误报催生)。
    existing = set()
    for d in [(ROOT / "runtime" / "legs"), (ROOT / "runtime")]:
        for f in d.glob("*.py"):
            existing.add(f.name)
            existing.add(f.stem)
    for r in rows:
        landed = r.get("landed_as")
        if not landed:
            continue
        target = landed.split("::")[0].strip()
        check(any(target in e or e in target for e in existing),
              f"landed_as 指向不存在的断言(空头注销): {r.get('id')} → {landed}")

    for r in rows:
        if r.get("source") == "probe":
            check(bool(r.get("signal")),
                  f"探针信号不得为空: {r.get('id')}")
        check(r.get("caught_by_assertion") is not None,
              f"信号必须声明断言是否抓到: {r.get('id')}")


# ── 4. 趋势不可篡改 ────────────────────────────────────────────────
def check_scale_chain():
    rows = jsonl(SCALE)
    if not rows:
        check(False, "修为刻度无历史——没有趋势就无法判断是否在原地踏步")
        return
    prev_hash = None
    for i, row in enumerate(rows):
        h = row.get("hash")
        if h is None:      # 哈希链引入前的行,跳过但记一次通过上限
            prev_hash = None
            continue
        body = {k: v for k, v in row.items() if k != "hash"}
        recomputed = hashlib.sha256(
            json.dumps(body, ensure_ascii=False, sort_keys=True).encode()
        ).hexdigest()[:16]
        check(recomputed == h, f"刻度第 {i+1} 行哈希不符——历史被改过")
        if prev_hash is not None:
            check(row.get("prev_hash") == prev_hash,
                  f"刻度第 {i+1} 行断链——中间有行被删/改")
        prev_hash = h


def main():
    check_tautology()
    check_escapes()
    check_scale_chain()
    print(f"结果: {PASSED} 通过, {FAILED} 失败")
    sys.exit(0 if FAILED == 0 else 1)


if __name__ == "__main__":
    main()
