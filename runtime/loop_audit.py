#!/usr/bin/env python3
"""loop_audit — 体检任何一个"自治循环"仓库。

这是 ycfs 指导真项目的方式:不是再写一篇方法论,是给一条能跑的检查。
(方法论住在 README 里 = 第四个住址 = 等于不存在。)

它抓四类失效,每一类都对应本仓库已经写下、但在真项目里没被执行的原则:

  1. 循环缺勤 —— verifier-six-layers L3:"探针靠定时器,定时器停了要有人知道,
     否则『一直绿』其实是『根本没跑』。" 循环停摆是最贵的失效,因为它静默。
  2. 零信息标签 —— 一个字段如果所有页面取值全同(如 confidence 全是 verified),
     它测不出任何东西。等价于"从不变红的检查":与根本没这个字段不可区分。
  3. 违反自己定的阈值 —— 循环在散文里给自己定了规则(如"最老页超 14 天要全刷新"),
     没有任何代码执行它。门槛只紧不松的反面:门槛根本不存在。
  4. 散文规则占比 —— .md 里写了多少条带数字的规则,其中多少条在代码里有对应检查。

用法:
    python3 runtime/loop_audit.py <repo路径> [--max-silence-hours N]
"""
import argparse
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

CRIT, WARN, OK = "❗", "⚠", "✓"


def sh(args, cwd):
    try:
        p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=60)
        return p.stdout.strip() if p.returncode == 0 else ""
    except Exception:
        return ""


def md_files(root):
    return [p for p in root.rglob("*.md") if ".git" not in p.parts]


# ── 1. 循环缺勤 ─────────────────────────────────────────────────────
def declared_cadence_hours(root):
    """从 LOOP.md / README / workflow 里找循环自己声明的节奏。"""
    text = ""
    for name in ("LOOP.md", "README.md", "CLAUDE.md"):
        f = root / name
        if f.exists():
            text += f.read_text(encoding="utf-8", errors="replace")
    for wf in (root / ".github" / "workflows").glob("*.y*ml") if (root / ".github" / "workflows").exists() else []:
        text += wf.read_text(encoding="utf-8", errors="replace")

    if re.search(r"cron:\s*[\"']?[\d*/, ]+\s+[\d*/,]+\s+\*\s+\*\s+\*", text):
        return 24.0, "CI cron(每日)"
    m = re.search(r"(\d+)\s*[–\-~]\s*(\d+)\s*min", text)
    if m:
        return int(m.group(2)) / 60.0, f"LOOP 声明 {m.group(0)}"
    if re.search(r"每天|daily|每日", text):
        return 24.0, "声明每日"
    m = re.search(r"every\s+(\d+)\s*(hour|min)", text, re.I)
    if m:
        n = int(m.group(1))
        return (n if m.group(2).lower().startswith("hour") else n / 60.0), m.group(0)
    return None, None


def check_absence(root, override):
    print("── 1. 循环缺勤(最贵的失效,因为它静默)")
    last = sh(["git", "log", "-1", "--format=%cI"], root)
    if not last:
        print(f"  {WARN} 读不到 git 历史"); return 0
    age_h = (datetime.now(timezone.utc)
             - datetime.fromisoformat(last)).total_seconds() / 3600
    cad, src = declared_cadence_hours(root)
    if override:
        cad, src = override, "命令行指定"
    print(f"  最后一次提交:{last[:10]}({age_h:.0f} 小时前 ≈ {age_h/24:.1f} 天)")
    if cad is None:
        print(f"  {WARN} 循环没有声明节奏 —— 那就无法判断它是不是停了")
        return 0
    print(f"  声明节奏:约 {cad:.1f} 小时一轮({src})")
    ratio = age_h / cad
    if ratio > 10:
        print(f"  {CRIT} 停摆:已静默 {ratio:.0f} 倍于自己声明的节奏。")
        print(f"      按 verifier-six-layers L3——缺勤要告警。现在没有任何东西会告诉你。")
        return 1
    if ratio > 3:
        print(f"  {WARN} 疑似落后:静默 {ratio:.1f} 倍于声明节奏")
    else:
        print(f"  {OK} 节奏正常")
    return 0


