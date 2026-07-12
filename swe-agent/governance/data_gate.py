"""governance.data_gate — 数据门禁策略核心(H1;D-003:云默认 + 按项目可收紧)。

语义(YCFS 数据门禁):
  · NDA 标记的工件(规格书/原理图/老项目资料)送往外部目的地(云 LLM/云沙箱)时,
    denylist 命中即硬停,需**逐一具名确认**;
  · 概括授权无效:approval 绑定且仅绑定一个具名工件,artifact_id 为通配/空一律拒;
  · 一次 approval 只放行一次(消耗式),第二个工件/第二次外传不被覆盖;
  · 路由:默认 cloud(D-003 SOTA 优先);项目标记 restricted 时强制 local,云目的地直接拒。
执行点:本模块为策略内核(纯逻辑,host 单测);实际拦截钩子随 A1 执行脊柱适配层接线
(opencode plugin permission.ask / PreToolUse 等价物),届时调用本内核裁决。
"""
from dataclasses import dataclass, field

EXTERNAL_DESTINATIONS = {"cloud_llm", "cloud_sandbox", "external_api"}
LOCAL_DESTINATIONS = {"local_llm", "local_sandbox", "local_fs"}


@dataclass
class Artifact:
    id: str
    kind: str           # "spec" | "schematic" | "legacy_project" | "code" | ...
    nda: bool = False   # NDA/客户机密标记


@dataclass
class Approval:
    artifact_id: str    # 必须具名;"*"/空 无效
    approver: str
    date: str
    consumed: bool = False

    def valid_for(self, artifact_id: str) -> bool:
        return (bool(self.artifact_id) and self.artifact_id != "*"
                and self.artifact_id == artifact_id
                and bool(self.approver) and not self.consumed)


@dataclass
class ProjectPolicy:
    project: str
    route: str = "cloud"        # "cloud"(D-003 默认) | "restricted"(强制本地)


@dataclass
class GateDecision:
    allow: bool
    reason: str
    needs_named_approval: bool = False


def request_egress(artifact: Artifact, destination: str,
                   policy: ProjectPolicy, approvals: list) -> GateDecision:
    """裁决一次工件外发。允许时消耗对应 approval(一次一件一放行)。"""
    external = destination in EXTERNAL_DESTINATIONS
    if destination not in EXTERNAL_DESTINATIONS | LOCAL_DESTINATIONS:
        return GateDecision(False, f"未知目的地 {destination}——未知即拒")

    # restricted 项目:外部目的地结构性拒绝(不是要审批,是没有这条边)
    if policy.route == "restricted" and external:
        return GateDecision(False,
                            f"项目 {policy.project} 为 restricted:{destination} 不存在放行边(需项目级改法)")

    # 本地目的地不出域,放行
    if not external:
        return GateDecision(True, "本地目的地,不出域")

    # 外部目的地:非 NDA 按 D-003 云默认放行;NDA 必须具名确认
    if not artifact.nda:
        return GateDecision(True, "非 NDA 工件,D-003 云路由放行")

    for ap in approvals:
        if ap.valid_for(artifact.id):
            ap.consumed = True
            return GateDecision(True, f"NDA 工件经具名确认放行(approver={ap.approver})")
    return GateDecision(False,
                        f"NDA 工件『{artifact.id}』外发 {destination} 被硬停——需逐一具名确认(概括授权无效)",
                        needs_named_approval=True)
