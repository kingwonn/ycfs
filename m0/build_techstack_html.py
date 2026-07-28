#!/usr/bin/env python3
"""build_techstack_html — 平台/技术栈选型 HTML(供审阅)。

从 m0/techstack.json(结构化真源)生成 site/techstack.html。选型串不手抄。
含:推导链(功能→子系统→构建/CI)、子系统卡(🧬第一性/📎参考分组,每张带候选、
理由、来源、批判、服务的功能/参数)。自包含、明暗自适应,与 spec.html 同一视觉体系。
"""
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "m0" / "techstack.json"
F = ROOT / "m0" / "functions.json"
OUT = ROOT / "site" / "techstack.html"


def esc(s):
    return html.escape(str(s))


def cards(subs, fname):
    def card(s):
        fp = s["origin"] == "first-principle"
        icon = "🧬" if fp else "📎"
        tag = f"第一性·{s['basis']}" if fp else "参考他家"
        opts = "".join(f"<li>{esc(o)}</li>" for o in s.get("options", []))
        serves = " ".join(
            f"<span class=chip>{esc(r)}<i>{esc(fname.get(r, ''))}</i></span>"
            for r in s.get("serves", []))
        return (f"<div class='card {s['origin']}'>"
                f"<div class=fh><b>{icon} {esc(s['id'])} · {esc(s['layer'])}</b>"
                f"<span class=pill>{esc(tag)}</span></div>"
                f"<div class=choice>选型:<code>{esc(s['choice'])}</code></div>"
                f"<div class=opts><span class=lbl>候选</span><ul>{opts}</ul></div>"
                f"<div class=reason>{esc(s['reason'])}</div>"
                f"<div class=src>来源:{esc(s['source'])}</div>"
                f"<div class=crit>⚠ {esc(s['critique'])}</div>"
                f"<div class=serves><span class=lbl>服务</span>{serves}</div></div>")
    fpc = "".join(card(s) for s in subs if s["origin"] == "first-principle")
    rf = "".join(card(s) for s in subs if s["origin"] == "reference")
    return (f"<h3>🧬 从第一性/方法论推演的选型</h3><div class=grid>{fpc}</div>"
            f"<h3>📎 参考已验证方案的选型</h3><div class=grid>{rf}</div>")


