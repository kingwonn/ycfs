#!/usr/bin/env python3
"""build_watchlist_html — 具身/Physical AI 观察列表 → site/watchlist.html + WATCHLIST.md + PROFILES.md。

从 m0/watchlist.json(名录)+ m0/profiles.json(七维深扒)生成:
  - 可筛选/搜索的 HTML 观察面板;有深扒的公司带🔬展开层(七维度),可"只看深扒"。
  - WATCHLIST.md(名录 markdown)+ PROFILES.md(深扒 markdown)。
不接门禁腿——外部厂商目录 + 分析,非自评产物。
"""
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
J = ROOT / "m0" / "watchlist.json"
P = ROOT / "m0" / "profiles.json"
OUT_HTML = ROOT / "site" / "watchlist.html"
OUT_MD = ROOT / "WATCHLIST.md"
OUT_PROF = ROOT / "PROFILES.md"

CAT = {"brain": "大脑", "robot": "整机", "datacol": "数采",
       "dataset": "数据集", "sensor": "传感器", "hand": "灵巧手"}
REL = {"customer": "客户", "competitor": "竞品", "supplier": "供应商",
       "adjacent": "相邻", "ecosystem": "生态"}
CTRY = {"CN": "中", "US": "美", "其他": "其他"}
# 七维度渲染顺序:(字段, 标签)
DIMS = [("pedigree", "① 出身"), ("bet", "② 押注"), ("motivation", "· 动机"),
        ("falsification", "· 证伪"), ("techstack", "③ 技术栈"),
        ("force_depth", "· 力这一维"), ("strength", "④ 优势"),
        ("weakness", "· 软肋"), ("relation", "⑤ 与我们关系"),
        ("signal", "⑥ 该盯的信号"), ("evidence", "⑦ 证据说明")]


def esc(s):
    return html.escape(str(s or ""))


def deep_block(pr):
    items = "".join(
        f"<div class=dim><span class=dk>{esc(label)}</span>"
        f"<span class=dv>{esc(pr[key])}</span></div>"
        for key, label in DIMS if pr.get(key))
    return f"<details class=deep><summary>🔬 深扒(七维度)</summary>{items}</details>"


def rows_html(cos, profiles):
    out = []
    for c in cos:
        pr = profiles.get(c["name"])
        text = " ".join(str(c.get(k, "")) for k in
                        ("name", "cn", "watch", "status", "note")).lower()
        if pr:
            text += " " + " ".join(str(v) for v in pr.values()).lower()
        site = c.get("site", "")
        link = (f"<a class=site href='https://{esc(site)}' target=_blank rel=noopener>"
                f"{esc(site)} ↗</a>") if site else "<span class=nosite>—</span>"
        cn = f"<span class=cn>{esc(c['cn'])}</span>" if c.get("cn") else ""
        badge = "<span class=deepbadge title='有七维深扒'>🔬</span>" if pr else ""
        out.append(
            f"<div class=row data-cat='{esc(c['cat'])}' data-country='{esc(c['country'])}' "
            f"data-rel='{esc(c['relation'])}' data-deep='{'1' if pr else '0'}' "
            f"data-text=\"{esc(text)}\">"
            f"<div class=rl><span class=nm>{esc(c['name'])}</span>{cn}{badge}"
            f"<span class='pill rel-{esc(c['relation'])}'>{esc(REL.get(c['relation'],''))}</span>"
            f"<span class=meta>{esc(CAT.get(c['cat'],''))} · {esc(CTRY.get(c['country'],c['country']))}</span></div>"
            f"<div class=watch><b>观察</b> {esc(c.get('watch',''))}</div>"
            f"<div class=status><b>状态</b> {esc(c.get('status','未找到'))}</div>"
            f"<div class=note>{esc(c.get('note',''))}</div>"
            f"{deep_block(pr) if pr else ''}"
            f"{link}</div>")
    return "".join(out)


def chip_row(name, items):
    chips = [f"<button class='chip active' data-f='{name}' data-v='all'>全部</button>"]
    for v, label in items:
        chips.append(f"<button class=chip data-f='{name}' data-v='{v}'>{label}</button>")
    return "".join(chips)


