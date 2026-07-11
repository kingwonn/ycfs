"""governance.statemachine — C1:「待真机」结构性终态断言。

YCFS 铁律:状态机上**不存在**「gate 全绿 → verified」的边。
唯一通往 verified 的转移是 `Card.transition_verified(signoff)`,它要求一份
完整有效的真机签字(RealMachineSignoff);任何其它路径——包括通用
`transition()`、包括 gate_green=True——都被结构性拒绝(抛 StructuralGateError),
这不是策略提醒,是不存在的边。

签字 schema 为最小集,E2 卡(真机证据结构化回流)将按 Q4b 答复扩展字段;
扩展只加不减(门槛只紧不松)。
"""
from dataclasses import dataclass, field

STATES = ("ready", "in-progress", "blocked-on-human", "done", "verified", "dropped")

# 显式转移白名单。注意:任何 (*, "verified") 都不在此表——结构性缺失。
ALLOWED = {
    ("ready", "in-progress"),
    ("ready", "blocked-on-human"),
    ("ready", "dropped"),
    ("in-progress", "done"),
    ("in-progress", "blocked-on-human"),
    ("in-progress", "dropped"),
    ("blocked-on-human", "ready"),
    ("blocked-on-human", "dropped"),
}


class StructuralGateError(Exception):
    """结构性拒绝:请求的边在状态机上不存在。"""


@dataclass
class RealMachineSignoff:
    card_id: str
    signer_name: str
    signer_role: str
    date: str
    evidence: list = field(default_factory=list)  # 真机证据引用(文件/URL),不得为空
    statement: str = ""                            # 签字声明,如"实测堵转跳闸 480ms,波形见附件"

    REQUIRED = ("card_id", "signer_name", "signer_role", "date", "statement")

    def validate(self):
        problems = [f"签字缺字段 {k}" for k in self.REQUIRED if not getattr(self, k)]
        if not self.evidence:
            problems.append("签字无证据引用(evidence 为空)——口头 verified 无效")
        if problems:
            raise StructuralGateError("; ".join(problems))


@dataclass
class Card:
    id: str
    state: str = "ready"
    gate_green: bool = False           # CI 全绿标志——它开不了 verified 的门
    signoff: RealMachineSignoff | None = None

    def transition(self, to):
        """通用转移:走白名单。到 verified 的请求一律结构性拒绝。"""
        if to == "verified":
            raise StructuralGateError(
                f"{self.id}: 不存在『{self.state} → verified』的边;"
                "verified 只能经 transition_verified(signoff) 携带真机签字进入"
            )
        if (self.state, to) not in ALLOWED:
            raise StructuralGateError(f"{self.id}: 不存在『{self.state} → {to}』的边")
        self.state = to
        return self.state

    def transition_verified(self, signoff):
        """唯一通往 verified 的边:done + 有效真机签字。gate_green 不是充分条件。"""
        if self.state != "done":
            raise StructuralGateError(
                f"{self.id}: verified 只能从 done 进入(当前 {self.state})——先过全部机器验收"
            )
        if signoff is None:
            raise StructuralGateError(f"{self.id}: 缺真机签字——gate 全绿 ≠ verified")
        signoff.validate()
        if signoff.card_id != self.id:
            raise StructuralGateError(
                f"{self.id}: 签字指向 {signoff.card_id},一次签字只绑一张具名卡(概括授权无效)"
            )
        self.signoff = signoff
        self.state = "verified"
        return self.state


def audit(cards):
    """审计扫描:任一 verified 卡缺有效签字 → 记为问题(P0:存在绕过边)。
    返回 (problems, pending_real_machine)。后者 = done 卡清单(PENDING_HUMAN 待真机队列)。"""
    problems, pending = [], []
    for c in cards:
        if c.state == "verified":
            if c.signoff is None:
                problems.append(f"{c.id}: verified 却无签字——存在绕过边,P0")
                continue
            try:
                c.signoff.validate()
            except StructuralGateError as e:
                problems.append(f"{c.id}: verified 但签字无效({e})")
            if c.signoff is not None and c.signoff.card_id != c.id:
                problems.append(f"{c.id}: 签字张冠李戴(指向 {c.signoff.card_id})")
        elif c.state == "done":
            pending.append(c.id)
        elif c.state not in STATES:
            problems.append(f"{c.id}: 未知状态 {c.state}")
    return problems, pending
