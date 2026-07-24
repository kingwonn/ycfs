#!/usr/bin/env python3
"""腿:choke-point 结构静态验证。

守什么(结构,不是行为):
  · 全仓库只有 runtime/outbound.py 定义 release()——对外放行点唯一。
  · outbound.py 不 import time、不 sleep、无 auto 放行词——结构上无"超时自动放行"边。
  · 除 outbound.py 外,仓库代码无对外网络原语(扫描豁免 legs/hooks:它们是执法层,
    模式串在源里作检测样本出现;豁免范围本身也是本腿断言之一,收窄即更严)。
  · policy default=deny 且 allow 规则 target_pattern 全部经 fullmatch 使用。
  · hook 接线示例注册了 PreToolUse 且覆盖 Bash 与写类工具;hook 源保护 APPROVALS 与 policy。
输出末行 "结果: N 通过, M 失败"。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PASSED = FAILED = 0


def check(cond, name):
    global PASSED, FAILED
    if cond:
        PASSED += 1
    else:
        FAILED += 1
        print(f"  ✗ {name}")


def main():
    outbound_src = (ROOT / "runtime" / "outbound.py").read_text(encoding="utf-8")
    hook_src = (ROOT / "runtime" / "hooks" / "pre_tool_use.py").read_text(encoding="utf-8")
    policy = json.loads((ROOT / "runtime" / "policy.json").read_text(encoding="utf-8"))
    settings = json.loads((ROOT / "runtime" / "claude-settings.example.json").read_text(encoding="utf-8"))

    py_files = [p for p in ROOT.rglob("*.py") if ".git" not in p.parts]

    # 1) release() 全仓库唯一,且在 outbound.py
    defs = [p for p in py_files if re.search(r"^def release\(", p.read_text(encoding="utf-8"), re.M)]
    check(len(defs) == 1 and defs[0].name == "outbound.py",
          f"release() 定义必须全仓库唯一且在 outbound.py(实际: {[str(p) for p in defs]})")

    # 2) outbound.py 无时间基放行
    check("import time" not in outbound_src and "sleep" not in outbound_src,
          "outbound.py 不得含 import time / sleep(无超时自动放行边)")
    check("auto" not in outbound_src.lower(), "outbound.py 不得出现 auto 字样(无自动放行)")

    # 3) release 依赖审批文件与哈希比对(静态弱证,行为由测试腿强证)
    check("approval" in outbound_src and "sha256" in outbound_src,
          "release 路径必须出现 approval 与 sha256")

    # 4) 网络原语扫描:除 outbound.py 与执法层(legs/hooks)外零命中
    net_tokens = ["requests" + ".post", "requests" + ".put", "urllib" + ".request",
                  "smtplib", "ftplib", "paramiko", "boto3", "http" + ".client"]
    exempt = {"outbound.py"}
    exempt_dirs = {"legs", "hooks"}
    hits = []
    for p in py_files:
        if p.name in exempt or (set(p.parts) & exempt_dirs):
            continue
        src = p.read_text(encoding="utf-8")
        hits += [f"{p.name}:{t}" for t in net_tokens if t in src]
    check(not hits, f"对外网络原语只许出现在 choke-point(命中: {hits})")
    check(exempt == {"outbound.py"} and exempt_dirs == {"legs", "hooks"},
          "扫描豁免范围锁定(只紧不松:改宽此集合即腿红)")

    # 5) policy:deny-by-default;allow 目标模式经 fullmatch 消费
    check(policy.get("default") == "deny", "policy.default 必须为 deny")
    check(len(policy.get("deny_payload_patterns", [])) >= 3, "红线模式 ≥ 3(只增不减)")
    check("re.fullmatch" in outbound_src, "target_pattern 必须以 fullmatch 消费(防子串旁路)")

    # 6) hook 接线与保护面
    pre = settings.get("hooks", {}).get("PreToolUse", [])
    matchers = " ".join(h.get("matcher", "") for h in pre)
    check("Bash" in matchers, "hook 示例必须覆盖 Bash")
    check("Write" in matchers and "Edit" in matchers, "hook 示例必须覆盖写类工具")
    check("GATES/APPROVALS/" in hook_src, "hook 必须保护 GATES/APPROVALS/(人签名区)")
    check(re.search(r"policy\\?\.json", hook_src) is not None, "hook 必须保护 runtime/policy.json(法只能人改)")
    check(re.search(r"approve", hook_src) is not None, "hook 必须拦 agent 自批 approve")

    # ── 出处(历练→内力):外部审计实测穿透 ──
    # "hook 的 Bash 分支只查对外原语、完全不检查文件写入,所以 policy.json 那句
    #  『此文件只能人改』对 Edit 成立,对 `echo {} > runtime/policy.json` 不成立。"
    # 该逃逸记于 GATES/REALITY.jsonl。以下断言让它不会再回来。
    check("BASH_WRITE" in hook_src, "hook 必须有 Bash 写入通道防线(仅防 Edit 不够)")
    # 用字面子串查,不做"正则里查正则"——那层转义本身就是个坑(这两条断言第一次写就踩了)
    for chan, desc in [("sed", "sed -i 原地编辑"), ("tee", "tee 写入"),
                       ("truncate", "truncate/shred 清空"),
                       ("checkout", "git checkout 回滚绕过"),
                       ("open\\(", "python -c 单行写文件")]:
        check(chan in hook_src, f"Bash 写入防线必须覆盖通道: {desc}")
    for law in ["gate\\.py", "legs/", "hooks/", "anchors\\.json", "floor\\.lock\\.json"]:
        check(law in hook_src, f"法典自身必须在保护面内: {law}")
    check("REALITY" in hook_src, "历练台账必须受保护(唯一外部锚,不许被测改)")

    print(f"结果: {PASSED} 通过, {FAILED} 失败")
    sys.exit(0 if FAILED == 0 else 1)


if __name__ == "__main__":
    main()