# ── 2. 零信息标签 ───────────────────────────────────────────────────
def check_zero_information(root):
    print("\n── 2. 零信息标签(取值全同的字段,等价于没有这个字段)")
    fields = defaultdict(list)
    for f in md_files(root):
        head = f.read_text(encoding="utf-8", errors="replace")[:1200]
        if not head.startswith("---"):
            continue
        fm = head.split("---", 2)
        if len(fm) < 3:
            continue
        for line in fm[1].splitlines():
            m = re.match(r"^(\w[\w-]*):\s*(.+?)\s*$", line)
            if m and m.group(1) not in ("title", "slug", "updated", "date"):
                fields[m.group(1)].append(m.group(2))
    # 天然常量字段:全同是正常的,不算失效
    CONSTANT_OK = {"lang", "layout", "type", "format", "locale"}
    bad = 0
    if not fields:
        print(f"  (无 frontmatter 字段)"); return 0
    for name, vals in sorted(fields.items()):
        uniq = set(vals)
        if len(vals) < 5:
            continue
        top = max(uniq, key=vals.count)
        share = vals.count(top) / len(vals)
        dist = ", ".join(f"{v}×{vals.count(v)}" for v in sorted(uniq, key=vals.count, reverse=True)[:4])
        if name in CONSTANT_OK:
            print(f"  ·  `{name}`: 全同({top})— 天然常量,不计")
        elif len(uniq) == 1:
            print(f"  {CRIT} `{name}`: {len(vals)} 处全部相同 = {top!r} —— 零信息")
            print(f"      它没测量任何东西,是被测系统贴给自己的标签。")
            bad = 1
        elif share >= 0.95:
            print(f"  {CRIT} `{name}`: {share:.1%} 是同一个值({dist})")
            print(f"      近似零信息。这个字段本该是裁决,现在更像是默认值。")
            print(f"      要它有意义,只有一个办法:让「不通过」真的会发生——")
            print(f"      定义什么条件下它必须是 draft/unverified,并让代码来判,而不是写页面的人自己填。")
            bad = 1
        elif share >= 0.85:
            print(f"  {WARN} `{name}`: {share:.1%} 集中在一个值({dist})— 判别力偏低")
        else:
            print(f"  {OK} `{name}`: {len(uniq)} 种取值({dist})")
    return bad


# ── 3. 违反自己定的阈值 ─────────────────────────────────────────────
def check_own_thresholds(root):
    print("\n── 3. 循环有没有守自己定的规则")
    text = ""
    for name in ("LOOP.md", "README.md", "CLAUDE.md"):
        f = root / name
        if f.exists():
            text += f.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"(?:exceeds?|超过|older than)\s*(\d+)\s*(?:days|天)", text)
    if not m:
        print("  (未在散文里找到陈旧度阈值)")
        return 0
    limit = int(m.group(1))
    dates = sorted(re.findall(r"^updated:\s*(\d{4}-\d{2}-\d{2})",
                              "\n".join(f.read_text(encoding="utf-8", errors="replace")[:400]
                                        for f in md_files(root)), re.M))
    if not dates:
        print(f"  声明阈值 {limit} 天,但没有页面带 updated: 字段"); return 0
    oldest = datetime.strptime(dates[0], "%Y-%m-%d").replace(tzinfo=timezone.utc)
    age = (datetime.now(timezone.utc) - oldest).days
    print(f"  自己定的规则:最老页超过 {limit} 天要全量刷新")
    print(f"  实际最老页:{dates[0]}({age} 天前)")
    if age > limit:
        print(f"  {CRIT} 已违反 {age - limit} 天,而没有任何代码在执行这条规则。")
        print(f"      规则住在 LOOP.md 的散文里 = 第四个住址 = 等于不存在。")
        return 1
    print(f"  {OK} 在阈值内")
    return 0


# ── 4. 散文规则 vs 可执行规则 ───────────────────────────────────────
def check_prose_ratio(root):
    print("\n── 4. 规则住在哪(代码 / context / 权限 才算数)")
    prose = 0
    for name in ("LOOP.md", "README.md", "CLAUDE.md", "AGENTS.md"):
        f = root / name
        if f.exists():
            t = f.read_text(encoding="utf-8", errors="replace")
            prose += len(re.findall(
                r"(?:must|never|always|至少|不得|必须|永不|只能)\b", t, re.I))
    execs = 0
    for pat in ("*.py", "*.mjs", "*.js", "*.sh", "*.ts"):
        for f in root.rglob(pat):
            if ".git" in f.parts or "node_modules" in f.parts:
                continue
            t = f.read_text(encoding="utf-8", errors="replace")
            execs += len(re.findall(r"\b(assert|raise|throw|exit\(1|process\.exit\(1)", t))
    print(f"  散文里的强规则(must/never/必须/不得…): {prose}")
    print(f"  代码里的强制点(assert/throw/exit 非零):   {execs}")
    if prose and execs == 0:
        print(f"  {CRIT} 全部规则都住在散文里,零执行点。")
        return 1
    if prose > execs * 3:
        print(f"  {WARN} 散文规则是执行点的 {prose/max(execs,1):.1f} 倍 —— 大部分规则没人执行")
    else:
        print(f"  {OK} 比例合理")
    return 0


def main():
    ap = argparse.ArgumentParser(description="体检一个自治循环仓库")
    ap.add_argument("repo")
    ap.add_argument("--max-silence-hours", type=float, default=None)
    a = ap.parse_args()
    root = Path(a.repo).resolve()
    if not root.exists():
        print(f"❌ 路径不存在: {root}", file=sys.stderr); return 2

    print("=" * 72)
    print(f"循环体检 · {root.name}")
    print("=" * 72)
    bad = 0
    bad |= check_absence(root, a.max_silence_hours)
    bad |= check_zero_information(root)
    bad |= check_own_thresholds(root)
    bad |= check_prose_ratio(root)
    print("=" * 72)
    print("❗ 有关键项未过。" if bad else "✓ 未发现关键失效。")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
