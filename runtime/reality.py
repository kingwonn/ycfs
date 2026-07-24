#!/usr/bin/env python3
"""reality — 历练通道:把现实接回来,并让它决定你下一条断言写什么。

这是整套体系里唯一不会自证的锚,也是 YCFS 原本完全缺失的一环
(README 写着"现实是最高裁决者",然后没有任何代码把现实接回来)。

━━ 为什么它是引擎,而不是又一个记录本 ━━

断言数会涨,但可能只是在给**容易的东西**加断言——错误藏在没被断言的地方,
而你不知道它在哪。靠想象补断言,补的永远是你已经想到的。

现实知道你漏了什么。每一次事故/对账差异/回滚/用户追问,都是现实在告诉你
"这里你没守住"。所以真正的功法是这条闭环:

    现实抓到 → 记为逃逸 → 逃逸必须变成一条断言 → 内力朝**正确方向**增长

**逃逸是你唯一可靠的选题来源。** 它把"该写什么断言"这个问题,
从你的想象力手里,交给现实。

━━ 用法 ━━

  record   记一次现实信号(现实抓到的,标 --escaped)
  owed     列出所有"欠着的断言"——现实抓到过、你还没编码的
  close    把一条逃逸标记为已编码,指向具体断言
  probe    跑注册的探针,自动拉取信号(probes.json)

  信号台账 GATES/REALITY.jsonl 入版本库——它是最贵的资产:
  你的系统在真实世界里失败过的完整历史。
"""
import argparse
import json
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "GATES" / "REALITY.jsonl"
PROBES = ROOT / "runtime" / "probes.json"

# 现实信号的标准通道。项目按需增补,但不要发明"内部测试"这类假通道——
# 通道的资格是:它的信号**不由被测系统产生**。
CHANNELS = [
    "事故",        # 生产故障
    "对账差异",    # 与独立真源核对不符
    "回滚",        # 发布后撤回
    "用户追问",    # 用户问"这个数为什么不对"
    "下游拒收",    # 下游系统/人拒绝了产出
    "人工纠错",    # 人发现并纠正了 AI 的错(README:111 说重大纠错全部来自这里)
]


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _rows():
    if not LEDGER.exists():
        return []
    out = []
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            try:
                out.append(json.loads(line))
            except Exception:
                pass
    return out


def _write_all(rows):
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with open(LEDGER, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def cmd_record(a):
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "id": uuid.uuid4().hex[:8],
        "ts": _now(),
        "channel": a.channel,
        "signal": a.signal,
        # 核心字段:我们的断言抓到了吗?没抓到 = 逃逸 = 欠一条断言
        "caught_by_assertion": not a.escaped,
        "landed_as": None,
        "cost": a.cost,
    }
    with open(LEDGER, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"已记录 {row['id']}  [{a.channel}]")
    if a.escaped:
        print("\n⚠ 这是一次逃逸:现实抓到了,你的断言没抓到。")
        print("  按功法,它现在欠你一条断言。写完后:")
        print(f"    python3 runtime/reality.py close {row['id']} --assertion <腿文件::断言名>")
    return 0


def cmd_owed(a):
    owed = [r for r in _rows()
            if r.get("caught_by_assertion") is False and not r.get("landed_as")]
    if not owed:
        rows = _rows()
        if not rows:
            print("台账为空。\n\n历练=0 意味着没有任何外部锚——所有断言都在自说自话。")
            print("接第一条通道:选一个你的系统在真实世界会被打脸的地方(对账差异 / 用户追问 / 回滚),")
            print("把它记进来。哪怕手工记,也比零强。")
        else:
            print(f"没有欠着的断言。台账 {len(rows)} 条,全部已编码或已被断言抓到。")
        return 0
    print(f"欠着 {len(owed)} 条断言 —— 这些是现实抓到、你还没编码的:\n")
    for r in owed:
        cost = f"  代价:{r['cost']}" if r.get("cost") else ""
        print(f"  [{r['id']}] {r['ts'][:10]}  ({r['channel']})  {r['signal']}{cost}")
    print("\n这份清单就是你的选题表——按它写断言,内力才朝正确方向长。")
    print("凭想象补的断言,补的永远是你已经想到的地方。")
    return 0


def cmd_close(a):
    rows = _rows()
    hit = False
    for r in rows:
        if r.get("id") == a.id:
            r["landed_as"] = a.assertion
            r["closed_ts"] = _now()
            hit = True
    if not hit:
        print(f"❌ 无此信号: {a.id}", file=sys.stderr)
        return 1
    _write_all(rows)
    print(f"✅ {a.id} → {a.assertion}")
    print("一次逃逸变成了一条永久断言。这一步是整套体系里唯一真正复利的动作。")
    return 0


def cmd_probe(a):
    """探针:自动从现实拉信号。probes.json 每项 {name, channel, cmd}。

    命令的 stdout 每行一个信号(纯文本);无输出=本次现实没说话。
    探针失败只警告,绝不阻塞——观测永不干预。
    """
    if not PROBES.exists():
        print("未配置探针。创建 runtime/probes.json:")
        print(json.dumps([{"name": "对账差异", "channel": "对账差异",
                           "cmd": ["your", "reconciliation", "check"]}],
                         ensure_ascii=False, indent=2))
        return 0
    probes = json.loads(PROBES.read_text(encoding="utf-8"))
    total = 0
    for p in probes:
        try:
            r = subprocess.run(p["cmd"], cwd=ROOT, capture_output=True,
                               text=True, timeout=300)
            lines = [l.strip() for l in (r.stdout or "").splitlines() if l.strip()]
        except Exception as e:
            print(f"  (警告: 探针 {p['name']} 失败: {e})")
            continue
        for line in lines:
            with open(LEDGER, "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "id": uuid.uuid4().hex[:8], "ts": _now(),
                    "channel": p["channel"], "signal": line,
                    "caught_by_assertion": False, "landed_as": None,
                    "cost": None, "source": "probe",
                }, ensure_ascii=False) + "\n")
            total += 1
        print(f"  {p['name']}: {len(lines)} 条信号")
    print(f"\n共 {total} 条。跑 `reality.py owed` 看欠着哪些断言。")
    return 0


def main():
    ap = argparse.ArgumentParser(description="历练通道:把现实接回来")
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("record", help="记一次现实信号")
    r.add_argument("--channel", required=True, choices=CHANNELS)
    r.add_argument("--signal", required=True, help="现实说了什么")
    r.add_argument("--escaped", action="store_true",
                   help="断言没抓到(现实先抓到的)→ 记为逃逸,欠一条断言")
    r.add_argument("--cost", default=None, help="这次的代价(可选)")
    r.set_defaults(fn=cmd_record)

    o = sub.add_parser("owed", help="列出欠着的断言")
    o.set_defaults(fn=cmd_owed)

    c = sub.add_parser("close", help="把逃逸标记为已编码")
    c.add_argument("id")
    c.add_argument("--assertion", required=True, help="腿文件::断言名")
    c.set_defaults(fn=cmd_close)

    p = sub.add_parser("probe", help="跑探针自动拉信号")
    p.set_defaults(fn=cmd_probe)

    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