PAGE = """<!doctype html><html lang=zh><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>具身/Physical AI 观察列表</title><style>
:root{{--bg:#fff;--fg:#16181d;--mut:#5f6672;--line:#e5e7eb;--card:#fafbfc;--acc:#2563eb;--chip:#eef2f7;--deep:#f6f3fb;--customer:#059669;--competitor:#dc2626;--supplier:#2563eb;--adjacent:#64748b;--ecosystem:#d97706}}
@media(prefers-color-scheme:dark){{:root{{--bg:#0d0f13;--fg:#e8eaed;--mut:#9aa0a8;--line:#252a33;--card:#141821;--acc:#60a5fa;--chip:#1c2230;--deep:#191526;--customer:#34d399;--competitor:#f87171;--supplier:#60a5fa;--adjacent:#94a3b8;--ecosystem:#fbbf24}}}}
:root[data-theme=dark]{{--bg:#0d0f13;--fg:#e8eaed;--mut:#9aa0a8;--line:#252a33;--card:#141821;--acc:#60a5fa;--chip:#1c2230;--deep:#191526;--customer:#34d399;--competitor:#f87171;--supplier:#60a5fa;--adjacent:#94a3b8;--ecosystem:#fbbf24}}
:root[data-theme=light]{{--bg:#fff;--fg:#16181d;--mut:#5f6672;--line:#e5e7eb;--card:#fafbfc;--acc:#2563eb;--chip:#eef2f7;--deep:#f6f3fb;--customer:#059669;--competitor:#dc2626;--supplier:#2563eb;--adjacent:#64748b;--ecosystem:#d97706}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:14.5px/1.6 -apple-system,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif}}
.wrap{{max-width:1080px;margin:0 auto;padding:26px 18px 80px}}
a.back{{color:var(--acc);text-decoration:none;font-size:13px}}
h1{{font-size:23px;margin:6px 0 3px}}.sub{{color:var(--mut);font-size:13px;margin:0 0 16px}}
.bar{{position:sticky;top:0;background:var(--bg);padding:10px 0;border-bottom:1px solid var(--line);z-index:5}}
.grp{{display:flex;flex-wrap:wrap;gap:5px;align-items:center;margin:5px 0}}
.grp .lbl{{font-size:11px;color:var(--mut);min-width:42px;text-transform:uppercase;letter-spacing:.05em}}
.chip{{font:12px/1 inherit;padding:5px 10px;border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:20px;cursor:pointer}}
.chip.active{{background:var(--acc);color:#fff;border-color:var(--acc)}}
#q{{width:100%;padding:8px 11px;margin-top:6px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--fg);font:14px inherit}}
.count{{font-size:12px;color:var(--mut);margin:10px 0 4px}}
.list{{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:10px;align-items:start}}
.row{{border:1px solid var(--line);border-radius:10px;padding:11px 13px;background:var(--card)}}
.rl{{display:flex;flex-wrap:wrap;align-items:baseline;gap:7px}}
.nm{{font-weight:700;font-size:14.5px}}.cn{{color:var(--mut);font-size:12.5px}}
.deepbadge{{font-size:12px}}
.meta{{margin-left:auto;font:11px ui-monospace,Menlo,monospace;color:var(--mut)}}
.pill{{font-size:10.5px;padding:1px 7px;border-radius:9px;color:#fff}}
.rel-customer{{background:var(--customer)}}.rel-competitor{{background:var(--competitor)}}.rel-supplier{{background:var(--supplier)}}.rel-adjacent{{background:var(--adjacent)}}.rel-ecosystem{{background:var(--ecosystem)}}
.watch{{font-size:12.5px;margin:7px 0 2px}}.status{{font-size:12px;color:var(--mut)}}
.watch b,.status b{{font-size:10px;color:var(--mut);text-transform:uppercase;letter-spacing:.05em;margin-right:4px;font-weight:600}}
.note{{font-size:11.5px;color:var(--mut);margin:5px 0 7px;padding-left:8px;border-left:2px solid var(--line)}}
.deep{{margin:6px 0 8px;background:var(--deep);border:1px solid var(--line);border-radius:8px;padding:2px 10px}}
.deep summary{{cursor:pointer;font-size:12px;font-weight:600;padding:7px 0;color:var(--acc)}}
.dim{{display:flex;gap:8px;font-size:11.5px;margin:5px 0;padding-bottom:5px;border-bottom:1px dashed var(--line)}}
.dim:last-child{{border-bottom:0}}
.dk{{flex:0 0 82px;color:var(--mut);font-weight:600}}.dv{{flex:1}}
.site{{font-size:11.5px;color:var(--acc);text-decoration:none}}.nosite{{font-size:11.5px;color:var(--mut)}}
.foot{{color:var(--mut);font-size:11.5px;margin-top:26px;border-top:1px solid var(--line);padding-top:12px}}
</style></head><body><div class=wrap>
<a class=back href="index.html">← 总览</a>
<h1>具身 / Physical AI 观察列表</h1>
<p class=sub>{n} 家中美主要玩家 · {np} 家含🔬七维深扒(押注/动机/技术栈/优劣/关系/信号/证据)· 按 类别·国别·关系·深扒 筛选,关键词搜索 · 数据 {updated},会变</p>

<div class=bar>
  <div class=grp><span class=lbl>类别</span>{cat_chips}</div>
  <div class=grp><span class=lbl>国别</span>{country_chips}</div>
  <div class=grp><span class=lbl>关系</span>{rel_chips}</div>
  <div class=grp><span class=lbl>深扒</span>{deep_chips}</div>
  <input id=q placeholder="搜索公司/产品/关键词(如 力觉、LeRobot、仿真、押注、动机)…">
</div>
<div class=count id=count></div>
<div class=list id=list>{rows}</div>

<div class=foot>数据源 <code>m0/watchlist.json</code>(名录)+ <code>m0/profiles.json</code>(七维深扒)→ 本页 + <code>WATCHLIST.md</code> + <code>PROFILES.md</code>。关系:<b style=color:var(--customer)>客户候选</b> / <b style=color:var(--competitor)>竞品</b> / <b style=color:var(--supplier)>供应商</b> / <b style=color:var(--adjacent)>相邻</b> / <b style=color:var(--ecosystem)>生态</b>。深扒含【推断】成分,已在⑦证据标注。<b>不接门禁、不自评</b>。</div>
</div>
<script>
const F={{cat:'all',country:'all',rel:'all',deep:'all'}};
const rows=[...document.querySelectorAll('.row')];
const q=document.getElementById('q'),count=document.getElementById('count');
function apply(){{
  const s=q.value.trim().toLowerCase();let n=0;
  for(const r of rows){{
    const ok=(F.cat=='all'||r.dataset.cat==F.cat)&&(F.country=='all'||r.dataset.country==F.country)
      &&(F.rel=='all'||r.dataset.rel==F.rel)&&(F.deep=='all'||r.dataset.deep==F.deep)
      &&(!s||r.dataset.text.includes(s));
    r.style.display=ok?'':'none';if(ok)n++;
  }}
  count.textContent='显示 '+n+' / 共 '+rows.length+' 家';
}}
document.querySelectorAll('.chip').forEach(c=>c.addEventListener('click',()=>{{
  const f=c.dataset.f;F[f]=c.dataset.v;
  document.querySelectorAll(`.chip[data-f='${{f}}']`).forEach(x=>x.classList.toggle('active',x==c));
  apply();
}}));
q.addEventListener('input',apply);apply();
</script>
</body></html>"""


