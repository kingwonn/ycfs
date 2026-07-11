#!/usr/bin/env python3
"""gate — swe-agent 门禁运行器(YCFS L2 骨架,本项目实例)。

一条命令跑全部**已实现**验收腿:任一腿红 → 退出非零。
未实现的门禁腿(交叉编译/静态分析/单测/仿真/60730 自检表)**诚实标 BLOCKED**,
既不算绿也不算红——它们等 PENDING_HUMAN 的 Q1–Q6 解锁,**绝不伪绿**。

铁律(继承自 templates/gate.py):
  · 门槛只紧不松 —— *_MIN 常量只允许往大改,永不为「凑过」调小。
  · 促升器不信调用方 —— 发布/促升前自己重跑本 gate。
  · 观测不干预门禁 —— 落历史行失败只警告,绝不影响门禁结果。
  · 不伪绿 —— 一条腿没真跑过,不许显示为通过(BLOCKED ≠ PASS)。
"""
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))

# ── 硬门槛(只紧不松) ──
CARD_MIN = 11          # BACKLOG 首批卡数下限
INTERVIEW_Q_MIN = 6    # PENDING_HUMAN 架构级问题数下限(已答的归档仍计入)
FLASH_MAX_BYTES = 512 * 1024   # STM32G474RE flash 预算(text+data 超出即红)
TEXT_MIN_BYTES = 200           # text 段下限:防"编译了个空壳"充数
STACK_FRAME_MAX_BYTES = 256    # 单函数最坏栈帧上限(-fstack-usage;只紧不松)
STATEMACHINE_MIN = 10          # C1 状态机单测断言数下限(防测试静默变少)
HOST_TEST_MIN = 25             # 固件 host 单测断言总数下限(sched 9 + thermal/interlock 16;只紧不松)
LAYER_FILES_MIN = 6            # 分层检查扫描文件数下限(防目录改名后静默空转)
PROVENANCE_MIN = 16            # D1 溯源核验断言数下限(含真 PDF 回环与中英等强 property)
RAM_BUDGET_BYTES = 4096        # data+bss 静态 RAM 预算(只紧不松)
BANNED_SYMBOLS = ("malloc", "free", "calloc", "realloc", "_sbrk", "sbrk")  # 禁动态分配
REQUIRED_DOCS = [
    "docs/ARCHITECTURE.md",
    "docs/verifier-firmware.md",
    "docs/reuse-landscape.md",
    "docs/unknown-map.md",
]
CARD_FIELDS = ("状态:", "翻译:", "验收")  # 每张卡必备字段


def _read(rel):
    with open(os.path.join(HERE, rel), encoding="utf-8") as f:
        return f.read()


# ── 已实现的绿腿:脚手架完整性自检 ──
def leg_scaffold_integrity():
    """决策无关的真实绿腿:验证 v0 脚手架结构完整、每张卡机器可查。"""
    problems = []

    # 1) 必备文档齐全
    for doc in REQUIRED_DOCS:
        if not os.path.exists(os.path.join(HERE, doc)):
            problems.append(f"缺文档 {doc}")

    # 2) BACKLOG 卡数与字段完整性
    try:
        backlog = _read("BACKLOG.md")
    except FileNotFoundError:
        return ["缺 BACKLOG.md"], {"cards": 0}
    # 卡 = 形如 "### A1 · ..." 的标题(字母+数字)
    card_headers = re.findall(r"^### ([A-Z]\d+) ·", backlog, re.MULTILINE)
    n_cards = len(card_headers)
    if n_cards < CARD_MIN:
        problems.append(f"卡数 {n_cards} < 硬门槛 {CARD_MIN}")
    # 每张卡的块必须含必备字段
    blocks = re.split(r"^### [A-Z]\d+ ·", backlog, flags=re.MULTILINE)[1:]
    for hid, block in zip(card_headers, blocks):
        for field in CARD_FIELDS:
            if field not in block:
                problems.append(f"卡 {hid} 缺字段「{field}」")

    # 3) DIGEST 至少一行数据(R\d 开头的表格行)
    try:
        digest = _read("DIGEST.md")
        if not re.search(r"^\| R\d+ \|", digest, re.MULTILINE):
            problems.append("DIGEST 无数据行(应有 | R1 | ...)")
    except FileNotFoundError:
        problems.append("缺 DIGEST.md")

    # 4) PENDING_HUMAN 的架构级问题数达标
    try:
        ph = _read("GATES/PENDING_HUMAN.md")
        n_q = len(re.findall(r"^### Q\d+ ·", ph, re.MULTILINE))
        if n_q < INTERVIEW_Q_MIN:
            problems.append(f"PENDING_HUMAN 问题数 {n_q} < 硬门槛 {INTERVIEW_Q_MIN}")
    except FileNotFoundError:
        problems.append("缺 GATES/PENDING_HUMAN.md")
        n_q = 0

    return problems, {"cards": n_cards, "docs": len(REQUIRED_DOCS), "interview_q": n_q}


