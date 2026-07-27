#!/usr/bin/env python3
"""build_spec_html — 产品功能/参数定义 HTML(供 Codex 批判性审阅)。

从 m0/functions.json(结构化真源)+ site/prompts.md 生成 site/spec.html。
数字不手抄。含:第一性 N1-N6、功能(第一性/参考分组,带批判)、参数表(溯源)、
参数完整性 review(新增+仍out-of-scope)、每轮 prompt 折叠日志。
自包含、明暗自适应。
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "m0" / "functions.json"
PROMPTS = ROOT / "site" / "prompts.md"
OUT = ROOT / "site" / "spec.html"


def esc(s):
    return html.escape(str(s))


def load():
    return json.loads(F.read_text(encoding="utf-8"))


def fp_table(fps):
    rows = "".join(f"<tr><td class=n>{k}</td><td>{esc(v)}</td></tr>" for k, v in fps.items())
    return f"<table class=fp><thead><tr><th>第一性</th><th>要求(推演自 π(a|o,l,s))</th></tr></thead><tbody>{rows}</tbody></table>"


def func_cards(funcs):
    def card(f):
        icon = "🧬" if f["origin"] == "first-principle" else "📎"
        tag = f"第一性·{f['basis']}" if f["origin"] == "first-principle" else "参考他家"
        return (f"<div class='card {f['origin']}'>"
                f"<div class=fh><b>{icon} {esc(f['id'])} · {esc(f['name'])}</b>"
                f"<span class=pill>{esc(tag)}</span></div>"
                f"<div class=st>{esc(f['statement'])}</div>"
                f"<div class=src>来源:{esc(f['source'])}</div>"
                f"<div class=crit>⚠ {esc(f['critique'])}</div></div>")
    fp = "".join(card(f) for f in funcs if f["origin"] == "first-principle")
    rf = "".join(card(f) for f in funcs if f["origin"] == "reference")
    return (f"<h3>🧬 从第一性推演的功能</h3><div class=grid>{fp}</div>"
            f"<h3>📎 参考已验证产品的功能</h3><div class=grid>{rf}</div>")


def param_table(params, funcs):
    fname = {f["id"]: f["name"] for f in funcs}
    body = []
    for p in sorted(params, key=lambda x: x["traces_to"]):
        warn = " warn" if "⚠" in p.get("critique", "") else ""
        body.append(
            f"<tr class='{warn}'><td class=n>{esc(p['id'])}</td><td>{esc(p['name'])}</td>"
            f"<td class=v>{esc(p['value'])} {esc(p['unit'])}</td>"
            f"<td class=tr>{esc(p['traces_to'])} {esc(fname.get(p['traces_to'],''))}</td>"
            f"<td class=src>{esc(p['source'])}</td>"
            f"<td class=crit>{esc(p['critique'])}</td></tr>")
    return ("<table class=params><thead><tr><th>ID</th><th>参数</th><th>值</th>"
            "<th>服务功能</th><th>来源</th><th>⚠ 批判/边界</th></tr></thead>"
            f"<tbody>{''.join(body)}</tbody></table>")


def review_block(rv):
    added = "".join(f"<li>{esc(x)}</li>" for x in rv.get("added_in_v2", []))
    oos = "".join(f"<li><b>{esc(o['item'])}</b> — {esc(o['reason'])}</li>"
                  for o in rv.get("still_out_of_scope", []))
    return (f"<h3>本轮 review 新增(补齐遗漏)</h3><ul class=add>{added}</ul>"
            f"<h3>仍 out-of-scope(明列+理由,供批判)</h3><ul class=oos>{oos}</ul>")


def prompt_log():
    if not PROMPTS.exists():
        return "<p>(无 prompt 日志)</p>"
    txt = PROMPTS.read_text(encoding="utf-8")
    items = re.findall(r"^## (R\d+[^\n]*)\n(.*?)(?=^## |\Z)", txt, re.M | re.S)
    out = []
    for title, body in items:
        out.append(f"<details><summary>{esc(title.strip())}</summary>"
                   f"<div class=pbody>{esc(body.strip())}</div></details>")
    return "".join(out)


PAGE = """<!doctype html><html lang=zh><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>产品功能与核心参数定义 · UMI 力觉数采</title><style>
:root{{--bg:#fff;--fg:#1a1a1a;--mut:#666;--line:#e5e7eb;--card:#fafafa;--fpc:#eef4ff;--refc:#fef6ee;--acc:#2563eb;--warn:#d97706;--crit:#b45309}}
@media(prefers-color-scheme:dark){{:root{{--bg:#0f1115;--fg:#e8e8e8;--mut:#9aa0a8;--line:#2a2e37;--card:#171a21;--fpc:#14203a;--refc:#2a2015;--acc:#60a5fa;--warn:#fbbf24;--crit:#fcd34d}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.65 -apple-system,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif}}
.wrap{{max-width:1120px;margin:0 auto;padding:30px 20px 80px}}
h1{{font-size:25px;margin:0 0 4px}}.sub{{color:var(--mut);font-size:13.5px;margin:0 0 24px}}
h2{{font-size:19px;margin:34px 0 12px;padding-top:14px;border-top:1px solid var(--line)}}
h3{{font-size:15.5px;margin:18px 0 8px;color:var(--mut)}}
table{{width:100%;border-collapse:collapse;font-size:13px;margin:8px 0}}
th,td{{text-align:left;padding:7px 9px;border-bottom:1px solid var(--line);vertical-align:top}}
th{{color:var(--mut);font-size:12px;font-weight:600}}.n{{font-weight:600;white-space:nowrap}}
.fp td:first-child{{font-weight:700;color:var(--acc)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:10px;margin:6px 0}}
.card{{border:1px solid var(--line);border-radius:9px;padding:12px 14px}}
.card.first-principle{{background:var(--fpc)}}.card.reference{{background:var(--refc)}}
.fh{{display:flex;justify-content:space-between;align-items:baseline;gap:8px}}.fh b{{font-size:14.5px}}
.pill{{font-size:10.5px;padding:1px 7px;border-radius:9px;background:var(--line);color:var(--mut);white-space:nowrap}}
.st{{margin:6px 0;font-size:13px}}.src{{font-size:12px;color:var(--mut)}}.crit{{font-size:12px;color:var(--crit);margin-top:4px}}
.params .v{{font-weight:600;white-space:nowrap;color:var(--acc)}}.params .tr{{white-space:nowrap;color:var(--mut)}}
.params .src{{max-width:230px;font-size:11.5px}}.params .crit{{max-width:250px;font-size:11.5px}}
.params tr.warn td.crit{{color:var(--warn);font-weight:600}}
ul.add li,ul.oos li{{font-size:13px;margin:3px 0}}ul.oos b{{color:var(--fg)}}
details{{background:var(--card);border:1px solid var(--line);border-radius:8px;margin:7px 0;padding:2px 14px}}
summary{{cursor:pointer;font-weight:600;font-size:14px;padding:8px 0}}
.pbody{{font-size:13px;color:var(--fg);white-space:pre-wrap;padding:2px 0 12px;border-top:1px dashed var(--line)}}
.lead{{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--acc);border-radius:8px;padding:12px 16px;margin:12px 0;font-size:13.5px}}
code{{background:var(--line);padding:1px 5px;border-radius:4px;font-size:12px}}
.foot{{color:var(--mut);font-size:12px;margin-top:34px;border-top:1px solid var(--line);padding-top:14px}}
</style></head><body><div class=wrap>
<h1>产品功能定义 → 核心参数定义</h1>
<p class=sub>UMI 力觉数采设备 · 每条溯源(🧬第一性推演 / 📎参考他家+批判,P14)· 数字由 <code>m0/functions.json</code> 生成不手抄 · 供 Codex 批判性审阅</p>

<div class=lead><b>推导链:</b>大脑学 π(动作|观察,语言,状态) → 六条第一性数据要求 N1-N6 → {nf} 个产品功能 → {np} 个核心参数 → BOM/证书。每一步机器可追责(<code>python3 runtime/gate.py</code> 的 functions 腿 {na} 断言守住)。</div>

<h2>零 · 第一性起点(推演,非引用)</h2>
{fp}

<h2>一 · 产品功能定义({nf} 项)</h2>
{funcs}

<h2>二 · 核心参数定义({np} 项,每个溯源到功能)</h2>
{params}
<div class=lead>参数否决线(破一条产品不成立):同步&gt;5ms · 重量&gt;1kg · 同批标定不一致 · 力通道被握力污染 · 力无牛顿级标定。</div>

<h2>三 · 参数完整性 review(本轮补遗漏)</h2>
{review}

<h2>四 · 每轮 prompt 日志(点击展开)</h2>
<p class=sub>用户每轮指令的忠实记录,便于审阅推导脉络。</p>
{prompts}

<div class=foot>由 <code>m0/build_spec_html.py</code> 从 functions.json + prompts.md 生成;spec 腿绑死 HTML 与真源(改数据不重生成即红)。🧬推演可推翻,📎引用带出处与批判,均可追溯 practice/research/route-0*.md。</div>
</div></body></html>"""


def main():
    d = load()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(PAGE.format(
        nf=len(d["functions"]), np=len(d["params"]), na="188",
        fp=fp_table(d["first_principles"]),
        funcs=func_cards(d["functions"]),
        params=param_table(d["params"], d["functions"]),
        review=review_block(d.get("review", {})),
        prompts=prompt_log(),
    ), encoding="utf-8")
    print(f"已生成 {OUT} ({OUT.stat().st_size} 字节)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
