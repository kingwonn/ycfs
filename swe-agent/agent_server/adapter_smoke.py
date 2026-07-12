#!/usr/bin/env python3
"""A1 增量一冒烟:opencode server API 面 + SSE 事件流 → 审计链落盘 + 防篡改自证。

覆盖 A1 验收的前两条(健康检查/事件流 append-only);
「样例任务重放字节一致」需 LLM prompt——等 ANTHROPIC_API_KEY(PENDING_HUMAN Q12)。
"""
import json
import subprocess
import sys
import threading
import time
import urllib.request

sys.path.insert(0, __import__("os").path.dirname(__file__))
from audit import append_event, verify_chain  # noqa: E402

BASE = "http://127.0.0.1:4096"
LOG = "/tmp/a1_audit.jsonl"
passed = failed = 0


def check(cond, name):
    global passed, failed
    if cond:
        passed += 1
    else:
        failed += 1
        print(f"FAIL: {name}")


def api(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method,
                                 data=json.dumps(body).encode() if body else None,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())


def capture_sse(stop, out):
    req = urllib.request.Request(BASE + "/event")
    with urllib.request.urlopen(req, timeout=30) as r:
        for raw in r:
            if stop.is_set():
                break
            line = raw.decode().strip()
            if line.startswith("data:"):
                out.append(json.loads(line[5:]))


def main():
    import os
    if os.path.exists(LOG):
        os.remove(LOG)

    # T1: 健康检查(OpenAPI /doc)
    doc = api("GET", "/doc")
    check(doc.get("openapi", "").startswith("3.1"), "T1 server 健康(/doc OpenAPI 3.1)")

    # T2: SSE 事件流订阅 → 触发会话事件 → 捕获
    events, stop = [], threading.Event()
    t = threading.Thread(target=capture_sse, args=(stop, events), daemon=True)
    t.start()
    time.sleep(1)
    s = api("POST", "/session", {"title": "A1-audit-smoke"})
    check(bool(s.get("id")), "T2a 会话创建")
    time.sleep(2)
    stop.set()
    check(len(events) >= 1, f"T2b SSE 捕获到事件({len(events)} 条)")

    # T3: 事件逐条入审计链
    for e in events:
        append_event(LOG, e)
    ok, probs, n = verify_chain(LOG)
    check(ok and n == len(events), f"T3 审计链完整({n} 条)")

    # T4: 防篡改——改历史任意一行,链必红
    lines = open(LOG).read().splitlines()
    if lines:
        row = json.loads(lines[0])
        row["event"]["__tampered"] = True
        lines[0] = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        open(LOG + ".tampered", "w").write("\n".join(lines) + "\n")
        ok2, _, _ = verify_chain(LOG + ".tampered")
        check(not ok2, "T4 篡改历史行被链校验抓红")

    print(f"RESULT: {passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