# ── 已实现的绿腿:文档内不出现伪 verified(状态机治理占位) ──
def leg_no_fake_verified():
    """卡不得自称 verified——verified 唯一路径穿过人的真机签字(BACKLOG C1)。
    v0 阶段没有任何卡应处于 verified;检出即红。"""
    problems = []
    backlog = _read("BACKLOG.md")
    if re.search(r"状态:`verified`", backlog):
        problems.append("发现 verified 卡但 v0 无真机签字管道——疑似绕过边")
    return problems, {}


# ── 已实现的绿腿:交叉编译(F1,D-001 解锁后激活) ──
def leg_cross_compile():
    """arm-none-eabi headless 构建:工具链版本锁定 + 可复现构建 + size 断言。
    工具链缺失 = 红(无法验证 ≠ 通过),不降级为 BLOCKED。"""
    import subprocess
    problems, counts = [], {}
    fw = os.path.join(HERE, "firmware")

    # 1) 工具链版本锁定(toolchain.lock 一致性)
    try:
        lock = dict(
            line.split("=", 1)
            for line in _read("firmware/toolchain.lock").strip().splitlines()
        )
        want = lock["arm-none-eabi-gcc"]
    except Exception as e:  # noqa: BLE001
        return [f"toolchain.lock 不可读: {e}"], counts
    try:
        got = subprocess.run(
            ["arm-none-eabi-gcc", "-dumpversion"],
            capture_output=True, text=True, timeout=30,
        ).stdout.strip()
    except FileNotFoundError:
        return ["arm-none-eabi-gcc 未安装(无法验证≠通过): apt-get install gcc-arm-none-eabi"], counts
    if got != want:
        problems.append(f"工具链版本 {got} ≠ lock {want}(可复现性破坏)")
    counts["gcc"] = got

    # 2) 一条命令构建
    p = subprocess.run(
        [os.path.join(fw, "build.sh")], capture_output=True, text=True, timeout=300, cwd=fw,
    )
    if p.returncode != 0:
        problems.append(f"构建失败 exit={p.returncode}")
        tail = ((p.stdout or "") + (p.stderr or "")).strip().splitlines()[-8:]
        problems += [f"  | {line}" for line in tail]
        return problems, counts

    # 3) 产物与 size 断言
    for artifact in ("build/firmware.elf", "build/firmware.map", "build/size.txt"):
        if not os.path.exists(os.path.join(fw, artifact)):
            problems.append(f"缺产物 {artifact}")
    try:
        size_out = _read("firmware/build/size.txt")
        m = re.search(r"^\s*(\d+)\s+(\d+)\s+(\d+)\s+\d+", size_out, re.MULTILINE)
        if not m:
            problems.append("size.txt 不可解析")
        else:
            text, data, bss = (int(m.group(i)) for i in (1, 2, 3))
            counts.update({"text": text, "data": data, "bss": bss})
            if text < TEXT_MIN_BYTES:
                problems.append(f"text {text}B < 下限 {TEXT_MIN_BYTES}B(疑似空壳)")
            if text + data > FLASH_MAX_BYTES:
                problems.append(f"flash 占用 {text + data}B > 预算 {FLASH_MAX_BYTES}B")
    except FileNotFoundError:
        pass  # 缺产物已在上面报过
    return problems, counts


# ── 资源预算腿的可测试内核(负向自测直接喂合成输入) ──
def _find_banned_symbols(nm_output):
    hits = []
    for line in nm_output.splitlines():
        parts = line.split()
        if parts and parts[-1] in BANNED_SYMBOLS:
            hits.append(parts[-1])
    return sorted(set(hits))


