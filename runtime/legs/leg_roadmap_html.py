#!/usr/bin/env python3
"""腿:roadmap.html 与真源(roadmap.json)同步(防陈旧/防手改)。

读【已提交】的 site/roadmap.html(不重新生成),校验:
  1. 每代的 name 与 bet 出现在 HTML(改 roadmap.json 不重生成即红)。
  2. G3 每个 fork 的 condition 出现在 HTML(分叉不漏)。
  3. 代数出现在 HTML。
  4. 自包含(无外链 http)、明暗自适应。
输出末行 "结果: N 通过, M 失败"。
"""
import html
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
HTML = ROOT / "site" / "roadmap.html"
R = ROOT / "m0" / "roadmap.json"
PASSED = FAILED = 0


def check(c, n):
    global PASSED, FAILED
    if c: PASSED += 1
    else:
        FAILED += 1; print(f"  ✗ {n}")


def main():
    check(HTML.exists(), "site/roadmap.html 存在(需先跑 build_roadmap_html)")
    if not HTML.exists():
        print(f"结果: {PASSED} 通过, {FAILED} 失败"); sys.exit(1)
    r = subprocess.run([sys.executable, "-c",
                        "import sys;sys.path.insert(0,'m0');import build_roadmap_html"],
                       cwd=ROOT, capture_output=True, text=True)
    check(r.returncode == 0, "build_roadmap_html 可导入")
    h = HTML.read_text(encoding="utf-8")
    d = json.loads(R.read_text(encoding="utf-8"))

    # 允许内部锚点链接(href="index.html" 等),但不许外链 http
    check("<!doctype html>" in h.lower(), "合法 HTML")
    check("prefers-color-scheme" in h, "明暗自适应")
    check("http://" not in h and "https://" not in h, "自包含无外链")

    gens = d["generations"]
    for g in gens:
        check(html.escape(g["name"]) in h, f"{g['id']} name「{g['name']}」在 HTML(否则陈旧)")
        check(html.escape(g["bet"]) in h, f"{g['id']} bet 在 HTML(否则陈旧)")
        for fk in g.get("forks", []):
            check(html.escape(fk["condition"]) in h,
                  f"{g['id']} Fork {fk['branch']} condition 在 HTML")

    check(f"{len(gens)}" in h, f"代数 {len(gens)} 在 HTML")

    print(f"结果: {PASSED} 通过, {FAILED} 失败")
    sys.exit(0 if FAILED == 0 else 1)


if __name__ == "__main__":
    main()
