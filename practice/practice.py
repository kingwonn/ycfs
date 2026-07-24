#!/usr/bin/env python3
"""练 —— 错题驱动的修炼闭环。功法在个人领域的最小实现。

和 runtime/ 那套是同一个形状,只是去掉了全部治理层
(个人练习没有对外动作、没有不可逆操作、错了不要钱,所以不需要门禁):

    现实出错 → 记一条 → 它永久存在 → 间隔重复直到掌握 → 弱点库 = 内力

为什么它比"每天背单词"强:选题不靠想象力。你练的永远是**现实刚刚打你脸的地方**,
不是你以为自己弱的地方。

用法:
    python3 practice/practice.py add  -d 英语 -w "listen 后面要加 to" -c "listen to music" -s "被同事纠正"
    python3 practice/practice.py review              今天该复习的
    python3 practice/practice.py review -d 英语       只练英语
    python3 practice/practice.py ok <id>             这次答对了
    python3 practice/practice.py no <id>             这次又错了(退回第一档)
    python3 practice/practice.py scale               刻度:内力多少、掌握多少、趋势

间隔:答对一次 +1 档,档位对应 1 / 3 / 7 / 21 / 60 天。连对五次算掌握。
答错退回第 0 档——**掌握不能靠时间自动到达,只能靠答对。**
"""
import argparse
import json
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOG = HERE / "errors.jsonl"
INTERVALS = [1, 3, 7, 21, 60]     # 天。答对一次进一档
MASTERED_AT = len(INTERVALS)      # 连对 5 次 = 掌握


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
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "w", encoding="utf-8") as f:
        for r in rs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def due(r):
    """到期该复习了吗?已掌握的不再出现。"""
    if r["level"] >= MASTERED_AT:
        return False
    last = datetime.fromisoformat(r["last_review"] or r["ts"])
    return now() >= last + timedelta(days=INTERVALS[min(r["level"], len(INTERVALS) - 1)])


def cmd_add(a):
    r = {
        "id": uuid.uuid4().hex[:6],
        "ts": now().isoformat(timespec="seconds"),
        "domain": a.domain,
        "wrong": a.wrong,          # 你错成了什么 / 卡在哪
        "correct": a.correct,      # 对的是什么
        "source": a.source,        # 现实信号来源——这一栏是这套方法的命门
        "level": 0,
        "last_review": None,
        "hits": 0, "misses": 0,
    }
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"已记 [{r['id']}] {a.domain}:{a.wrong}")
    if not a.source:
        print("  ⚠ 没写来源。凭想象补的题,补的永远是你已经想到的地方——"
              "下次写上是谁/什么打了你脸。")
    else:
        print(f"  来源:{a.source}  ← 这是唯一不靠想象力的选题依据")
    print("  明天到期。")
    return 0


def cmd_review(a):
    rs = [r for r in rows() if (not a.domain or r["domain"] == a.domain)]
    d = [r for r in rs if due(r)]
    if not d:
        pend = [r for r in rs if r["level"] < MASTERED_AT]
        if not rs:
            print("还没有错题。\n\n起手方式:今天遇到第一个说不出/听不懂的地方,就记一条。")
            print("不用凑数——这套方法的全部价值在于「只练现实打过你脸的地方」。")
        else:
            nxt = min(
                (datetime.fromisoformat(r["last_review"] or r["ts"])
                 + timedelta(days=INTERVALS[min(r["level"], len(INTERVALS) - 1)]))
                for r in pend) if pend else None
            print(f"今天没有到期的。待攻克 {len(pend)} 条"
                  + (f",下一条 {nxt.date()} 到期。" if nxt else "(全部已掌握)。"))
        return 0
    print(f"今天该练 {len(d)} 条:\n")
    for r in d:
        print(f"  [{r['id']}] ({r['domain']}) 第 {r['level']+1} 档")
        print(f"        题:{r['wrong']}")
        print(f"        ——(想好了再看)答:{r['correct']}")
        if r["source"]:
            print(f"        当时:{r['source']}")
        print()
    print("答对: practice.py ok <id>    又错了: practice.py no <id>")
    return 0