def _check_su(text, src_only=True):
    """解析 -fstack-usage 输出。返回 (problems, max_frame)。
    非 static 限定(dynamic/bounded = VLA/alloca)即红;超帧上限即红。"""
    problems, max_frame = [], 0
    for line in text.strip().splitlines():
        cols = line.split("\t")
        if len(cols) < 3:
            continue
        loc, size_s, qual = cols[0], cols[1], cols[2]
        if src_only and not any(d in loc for d in ("/platform/", "/products/", "/bsp/")):
            continue  # 只统计工程源(分层目录);跳过 CMake 编译器探测等
        size = int(size_s)
        max_frame = max(max_frame, size)
        if qual != "static":
            problems.append(f"{loc} 栈帧非静态({qual}):疑似 VLA/alloca")
        if size > STACK_FRAME_MAX_BYTES:
            problems.append(f"{loc} 栈帧 {size}B > 上限 {STACK_FRAME_MAX_BYTES}B")
    return problems, max_frame


# ── 已实现的绿腿:资源预算(B3) ──
def leg_resource_budget():
    """禁动态分配(nm 符号封禁)+ 最坏栈帧上限(-fstack-usage)+ 静态 RAM 预算 + ISR 预算表存在。"""
    import subprocess
    problems, counts = [], {}
    fw = os.path.join(HERE, "firmware")
    elf = os.path.join(fw, "build", "firmware.elf")
    if not os.path.exists(elf):
        return ["缺 firmware.elf(先跑 cross-compile 腿)"], counts

    # 1) 动态分配符号封禁
    try:
        nm = subprocess.run(["arm-none-eabi-nm", elf], capture_output=True, text=True, timeout=60).stdout
    except FileNotFoundError:
        return ["arm-none-eabi-nm 未安装(无法验证≠通过)"], counts
    banned = _find_banned_symbols(nm)
    if banned:
        problems.append(f"检出动态分配符号: {', '.join(banned)}(固件禁 malloc)")

    # 2) 栈帧上限(.su)
    su_text = []
    for root, _dirs, files in os.walk(os.path.join(fw, "build")):
        for fn in files:
            if fn.endswith(".su"):
                with open(os.path.join(root, fn), encoding="utf-8") as f:
                    su_text.append(f.read())
    if not su_text:
        problems.append("未找到 .su 文件(-fstack-usage 未生效?)")
    else:
        su_problems, max_frame = _check_su("\n".join(su_text))
        problems += su_problems
        counts["max_frame"] = max_frame

    # 3) 静态 RAM 预算(data+bss)
    try:
        m = re.search(r"^\s*(\d+)\s+(\d+)\s+(\d+)\s+\d+", _read("firmware/build/size.txt"), re.MULTILINE)
        if m:
            static_ram = int(m.group(2)) + int(m.group(3))
            counts["static_ram"] = static_ram
            if static_ram > RAM_BUDGET_BYTES:
                problems.append(f"静态 RAM {static_ram}B > 预算 {RAM_BUDGET_BYTES}B")
    except FileNotFoundError:
        problems.append("缺 size.txt")

    # 4) ISR 预算表骨架存在且含规则行
    try:
        isr = _read("firmware/isr-budget.md")
        if "WCET" not in isr:
            problems.append("isr-budget.md 缺 WCET 列")
    except FileNotFoundError:
        problems.append("缺 firmware/isr-budget.md")
    return problems, counts


# ── 已实现的绿腿:bench 题目质量自检(K1) ──
def leg_bench_self_check():
    """agent 评测基准的题目质量自检:参考实现全绿/buggy 必红/出生证齐/哈希锁一致/题数下限。"""
    import subprocess
    p = subprocess.run(
        [sys.executable, os.path.join(HERE, "bench", "run_bench.py")],
        capture_output=True, text=True, timeout=300,
    )
    counts = {}
    try:
        data = json.loads(p.stdout)
        counts = {"bug_fix": data["bug_fix"], "spec_qa": data["spec_qa"]}
        problems = data["problems"]
    except (json.JSONDecodeError, KeyError):
        problems = [f"run_bench 输出不可解析(rc={p.returncode}): {p.stdout[-200:]}{p.stderr[-200:]}"]
    if p.returncode != 0 and not problems:
        problems = [f"run_bench 退出码 {p.returncode}"]
    return problems, counts


