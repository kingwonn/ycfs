#!/usr/bin/env python3
"""check_layers — 分层依赖检查(G3):platform/ 与 products/ 不得 include 芯片头。

规则(只紧不松):
  · platform/**、products/** 禁止 #include stm32*/core_cm*/cmsis*/*_hal_* —— 芯片知识只许住 bsp/hal。
  · 扫描文件数为 0 视为失败(防目录改名后静默空转)。
输出 JSON:{checked, violations:[...]}。作为 gate 的 layer-deps 腿。
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FW = os.path.dirname(HERE)

FORBIDDEN = re.compile(r'#include\s+["<](stm32|core_cm|cmsis|[\w/]*_hal_)', re.IGNORECASE)
SCOPES = ("platform", "products")


def scan_text(rel_path, text):
    """可测内核:返回该文件的违规行列表。"""
    out = []
    for ln, line in enumerate(text.splitlines(), 1):
        if FORBIDDEN.search(line):
            out.append(f"{rel_path}:{ln}: {line.strip()}")
    return out


def main():
    checked, violations = 0, []
    for scope in SCOPES:
        root = os.path.join(FW, scope)
        for dirpath, _dirs, files in os.walk(root):
            for fn in files:
                if fn.endswith((".c", ".h")):
                    p = os.path.join(dirpath, fn)
                    checked += 1
                    with open(p, encoding="utf-8") as f:
                        violations += scan_text(os.path.relpath(p, FW), f.read())
    ok = checked > 0 and not violations
    print(json.dumps({"checked": checked, "violations": violations}, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
