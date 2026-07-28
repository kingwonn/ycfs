#!/usr/bin/env python3
"""build_roadmap_html — 三代产品 roadmap HTML(供审阅/分享)。

从 m0/roadmap.json(结构化真源)生成 site/roadmap.html。文案不手抄。
含:代际时间轴(G1→G2→G3,每代为下一代设门)、每代押注/证伪/退路三联、
准入→出口门条、消解风险徽标、激活的功能/子系统 chips、G3 按 G2 判决的双分叉。
自包含、明暗自适应,与 spec/techstack 同一视觉体系。
"""
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
R = ROOT / "m0" / "roadmap.json"
F = ROOT / "m0" / "functions.json"
T = ROOT / "m0" / "techstack.json"
OUT = ROOT / "site" / "roadmap.html"


def esc(s):
    return html.escape(str(s))


def gen_block(g, name_of):
    fp = g["origin"] == "first-principle"
    icon = "🧬" if fp else "📎"
    tag = f"第一性·{g['basis']}" if fp else "参考他家"
    ns = "<span class=ns>★ 北极星</span>" if g.get("north_star") else ""
    ships = "".join(f"<li>{esc(s)}</li>" for s in g.get("ships", []))
    traces = " ".join(
        f"<span class=chip>{esc(r)}<i>{esc(name_of.get(r, ''))}</i></span>"
        for r in g.get("traces", []))
    forks = ""
    if g.get("forks"):
        cards = ""
        for fk in g["forks"]:
            cards += (f"<div class=fork><div class=fb>Fork {esc(fk['branch'])}</div>"
                      f"<div class=fcond>{esc(fk['condition'])}</div>"
                      f"<div class=fkv><span>产品</span>{esc(fk['product'])}</div>"
                      f"<div class=fkv><span>商业</span>{esc(fk['business'])}</div></div>")
        forks = (f"<div class=forks><div class=forkhead>⑃ 按 "
                 f"{esc(g.get('fork_on',''))} 的力迁移判决分叉(两支都做成可执行)</div>"
                 f"<div class=forkgrid>{cards}</div></div>")
    return (
        f"<section class='gen {g['origin']}'>"
        f"<div class=gh><div class=gid>{esc(g['id'])}</div>"
        f"<div class=gt><b>{esc(g['name'])}</b>{ns}"
        f"<div class=gmeta><span class=hz>{esc(g['horizon'])}</span>"
        f"<span class=tier>{esc(g['tier'])}</span>"
        f"<span class=pill>{icon} {esc(tag)}</span></div></div></div>"
        f"<div class=goal>{esc(g['goal'])}</div>"
        f"<div class=ships><span class=lbl>交付</span><ul>{ships}</ul></div>"
        f"<div class=triad>"
        f"<div class='t bet'><span class=lbl>押注</span>{esc(g['bet'])}</div>"
        f"<div class='t fal'><span class=lbl>证伪(可裁决)</span>{esc(g['falsification'])}</div>"
        f"<div class='t fbk'><span class=lbl>退路</span>{esc(g['fallback'])}</div>"
        f"</div>"
        f"<div class=gate><div class=ge><span class=lbl>准入</span>{esc(g['entry'])}</div>"
        f"<div class=gx><span class=lbl>出口</span>{esc(g['exit'])}</div></div>"
        f"{forks}"
        f"<div class=foota><span class=derisk>消解风险:{esc(g['de_risks'])}</span>"
        f"<span class=src>来源:{esc(g['source']) if g.get('source') else esc(g.get('basis',''))}</span></div>"
        f"<div class=crit>⚠ {esc(g['critique'])}</div>"
        f"<div class=traces>{traces}</div>"
        f"</section>")