# ── 已实现的绿腿:C1 状态机结构性断言 ──
def leg_state_machine():
    """「gate 绿→verified」边结构性不存在的单测;断言数 ≥ 下限且零失败。"""
    import subprocess
    p = subprocess.run(
        [sys.executable, "test_statemachine.py"],
        capture_output=True, text=True, timeout=120,
        cwd=os.path.join(HERE, "governance"),
    )
    out = (p.stdout or "") + (p.stderr or "")
    m = re.search(r"RESULT: (\d+) passed, (\d+) failed", out)
    problems = []
    if p.returncode != 0:
        problems.append(f"退出码 {p.returncode} ≠ 0")
    if not m:
        problems.append("未见 RESULT 行(测试可能被跳过)")
        return problems, {}
    n_pass, n_fail = int(m.group(1)), int(m.group(2))
    if n_fail != 0:
        problems.append(f"失败 {n_fail} ≠ 0")
    if n_pass < STATEMACHINE_MIN:
        problems.append(f"通过 {n_pass} < 硬门槛 {STATEMACHINE_MIN}(测试静默变少?)")
    return problems, {"asserts": n_pass}


# ── 已实现的绿腿:固件 host 单测(G3,激活原 BLOCKED 的 host-unit-test) ──
def leg_host_unit_test():
    """host gcc 编译并运行全部固件纯逻辑单测;断言总数 ≥ 下限且零失败。"""
    import subprocess
    fw = os.path.join(HERE, "firmware")
    inc = ["-I", os.path.join(fw, "platform", "core"),
           "-I", os.path.join(fw, "platform", "control"),
           "-I", os.path.join(fw, "platform", "safety")]
    suites = [
        ("sched", ["tests/host/test_sched.c", "platform/core/sched.c"]),
        ("thermal", ["tests/host/test_thermal.c", "platform/control/thermal_pi.c",
                     "platform/safety/interlock.c"]),
    ]
    problems, total = [], 0
    for name, srcs in suites:
        exe = f"/tmp/gate_t_{name}"
        cmd = ["gcc", "-std=c11", "-Wall", "-Werror", *inc,
               *[os.path.join(fw, s) for s in srcs], "-lm", "-o", exe]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if p.returncode != 0:
            problems.append(f"{name}: 编译失败 {p.stderr[-150:]}")
            continue
        r = subprocess.run([exe], capture_output=True, text=True, timeout=60)
        m = re.search(r"RESULT: (\d+) passed, (\d+) failed", r.stdout)
        if not m:
            problems.append(f"{name}: 未见 RESULT 行(测试可能被跳过)")
            continue
        n_pass, n_fail = int(m.group(1)), int(m.group(2))
        total += n_pass
        if n_fail != 0 or r.returncode != 0:
            problems.append(f"{name}: 失败 {n_fail},退出码 {r.returncode}")
    if total < HOST_TEST_MIN:
        problems.append(f"断言总数 {total} < 硬门槛 {HOST_TEST_MIN}(测试静默变少?)")
    return problems, {"asserts": total}


# ── 已实现的绿腿:分层依赖检查(G3) ──
def leg_layer_deps():
    """platform/products 不得 include 芯片头;扫描数低于下限即红(防静默空转)。"""
    import subprocess
    p = subprocess.run(
        [sys.executable, os.path.join(HERE, "firmware", "tools", "check_layers.py")],
        capture_output=True, text=True, timeout=60,
    )
    try:
        data = json.loads(p.stdout)
    except json.JSONDecodeError:
        return [f"check_layers 输出不可解析: {p.stdout[-150:]}"], {}
    problems = list(data.get("violations", []))
    checked = data.get("checked", 0)
    if checked < LAYER_FILES_MIN:
        problems.append(f"扫描文件数 {checked} < 下限 {LAYER_FILES_MIN}(目录空转?)")
    return problems, {"files": checked}


