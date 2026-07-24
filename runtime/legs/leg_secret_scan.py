#!/usr/bin/env python3
"""腿:提交前密钥扫描(派发纪律"提交前跑密钥扫描硬停"的最小实现)。

扫 *.py/*.md/*.json/*.txt,自身与测试腿豁免(模式串在其源里作样本出现)。
输出末行 "结果: N 文件, M 命中";M≠0 即腿红。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SELF = Path(__file__).resolve()

PATTERNS = [
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    r"\bAKIA[0-9A-Z]{16}\b",
    r"\bghp_[A-Za-z0-9]{36}\b",
    r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b",
    r"\bsk-[A-Za-z0-9]{32,}\b",
]
EXEMPT_NAMES = {SELF.name, "leg_outbound_tests.py"}


def main():
    scanned, hits = 0, []
    for p in ROOT.rglob("*"):
        if ".git" in p.parts or p.suffix not in {".py", ".md", ".json", ".txt"}:
            continue
        if p.name in EXEMPT_NAMES:
            continue
        scanned += 1
        text = p.read_text(encoding="utf-8", errors="replace")
        for pat in PATTERNS:
            if re.search(pat, text):
                hits.append(f"{p.relative_to(ROOT)} ~ {pat}")
    for h in hits:
        print(f"  ✗ 疑似密钥: {h}")
    print(f"结果: {scanned} 文件, {len(hits)} 命中")
    sys.exit(0 if not hits else 1)


if __name__ == "__main__":
    main()