def _mark(rid, ok):
    rs = rows()
    hit = None
    for r in rs:
        if r["id"] == rid:
            hit = r
            r["last_review"] = now().isoformat(timespec="seconds")
            if ok:
                r["level"] += 1
                r["hits"] += 1
            else:
                r["level"] = 0       # 掌握只能靠答对,不能靠时间熬过去
                r["misses"] += 1
    if not hit:
        print(f"❌ 无此条: {rid}", file=sys.stderr)
        return 1
    save(rs)
    if ok and hit["level"] >= MASTERED_AT:
        print(f"✅ [{rid}] 连对 {MASTERED_AT} 次 —— 掌握了,不再出现。")
    elif ok:
        nxt = INTERVALS[min(hit["level"], len(INTERVALS) - 1)]
        print(f"✅ [{rid}] 进第 {hit['level']+1} 档,{nxt} 天后再问。")
    else:
        print(f"↩ [{rid}] 退回第 1 档,明天再问。错了不丢人,漏掉才丢人。")
    return 0


def cmd_scale(a):
    rs = rows()
    if not rs:
        print("刻度为空。记第一条错题后再来。")
        return 0
    W = 58
    print("=" * W)
    print("修炼刻度 —— 你现在多强")
    print("=" * W)
    doms = {}
    for r in rs:
        doms.setdefault(r["domain"], []).append(r)
    for dom, items in sorted(doms.items(), key=lambda x: -len(x[1])):
        mastered = sum(1 for r in items if r["level"] >= MASTERED_AT)
        sourced = sum(1 for r in items if r["source"])
        print(f"  {dom}")
        print(f"    内力 · 弱点库      {len(items):>4} 条")
        print(f"    攻克 · 已掌握      {mastered:>4} 条  ({mastered/len(items):.0%})")
        print(f"    在练 · 待攻克      {len(items)-mastered:>4} 条")
        print(f"    来源 · 有现实出处  {sourced:>4} 条  ({sourced/len(items):.0%})"
              + ("  ← 越高越好" if sourced == len(items) else "  ⚠ 其余是凭想象补的"))
        total_m = sum(r["misses"] for r in items)
        print(f"    反复错 · 累计答错  {total_m:>4} 次"
              + ("  ← 这些是真难点,值得单独攻" if total_m else ""))
        print()
    print("-" * W)
    print("  判据:弱点库在涨 + 攻克率在涨 = 在变强。")
    print("        弱点库不涨 = 你没在接触让你出错的难度,原地踏步。")
    print("=" * W)
    return 0


def main():
    ap = argparse.ArgumentParser(description="错题驱动的修炼闭环")
    sub = ap.add_subparsers(dest="cmd", required=True)

    a1 = sub.add_parser("add", help="记一条现实打你脸的地方")
    a1.add_argument("-d", "--domain", required=True, help="领域,如 英语 / 自我精进")
    a1.add_argument("-w", "--wrong", required=True, help="你错成了什么/卡在哪")
    a1.add_argument("-c", "--correct", required=True, help="对的是什么")
    a1.add_argument("-s", "--source", default="", help="现实来源:谁/什么打了你脸")
    a1.set_defaults(fn=cmd_add)

    a2 = sub.add_parser("review", help="今天该练什么")
    a2.add_argument("-d", "--domain", default=None)
    a2.set_defaults(fn=cmd_review)

    a3 = sub.add_parser("ok", help="答对了")
    a3.add_argument("id"); a3.set_defaults(fn=lambda a: _mark(a.id, True))

    a4 = sub.add_parser("no", help="又错了")
    a4.add_argument("id"); a4.set_defaults(fn=lambda a: _mark(a.id, False))

    a5 = sub.add_parser("scale", help="刻度")
    a5.set_defaults(fn=cmd_scale)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