# ── 已实现的绿腿:L1 溯源核验(D1) ──
def leg_provenance():
    """引用解析核验单测:真值放行/篡改与伪造页 100% 拦/中英等强/无出处硬阻断/真 PDF 回环。"""
    import subprocess
    p = subprocess.run(
        [sys.executable, "test_provenance.py"],
        capture_output=True, text=True, timeout=180,
        cwd=os.path.join(HERE, "provenance"),
    )
    out = (p.stdout or "") + (p.stderr or "")
    m = re.search(r"RESULT: (\d+) passed, (\d+) failed", out)
    problems = []
    if not m:
        return [f"未见 RESULT 行(rc={p.returncode}): {out[-200:]}"], {}
    n_pass, n_fail = int(m.group(1)), int(m.group(2))
    if n_fail != 0 or p.returncode != 0:
        problems.append(f"失败 {n_fail},退出码 {p.returncode}")
    if n_pass < PROVENANCE_MIN:
        problems.append(f"通过 {n_pass} < 硬门槛 {PROVENANCE_MIN}")
    return problems, {"asserts": n_pass}


# 绿腿:现在就能真跑、能给绿灯的
ACTIVE_LEGS = [
    ("scaffold-integrity", leg_scaffold_integrity),
    ("no-fake-verified", leg_no_fake_verified),
    ("cross-compile", leg_cross_compile),
    ("resource-budget", leg_resource_budget),
    ("bench-self-check", leg_bench_self_check),
    ("state-machine", leg_state_machine),
    ("host-unit-test", leg_host_unit_test),
    ("layer-deps", leg_layer_deps),
    ("provenance-check", leg_provenance),
]

# BLOCKED 腿:结构上要有,但等决策/实现解锁。诚实展示,绝不伪绿。
BLOCKED_LEGS = [
    ("static-analysis MISRA (cppcheck+clang-tidy)", "F1 已立,此腿下一张卡实现"),
    ("renode-sim (map, not territory)", "待 Renode 环境接入"),
    ("iec60730-selftest-table (L0)", "阻塞于 Q2 样例(卡 B2;D-004 已定全球合规面)"),
]


def main():
    W = 82
    print("=" * W)
    print("swe-agent gate · YCFS L2 门禁(v0)")
    print("-" * W)
    failures, legs_detail = [], []
    t0 = time.time()

    for i, (name, fn) in enumerate(ACTIVE_LEGS, 1):
        ts = time.time()
        try:
            problems, counts = fn()
        except Exception as e:  # noqa: BLE001
            problems, counts = [f"腿异常: {e}"], {}
        dt = time.time() - ts
        ok = not problems
        legs_detail.append((name, ok, dt))
        cnt = "  ".join(f"{k}={v}" for k, v in counts.items())
        print(f"[{i}/{len(ACTIVE_LEGS)}] {'✅' if ok else '❌'} {name}  ({dt:.2f}s)  {cnt}")
        if not ok:
            for pr in problems:
                print(f"        ✗ {pr}")
            failures.append(name)

    print("-" * W)
    print(f"BLOCKED(诚实展示,不计入绿,等解锁) — {len(BLOCKED_LEGS)} 腿:")
    for name, why in BLOCKED_LEGS:
        print(f"   ⏸  {name}  —  {why}")

    print("-" * W)
    _append_history(legs_detail, failures, len(BLOCKED_LEGS), time.time() - t0)

    if failures:
        print(f"门禁: ❌ FAIL — {len(failures)}/{len(ACTIVE_LEGS)} 活跃腿未过: {', '.join(failures)}")
        sys.exit(1)
    print(f"门禁: ✅ PASS — 全部 {len(ACTIVE_LEGS)} 活跃腿通过;{len(BLOCKED_LEGS)} 腿 BLOCKED 待解锁(非绿)。")
    sys.exit(0)


def _append_history(legs, failures, n_blocked, total_dt):
    """观测:每次运行落一行时间序列。落行失败只警告——观测永不干预门禁。"""
    try:
        row = {
            "result": "PASS" if not failures else "FAIL",
            "active_legs": len(legs),
            "failed": failures,
            "blocked_legs": n_blocked,
            "duration_s": round(total_dt, 2),
        }
        with open(os.path.join(HERE, "gate_history.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    except Exception as e:  # noqa: BLE001
        print(f"        (警告: gate 历史落行失败: {e})")


if __name__ == "__main__":
    main()
