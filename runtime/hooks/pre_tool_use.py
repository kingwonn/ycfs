#!/usr/bin/env python3
"""PreToolUse hook — deny-by-default 对外拦截 + "法不可被 agent 改写"。

接线(runtime/claude-settings.example.json 抄进项目 .claude/settings.json):
  PreToolUse: Bash / Write / Edit / MultiEdit / NotebookEdit → 本脚本。

拒绝三类事,其余放行:
  1. Bash 里的对外原语(发信/上传/发布/推 main)——对外动作必须走 runtime/outbound.py 的
     submit→人审→release,不许 agent 直接出网。
  2. Bash 自批:outbound.py approve 只许人在自己的终端跑。
  3. 写"法"与"人签名区":GATES/APPROVALS/、GATES/OUTBOX/released/、runtime/policy.json。

注:模式里个别词用字符类拆开(如 cur[l]),避免被 choke-point 静态扫描腿当成对外原语误报。
"""
import json
import re
import sys

OUTBOUND_BASH = [
    r"\bcur[l]\b.*(-X\s*(POST|PUT|DELETE)|--data\b|-d\s|--upload-file\b|-F\s)",
    r"\bwge[t]\b.*--post",
    r"\b(sendmail|mailx?)\b",
    r"\bscp\b|\brsync\b.*:",
    r"\bnpm\s+publish\b|\btwine\s+upload\b|\bgem\s+push\b|\bcargo\s+publish\b",
    r"\bdocker\s+push\b|\bgh\s+release\b",
    r"\bgit\s+push\b.*\b(main|master)\b",
    r"outbound\.py\s+(approve|release)\b",
]

# 法与人签名区:agent 一律不可写。
# 教训(实测穿透):此前只列三条,gate.py / legs/ / hook 自身 / anchors.json 全在
# 执行者写域内——执法者可以改写自己。
PROTECTED_PATHS = [
    r"GATES/APPROVALS/",
    r"GATES/OUTBOX/released/",
    r"GATES/REALITY\.jsonl$",        # 历练台账:唯一外部锚,不许被测改
    r"runtime/policy\.json$",
    r"runtime/anchors\.json$",       # 真值锚声明
    r"runtime/floor\.lock\.json$",   # 棘轮基线
    r"runtime/gate\.py$",            # 执法者本身
    r"runtime/legs/",                # 断言本身
    r"runtime/hooks/",               # hook 此前连自己都不保护
    r"runtime/scale_history\.jsonl$",  # 趋势(哈希链另有校验,双保险)
]

# Bash 写入通道。教训(实测穿透):此前 Bash 分支只查对外原语、完全不查文件写入,
# 于是 `echo {} > runtime/policy.json` 畅通无阻——"此文件只能人改"是一句假话。
BASH_WRITE = [
    r">>?\s*\S*(?:policy|anchors|floor\.lock)\.json",
    r">>?\s*\S*runtime/(?:gate\.py|legs/|hooks/)",
    r">>?\s*\S*(?:GATES/APPROVALS|GATES/REALITY|scale_history)",
    r"\bsed\b[^|;]*-i",                    # 原地编辑
    r"\btee\b[^|;]*\s(?:runtime|GATES)/",
    r"\b(?:cp|mv|install)\b[^|;]*\s(?:runtime|GATES)/\S*(?:policy|anchors|gate\.py|legs/|hooks/|floor\.lock)",
    r"\btruncate\b|\bshred\b",
    r"python3?\s+-c\b[^|;]*open\([^)]*['\"](?:w|a)",   # python 单行写文件
    r"\bgit\s+checkout\b[^|;]*\bruntime/",  # 用 git 回滚绕过保护
]


def deny(reason: str):
    print(json.dumps({
        "decision": "block",
        "reason": reason,
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        },
    }, ensure_ascii=False))
    sys.exit(0)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # 读不懂输入不裁决,交回默认权限系统

    tool = data.get("tool_name", "")
    ti = data.get("tool_input", {}) or {}

    if tool == "Bash":
        cmd = ti.get("command", "")
        for pat in OUTBOUND_BASH:
            if re.search(pat, cmd):
                deny("对外/自批动作被门禁拦截:必须走 runtime/outbound.py 的 "
                     "submit → 人审(GATES/PENDING_HUMAN)→ release。命中: " + pat)
        for pat in BASH_WRITE:
            if re.search(pat, cmd):
                deny("经 Bash 写入法/人签名区被拦截。法只能人改,且不得绕道 shell。"
                     "命中: " + pat)

    if tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        path = ti.get("file_path", "") or ti.get("notebook_path", "")
        for pat in PROTECTED_PATHS:
            if re.search(pat, path):
                deny("此路径是法/人签名区,agent 不可写: " + path)

    sys.exit(0)  # 放行


if __name__ == "__main__":
    main()
