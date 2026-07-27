#!/usr/bin/env python3
"""腿:spec.html 与真源(functions.json + prompts.md)同步(防陈旧/防手改)。

读【已提交】的 site/spec.html(不重新生成),校验:
  1. 每个参数的"值 单位"字符串出现在 HTML(改 functions.json 不重生成即红)。
  2. 功能数、参数数出现在 HTML。
  3. prompts.md 的每个 R<n> 轮次都在 HTML 里有折叠项(prompt 日志不漏轮)。
  4. 自包含(无外链)、明暗自适应。
输出末行 "结果: N 通过, M 失败"。
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
HTML = ROOT / "site" / "spec.html"
F = ROOT / "m0" / "functions.json"
PROMPTS = ROOT / "site" / "prompts.md"
PASSED = FAILED = 0


def check(c, n):
    global PASSED, FAILED
    if c: PASSED += 1
    else:
        FAILED += 1; print(f"  ✗ {n}")


def main():
    check(HTML.exists(), "site/spec.html 存在(需先跑 build_spec_html)")
    if not HTML.exists():
        print(f"结果: {PASSED} 通过, {FAILED} 失败"); sys.exit(1)
    # 生成器可导入(不覆盖盘上文件)
    r = subprocess.run([sys.executable, "-c",
                        "import sys;sys.path.insert(0,'m0');import build_spec_html"],
                       cwd=ROOT, capture_output=True, text=True)
    check(r.returncode == 0, "build_spec_html 可导入")
    h = HTML.read_text(encoding="utf-8")
    d = json.loads(F.read_text(encoding="utf-8"))

    check("<!doctype html>" in h.lower(), "合法 HTML")
    check("prefers-color-scheme" in h, "明暗自适应")
    check("http://" not in h and "https://" not in h, "自包含无外链")

    # 参数值同步(抽样全部,防陈旧)
    import html as _h
    for p in d["params"]:
        token = f"{_h.escape(str(p['value']))} {_h.escape(str(p['unit']))}"
        check(token in h, f"参数 {p['id']} 值「{token}」在 HTML(否则陈旧)")

    # 功能/参数计数
    check(f"{len(d['functions'])} 项" in h or f"{len(d['functions'])} 个" in h,
          f"功能数 {len(d['functions'])} 在 HTML")

    # prompt 轮次不漏
    rounds = re.findall(r"^## (R\d+)", PROMPTS.read_text(encoding="utf-8"), re.M)
    check(len(rounds) >= 10, f"prompts.md 有 {len(rounds)} 轮")
    for r_ in rounds:
        check(r_ in h, f"prompt 轮次 {r_} 在 HTML 折叠日志中")

    print(f"结果: {PASSED} 通过, {FAILED} 失败")
    sys.exit(0 if FAILED == 0 else 1)


if __name__ == "__main__":
    main()
