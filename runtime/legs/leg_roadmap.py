#!/usr/bin/env python3
"""腿:三代 roadmap 的决策自洽(代际递进 + 不骑墙 + 分叉纪律 + 溯源)。

守 m0/roadmap.json:
  1. 恰好 3 代,id 为 G1/G2/G3 且按序。
  2. 每代承重字段非空:name/horizon/tier/goal/bet/falsification/fallback/entry/exit
     /de_risks/critique,ships≥1,traces≥1。
  3. 不骑墙:falsification 与 fallback 都非空且**不相等**(有可裁决的证伪,且证伪触发后有
     明确退路——不是"两边都对"的和稀泥)。
  4. 溯源(P14):origin∈{first-principle,reference};first-principle 必有 basis∈N1-N6;
     reference 必有 source;两类都要 critique。
  5. de_risks 指向 risks 表里真实存在的风险(无孤儿风险)。
  6. traces 的每个 id 是真实功能(F*,functions.json)或子系统(S*,techstack.json)。
  7. 代际递进:G1.entry_depends_on 为空;G2 依赖 G1;G3 依赖 G2(每代被上一代出口设门,
     不是三个并行的猜)。
  8. G3 必分叉:fork_on=="G2";forks≥2,每支有 condition/product/business。
  9. 恰好一代标 north_star(北极星只有一个)。
输出末行 "结果: N 通过, M 失败"。
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
R = ROOT / "m0" / "roadmap.json"
F = ROOT / "m0" / "functions.json"
T = ROOT / "m0" / "techstack.json"
PASSED = FAILED = 0


def check(c, n):
    global PASSED, FAILED
    if c: PASSED += 1
    else:
        FAILED += 1; print(f"  ✗ {n}")


def main():
    for p in (R, F, T):
        check(p.exists(), f"{p.relative_to(ROOT)} 存在")
    if not (R.exists() and F.exists() and T.exists()):
        print(f"结果: {PASSED} 通过, {FAILED} 失败"); sys.exit(1)

    d = json.loads(R.read_text(encoding="utf-8"))
    fd = json.loads(F.read_text(encoding="utf-8"))
    td = json.loads(T.read_text(encoding="utf-8"))
    fps = fd["first_principles"]                       # N1-N6
    fids = {f["id"] for f in fd["functions"]}          # F*
    sids = {s["id"] for s in td["subsystems"]}         # S*
    valid_traces = fids | sids
    risks = d.get("risks", {})
    gens = d["generations"]

    # 1. 恰好 3 代且按序
    check(len(gens) == 3, f"恰好 3 代(实为 {len(gens)})")
    check([g["id"] for g in gens] == ["G1", "G2", "G3"], "代际 id 为 G1/G2/G3 且按序")

    ns_count = 0
    for g in gens:
        gid = g.get("id", "?")
        # 2. 承重字段非空
        for k in ("name", "horizon", "tier", "goal", "bet",
                  "falsification", "fallback", "entry", "exit", "critique"):
            check(bool(g.get(k)), f"{gid} 有非空 {k}")
        check(len(g.get("ships", [])) >= 1, f"{gid} ships ≥1")
        check(len(g.get("traces", [])) >= 1, f"{gid} traces ≥1")
        # 3. 不骑墙:证伪 ≠ 退路,且都非空
        check(bool(g.get("falsification")) and bool(g.get("fallback"))
              and g["falsification"].strip() != g["fallback"].strip(),
              f"{gid} 证伪与退路都在且不相等(不骑墙)")
        # 4. 溯源
        check(g.get("origin") in ("first-principle", "reference"), f"{gid} origin 合法")
        if g.get("origin") == "first-principle":
            check(g.get("basis") in fps, f"{gid} 第一性 basis {g.get('basis')} 在 N1-N6")
        else:
            check(bool(g.get("source")), f"{gid} 参考类必有 source")
        check(bool(g.get("critique")), f"{gid} 有 critique(P14)")
        # 5. de_risks 无孤儿
        check(g.get("de_risks") in risks, f"{gid} de_risks {g.get('de_risks')} 是真实风险")
        # 6. traces 真实
        for ref in g.get("traces", []):
            check(ref in valid_traces, f"{gid} traces 的 {ref} 是真实功能/子系统")
        # 9. north_star 计数
        if g.get("north_star"):
            ns_count += 1

    by_id = {g["id"]: g for g in gens}
    # 7. 代际递进
    check(by_id["G1"].get("entry_depends_on") in (None, "", "now"),
          "G1 无前置依赖(可立即启动)")
    check(by_id["G2"].get("entry_depends_on") == "G1", "G2 准入依赖 G1 出口")
    check(by_id["G3"].get("entry_depends_on") == "G2", "G3 准入依赖 G2 出口")

    # 8. G3 必分叉
    g3 = by_id["G3"]
    check(g3.get("fork_on") == "G2", "G3 按 G2 判决分叉(fork_on==G2)")
    forks = g3.get("forks", [])
    check(len(forks) >= 2, f"G3 分叉 ≥2 支(实为 {len(forks)})")
    for fk in forks:
        b = fk.get("branch", "?")
        for k in ("condition", "product", "business"):
            check(bool(fk.get(k)), f"G3 Fork {b} 有非空 {k}")

    # 9. 北极星恰一
    check(ns_count == 1, f"恰好一代标 north_star(实为 {ns_count})")

    # 每条风险至少被一代承接(风险台账无悬空)
    covered = {g.get("de_risks") for g in gens}
    for rk in risks:
        check(rk in covered, f"风险 {rk} 至少被一代承接")

    print(f"结果: {PASSED} 通过, {FAILED} 失败")
    sys.exit(0 if FAILED == 0 else 1)


if __name__ == "__main__":
    main()
