#!/usr/bin/env python3
"""腿:HTML 仪表盘与决策矩阵引擎保持同步(防陈旧/防手改数字)。

守:site/product.html 里出现的各模态×各档冠军得分,必须与 tradeoff 引擎当前算出的一致。
若有人手改了 HTML 的数字、或改了 routes 数据却没重新生成 HTML,本腿变红。
这是"被测不能自证"在展示层的落地:展示数字不能脱离计算源自说自话。
输出末行 "结果: N 通过, M 失败"。
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "m0"))
from tradeoff import PROFILES, rank  # noqa

HTML = ROOT / "site" / "product.html"
PASSED = FAILED = 0


def check(c, n):
    global PASSED, FAILED
    if c: PASSED += 1
    else:
        FAILED += 1; print(f"  ✗ {n}")


def main():
    # 关键:不在这里重新生成,而是读【已在盘上/已提交】的 HTML 与引擎当前输出比对。
    # 若改了 routes 数据却没跑 build_dashboard,或有人手改了 HTML 数字,盘上文件就会
    # 与引擎脱节 → 本腿红。这才是真的"防陈旧"(此前每次重生成=自洽=验不出陈旧,
    # 由阴性对照抓到并修正)。生成器可运行性单独验一次(在副本上,不覆盖盘上文件)。
    check(HTML.exists(), "site/product.html 存在(需先跑 build_dashboard 生成)")
    if not HTML.exists():
        print(f"结果: {PASSED} 通过, {FAILED} 失败"); sys.exit(1)
    r = subprocess.run([sys.executable, "-c",
                        "import sys;sys.path.insert(0,'m0');import build_dashboard"],
                       cwd=ROOT, capture_output=True, text=True)
    check(r.returncode == 0, "build_dashboard 可导入")
    h = HTML.read_text(encoding="utf-8")

    check("<!doctype html>" in h.lower(), "是合法 HTML 文档")
    check("prefers-color-scheme" in h, "明暗主题自适应")
    check("http://" not in h and "https://" not in h.replace("http-equiv", ""),
          "自包含(无外链依赖)")

    # 每个模态每档的冠军得分必须出现在 HTML 里
    stems = [p.stem for p in (ROOT / "practice" / "routes").glob("*.json")
             if not p.stem.startswith("_")]
    for stem in stems:
        for prof in PROFILES:
            champ = rank(stem, prof)["rows"][0]
            token = f"{champ['score']:.3f}"
            check(token in h, f"{stem}/{prof} 冠军得分 {token} 在 HTML 中(否则陈旧)")

    print(f"结果: {PASSED} 通过, {FAILED} 失败")
    sys.exit(0 if FAILED == 0 else 1)


if __name__ == "__main__":
    main()
