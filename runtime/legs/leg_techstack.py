#!/usr/bin/env python3
"""腿:平台/技术栈选型的溯源自洽(P14 落到实现选型上)。

守 m0/techstack.json:
  1. 每个子系统有:layer/choice/origin/reason/source/critique/serves,均非空。
  2. origin∈{first-principle,reference};first-principle 必有 basis∈N1-N6(在
     functions.json 里有定义);reference 必带 critique(P14:引用他家必批判)。
  3. 每个子系统至少列 2 个候选(options)——真选型必有被否的备选,否则是"钦定"。
  4. serves 指向的每个 id 都是 functions.json 里真实存在的功能(F*)或参数(P*),
     无孤儿(选型必须服务于某条已定义的功能/参数,不能自娱自乐)。
  5. 覆盖面:所有子系统的 serves 合起来覆盖 ≥8 个不同功能(选型确实撑起了功能定义)。
输出末行 "结果: N 通过, M 失败"。
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
T = ROOT / "m0" / "techstack.json"
F = ROOT / "m0" / "functions.json"
PASSED = FAILED = 0


def check(c, n):
    global PASSED, FAILED
    if c: PASSED += 1
    else:
        FAILED += 1; print(f"  ✗ {n}")


def main():
    check(T.exists(), "m0/techstack.json 存在")
    check(F.exists(), "m0/functions.json 存在(校验 serves 溯源)")
    if not (T.exists() and F.exists()):
        print(f"结果: {PASSED} 通过, {FAILED} 失败"); sys.exit(1)

    t = json.loads(T.read_text(encoding="utf-8"))
    fd = json.loads(F.read_text(encoding="utf-8"))
    subs = t["subsystems"]
    fps = fd["first_principles"]                       # N1-N6
    fids = {f["id"] for f in fd["functions"]}          # F*
    pids = {p["id"] for p in fd["params"]}             # P*
    valid_ids = fids | pids

    check(len(subs) >= 8, f"子系统数 {len(subs)} ≥ 8(选型覆盖够完整)")

    ids = [s["id"] for s in subs]
    check(len(ids) == len(set(ids)), "子系统 id 无重复")

    served_funcs = set()
    for s in subs:
        sid = s.get("id", "?")
        # 1. 承重字段非空
        for k in ("layer", "choice", "reason", "source", "critique"):
            check(bool(s.get(k)), f"{sid} 有非空 {k}")
        # 2. origin 合法 + 溯源纪律
        check(s.get("origin") in ("first-principle", "reference"),
              f"{sid} origin 合法")
        if s.get("origin") == "first-principle":
            check(s.get("basis") in fps,
                  f"{sid} 第一性 basis {s.get('basis')} 在 N1-N6 有定义")
        else:  # reference
            check(bool(s.get("critique")),
                  f"{sid} 参考类必带 critique(P14 引用他家必批判)")
            check(bool(s.get("source")), f"{sid} 参考类必有 source")
        # 3. 至少两个候选(真选型有被否备选)
        check(len(s.get("options", [])) >= 2,
              f"{sid} 列 ≥2 候选(选型必有被否备选,非钦定)")
        # 4. serves 非空且每个 id 真实存在
        serves = s.get("serves", [])
        check(len(serves) >= 1, f"{sid} serves 非空(选型必服务某功能/参数)")
        for ref in serves:
            check(ref in valid_ids,
                  f"{sid} serves 的 {ref} 是真实功能/参数(无孤儿选型)")
            if ref in fids:
                served_funcs.add(ref)

    # 5. 覆盖面:选型合起来撑起 ≥8 个功能
    check(len(served_funcs) >= 8,
          f"选型覆盖 {len(served_funcs)} 个功能 ≥8({sorted(served_funcs)})")

    print(f"结果: {PASSED} 通过, {FAILED} 失败")
    sys.exit(0 if FAILED == 0 else 1)


if __name__ == "__main__":
    main()
