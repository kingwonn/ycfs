#!/usr/bin/env python3
"""gate — 只拦「诚实性」,不拦「能力」。

━━ 划分理由 ━━
能力(断言数、覆盖面)去 runtime/scale.py 当刻度量,不阻塞。
门禁只留四条:不可逆、对外、不泄密、不自证。
  · 拦能力需要门槛,门槛可被放宽,于是需要棘轮保护棘轮——无穷回退。
  · 拦诚实性只需布尔量,无处可松。治理层深度停在 1。

━━ 门槛只紧不松:从散文变成机械 ━━
此前四个门槛是手写常量,而实测水位早已把它们甩开(secret-scan 实测 23 / 门槛 10)
——删掉一半断言,门禁仍然全绿。"只紧不松"写了 12 次,实际执行的是"只松不紧"。

现在改成**快照棘轮**:基线存 runtime/floor.lock.json,每次运行
  实测 > 基线 → 自动写回新基线(收紧是自动的)
  实测 < 基线 → 直接红(放松在结构上不可能)
`_ratchet()` 在代码层只写更大的值,即使被恶意调用也无法调低。
基线文件由 hook 保护,agent 不可写。**没有人需要"记得"这条铁律了。**

━━ 阴性对照 ━━
一个从不变红的检查,与一个根本没跑的检查,信息上不可区分。
本 gate 的 14 次历史运行里只有第一次红过,没有任何一条腿证明过自己会红。
`--selftest` 对每条腿施加一个已知坏扰动,要求它必须红。

用法:  python3 runtime/gate.py              跑门禁
       python3 runtime/gate.py --selftest   证明每条腿会红
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LOCK = HERE / "floor.lock.json"
HISTORY = HERE / "gate_history.jsonl"
CONTROLS = HERE / "negative_controls.json"


class Leg:
    def __init__(self, name, script, pattern, timeout=300):
        self.name, self.script, self.pattern, self.timeout = name, script, pattern, timeout


# 四条腿 = 四种诚实性。能力断言不进这里。
LEGS = [
    Leg("outbound-tests", "runtime/legs/leg_outbound_tests.py",
        r"结果: (\d+) 通过, (\d+) 失败"),
    Leg("choke-point-static", "runtime/legs/leg_choke_point.py",
        r"结果: (\d+) 通过, (\d+) 失败"),
    Leg("secret-scan", "runtime/legs/leg_secret_scan.py",
        r"结果: (\d+) 文件, (\d+) 命中"),
    Leg("no-self-certification", "runtime/legs/leg_no_self_certification.py",
        r"结果: (\d+) 通过, (\d+) 失败"),
    # M0-4:数据管线骨架 + 证书判别力(好批必过、坏批必被抓)
    Leg("pipeline", "runtime/legs/leg_pipeline.py",
        r"结果: (\d+) 通过, (\d+) 失败"),
    # 选型决策矩阵:引擎自洽 + 权重有区分力 + 路线文件格式合规
    Leg("tradeoff", "runtime/legs/leg_tradeoff.py",
        r"结果: (\d+) 通过, (\d+) 失败"),
    # HTML 仪表盘与引擎同步(展示数字不脱离计算源)
    Leg("dashboard", "runtime/legs/leg_dashboard.py",
        r"结果: (\d+) 通过, (\d+) 失败"),
    # M2:力消融框架的判别力(能区分'力有用/无用')
    Leg("ablation", "runtime/legs/leg_ablation.py",
        r"结果: (\d+) 通过, (\d+) 失败"),
]


def run_leg(leg, cwd=ROOT):
    t0 = time.time()
    try:
        p = subprocess.run([sys.executable, leg.script], cwd=cwd,
                           capture_output=True, text=True, timeout=leg.timeout)
        out, rc = (p.stdout or "") + (p.stderr or ""), p.returncode
    except subprocess.TimeoutExpired:
        out, rc = f"[TIMEOUT>{leg.timeout}s]", 124
    m = re.search(leg.pattern, out)
    passed = int(m.group(1)) if m else None
    failed = int(m.group(2)) if m else None
    return {"rc": rc, "out": out, "passed": passed, "failed": failed,
            "dt": time.time() - t0}


def load_lock():
    if not LOCK.exists():
        return {}
    try:
        return json.loads(LOCK.read_text(encoding="utf-8")).get("legs", {})
    except Exception:
        return {}


def _ratchet(lock, name, actual):
    """只写更大的值。棘轮的全部安全性在这一个函数里——它没有调低的分支。"""
    prev = lock.get(name)
    if prev is None or actual > prev:
        lock[name] = actual
        return True
    return False


def save_lock(lock):
    LOCK.write_text(json.dumps({
        "_comment": "水位棘轮基线。gate 自动上调,永不下调(_ratchet 无调低分支)。"
                    "由 hook 保护,agent 不可写。要下调只能人手改,且该动作会留在 git 历史里。",
        "legs": lock,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def cmd_gate():
    lock = load_lock()
    W = 78
    print("=" * W)
    failures, detail, raised = [], [], []
    t0 = time.time()

    for i, leg in enumerate(LEGS, 1):
        r = run_leg(leg)
        problems = []
        if r["rc"] != 0:
            problems.append(f"退出码 {r['rc']} ≠ 0")
        if r["passed"] is None:
            problems.append("未见结果行(腿可能被跳过)")
        else:
            if r["failed"]:
                problems.append(f"失败/命中 {r['failed']} ≠ 0")
            floor = lock.get(leg.name)
            if floor is not None and r["passed"] < floor:
                problems.append(f"水位下降 {r['passed']} < 棘轮基线 {floor} "
                                f"—— 门槛只紧不松,断言不许变少")
            elif _ratchet(lock, leg.name, r["passed"]):
                raised.append((leg.name, floor, r["passed"]))

        ok = not problems
        detail.append({"leg": leg.name, "ok": ok, "passed": r["passed"],
                       "floor": lock.get(leg.name), "dt": round(r["dt"], 2)})
        base = lock.get(leg.name)
        print(f"[{i}/{len(LEGS)}] {'✅' if ok else '❌'} {leg.name}  "
              f"({r['dt']:.1f}s)  实测 {r['passed']} / 基线 {base}")
        for p in problems:
            print(f"      ✗ {p}")
        if not ok:
            failures.append(leg.name)

    print("-" * W)
    for name, old, new in raised:
        print(f"  ⤴ 棘轮收紧: {name}  {old} → {new}(自动,不可逆)")
    save_lock(lock)
    _append_history(detail, failures, time.time() - t0)

    if failures:
        print(f"门禁: ❌ FAIL — {len(failures)} 腿未过: {', '.join(failures)}")
        return 1
    print(f"门禁: ✅ PASS — 全部 {len(LEGS)} 腿通过。")
    print("(能力看刻度: python3 runtime/scale.py)")
    return 0


def cmd_selftest():
    """阴性对照:对每条腿施加已知坏扰动,要求它必须红。

    在仓库副本上做,绝不碰真实文件。
    """
    if not CONTROLS.exists():
        print(f"❌ 缺 {CONTROLS.name} —— 无阴性对照 = 无法证明任何一条腿会红")
        return 1
    controls = json.loads(CONTROLS.read_text(encoding="utf-8"))
    W = 78
    print("=" * W)
    print("阴性对照:每条腿必须能被打红。从不变红的检查 = 没跑的检查。")
    print("=" * W)

    by_leg = {c["leg"]: c for c in controls}
    bad = []
    for leg in LEGS:
        c = by_leg.get(leg.name)
        if not c:
            print(f"  ❌ {leg.name}: 无阴性对照声明")
            bad.append(leg.name)
            continue
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp) / "repo"
            shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns(
                ".git", "__pycache__", "*.pyc"))
            target = work / c["file"]
            if not target.exists():
                print(f"  ❌ {leg.name}: 扰动目标不存在 {c['file']}")
                bad.append(leg.name); continue
            src = target.read_text(encoding="utf-8")
            mutated, n = re.subn(c["find"], c["replace"], src, count=1, flags=re.M)
            if n == 0:
                print(f"  ❌ {leg.name}: 扰动未命中(find 失效,对照已腐坏)")
                bad.append(leg.name); continue
            target.write_text(mutated, encoding="utf-8")

            r = run_leg(leg, cwd=work)
            if r["rc"] == 0 and not r["failed"]:
                print(f"  ❌ {leg.name}: 施加「{c['why']}」后仍然绿 —— 这条腿抓不住它该抓的东西")
                bad.append(leg.name)
            else:
                print(f"  ✅ {leg.name}: 「{c['why']}」→ 变红(证明它有判别力)")

    print("-" * W)
    if bad:
        print(f"阴性对照: ❌ FAIL — {len(bad)} 条腿未证明会红: {', '.join(bad)}")
        return 1
    print(f"阴性对照: ✅ PASS — {len(LEGS)} 条腿全部证明有判别力。")
    return 0


def _append_history(detail, failures, total_dt):
    """观测永不干预门禁:落行失败只警告。

    记各腿通过数——此前只记 result/legs/failed/duration,历史最高水位无法审计。
    """
    try:
        row = {
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "result": "PASS" if not failures else "FAIL",
            "legs": detail,                      # 含每条腿的实测值与基线
            "failed": failures,
            "duration_s": round(total_dt, 1),
        }
        with open(HISTORY, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"      (警告: gate 历史落行失败: {e})")


if __name__ == "__main__":
    sys.exit(cmd_selftest() if "--selftest" in sys.argv else cmd_gate())
