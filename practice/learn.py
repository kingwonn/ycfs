#!/usr/bin/env python3
"""学 —— 预测驱动的领域学习闭环。

━━ 为什么不是笔记工具 ━━
学一个技术领域,失败模式不是"学不会",是**以为自己懂了**。
读论文点头、看完视频觉得清楚了——这些不产生任何错误信号,所以你不知道哪儿是洞。

解法沿用你自己那条原则(每个评估自带证伪条件),搬到学习上:
**每一句「我懂了」必须先变成一个可能被打脸的预测。**

    登记概念 → 强制写一条可证伪的预测 → 对照现实(论文/代码/实验)→ 对错入账

预测对了只是确认。**预测错了才是真学到**——那一刻你才知道自己原来的模型是错的。

━━ 分层,因为读不懂前沿多半不是前沿难 ━━
每个概念挂一层:基础 / 中层 / 前沿。
刻度会分层算预测准确率,然后诊断:
  前沿低 + 基础也低  → 别硬啃前沿了,回去补基础(最常见的坑)
  前沿低 + 基础高    → 正常,前沿本来就该常错
  全部都高           → 你选的题太简单,没在学新东西

用法:
    learn.py add -c "VLA 的 action head" -l 中层 \
        -p "我预测 VLA 输出的是离散 token 化的动作,不是连续值" -w "读 GR00T 论文第4节"
    learn.py check <id> --wrong -a "两种都有,π0 用 flow matching 出连续动作"
    learn.py open          还没验证的预测
    learn.py scale         刻度
"""
import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOG = HERE / "learned.jsonl"
LAYERS = ["基础", "中层", "前沿"]


def now():
    return datetime.now(timezone.utc)


def rows():
    if not LOG.exists():
        return []
    out = []
    for line in LOG.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            try:
                out.append(json.loads(line))
            except Exception:
                pass
    return out


def save(rs):
    with open(LOG, "w", encoding="utf-8") as f:
        for r in rs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def cmd_add(a):
    r = {
        "id": uuid.uuid4().hex[:6],
        "ts": now().isoformat(timespec="seconds"),
        "domain": a.domain,
        "concept": a.concept,
        "layer": a.layer,
        "prediction": a.predict,      # 可证伪的预测——命门在这一栏
        "where": a.where,             # 拿什么验证:论文/代码/实验
        "result": None,               # right | wrong
        "actual": None,               # 现实其实是什么
    }
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"已登记 [{r['id']}] ({a.layer}) {a.concept}")
    print(f"  预测:{a.predict}")
    print(f"  验证:{a.where or '⚠ 没写用什么验证——那这条预测无法被打脸,等于没写'}")

    # 质量提醒:一条好预测必须有可能是错的
    weak = ["很重要", "有用", "是关键", "会更好", "有帮助", "很复杂"]
    if any(w in a.predict for w in weak) or len(a.predict) < 12:
        print("\n  ⚠ 这条预测可能不可证伪。")
        print("     「X 很重要」永远不会错,所以它测不出你懂没懂。")
        print("     改成能被具体事实推翻的形式:「我预测 X 的做法是 A 而不是 B」。")
    return 0


def cmd_check(a):
    rs = rows()
    hit = None
    for r in rs:
        if r["id"] == a.id:
            hit = r
            r["result"] = "right" if a.right else "wrong"
            r["actual"] = a.actual
            r["checked"] = now().isoformat(timespec="seconds")
    if not hit:
        print(f"❌ 无此条: {a.id}", file=sys.stderr)
        return 1
    save(rs)
    if a.right:
        print(f"✓ [{a.id}] 预测对了。({hit['layer']}·{hit['concept']})")
        print("  只是确认,信息量小。下一条预测挑更难的。")
    else:
        print(f"✗ [{a.id}] 预测错了。({hit['layer']}·{hit['concept']})")
        print(f"  现实:{a.actual}")
        print("  ← 这一刻才是真学到。你原来的模型被打掉了一块。")
    return 0


