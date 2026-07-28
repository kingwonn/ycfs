#!/usr/bin/env python3
"""腿:techstack.html 与真源(techstack.json)同步(防陈旧/防手改)。

读【已提交】的 site/techstack.html(不重新生成),校验:
  1. 每个子系统的 choice 选型串出现在 HTML(改 techstack.json 不重生成即红)。
  2. 每个子系统的 id、layer 出现在 HTML。
  3. 子系统数出现在 HTML。
  4. 自包含(无外链)、明暗自适应。
输出末行 "结果: N 通过, M 失败"。
"""
import html
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
HTML = ROOT / "site" / "techstack.html"
T = ROOT / "m0" / "techstack.json"
PASSED = FAILED = 0


def check(c, n):
    global PASSED, FAILED
    if c: PASSED += 1
    else:
        FAILED += 1; print(f"  ✗ {n}")


def main():
    check(HTML.exists(), "site/techstack.html 存在(需先跑 build_techstack_html)")
    if not HTML.exists():
        print(f"结果: {PASSED} 通过, {FAILED} 失败"); sys.exit(1)
    # 生成器可导入(不覆盖盘上文件)
    r = subprocess.run([sys.executable, "-c",
                        "import sys;sys.path.insert(0,'m0');import build_techstack_html"],
                       cwd=ROOT, capture_output=True, text=True)
    check(r.returncode == 0, "build_techstack_html 可导入")
    h = HTML.read_text(encoding="utf-8")
    t = json.loads(T.read_text(encoding="utf-8"))

    check("<!doctype html>" in h.lower(), "合法 HTML")
    check("prefers-color-scheme" in h, "明暗自适应")
    check("http://" not in h and "https://" not in h, "自包含无外链")

    subs = t["subsystems"]
    for s in subs:
        for field in ("id", "layer", "choice"):
            token = html.escape(str(s[field]))
            check(token in h, f"{s['id']} 的 {field}「{s[field]}」在 HTML(否则陈旧)")

    check(f"{len(subs)} 项" in h or f"{len(subs)} 个" in h,
          f"子系统数 {len(subs)} 在 HTML")

    print(f"结果: {PASSED} 通过, {FAILED} 失败")
    sys.exit(0 if FAILED == 0 else 1)


if __name__ == "__main__":
    main()
