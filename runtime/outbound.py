#!/usr/bin/env python3
"""outbound — 对外动作唯一 choke-point(YCFS 对外门禁参考实现,雷达路线图①)

状态机:submit → pending_review → released / rejected

结构保证(不是约定,是代码形状):
  · 全仓库只有这一个 release();对外动作只能经它放行(choke-point 唯一性由
    runtime/legs/leg_choke_point.py 静态腿在 gate 里守护)。
  · release() 无人审批文件即硬失败;审批绑定载荷哈希,审批后载荷被改动即失效。
  · 本文件不引入任何时间/延时机制——结构上不存在"超时自动放行"这条边
    (超时即放行 = 把硬门禁降级成软门禁,违反"门槛只紧不松")。
  · policy 为 deny-by-default:无允许规则匹配即拒;policy 文件由 hook 保护,
    agent 不可改写(法只能人立)。
  · approve 仅供人在自己的终端执行;在 Claude Code harness 下,
    runtime/hooks/pre_tool_use.py 拒绝 agent 调用 approve 或写 GATES/APPROVALS/。
"""
import hashlib
import json
import os
import re
import sys
import uuid
from pathlib import Path

_HERE = Path(__file__).resolve().parent
POLICY_PATH = _HERE / "policy.json"


class Denied(Exception):
    """提交被 policy 拒绝(deny-by-default 或红线命中)。"""


class Blocked(Exception):
    """放行被硬阻断(无审批 / 审批失效)。"""


def _root() -> Path:
    # 测试经 YCFS_ROOT 指向临时目录,不碰真实 GATES;法(policy)始终读仓库内真身。
    return Path(os.environ.get("YCFS_ROOT") or _HERE.parent)


def _dirs():
    root = _root()
    d = {
        "pending": root / "GATES" / "OUTBOX" / "pending",
        "released": root / "GATES" / "OUTBOX" / "released",
        "rejected": root / "GATES" / "OUTBOX" / "rejected",
        "approvals": root / "GATES" / "APPROVALS",
    }
    for p in d.values():
        p.mkdir(parents=True, exist_ok=True)
    return d


def _sha256(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _load_policy() -> dict:
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    if policy.get("default") != "deny":
        raise Denied("policy.default 必须是 deny——deny-by-default 是硬要求")
    return policy


def submit(kind: str, target: str, payload: str) -> str:
    """登记一个对外动作。返回 item id;被 policy 拒绝则抛 Denied 并落 rejected 记录。"""
    policy = _load_policy()
    d = _dirs()

    reason = None
    for pat in policy.get("deny_payload_patterns", []):
        if re.search(pat, payload):
            reason = f"红线命中: 载荷匹配拒绝模式 {pat!r}"
            break
    if reason is None:
        allowed = any(
            rule.get("kind") == kind and re.fullmatch(rule.get("target_pattern", "$^"), target)
            for rule in policy.get("allow", [])
        )
        if not allowed:
            reason = f"deny-by-default: 无允许规则匹配 kind={kind!r} target={target!r}"

    item_id = uuid.uuid4().hex[:12]
    if reason is not None:
        (d["rejected"] / f"{item_id}.json").write_text(
            json.dumps({"id": item_id, "kind": kind, "target": target,
                        "status": "rejected", "reason": reason}, ensure_ascii=False, indent=2),
            encoding="utf-8")
        raise Denied(reason)

    record = {"id": item_id, "kind": kind, "target": target,
              "payload": payload, "sha256": _sha256(payload), "status": "pending_review"}
    (d["pending"] / f"{item_id}.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    return item_id


def approve(item_id: str) -> Path:
    """人审批:把当前载荷哈希写进审批文件。仅供人在自己的终端执行(hook 拒 agent)。"""
    d = _dirs()
    pending = d["pending"] / f"{item_id}.json"
    if not pending.exists():
        raise Blocked(f"无此待审项: {item_id}")
    record = json.loads(pending.read_text(encoding="utf-8"))
    approval = d["approvals"] / f"{item_id}.approval"
    approval.write_text(
        json.dumps({"id": item_id, "sha256": _sha256(record["payload"])},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    return approval


def release(item_id: str) -> dict:
    """唯一放行函数。审批文件缺失或哈希不符 → Blocked,绝不放行。"""
    d = _dirs()
    pending = d["pending"] / f"{item_id}.json"
    if not pending.exists():
        raise Blocked(f"无此待审项: {item_id}")
    record = json.loads(pending.read_text(encoding="utf-8"))

    approval_path = d["approvals"] / f"{item_id}.approval"
    if not approval_path.exists():
        raise Blocked(f"未见人审批文件: {approval_path.name} —— 对外动作人审前不可执行")
    approval = json.loads(approval_path.read_text(encoding="utf-8"))
    if approval.get("sha256") != _sha256(record["payload"]):
        raise Blocked("审批哈希不匹配: 载荷在审批后被改动,审批失效,退回人审")

    record["status"] = "released"
    (d["released"] / f"{item_id}.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    pending.unlink()
    return record


def _cli(argv):
    usage = "用法: outbound.py submit <kind> <target> <payload> | approve <id> | release <id> | list"
    if not argv:
        print(usage); return 2
    cmd, args = argv[0], argv[1:]
    try:
        if cmd == "submit" and len(args) == 3:
            print(submit(*args)); return 0
        if cmd == "approve" and len(args) == 1:
            print(f"已审批: {approve(args[0])}"); return 0
        if cmd == "release" and len(args) == 1:
            rec = release(args[0])
            print(f"已放行: {rec['id']} kind={rec['kind']} target={rec['target']}"); return 0
        if cmd == "list":
            for sub in ("pending", "released", "rejected"):
                for f in sorted(_dirs()[sub].glob("*.json")):
                    print(f"{sub}: {f.stem}")
            return 0
    except (Denied, Blocked) as e:
        print(f"❌ {e}", file=sys.stderr); return 1
    print(usage); return 2


if __name__ == "__main__":
    sys.exit(_cli(sys.argv[1:]))
