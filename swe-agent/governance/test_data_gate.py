#!/usr/bin/env python3
"""H1 单测:数据门禁——NDA 硬停/具名确认/概括授权无效/approval 消耗式/restricted 路由。"""
import sys
from data_gate import Approval, Artifact, GateDecision, ProjectPolicy, request_egress

passed = failed = 0


def check(cond, name):
    global passed, failed
    if cond:
        passed += 1
    else:
        failed += 1
        print(f"FAIL: {name}")


CLOUD = ProjectPolicy("hairdryer", route="cloud")
RESTRICTED = ProjectPolicy("client_x", route="restricted")
NDA_SCH = Artifact("schematic_v2.pdf", "schematic", nda=True)
NDA_SPEC = Artifact("mcu_spec_cn.pdf", "spec", nda=True)
PUB_DOC = Artifact("stm32g474_ds.pdf", "spec", nda=False)


def ok(a, d, p, ap):  # noqa: ANN001
    return request_egress(a, d, p, ap)


# T1: NDA 原理图 → 云,无审批 → 硬停且提示需具名确认
d = ok(NDA_SCH, "cloud_llm", CLOUD, [])
check(not d.allow and d.needs_named_approval, "T1 NDA 外发无审批被硬停")

# T2: 概括授权("*")无效
d = ok(NDA_SCH, "cloud_llm", CLOUD, [Approval("*", "老板", "2026-07-07")])
check(not d.allow, "T2 通配审批不放行(概括授权无效)")

# T3: 空 artifact_id 审批无效
d = ok(NDA_SCH, "cloud_llm", CLOUD, [Approval("", "老板", "2026-07-07")])
check(not d.allow, "T3 空指向审批无效")

# T4: 具名审批放行且仅放行该工件
aps = [Approval("schematic_v2.pdf", "张工", "2026-07-07")]
d = ok(NDA_SCH, "cloud_llm", CLOUD, aps)
check(d.allow, "T4a 具名审批放行对应工件")
d = ok(NDA_SPEC, "cloud_llm", CLOUD, aps)
check(not d.allow, "T4b 同一审批不覆盖第二个工件")

# T5: 审批消耗式——同一工件第二次外发需再次确认
aps = [Approval("schematic_v2.pdf", "张工", "2026-07-07")]
ok(NDA_SCH, "cloud_llm", CLOUD, aps)
d = ok(NDA_SCH, "cloud_llm", CLOUD, aps)
check(not d.allow, "T5 一次确认只放行一次")

# T6: 非 NDA 工件云路由直接放行(D-003)
d = ok(PUB_DOC, "cloud_llm", CLOUD, [])
check(d.allow, "T6 非 NDA 走 D-003 云默认")

# T7: restricted 项目外部目的地结构性拒绝(即使有具名审批)
d = ok(NDA_SCH, "cloud_llm", RESTRICTED, [Approval("schematic_v2.pdf", "张工", "2026-07-07")])
check(not d.allow and not d.needs_named_approval, "T7 restricted 无放行边(审批也不行)")

# T8: 本地目的地不出域,放行(含 restricted)
check(ok(NDA_SCH, "local_llm", RESTRICTED, []).allow, "T8 本地路由放行")

# T9: 未知目的地拒
check(not ok(PUB_DOC, "mystery_service", CLOUD, []).allow, "T9 未知目的地即拒")

print(f"RESULT: {passed} passed, {failed} failed")
sys.exit(0 if failed == 0 else 1)
