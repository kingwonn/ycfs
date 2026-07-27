#!/usr/bin/env python3
"""腿:引用纪律(P14)——承重文档必须标来源,引用他家必须带批判。

守(对 practice/research/*.md、practice/route-*.md、PRODUCT*.md):
  1. 有来源标记:含 [有据] 或 [推断] 或 "Sources"/"出处"/"来源" 或 http 链接。
  2. 引用他家必带批判:含引用/竞品词(鹿明/UMI/π0/DexUMI/RDP/在位者/报告称…)的文档,
     必须同时含批判词(批判/局限/夸大/短板/未解/caveat/风险/存疑/边界),不许只吹不评。
  3. 推演类文档必带推导链:含"第一性/推论/公理/推演"的文档,必须也含来源或"理论"标记
     (推演不能凭空,要标依赖的理论)。
一个"只给结论不给来源"的承重文档 = 违反 P14 = 红。
输出末行 "结果: N 通过, M 失败"。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PASSED = FAILED = 0

# 承重文档:研究、技术路线、产品定义、关键设计
TARGETS = []
for pat in ["practice/research/*.md", "practice/route-*.md",
            "PRODUCT*.md", "m0/M0-*.md", "m2/data-availability.md",
            "m0/fixtures/prov_fixture.md"]:
    TARGETS += sorted(ROOT.glob(pat))

SRC_MARKS = ["[有据]", "[推断]", "Sources", "出处", "来源", "http"]
CITE_WORDS = ["鹿明", "松灵", "UMI", "π0", "GR00T", "DexUMI", "RDP", "ForceMimic",
              "TacUMI", "在位者", "报告称", "论文", "arXiv", "帕西尼", "光轮", "智元"]
CRIT_WORDS = ["批判", "局限", "夸大", "短板", "未解", "caveat", "风险", "存疑",
              "边界", "诚实", "不吹", "推翻", "缺口", "订正", "纠正", "已死", "出局"]
DERIV_WORDS = ["第一性", "推论", "公理", "推演", "倒推"]


def check(c, n):
    global PASSED, FAILED
    if c: PASSED += 1
    else:
        FAILED += 1; print(f"  ✗ {n}")


def main():
    check(len(TARGETS) > 0, "存在承重文档")
    for f in TARGETS:
        t = f.read_text(encoding="utf-8")
        rel = f.relative_to(ROOT)

        # 1. 有来源标记
        check(any(m in t for m in SRC_MARKS), f"{rel} 有来源标记([有据]/出处/链接)")

        # 2. 引用他家必带批判
        cites = [w for w in CITE_WORDS if w in t]
        if len(cites) >= 2:  # 确实在讲他家方案
            check(any(w in t for w in CRIT_WORDS),
                  f"{rel} 引用他家({','.join(cites[:3])}…)必须带批判分析")

        # 3. 推演类必带依据
        if any(w in t for w in DERIV_WORDS):
            check(any(m in t for m in SRC_MARKS) or "理论" in t or "依据" in t,
                  f"{rel} 含推演,须标理论依据/来源(推演不能凭空)")

    print(f"结果: {PASSED} 通过, {FAILED} 失败")
    sys.exit(0 if FAILED == 0 else 1)


if __name__ == "__main__":
    main()