def cmd_open(a):
    o = [r for r in rows() if r["result"] is None]
    if not o:
        print("没有待验证的预测。" if rows() else
              "还没开始。\n\n起手:挑一个你自以为懂的概念,写下一条**可能被打脸**的预测,再去查。")
        return 0
    print(f"待验证 {len(o)} 条:\n")
    for r in o:
        print(f"  [{r['id']}] ({r['layer']}) {r['concept']}")
        print(f"        预测:{r['prediction']}")
        print(f"        去验:{r['where']}")
        print()
    print("验完: learn.py check <id> --right | --wrong -a \"现实是什么\"")
    return 0


def cmd_scale(a):
    rs = [r for r in rows() if r["result"]]
    allr = rows()
    if not allr:
        print("刻度为空。登记第一条预测后再来。")
        return 0
    W = 60
    print("=" * W)
    print("学习刻度 —— 你的模型有多准(不是你读了多少)")
    print("=" * W)
    print(f"  已登记 {len(allr)} 条,已验证 {len(rs)} 条,待验证 {len(allr)-len(rs)} 条\n")

    acc = {}
    for layer in LAYERS:
        items = [r for r in rs if r["layer"] == layer]
        if not items:
            print(f"  {layer:<4}  —— 还没有验证过的预测")
            continue
        right = sum(1 for r in items if r["result"] == "right")
        a_ = right / len(items)
        acc[layer] = a_
        bar = "█" * int(a_ * 20) + "·" * (20 - int(a_ * 20))
        print(f"  {layer:<4}  {bar} {a_:.0%}   ({right}/{len(items)} 条预测命中)")

    print("-" * W)
    base, front = acc.get("基础"), acc.get("前沿")
    if base is not None and base < 0.6:
        print("  ❗ 基础层预测准确率低于 60% —— 地基有洞。")
        print("     现在读前沿是在浪费时间:你会把「看不懂」误当成「这篇难」。")
    elif front is not None and front < 0.5 and (base or 1) >= 0.7:
        print("  ✓ 前沿常错、基础扎实 —— 这是健康状态。前沿本来就该常被打脸。")
    elif acc and all(v >= 0.9 for v in acc.values()):
        print("  ⚠ 全部准确率 ≥ 90% —— 你挑的题太简单了。")
        print("     预测从不出错 = 没在学新东西,只在确认已知。挑更难的下手。")
    wrongs = [r for r in rs if r["result"] == "wrong"]
    if wrongs:
        print(f"\n  被打脸 {len(wrongs)} 次 —— 这些是你真正学到的地方:")
        for r in wrongs[-5:]:
            print(f"    · ({r['layer']}) {r['concept']}: {r['actual'][:52]}")
    print("=" * W)
    print("  判据:预测量在涨 + 前沿准确率缓慢上升 = 在真学。")
    print("        只涨阅读量、不涨预测量 = 在收集安慰感。")
    return 0


def main():
    ap = argparse.ArgumentParser(description="预测驱动的领域学习")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("add", help="登记一个概念 + 一条可证伪预测")
    p.add_argument("-c", "--concept", required=True)
    p.add_argument("-l", "--layer", required=True, choices=LAYERS)
    p.add_argument("-p", "--predict", required=True, help="可能被打脸的预测")
    p.add_argument("-w", "--where", default="", help="拿什么验证:论文/代码/实验")
    p.add_argument("-d", "--domain", default="Physical AI")
    p.set_defaults(fn=cmd_add)

    c = sub.add_parser("check", help="对照现实验证")
    c.add_argument("id")
    g = c.add_mutually_exclusive_group(required=True)
    g.add_argument("--right", action="store_true")
    g.add_argument("--wrong", action="store_true")
    c.add_argument("-a", "--actual", default="", help="现实其实是什么")
    c.set_defaults(fn=cmd_check)

    o = sub.add_parser("open", help="待验证的预测")
    o.set_defaults(fn=cmd_open)

    s = sub.add_parser("scale", help="刻度")
    s.set_defaults(fn=cmd_scale)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