PAGE = """<!doctype html><html lang=zh><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>平台与技术栈选型 · UMI 力觉数采</title><style>
:root{{--bg:#fff;--fg:#1a1a1a;--mut:#666;--line:#e5e7eb;--card:#fafafa;--fpc:#eef4ff;--refc:#fef6ee;--acc:#2563eb;--warn:#d97706;--crit:#b45309;--chip:#eef2f7}}
@media(prefers-color-scheme:dark){{:root{{--bg:#0f1115;--fg:#e8e8e8;--mut:#9aa0a8;--line:#2a2e37;--card:#171a21;--fpc:#14203a;--refc:#2a2015;--acc:#60a5fa;--warn:#fbbf24;--crit:#fcd34d;--chip:#1c2230}}}}
:root[data-theme=dark]{{--bg:#0f1115;--fg:#e8e8e8;--mut:#9aa0a8;--line:#2a2e37;--card:#171a21;--fpc:#14203a;--refc:#2a2015;--acc:#60a5fa;--warn:#fbbf24;--crit:#fcd34d;--chip:#1c2230}}
:root[data-theme=light]{{--bg:#fff;--fg:#1a1a1a;--mut:#666;--line:#e5e7eb;--card:#fafafa;--fpc:#eef4ff;--refc:#fef6ee;--acc:#2563eb;--warn:#d97706;--crit:#b45309;--chip:#eef2f7}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.65 -apple-system,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif}}
.wrap{{max-width:1120px;margin:0 auto;padding:30px 20px 80px}}
a.back{{color:var(--acc);text-decoration:none;font-size:13px}}
h1{{font-size:25px;margin:6px 0 4px}}.sub{{color:var(--mut);font-size:13.5px;margin:0 0 24px}}
h2{{font-size:19px;margin:34px 0 12px;padding-top:14px;border-top:1px solid var(--line)}}
h3{{font-size:15.5px;margin:20px 0 8px;color:var(--mut)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:10px;margin:6px 0}}
.card{{border:1px solid var(--line);border-radius:9px;padding:13px 15px}}
.card.first-principle{{background:var(--fpc)}}.card.reference{{background:var(--refc)}}
.fh{{display:flex;justify-content:space-between;align-items:baseline;gap:8px}}.fh b{{font-size:14.5px}}
.pill{{font-size:10.5px;padding:1px 7px;border-radius:9px;background:var(--line);color:var(--mut);white-space:nowrap}}
.choice{{margin:8px 0 6px;font-size:13px}}code{{background:var(--line);padding:1.5px 6px;border-radius:5px;font:12.5px/1.4 ui-monospace,"SF Mono",Menlo,Consolas,monospace}}
.opts{{font-size:12px;color:var(--mut);margin:4px 0}}.opts ul{{margin:3px 0 0;padding-left:18px}}.opts li{{margin:1px 0}}
.lbl{{display:inline-block;font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);margin-right:6px}}
.reason{{margin:7px 0;font-size:13px}}.src{{font-size:12px;color:var(--mut)}}
.crit{{font-size:12px;color:var(--crit);margin-top:5px}}
.serves{{margin-top:8px;display:flex;flex-wrap:wrap;gap:4px;align-items:center}}
.chip{{font-size:11px;background:var(--chip);border:1px solid var(--line);border-radius:7px;padding:1px 7px;white-space:nowrap}}.chip i{{color:var(--mut);font-style:normal;margin-left:4px}}
.lead{{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--acc);border-radius:8px;padding:12px 16px;margin:12px 0;font-size:13.5px}}
.foot{{color:var(--mut);font-size:12px;margin-top:34px;border-top:1px solid var(--line);padding-top:14px}}
</style></head><body><div class=wrap>
<a class=back href="index.html">← 总览</a>
<h1>平台与技术栈选型</h1>
<p class=sub>UMI 力觉数采设备 · 每条选型溯源(🧬第一性/方法论推演 / 📎参考他家+批判,P14)· 选型串由 <code>m0/techstack.json</code> 生成不手抄</p>

<div class=lead><b>推导链:</b>{np} 个核心参数 → {ns} 个实现子系统 → 用 <code>ycfs gate</code> + GitHub Actions 守住(被测不能自证)。选型只回答"用什么实现已定义的功能",不新增需求;每个子系统的 <code>serves</code> 指回它服务的功能/参数,无孤儿(<code>techstack</code> 腿守住)。</div>

<h2>子系统选型(共 {ns} 项)</h2>
{cards}

<div class=lead><b>为什么现在能上 GitHub Pages / Artifact:</b>数据(<code>m0/*.json</code>)→ 生成器(<code>build_*_html.py</code>)→ 门禁(<code>gate</code> 绑死 HTML 与真源)→ CI 发布。此前只用 <code>SendUserFile</code> 发文件(不是可分享的托管页);S10 选型接入 GitHub Actions 后,同一套门禁在受保护面上重跑,产物直接部署成 Pages。</div>

<div class=foot>由 <code>m0/build_techstack_html.py</code> 从 techstack.json 生成;techstack-html 腿绑死 HTML 与真源(改选型不重生成即红)。🧬推演可推翻,📎引用带出处与批判,均可追溯 practice/research/route-0*.md。</div>
</div></body></html>"""


def main():
    t = json.loads(T.read_text(encoding="utf-8"))
    fd = json.loads(F.read_text(encoding="utf-8"))
    fname = {f["id"]: f["name"] for f in fd["functions"]}
    fname.update({p["id"]: p["name"] for p in fd["params"]})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(PAGE.format(
        ns=len(t["subsystems"]), np=len(fd["params"]),
        cards=cards(t["subsystems"], fname),
    ), encoding="utf-8")
    print(f"已生成 {OUT} ({OUT.stat().st_size} 字节)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
