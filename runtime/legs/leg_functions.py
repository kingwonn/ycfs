#!/usr/bin/env python3
"""腿:功能→参数定义的溯源自洽(P14 落到功能定义上)。

守 m0/functions.json:
  1. 每个功能有溯源:origin∈{first-principle,reference};first-principle 必有 basis∈N1-N6,
     reference 必有 source。
  2. 参考类功能(reference)必带 critique(P14:引用他家必批判)。
  3. 每个参数 traces_to 一个真实存在的功能 id(无孤儿参数)。
  4. 每个参数有 source 与 critique(承重定义必带边界)。
  5. 值不与 cert 阈值矛盾:同步误差参数(P9)≤ cert THRESHOLDS.sync_error_p99_ms。
  6. 每个 first-principle basis 引用的 N 标签在 first_principles 里有定义。
输出末行 "结果: N 通过, M 失败"。
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
F = ROOT / "m0" / "functions.json"
PASSED = FAILED = 0


def check(c, n):
    global PASSED, FAILED
    if c: PASSED += 1
    else:
        FAILED += 1; print(f"  ✗ {n}")


def main():
    check(F.exists(), "m0/functions.json 存在")
    if not F.exists():
        print(f"结果: {PASSED} 通过, {FAILED} 失败"); sys.exit(1)
    d = json.loads(F.read_text(encoding="utf-8"))
    fps = d["first_principles"]
    funcs = d["functions"]
    params = d["params"]
    fids = {f["id"] for f in funcs}

    check(len(funcs) >= 8, f"功能数 {len(funcs)} ≥ 8(功能定义够完整)")

    for f in funcs:
        fid = f["id"]
        check(f.get("origin") in ("first-principle", "reference"),
              f"{fid} origin 合法")
        if f.get("origin") == "first-principle":
            check(f.get("basis") in fps, f"{fid} 第一性 basis {f.get('basis')} 有定义")
        else:  # reference
            check(bool(f.get("source")), f"{fid} 参考类必有 source")
            check(bool(f.get("critique")), f"{fid} 参考类必带 critique(P14 引用必批判)")
        # 所有功能都要有 statement 与 source
        check(bool(f.get("statement")), f"{fid} 有 statement")
        check(bool(f.get("source")), f"{fid} 有 source")

    # 参数:溯源到真实功能 + 有 source/critique
    for p in params:
        pid = p["id"]
        check(p.get("traces_to") in fids,
              f"{pid} traces_to {p.get('traces_to')} 是真实功能(无孤儿参数)")
        check(bool(p.get("source")), f"{pid} 有 source")
        check(bool(p.get("critique")), f"{pid} 有 critique(承重参数带边界)")
        check(p.get("value") is not None and p.get("unit"), f"{pid} 有值与单位")

    # 每个功能至少被一个参数覆盖(除纯软件功能 F7/F8/F9/F10 可无数值参数)
    covered = {p["traces_to"] for p in params}
    hw_funcs = {"F1", "F2", "F3", "F4", "F5", "F6"}
    for fid in hw_funcs:
        check(fid in covered, f"{fid} 至少有一个核心参数覆盖")

    # 值不与 cert 阈值矛盾
    sys.path.insert(0, str(ROOT / "m0"))
    from cert import THRESHOLDS
    sync_params = [p for p in params if p["traces_to"] == "F4"]
    for p in sync_params:
        # P9 铺量档目标(取值 5)应 ≤ 证书阈值
        if isinstance(p["value"], (int, float)):
            check(p["value"] <= THRESHOLDS["sync_error_p99_ms"],
                  f"{p['id']} 同步目标 {p['value']}ms ≤ 证书阈值 "
                  f"{THRESHOLDS['sync_error_p99_ms']}ms")

    print(f"结果: {PASSED} 通过, {FAILED} 失败")
    sys.exit(0 if FAILED == 0 else 1)


if __name__ == "__main__":
    main()
