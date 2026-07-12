"""agent_server.audit — append-only 事件审计链(A1/E1 内核)。

每行 = {seq, prev, hash, event}:hash = sha256(prev + canonical(event))。
篡改/删除/重排任意历史行 → verify_chain 必红。这是「可追索/可审计」的最小硬核:
真相不靠 opencode 本地存储(可随时重启),靠这条链。
"""
import hashlib
import json
import os

GENESIS = "0" * 64


def _canon(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def append_event(path: str, event: dict) -> dict:
    """追加一条事件,返回落盘的信封行。"""
    prev, seq = GENESIS, 0
    if os.path.exists(path) and os.path.getsize(path) > 0:
        with open(path, "rb") as f:
            last = f.read().splitlines()[-1]
        row = json.loads(last)
        prev, seq = row["hash"], row["seq"] + 1
    h = hashlib.sha256((prev + _canon(event)).encode()).hexdigest()
    row = {"seq": seq, "prev": prev, "hash": h, "event": event}
    with open(path, "a", encoding="utf-8") as f:
        f.write(_canon(row) + "\n")
    return row


def verify_chain(path: str):
    """校验整条链;返回 (ok, problems, n)。"""
    problems, prev, n = [], GENESIS, 0
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f):
            if not line.strip():
                continue
            row = json.loads(line)
            want = hashlib.sha256((prev + _canon(row["event"])).encode()).hexdigest()
            if row["seq"] != n:
                problems.append(f"行{i}: seq {row['seq']} ≠ {n}(删行/重排?)")
            if row["prev"] != prev:
                problems.append(f"行{i}: prev 断链")
            if row["hash"] != want:
                problems.append(f"行{i}: hash 不符(事件被篡改)")
            prev, n = row["hash"], n + 1
    return (not problems), problems, n
