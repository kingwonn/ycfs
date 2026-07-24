#!/usr/bin/env python3
"""scale — 修为刻度。测量"你现在多强",不拦你。

为什么它不是门禁(这是本文件存在的全部理由):

  门禁给的是 0/1:过 / 不过。它只在变红那一刻给信息,平时沉默。
  于是"每轮都绿、总体原地踏步"在门禁下**读数完全相同**——这正是 70+ 轮没达预期
  却看不出原因的机制。

  刻度给的是连续量与趋势。同一批断言,当成门禁用是戒律(拦你越界),
  当成刻度用是内力(告诉你多强)。**你缺的一直是后者。**

  副作用:门槛可以被放宽,所以需要棘轮;棘轮需要保护;保护需要再保护——无穷回退。
  刻度没有门槛,只有数。删断言不会"更容易过",只会让数字直接掉下来。
  **回退问题在改成刻度的那一刻消失,不是被解决,是不再存在。**

五个维度(取自修仙比喻,因为它比法律比喻更贴"什么真的复利"):
  内力 — 断言总数。你的领域里"什么算对"被编码了多少。唯一真正的复利资产。
  法宝 — 自建工具数。每建一个是永久杠杆。
  历练 — 现实信号通道数。唯一不会自证的外部锚。
  人力 — 人的介入量与待人事项龄期。**这个要往下走。**
  逃逸 — 现实抓到、而断言没抓到的错误数。衡量内力的真假。

用法:  python3 runtime/scale.py          测量并落一行历史
       python3 runtime/scale.py --trend  只看趋势,不落行
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HISTORY = ROOT / "runtime" / "scale_history.jsonl"   # 必须入版本库:趋势就是资产
REALITY = ROOT / "GATES" / "REALITY.jsonl"           # 历练台账(现实回读)


# ── 内力:跑所有腿,数断言 ────────────────────────────────────────────
def measure_neili():
    total, legs, detail = 0, 0, {}
    for leg in sorted((ROOT / "runtime" / "legs").glob("leg_*.py")):
        try:
            p = subprocess.run([sys.executable, str(leg)], cwd=ROOT,
                               capture_output=True, text=True, timeout=300)
            out = (p.stdout or "") + (p.stderr or "")
        except subprocess.TimeoutExpired:
            continue
        m = re.search(r"结果: (\d+) (?:通过|文件), (\d+) (?:失败|命中)", out)
        if m:
            n = int(m.group(1))
            total += n
            legs += 1
            detail[leg.stem.replace("leg_", "")] = n
    return total, legs, detail


# ── 法宝:自建工具 ──────────────────────────────────────────────────
def measure_fabao():
    """工具 = 让 AI 能触达你的系统的东西。腿是断言不是工具,排除。"""
    tools = [p for p in (ROOT / "runtime").glob("*.py")
             if p.stem not in {"scale", "gate"}]
    hooks = list((ROOT / "runtime" / "hooks").glob("*.py"))
    mcp = 0
    for cfg in [ROOT / ".mcp.json", ROOT / ".claude" / "settings.json"]:
        if cfg.exists():
            try:
                mcp += len(json.loads(cfg.read_text(encoding="utf-8")).get("mcpServers", {}))
            except Exception:
                pass
    return len(tools) + len(hooks) + mcp


# ── 历练:现实信号 ──────────────────────────────────────────────────
def measure_lilian():
    """现实回读台账。每行 = 一次真实世界反馈(事故/对账差异/用户追问/回滚/退款)。

    格式: {"ts":..., "channel":"对账差异", "signal":..., "caught_by_assertion":true|false}
    caught_by_assertion=false 的行 = 逃逸:现实抓到了,你的断言没抓到。
    """
    if not REALITY.exists():
        return 0, 0, 0, 0
    channels, total, escaped, owed = set(), 0, 0, 0
    for line in REALITY.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            row = json.loads(line)
        except Exception:
            continue
        total += 1
        channels.add(row.get("channel", "?"))
        if row.get("caught_by_assertion") is False:
            escaped += 1
            if not row.get("landed_as"):
                owed += 1      # 还没变成断言的逃逸 = 欠着的内力
    return len(channels), total, escaped, owed


# ── 人力:应该往下走的那个数 ────────────────────────────────────────
def measure_renli():
    pending_file = ROOT / "GATES" / "PENDING_HUMAN.md"
    pending = 0
    if pending_file.exists():
        pending = len(re.findall(r"^\d+\.\s+\*\*",
                                 pending_file.read_text(encoding="utf-8"), re.M))
    precedents = 0
    pf = ROOT / "PRECEDENTS.md"
    if pf.exists():
        precedents = len(re.findall(r"^### P\d+", pf.read_text(encoding="utf-8"), re.M))
    cards_done = 0
    bf = ROOT / "BACKLOG.md"
    if bf.exists():
        cards_done = len(re.findall(r"状态:`done`", bf.read_text(encoding="utf-8")))
    return pending, precedents, cards_done


def read_history():
    if not HISTORY.exists():
        return []
    rows = []
    for line in HISTORY.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                rows.append(json.loads(line))
            except Exception:
                pass
    return rows


def measure():
    neili, legs, detail = measure_neili()
    channels, reality_rows, escaped, owed = measure_lilian()
    pending, precedents, cards_done = measure_renli()
    return {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "内力_断言总数": neili,
        "内力_腿数": legs,
        "内力_明细": detail,
        "法宝_工具数": measure_fabao(),
        "历练_通道数": channels,
        "历练_信号数": reality_rows,
        "逃逸_数": escaped,
        "逃逸_未偿": owed,
        "逃逸率": round(escaped / reality_rows, 3) if reality_rows else None,
        "人力_待人事项": pending,
        "人力_判例数": precedents,
        "卡_已完成": cards_done,
    }


def render(cur, prev):
    def d(key):
        if not prev or prev.get(key) is None or cur.get(key) is None:
            return ""
        delta = cur[key] - prev[key]
        return f"  ({delta:+d})" if delta else "  (—)"

    W = 66
    print("=" * W)
    print("修为刻度 —— 你现在多强(不是你有没有越界)")
    print("=" * W)
    print(f"  内力 · 断言总数     {cur['内力_断言总数']:>6}{d('内力_断言总数')}"
          f"   [{cur['内力_腿数']} 条腿]")
    for k, v in sorted(cur["内力_明细"].items(), key=lambda x: -x[1]):
        print(f"         · {k:<22}{v:>5}")
    print(f"  法宝 · 自建工具     {cur['法宝_工具数']:>6}{d('法宝_工具数')}")
    print(f"  历练 · 现实通道     {cur['历练_通道数']:>6}{d('历练_通道数')}"
          f"   [信号 {cur['历练_信号数']}]")
    esc = "—" if cur["逃逸率"] is None else f"{cur['逃逸率']:.1%}"
    print(f"  逃逸 · 现实抓到而断言没抓到  {cur['逃逸_数']:>3}   逃逸率 {esc}")
    owed = cur.get('逃逸_未偿', 0)
    mark = "✓ 已全部编码" if owed == 0 and cur['逃逸_数'] else f"← 欠着 {owed} 条断言"
    print(f"       · 未偿(还没变成断言) {owed:>3}   {mark}")
    print("-" * W)
    print(f"  人力 · 待人事项     {cur['人力_待人事项']:>6}{d('人力_待人事项')}"
          f"   判例 {cur['人力_判例数']}{d('人力_判例数')}")
    print(f"  产出 · 已完成卡     {cur['卡_已完成']:>6}{d('卡_已完成')}")
    print("-" * W)

    # 诊断:说人话,并且敢说难听的
    diag = []
    if cur.get("逃逸_未偿", 0) > 0:
        diag.append(f"→ 欠着 {cur['逃逸_未偿']} 条断言。跑 `python3 runtime/reality.py owed` 看选题表。\n"
                    "     现实已经告诉你漏在哪了,这是唯一不靠想象力的选题来源。")
    if cur["历练_通道数"] == 0:
        diag.append("❗ 历练=0 —— 没有任何现实信号接回来。这是最大缺口:\n"
                    "     所有断言都在自说自话,没有一个外部锚能证明它们守的是真东西。")
    if cur["逃逸率"] is None:
        diag.append("❗ 逃逸率无法计算 —— 没有现实数据,内力的真假不可知。\n"
                    "     断言数涨了不等于变强了,也可能只是在给容易的东西加断言。")
    if prev:
        dn = cur["内力_断言总数"] - prev["内力_断言总数"]
        dc = cur["卡_已完成"] - prev["卡_已完成"]
        if dc > 0 and dn <= 0:
            diag.append(f"⚠ 完成了 {dc} 张卡,断言数没涨 —— 这几轮的力气没有变成内力。\n"
                        "     这就是跑步机:每轮都成功,总体不变强。")
        if dn > 0 and dc == 0:
            diag.append(f"✓ 断言 +{dn} 而未消耗新卡 —— 纯立法轮,内力在涨。")
    if cur["法宝_工具数"] < 3:
        diag.append("⚠ 法宝偏少 —— 工具是永久杠杆,流程纪律不是。检查力气是否花在了写规矩上。")

    if diag:
        for line in diag:
            print(f"  {line}")
    else:
        print("  (无异常)")
    print("=" * W)


def _row_hash(row):
    """哈希链:每行绑定前一行。改历史会断链——趋势不可篡改。

    没有这个,"修为在涨"就是一句可以被随手改好看的话。
    """
    import hashlib
    body = {k: v for k, v in row.items() if k != "hash"}
    return hashlib.sha256(json.dumps(body, ensure_ascii=False,
                                     sort_keys=True).encode()).hexdigest()[:16]


def main():
    trend_only = "--trend" in sys.argv
    hist = read_history()
    cur = measure()
    prev = hist[-1] if hist else None
    render(cur, prev)

    if trend_only:
        return 0
    cur["prev_hash"] = prev.get("hash") if prev else None
    cur["hash"] = _row_hash(cur)
    with open(HISTORY, "a", encoding="utf-8") as f:
        f.write(json.dumps(cur, ensure_ascii=False) + "\n")
    print(f"已落第 {len(hist) + 1} 次测量 → runtime/scale_history.jsonl")
    print("\n刻度只测量,永不阻塞。要拦的东西在 runtime/gate.py(只拦不可逆与对外)。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
