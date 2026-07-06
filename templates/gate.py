#!/usr/bin/env python3
"""gate — 一条命令跑全部验收。任一腿红 → 退出非零。

YCFS 的 L2 门禁骨架。把你项目的每一类验收做成一条"腿":一个子命令 +
一个校验函数(防"测试静默变少/被跳过"——不光看退出码,还查输出里的断言数)。

铁律:
  · 门槛只紧不松 —— 下面的 *_MIN 常量只允许往大改,永不为"凑过"调小。
  · 促升器不信调用方 —— 发布/促升前自己重跑本 gate,不信任何"我已经跑过了"。
  · 观测不干预门禁 —— 落历史行失败只警告,绝不影响门禁结果。
"""
import subprocess, sys, time, re, os

# ── 硬门槛(只紧不松) ──
UNIT_A_MIN = 100      # A 类单测断言数下限
UNIT_B_MIN = 50


class Leg:
    def __init__(self, name, cmd, verify=None, cwd=None, timeout=300):
        self.name, self.cmd, self.verify, self.cwd, self.timeout = name, cmd, verify, cwd, timeout


def run(leg):
    t0 = time.time()
    try:
        p = subprocess.run(leg.cmd, cwd=leg.cwd, capture_output=True, text=True, timeout=leg.timeout)
        out, rc = (p.stdout or "") + (p.stderr or ""), p.returncode
    except subprocess.TimeoutExpired:
        out, rc = f"[TIMEOUT>{leg.timeout}s]", 124
    problems = []
    if rc != 0:
        problems.append(f"退出码 {rc} ≠ 0")
    if leg.verify:
        problems += leg.verify(out) or []
    return out, problems, time.time() - t0


def v_min(pat, floor):
    """校验输出里"N 通过, 0 失败"形态的断言数 ≥ floor 且零失败。"""
    def v(out):
        m = re.search(pat, out)
        if not m:
            return ["未见通过行(测试可能被跳过)"]
        passed, failed = int(m.group(1)), int(m.group(2))
        p = []
        if failed != 0:
            p.append(f"失败 {failed} ≠ 0")
        if passed < floor:
            p.append(f"通过 {passed} < 硬门槛 {floor}")
        return p
    return v


LEGS = [
    Leg("unit-a", ["your", "test", "command", "a"], verify=v_min(r"结果: (\d+) 通过, (\d+) 失败", UNIT_A_MIN)),
    Leg("unit-b", ["your", "test", "command", "b"], verify=v_min(r"结果: (\d+) 通过, (\d+) 失败", UNIT_B_MIN)),
    Leg("typecheck", ["your", "typecheck", "command"]),
    Leg("secret-scan", ["your", "secret", "scan"]),
    # ... 每一类验收加一条腿。门槛写进 verify,只紧不松。
]


def main():
    W = 78
    print("=" * W)
    failures, legs_detail = [], []
    t0 = time.time()
    for i, leg in enumerate(LEGS, 1):
        out, problems, dt = run(leg)
        ok = not problems
        legs_detail.append((leg.name, ok, dt))
        print(f"[{i}/{len(LEGS)}] {'✅' if ok else '❌'} {leg.name}  ({dt:.1f}s)")
        if not ok:
            for pr in problems:
                print(f"      ✗ {pr}")
            failures.append(leg.name)
    print("-" * W)
    _append_history(legs_detail, failures, time.time() - t0)  # 观测,失败只警告
    if failures:
        print(f"门禁: ❌ FAIL — {len(failures)} 腿未过: {', '.join(failures)}")
        sys.exit(1)
    print(f"门禁: ✅ PASS — 全部 {len(LEGS)} 腿通过。")
    sys.exit(0)


def _append_history(legs, failures, total_dt):
    """L3/观测:每次运行落一行时间序列。落行失败只警告——观测永不干预门禁。"""
    try:
        import json
        row = {"result": "PASS" if not failures else "FAIL", "legs": len(legs),
               "failed": failures, "duration_s": round(total_dt, 1)}
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gate_history.jsonl"), "a") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"      (警告: gate 历史落行失败: {e})")


if __name__ == "__main__":
    main()