PAGE = """<!doctype html><html lang=zh><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>三代产品 Roadmap · UMI 力觉数采</title><style>
:root{{--bg:#fff;--fg:#1a1a1a;--mut:#666;--line:#e5e7eb;--card:#fafafa;--g1:#eef4ff;--g2:#eefaf3;--g3:#f6effc;--acc:#2563eb;--bet:#2563eb;--fal:#b45309;--fbk:#0891b2;--crit:#b45309;--chip:#eef2f7;--ns:#d97706}}
@media(prefers-color-scheme:dark){{:root{{--bg:#0f1115;--fg:#e8e8e8;--mut:#9aa0a8;--line:#2a2e37;--card:#171a21;--g1:#14203a;--g2:#0f2620;--g3:#231733;--acc:#60a5fa;--bet:#60a5fa;--fal:#fbbf24;--fbk:#22d3ee;--crit:#fcd34d;--chip:#1c2230;--ns:#fbbf24}}}}
:root[data-theme=dark]{{--bg:#0f1115;--fg:#e8e8e8;--mut:#9aa0a8;--line:#2a2e37;--card:#171a21;--g1:#14203a;--g2:#0f2620;--g3:#231733;--acc:#60a5fa;--bet:#60a5fa;--fal:#fbbf24;--fbk:#22d3ee;--crit:#fcd34d;--chip:#1c2230;--ns:#fbbf24}}
:root[data-theme=light]{{--bg:#fff;--fg:#1a1a1a;--mut:#666;--line:#e5e7eb;--card:#fafafa;--g1:#eef4ff;--g2:#eefaf3;--g3:#f6effc;--acc:#2563eb;--bet:#2563eb;--fal:#b45309;--fbk:#0891b2;--crit:#b45309;--chip:#eef2f7;--ns:#d97706}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.65 -apple-system,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif}}
.wrap{{max-width:1080px;margin:0 auto;padding:30px 20px 80px}}
a.back{{color:var(--acc);text-decoration:none;font-size:13px}}
h1{{font-size:25px;margin:6px 0 4px}}.sub{{color:var(--mut);font-size:13.5px;margin:0 0 22px}}
.lead{{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--acc);border-radius:8px;padding:12px 16px;margin:12px 0 8px;font-size:13.5px}}
.flow{{display:flex;flex-direction:column;gap:0;margin-top:18px}}
.gen{{border:1px solid var(--line);border-radius:12px;padding:16px 18px;position:relative}}
.gen.first-principle{{border-left:4px solid var(--acc)}}.gen.reference{{border-left:4px solid var(--mut)}}
.conn{{height:26px;width:2px;background:var(--line);margin:0 auto;position:relative}}
.conn::after{{content:"▼";position:absolute;left:-6px;bottom:-4px;color:var(--mut);font-size:12px}}
.gh{{display:flex;gap:12px;align-items:flex-start}}
.gid{{font:700 15px/1 ui-monospace,Menlo,monospace;background:var(--acc);color:#fff;border-radius:8px;padding:8px 11px;white-space:nowrap}}
.gen.reference .gid{{background:var(--mut)}}
.gt b{{font-size:16px}}.gmeta{{display:flex;flex-wrap:wrap;gap:6px;margin-top:5px;align-items:center}}
.hz,.tier{{font:11.5px/1 ui-monospace,Menlo,monospace;color:var(--mut);border:1px solid var(--line);border-radius:6px;padding:3px 7px}}
.pill{{font-size:10.5px;padding:2px 8px;border-radius:9px;background:var(--chip);color:var(--mut)}}
.ns{{font-size:11px;color:var(--ns);border:1px solid var(--ns);border-radius:7px;padding:1px 7px;margin-left:8px;white-space:nowrap}}
.goal{{margin:11px 0 4px;font-size:13.5px}}
.lbl{{display:block;font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);margin-bottom:3px}}
.ships{{margin:8px 0}}.ships ul{{margin:2px 0 0;padding-left:18px;font-size:12.5px;color:var(--mut)}}.ships li{{margin:1px 0}}
.triad{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:10px 0}}
.t{{border:1px solid var(--line);border-radius:9px;padding:9px 11px;font-size:12.5px;background:var(--card)}}
.t.bet{{border-top:2px solid var(--bet)}}.t.fal{{border-top:2px solid var(--fal)}}.t.fbk{{border-top:2px solid var(--fbk)}}
.gate{{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:8px 0}}
.ge,.gx{{border:1px dashed var(--line);border-radius:9px;padding:9px 11px;font-size:12.5px}}
.gx{{background:var(--g2)}}
.forks{{margin:10px 0;border:1px solid var(--line);border-radius:10px;padding:10px 12px;background:var(--g3)}}
.forkhead{{font-size:12.5px;font-weight:600;margin-bottom:8px}}
.forkgrid{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
.fork{{border:1px solid var(--line);border-radius:9px;padding:9px 11px;background:var(--bg)}}
.fb{{font:700 12px/1 ui-monospace,Menlo,monospace;color:var(--acc);margin-bottom:4px}}
.fcond{{font-size:12.5px;font-weight:600;margin-bottom:6px}}
.fkv{{font-size:12px;margin:2px 0}}.fkv span{{display:inline-block;min-width:34px;color:var(--mut);font-size:10.5px;text-transform:uppercase;letter-spacing:.05em}}
.foota{{display:flex;flex-wrap:wrap;gap:10px 16px;margin:10px 0 2px;font-size:11.5px}}
.derisk{{color:var(--fal);font-weight:600}}.src{{color:var(--mut)}}
.crit{{font-size:12px;color:var(--crit);margin:4px 0 8px}}
.traces{{display:flex;flex-wrap:wrap;gap:4px}}
.chip{{font-size:11px;background:var(--chip);border:1px solid var(--line);border-radius:7px;padding:1px 7px;white-space:nowrap}}.chip i{{color:var(--mut);font-style:normal;margin-left:4px}}
.foot{{color:var(--mut);font-size:12px;margin-top:30px;border-top:1px solid var(--line);padding-top:14px}}
@media(max-width:680px){{.triad,.gate,.forkgrid{{grid-template-columns:1fr}}}}
</style></head><body><div class=wrap>
<a class=back href="index.html">← 总览</a>
<h1>三代产品 Roadmap</h1>
<p class=sub>UMI 力觉数采 · 代际=时间层(G1→G2→G3,每代为下一代去风险并设门)· 文案由 <code>m0/roadmap.json</code> 生成不手抄</p>

<div class=lead><b>读法:</b>这不是三档并卖的 SKU(那是 <a class=back href="product.html">产品矩阵</a>),而是<b>时间上的递进押注</b>——每代一个可裁决的押注 + 证伪条件 + 退路(不骑墙),且被上一代的<b>出口</b>设门才启动。<b>G3 不预设方向:它按 G2『力能否跨本体』的判决分叉</b>,两条路都提前做成可执行。这正是"把最大风险的验证与'要不要造设备'绑成同一件事"。</div>

<div class=flow>{blocks}</div>

<div class=foot>由 <code>m0/build_roadmap_html.py</code> 从 roadmap.json 生成;roadmap 腿({na} 断言)守代际递进/证伪≠退路/de_risks 无孤儿/G3 必分叉,roadmap-html 腿绑死此页与真源(改文案不重生成即红)。🧬第一性带 N1-N6 依据,📎参考带出处+批判(P14),均可追溯 PRODUCT.md / practice/research/route-0*.md。</div>
</div></body></html>"""


def main():
    d = json.loads(R.read_text(encoding="utf-8"))
    fd = json.loads(F.read_text(encoding="utf-8"))
    td = json.loads(T.read_text(encoding="utf-8"))
    name_of = {f["id"]: f["name"] for f in fd["functions"]}
    name_of.update({s["id"]: s["layer"] for s in td["subsystems"]})
    gens = d["generations"]
    blocks = '<div class=conn></div>'.join(gen_block(g, name_of) for g in gens)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(PAGE.format(blocks=blocks, na="93"), encoding="utf-8")
    print(f"已生成 {OUT} ({OUT.stat().st_size} 字节)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
