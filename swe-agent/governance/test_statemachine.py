#!/usr/bin/env python3
"""C1 单测:验证「gate 绿→verified」这条边结构上不存在,且审计能抓绕过。"""
import sys
from statemachine import ALLOWED, Card, RealMachineSignoff, StructuralGateError, audit

passed = failed = 0


def check(cond, name):
    global passed, failed
    if cond:
        passed += 1
    else:
        failed += 1
        print(f"FAIL: {name}")


def expect_structural(fn, name):
    try:
        fn()
        check(False, name + "(未抛 StructuralGateError)")
    except StructuralGateError:
        check(True, name)


def good_signoff(card_id="C-1"):
    return RealMachineSignoff(
        card_id=card_id, signer_name="张工", signer_role="固件测试负责人",
        date="2026-07-07", evidence=["evidence/scope-stall-trip.png"],
        statement="实测堵转跳闸 480ms,波形见附件",
    )


# T1: gate 全绿也不能走通用转移到 verified
c = Card("C-1", state="done", gate_green=True)
expect_structural(lambda: c.transition("verified"), "T1 done+gate_green transition('verified') 被结构性拒绝")

# T2: 白名单里没有任何 (*, verified) 边
check(not any(to == "verified" for _f, to in ALLOWED), "T2 转移白名单结构上无 verified 边")

# T3: transition_verified 无签字 → 拒绝
c = Card("C-1", state="done", gate_green=True)
expect_structural(lambda: c.transition_verified(None), "T3 缺签字被拒")

# T4: 签字证据为空 → 拒绝
s = good_signoff(); s.evidence = []
expect_structural(lambda: Card("C-1", state="done").transition_verified(s), "T4 空证据签字被拒")

# T5: 签字张冠李戴(指向别的卡)→ 拒绝
expect_structural(lambda: Card("C-2", state="done").transition_verified(good_signoff("C-1")),
                  "T5 签字卡号不符被拒(概括授权无效)")

# T6: 未到 done(机器验收未过)→ 拒绝
expect_structural(lambda: Card("C-1", state="in-progress").transition_verified(good_signoff()),
                  "T6 未过机器验收不得 verified")

# T7: 正道:done + 有效签字 → verified
c = Card("C-1", state="done")
check(c.transition_verified(good_signoff()) == "verified", "T7 有效签字进入 verified")

# T8: 审计抓绕过——手工伪造 verified 无签字(模拟直接改存储)
tampered = Card("C-9", state="done"); tampered.state = "verified"  # 绕过转移函数直改
probs, pending = audit([tampered, Card("C-3", state="done"), c])
check(any("绕过边" in p for p in probs), "T8 审计抓到无签字 verified")

# T9: 待真机队列可枚举(done 卡)
check(pending == ["C-3"], "T9 PENDING_HUMAN 待真机队列枚举")

# T10: 合法 verified 卡审计通过
probs2, _ = audit([c])
check(probs2 == [], "T10 合法签字卡审计零问题")

print(f"RESULT: {passed} passed, {failed} failed")
sys.exit(0 if failed == 0 else 1)
