#!/usr/bin/env python3
"""腿:对外状态机行为验收。

守什么:无审批即硬阻断;审批绑定哈希,篡改即失效;deny-by-default;红线命中即拒。
property 风格:N 条被篡改载荷必全判红(零漏放),N 条已审批真载荷必全放行(零误伤)。
输出末行 "结果: N 通过, M 失败" 供 gate 解析;M≠0 或 N 低于硬门槛即腿红。
"""
import importlib.util
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
_spec = importlib.util.spec_from_file_location("outbound", ROOT / "runtime" / "outbound.py")
outbound = importlib.util.module_from_spec(_spec)

PASSED = FAILED = 0


def check(cond, name):
    global PASSED, FAILED
    if cond:
        PASSED += 1
    else:
        FAILED += 1
        print(f"  ✗ {name}")


def expect_raises(exc, fn, name):
    try:
        fn()
    except exc:
        check(True, name)
    except Exception as e:  # 错误类型也算失败——错误要具名
        check(False, f"{name}(抛了 {type(e).__name__} 而非 {exc.__name__}: {e})")
    else:
        check(False, f"{name}(未阻断,静默放行!)")


def main():
    with tempfile.TemporaryDirectory() as tmp:
        os.environ["YCFS_ROOT"] = tmp
        _spec.loader.exec_module(outbound)
        pend = Path(tmp) / "GATES" / "OUTBOX" / "pending"

        # ── deny-by-default ──
        expect_raises(outbound.Denied, lambda: outbound.submit("wire_transfer", "anywhere", "x"),
                      "未列 kind 必拒")
        expect_raises(outbound.Denied, lambda: outbound.submit("email", "ceo@else.com", "x"),
                      "kind 允许但 target 不匹配必拒")
        expect_raises(outbound.Denied,
                      lambda: outbound.submit("email", "review@exampleXcom", "x"),
                      "target_pattern 必须 fullmatch(. 不作通配旁路)")

        # ── 红线:载荷命中拒绝模式,即使 kind/target 都允许 ──
        for bad in ["-----BEGIN RSA PRIVATE KEY-----", "password=hunter2", "11010119900307771X"]:
            expect_raises(outbound.Denied,
                          lambda b=bad: outbound.submit("email", "review@example.com", b),
                          f"红线载荷必拒: {bad[:20]}…")

        # ── 无审批即硬阻断 ──
        i = outbound.submit("email", "review@example.com", "hello r1")
        expect_raises(outbound.Blocked, lambda: outbound.release(i), "无审批文件 release 必阻断")
        check((pend / f"{i}.json").exists(), "阻断后仍留在 pending(不销毁、不放行)")

        # ── 审批 → 放行;放行不可重放 ──
        outbound.approve(i)
        rec = outbound.release(i)
        check(rec["status"] == "released", "审批后放行,状态=released")
        expect_raises(outbound.Blocked, lambda: outbound.release(i), "已放行项不可重放")

        # ── property:20 条审批后被篡改的载荷,必全判红(零漏放) ──
        for k in range(20):
            j = outbound.submit("email", "review@example.com", f"legit-{k}")
            outbound.approve(j)
            p = pend / f"{j}.json"
            r = json.loads(p.read_text(encoding="utf-8"))
            r["payload"] = f"tampered-{k}"  # 审批之后偷改载荷
            p.write_text(json.dumps(r, ensure_ascii=False), encoding="utf-8")
            expect_raises(outbound.Blocked, lambda jj=j: outbound.release(jj),
                          f"篡改#{k} 必阻断")

        # ── property:20 条已审批真载荷,必全放行(零误伤) ──
        for k in range(20):
            j = outbound.submit("email", "review@example.com", f"clean-{k}")
            outbound.approve(j)
            try:
                check(outbound.release(j)["status"] == "released", f"真载荷#{k} 零误伤")
            except Exception as e:
                check(False, f"真载荷#{k} 被误阻断: {e}")

    print(f"结果: {PASSED} 通过, {FAILED} 失败")
    sys.exit(0 if FAILED == 0 else 1)


if __name__ == "__main__":
    main()