def build_html(d, profiles):
    cos = d["companies"]
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(PAGE.format(
        n=len(cos), np=len(profiles), updated=esc(d.get("updated", "")),
        cat_chips=chip_row("cat", list(CAT.items())),
        country_chips=chip_row("country", [("CN", "中"), ("US", "美"), ("其他", "其他")]),
        rel_chips=chip_row("rel", list(REL.items())),
        deep_chips=chip_row("deep", [("1", "有深扒")]),
        rows=rows_html(cos, profiles),
    ), encoding="utf-8")
    return len(cos)


def build_md(d):
    cos = d["companies"]
    lines = ["# WATCHLIST — 具身 / Physical AI 观察列表", "",
             f"> {len(cos)} 家中美主要玩家,由 `m0/watchlist.json` 生成(可筛选版见 `site/watchlist.html`,深扒见 `PROFILES.md`)。",
             f"> 数据 {d.get('updated','')},会变。关系:客户候选/竞品/供应商/相邻/生态。不接门禁、不自评。", ""]
    order = ["brain", "robot", "datacol", "dataset", "sensor", "hand"]
    title = {"brain": "大脑 / 基座模型", "robot": "整机 / 人形",
             "datacol": "数据采集(竞品/相邻)", "dataset": "数据集 / 格式标准",
             "sensor": "力/触觉传感器(供应商)", "hand": "灵巧手(重定向目标)"}
    for cat in order:
        group = [c for c in cos if c["cat"] == cat]
        if not group:
            continue
        lines += [f"## {title[cat]}（{len(group)}）", "",
                  "| 名称 | 国 | 观察什么 | 状态 | 关系 | 来源 | 关键批判 |",
                  "|---|---|---|---|---|---|---|"]
        for c in group:
            nm = c["name"] + (f"（{c['cn']}）" if c.get("cn") else "")
            lines.append(
                f"| {nm} | {CTRY.get(c['country'],c['country'])} | {c.get('watch','')} | "
                f"{c.get('status','未找到')} | {REL.get(c['relation'],'')} | "
                f"{c.get('site','') or '—'} | {c.get('note','')} |")
        lines.append("")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_profiles_md(profiles, updated):
    lines = ["# PROFILES — 重点公司七维深扒", "",
             f"> {len(profiles)} 家(直接竞品 + 头部客户候选 + 押注对照组),按 `PROFILE-DIMENSIONS.md` 七维度。",
             f"> 数据 {updated}。证据等级:【实】多源/一手,【口】厂商口径,【推】我方推断。不接门禁、不自评。", ""]
    for name, pr in profiles.items():
        lines += [f"## {name}", ""]
        for key, label in DIMS:
            if pr.get(key):
                lines.append(f"- **{label}**:{pr[key]}")
        lines.append("")
    OUT_PROF.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    d = json.loads(J.read_text(encoding="utf-8"))
    profiles = {}
    if P.exists():
        profiles = json.loads(P.read_text(encoding="utf-8")).get("profiles", {})
    n = build_html(d, profiles)
    build_md(d)
    build_profiles_md(profiles, d.get("updated", ""))
    print(f"已生成 {OUT_HTML}、{OUT_MD}、{OUT_PROF}（{n} 家,其中 {len(profiles)} 家深扒）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
