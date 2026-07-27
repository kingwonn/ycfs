#!/usr/bin/env python3
"""腿:力消融框架的判别力(M2 骨架必须能区分'力有用/无用')。

守:框架不能退化为"给什么数据都说力有用"。
  · contact 世界:力增益必须 > 0(同本体与跨本体)
  · null 世界:力增益必须 ≈ 0(|Δ| 小,不误报力有用)
一个"力永远显示有用"的框架 = 无判别力 = 不能用来做承重的产品决策。
输出末行 "结果: N 通过, M 失败"。
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "m2"))
from ablation import run_within, run_cross  # noqa

PASSED = FAILED = 0


def check(c, n):
    global PASSED, FAILED
    if c: PASSED += 1
    else:
        FAILED += 1; print(f"  ✗ {n}")


def main():
    # contact 世界:力应提升
    vo, vf = run_within("contact")
    d_contact = vf.mean() - vo.mean()
    check(d_contact > 0.03, f"contact 世界力应提升(Δ={d_contact:+.3f}>0.03)")

    cvo, cvf = run_cross("contact")
    check(cvf - cvo > 0.0, f"contact 世界力跨本体应保留(Δ={cvf-cvo:+.3f}>0)")

    # null 世界:力不应提升(判别力的关键——能识别力无用)
    nvo, nvf = run_within("null")
    d_null = nvf.mean() - nvo.mean()
    check(abs(d_null) < 0.05, f"null 世界力不应提升(|Δ|={abs(d_null):.3f}<0.05)")

    # 核心判别:contact 的力增益必须显著大于 null 的
    check(d_contact - d_null > 0.05,
          f"框架必须区分两世界(contact Δ {d_contact:+.3f} 应远大于 null Δ {d_null:+.3f})")

    print(f"结果: {PASSED} 通过, {FAILED} 失败")
    sys.exit(0 if FAILED == 0 else 1)


if __name__ == "__main__":
    main()
