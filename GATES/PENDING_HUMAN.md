# PENDING_HUMAN — 等人签字/回答(loop 不等待,但每轮报告)

> 回答方式:直接在任何会话里说,当值 AI 会更新对应卡状态并解除阻塞。

## 方向 gate(战略选择,答案会改变要做什么)
1. **Lane R 继续推进顺序**:R1 已全绿。默认按 R4(EARS 验收 lint,零外部依赖)→ R2(分支保护)→ R3(L1 出口双门)推进 — 建议:同意默认;若你想先接某个真实项目,直接说,R3 会提前。

## 数据 gate(PII / 非本项目资源 / 不可逆)
2. 暂无。

## 对外 gate(发送 / 发布 / 花钱 / 生产切换)
3. **R2 分支保护配置**:GitHub 仓库设置"生成者≠合并者 + agent 身份无 merge 权"只能仓库管理员操作 — 需要你在 Settings → Branches 配置;配置后 R2 的 CI 腿才有意义。

## 事实核实(决定哪些牌能打)
4. **R3 的真源**:L1 出口双门需要一个真实项目的"真值源"(数据库/凭证/基线文件)。你想先接哪个项目?它的真值有出生证吗(谁编/何时/被谁接受)?

---
每条写清:**触发条件、需要人给什么、答案解锁什么**。让签字变成 10 秒的事。

## 权限 gate(功法第 0 步 —— 只有你能做,我做了不算)
5. **激活 hook**:把 `runtime/claude-settings.example.json` 的内容并入项目 `.claude/settings.json`。
   现状:hook 已写好、已实测(Edit 与 Bash 两条通道的绕过全部封死),但**没有生效**——
   它只是仓库里的一个文件。**我自己装上它,等于被测给自己上锁,不算数**;
   由你装,它才是一条 agent 够不到的边界。
   验收:装好后 `echo '{"tool_name":"Edit","tool_input":{"file_path":"runtime/gate.py"}}' | python3 runtime/hooks/pre_tool_use.py` 在真实会话里生效。

6. **把不可逆能力从环境里拿掉**(比 hook 更硬的一层):
   凭证、出网、生产库连接——不要靠正则禁止 agent 用,直接让它在环境里拿不到。
   研究给的判据:**它拿不到密钥,就不需要你写规则禁止它用密钥。**
   正则防线可以被穷举绕过(本轮已实测穿透一次),权限边界不能。

7. **启用 GitHub Pages(把产品定义发成可分享的站点)**:
   仓库 Settings → Pages → Source 设为 **"GitHub Actions"**(仓库管理员权限,agent 够不到)。
   现状:`.github/workflows/pages.yml` 已写好——先跑 `gate`(红则不发)+ 阴性对照 + 重生成无 diff,
   再上传 `site/`;**deploy 只在默认分支 `main` 触发**(功能分支只验证不发布,避开环境保护)。
   验收:启用后,把本分支合入 `main` → Actions 的 pages 工作流绿 → 站点 URL 可访问
   (`index.html` 总览 → product/spec/techstack 三页)。
   ⚠ 说明:从功能分支部署 Pages 受 `github-pages` 环境保护限制,正式对外须在受保护主分支发。
