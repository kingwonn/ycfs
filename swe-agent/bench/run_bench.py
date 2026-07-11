#!/usr/bin/env python3
"""run_bench — agent 评测基准套件的跑分与自检(K1)。

--self-check:题目质量自检(gate 的 bench-self-check 腿跑这个):
  · 每题 manifest/记录含完整出生证;
  · bug_fix:参考实现+测试必须全绿(题目可判);buggy+测试必须变红(bug 可检出,非废题);
  · 字节同源探针:buggy 源与参考实现不得同源(否则没埋 bug);
  · 真值哈希与 manifest.sha256 一致(防改题凑分);
  · 题数下限(只紧不松)。
--list:列出全部题目与出生证。
agent 跑分模式待 M1 执行脊柱接入。
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
REF_IMPL = os.path.join(REPO, "firmware", "src", "protection.c")
INCLUDE = os.path.join(REPO, "firmware", "src")
TEST = os.path.join(HERE, "cases", "bug_fix", "test_protection.c")
SHA_FILE = os.path.join(HERE, "manifest.sha256")

# ── 硬门槛(只紧不松) ──
BUGFIX_MIN = 2
SPECQA_MIN = 6


def _compile_and_run(impl_path):
    """host gcc 编译 测试+被测实现,返回 (exit_code, output)。"""
    with tempfile.TemporaryDirectory() as td:
        exe = os.path.join(td, "t")
        p = subprocess.run(
            ["gcc", "-std=c11", "-Wall", "-I", INCLUDE, TEST, impl_path, "-o", exe],
            capture_output=True, text=True, timeout=120,
        )
        if p.returncode != 0:
            return 100, "COMPILE_FAIL:\n" + p.stderr
        r = subprocess.run([exe], capture_output=True, text=True, timeout=60)
        return r.returncode, r.stdout + r.stderr


def _sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def _truth_files():
    files = [TEST, REF_IMPL, os.path.join(HERE, "cases", "spec_qa.jsonl")]
    for case in sorted(_bugfix_cases()):
        files.append(os.path.join(case, "manifest.json"))
        files.append(os.path.join(case, "protection_buggy.c"))
    return files


def _bugfix_cases():
    root = os.path.join(HERE, "cases", "bug_fix")
    return [os.path.join(root, d) for d in sorted(os.listdir(root))
            if os.path.isdir(os.path.join(root, d))]


def write_hashes():
    with open(SHA_FILE, "w", encoding="utf-8") as f:
        for p in _truth_files():
            f.write(f"{_sha(p)}  {os.path.relpath(p, REPO)}\n")
    print(f"已写 {SHA_FILE}")


def self_check():
    problems, n_bugfix, n_specqa = [], 0, 0

    # 1) 参考实现必须让测试全绿(题目可判)
    rc, out = _compile_and_run(REF_IMPL)
    if rc != 0:
        problems.append(f"参考实现未过判定测试(rc={rc}):题目本身不可判\n{out[-400:]}")
    ref_hash = _sha(REF_IMPL)

    # 2) 每道 bug_fix:出生证完整 + buggy 必须变红 + 非同源
    for case in _bugfix_cases():
        n_bugfix += 1
        cid = os.path.basename(case)
        mpath = os.path.join(case, "manifest.json")
        bpath = os.path.join(case, "protection_buggy.c")
        try:
            m = json.load(open(mpath, encoding="utf-8"))
            prov = m["provenance"]
            for k in ("constructed_by", "truth_anchor", "date"):
                if not prov.get(k):
                    problems.append(f"{cid}: 出生证缺 {k}")
        except Exception as e:  # noqa: BLE001
            problems.append(f"{cid}: manifest 不可读 {e}")
            continue
        if _sha(bpath) == ref_hash:
            problems.append(f"{cid}: buggy 与参考实现字节同源——没埋 bug(自证探针)")
            continue
        rc, out = _compile_and_run(bpath)
        if rc == 0:
            problems.append(f"{cid}: buggy 竟然全绿——bug 不可检出,废题")
        elif rc == 100:
            problems.append(f"{cid}: buggy 编译失败(应是逻辑 bug 而非编译错)\n{out[-200:]}")

    # 3) spec_qa:schema + 出处非空
    qa_path = os.path.join(HERE, "cases", "spec_qa.jsonl")
    for i, line in enumerate(open(qa_path, encoding="utf-8"), 1):
        if not line.strip():
            continue
        n_specqa += 1
        try:
            q = json.loads(line)
            if not (q.get("question") and q.get("answer")):
                problems.append(f"spec_qa 第{i}行: 缺问题或答案")
            if not q.get("provenance", {}).get("url"):
                problems.append(f"spec_qa 第{i}行: 出处 URL 为空(零编造)")
        except json.JSONDecodeError as e:
            problems.append(f"spec_qa 第{i}行: JSON 不合法 {e}")

    # 4) 题数下限(只紧不松)
    if n_bugfix < BUGFIX_MIN:
        problems.append(f"bug_fix 题数 {n_bugfix} < 下限 {BUGFIX_MIN}")
    if n_specqa < SPECQA_MIN:
        problems.append(f"spec_qa 题数 {n_specqa} < 下限 {SPECQA_MIN}")

    # 5) 真值哈希锁(防改题凑分)
    if os.path.exists(SHA_FILE):
        for line in open(SHA_FILE, encoding="utf-8"):
            want, rel = line.strip().split(None, 1)
            p = os.path.join(REPO, rel)
            if not os.path.exists(p):
                problems.append(f"哈希锁指向的文件消失: {rel}")
            elif _sha(p) != want:
                problems.append(f"真值文件被改动且未重签哈希锁: {rel}")
    else:
        problems.append("缺 manifest.sha256(先跑 --write-hashes)")

    print(json.dumps({"bug_fix": n_bugfix, "spec_qa": n_specqa,
                      "problems": problems}, ensure_ascii=False, indent=1))
    return 0 if not problems else 1


def list_cases():
    for case in _bugfix_cases():
        m = json.load(open(os.path.join(case, "manifest.json"), encoding="utf-8"))
        print(f"[bug_fix] {m['id']} — {m['seeded_bug'][:50]}… 出生证:{m['provenance']['date']}")
    for line in open(os.path.join(HERE, "cases", "spec_qa.jsonl"), encoding="utf-8"):
        if line.strip():
            q = json.loads(line)
            print(f"[spec_qa] {q['id']} — {q['question'][:40]}… 出处:{q['provenance']['url'][:50]}")


if __name__ == "__main__":
    if "--write-hashes" in sys.argv:
        write_hashes()
    elif "--list" in sys.argv:
        list_cases()
    else:
        sys.exit(self_check())
