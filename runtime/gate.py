#!/usr/bin/env python3
"""gate — 一条命令跑全部验收。任一腿红 → 退出非零。(R1 实例,承 templates/gate.py)

铁律:
  · 门槛只紧不松 —— *_MIN 只允许往大改,永不为"凑过"调小。
  · 促升器不信调用方 —— 任何发布/合并前自己重跑本 gate。
  · 观测不干预门禁 —— 历史落行失败只警告。
"""
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# ── 硬门槛(只紧不松) ──
OUTBOUND_MIN = 50   # 对外状态机行为断言数下限
STATIC_MIN = 13     # choke-point 结构断言数下限
SECRET_FILES_MIN = 10  # 密钥扫描覆盖文件数下限
SELF_CERT_MIN = 10     # 自证通道检测断言数下限


class Leg:
    def __init__(self, name, cmd, verify=None, timeout=300):
        self.name, self.cmd, self.verify, self.timeout = name, cmd, verify, timeout


def run(leg):
    t0 = time.time()
    try:
        p = subprocess.run(leg.cmd, cwd=ROOT, capture_output=True, text=True, timeout=leg.timeout)
        out, rc = (p.stdout or "") + (p.stderr or ""), p.returncode
    except subprocess.TimeoutExpired:
        out, rc = f"[TIMEOUT>{leg.timeout}s]", 124
    problems = []
    if rc != 0:
        problems.append(f"退出码 {rc} ≠ 0")
    if leg.verify:
        problems += leg.verify(out) or []
    return out, problems, time.time() - t0


def v_min(pat, floor, fail_must_zero=True):
    def v(out):
        m = re.search(pat, out)
        if not m:
            return ["未见结果行(腿可能被跳过)"]
        passed, failed = int(m.group(1)), int(m.group(2))
        p = []
        if fail_must_zero and failed != 0:
            p.append(f"失败/命中 {failed} ≠ 0")
        if passed < floor:
            p.append(f"通过/覆盖 {passed} < 硬门槛 {floor}")
        return p
    return v


# ── 门禁只拦「诚实性」,不拦「能力」 ──
#
# 能力(断言数、工具数、覆盖面)去 runtime/scale.py 当刻度量,不阻塞。
# 门禁只保留四条:不可逆、对外、不泄密、不自证。理由:
#   · 拦能力需要门槛,门槛可被放宽,于是需要棘轮保护棘轮——无穷回退。
#   · 拦诚实性不需要门槛,只需要"有没有"——布尔量,无处可松。
# 这个划分让治理层深度停在 1,锚在系统外(现实 / 人的签字)。
LEGS = [
    Leg("outbound-tests", [sys.executable, "runtime/legs/leg_outbound_tests.py"],
        verify=v_min(r"结果: (\d+) 通过, (\d+) 失败", OUTBOUND_MIN)),
    Leg("choke-point-static", [sys.executable, "runtime/legs/leg_choke_point.py"],
        verify=v_min(r"结果: (\d+) 通过, (\d+) 失败", STATIC_MIN)),
    Leg("secret-scan", [sys.executable, "runtime/legs/leg_secret_scan.py"],
        verify=v_min(r"结果: (\d+) 文件, (\d+) 命中", SECRET_FILES_MIN)),
    # 铁律「被测不能自证」的可执行形态。此前它在仓库里出现 8 次、执行 0 次。
    Leg("no-self-certification", [sys.executable, "runtime/legs/leg_no_self_certification.py"],
        verify=v_min(r"结果: (\d+) 通过, (\d+) 失败", SELF_CERT_MIN)),
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
        tail = [l for l in out.strip().splitlines() if l.strip()][-1:] if out.strip() else []
        for l in tail:
            print(f"      {l}")
        if not ok:
            for pr in problems:
                print(f"      ✗ {pr}")
            failures.append(leg.name)
    print("-" * W)
    _append_history(legs_detail, failures, time.time() - t0)
    if failures:
        print(f"门禁: ❌ FAIL — {len(failures)} 腿未过: {', '.join(failures)}")
        sys.exit(1)
    print(f"门禁: ✅ PASS — 全部 {len(LEGS)} 腿通过。")
    sys.exit(0)


def _append_history(legs, failures, total_dt):
    try:
        row = {"result": "PASS" if not failures else "FAIL", "legs": len(legs),
               "failed": failures, "duration_s": round(total_dt, 1)}
        with open(os.path.join(HERE, "gate_history.jsonl"), "a") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"      (警告: gate 历史落行失败: {e})")


if __name__ == "__main__":
    main()
