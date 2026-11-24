# -*- coding: utf-8 -*-
"""Static site generator for sangmin2-rf.github.io  ->  docs/
Usage:  python build.py
"""
import html, os, re
from data import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
esc = html.escape

# ------------------------------------------------------------------ helpers
def bold_me(authors):
    s = esc(authors)
    if "**" in s:
        return re.sub(r"\*\*(.+?)\*\*", r"<b class='me'>\1</b>", s)
    for n in ["S.-M. Lee", "S. Lee"]:
        if n in s:
            return s.replace(n, f"<b class='me'>{n}</b>", 1)
    return s

def bib(p, kind):
    a = p["authors"].replace("**", "").replace("*", "")
    a = " and ".join(x.strip() for x in re.split(r",\s*(?:and\s+)?|\s+and\s+", a) if x.strip())
    L = [f"@{kind}{{{p['key']},", f"  title     = {{{p['title']}}},", f"  author    = {{{a}}},"]
    L.append(f"  journal   = {{{JOURNAL_FULL.get(p['jabbr'], p['jabbr'])}}}," if kind == "article" else f"  booktitle = {{{p['venue']}}},")
    L.append(f"  year      = {{{p['year']}}},")
    if p.get("doi"): L.append(f"  doi       = {{{p['doi']}}},")
    if p.get("status"): L.append(f"  note      = {{{p['status']}}},")
    return "\n".join(L + ["}"])

def stats():
    j = len(JOURNALS); jf = sum(1 for p in JOURNALS if p["first"])
    aw = sum(len(v) for k, v in AWARDS if k != "Undergraduate Competitions")
    return [(j, "Journal papers", f"{jf} as first author"), (len(INTL_CONF), "International conference papers", "IEEE AP-S/URSI, ISAP"),
            (len(DOMESTIC), "Domestic conference papers", "KIEES and others"), (len(PATENTS), "Korean patents", "1 registered, 1 filed"),
            (aw, "Awards & grants", "since 2020")]

MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
def fmt_date(d):
    y, m, dd = d.split("-")
    return f"{MON[int(m)-1]} {int(dd)}, {y}" if dd != "01" else f"{MON[int(m)-1]} {y}"

KIND_LABEL = {"paper": "Publication", "award": "Award", "grant": "Grant", "talk": "Talk", "milestone": "Milestone"}

# ------------------------------------------------------------------ CSS
CSS = r"""
:root{
--paper:#ffffff;--paper-2:#f5f6f8;--card:#ffffff;--ink:#0b0d12;--ink-2:#3a3f4b;--muted:#6b7280;--line:#eceef2;--line-2:#dfe2e8;
--accent:#4338ca;--accent-2:#0891b2;--accent-ink:#ffffff;--accent-soft:#eef0ff;--sage:#047857;--sage-soft:#e8f6f0;--gold:#a16207;--gold-soft:#fdf5e1;--plum:#7c3aed;--plum-soft:#f3edff;
--display:"Inter Tight","Pretendard Variable",Pretendard,-apple-system,"Segoe UI",sans-serif;
--sans:"Inter","Pretendard Variable",Pretendard,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;
--mono:"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--r:20px;
--shadow:0 1px 2px rgba(15,23,42,.04),0 12px 32px -16px rgba(15,23,42,.14);--glow1:rgba(99,102,241,.18);--glow2:rgba(6,182,212,.14)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
--paper:#09090b;--paper-2:#131318;--card:#111115;--ink:#f4f4f6;--ink-2:#c9cbd3;--muted:#8b8f9c;--line:#1f2027;--line-2:#2c2d36;
--accent:#a5b4fc;--accent-2:#67e8f9;--accent-ink:#09090b;--accent-soft:#1c1d3a;--sage:#6ee7b7;--sage-soft:#0f2a22;--gold:#fcd34d;--gold-soft:#2a2210;--plum:#c4b5fd;--plum-soft:#221a3a;
--shadow:0 0 0 1px rgba(255,255,255,.02);--glow1:rgba(99,102,241,.22);--glow2:rgba(6,182,212,.12)}}
:root[data-theme="dark"]{--paper:#09090b;--paper-2:#131318;--card:#111115;--ink:#f4f4f6;--ink-2:#c9cbd3;--muted:#8b8f9c;--line:#1f2027;--line-2:#2c2d36;
--accent:#a5b4fc;--accent-2:#67e8f9;--accent-ink:#09090b;--accent-soft:#1c1d3a;--sage:#6ee7b7;--sage-soft:#0f2a22;--gold:#fcd34d;--gold-soft:#2a2210;--plum:#c4b5fd;--plum-soft:#221a3a;
--shadow:0 0 0 1px rgba(255,255,255,.02);--glow1:rgba(99,102,241,.22);--glow2:rgba(6,182,212,.12)}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:90px;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font:16.5px/1.7 var(--sans);-webkit-font-smoothing:antialiased;font-feature-settings:"cv11","ss01";letter-spacing:-.006em}
body::before{content:"";position:fixed;inset:-20% -10% auto auto;width:900px;height:900px;pointer-events:none;z-index:-1;
background:radial-gradient(closest-side,var(--glow1),transparent 70%),radial-gradient(closest-side at 30% 70%,var(--glow2),transparent 70%);filter:blur(20px);opacity:.9}
a{color:inherit;text-decoration:none;background-image:linear-gradient(currentColor,currentColor);background-size:100% 1px;background-position:0 100%;background-repeat:no-repeat;transition:color .15s}
a:hover{color:var(--accent)}
::selection{background:var(--accent);color:#fff}
.skip{position:absolute;left:-999px}.skip:focus{left:16px;top:12px;background:var(--card);padding:8px 12px;border-radius:8px;z-index:99}
.wrap{max-width:1140px;margin:0 auto;padding:0 32px}
/* header */
header.top{position:sticky;top:0;z-index:30;background:color-mix(in srgb,var(--paper) 72%,transparent);backdrop-filter:blur(16px) saturate(1.6);border-bottom:1px solid color-mix(in srgb,var(--line) 70%,transparent)}
header.top .wrap{height:68px;display:flex;align-items:center;gap:24px}
.brand{font-family:var(--display);font-size:17px;font-weight:650;letter-spacing:-.02em;background:none;display:inline-flex;align-items:center;gap:10px}
.brand::before{content:"";width:10px;height:10px;border-radius:3px;background:linear-gradient(135deg,var(--accent),var(--accent-2));box-shadow:0 0 0 4px var(--accent-soft)}
.brand i{font-style:normal}
nav.main{margin-left:auto;display:flex;gap:4px;align-items:center}
nav.main a{background:none;color:var(--muted);font-size:14.5px;font-weight:500;padding:7px 14px;border-radius:10px}
nav.main a:hover{color:var(--ink);background:var(--paper-2)}nav.main a[aria-current="page"]{color:var(--ink);background:var(--paper-2)}
.theme{margin-left:4px;width:36px;height:36px;border-radius:10px;border:1px solid var(--line-2);background:var(--card);color:var(--muted);cursor:pointer;display:grid;place-items:center}
.theme:hover{color:var(--ink)}
/* type */
.eyebrow{display:inline-flex;align-items:center;gap:10px;font:500 12px/1 var(--mono);letter-spacing:.04em;text-transform:uppercase;color:var(--ink-2);
padding:8px 12px;border:1px solid var(--line-2);border-radius:999px;background:color-mix(in srgb,var(--card) 70%,transparent)}
.eyebrow::before{content:"";width:6px;height:6px;border-radius:50%;background:#10b981;box-shadow:0 0 0 3px rgba(16,185,129,.18)}
h1,h2,h3,h4{font-family:var(--display);font-weight:600;letter-spacing:-.025em;margin:0}
.sec{padding:96px 0 0}.sec-h{display:flex;flex-direction:column;gap:10px;margin-bottom:32px}
.sec-h .n{font:500 12px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}
.sec-h .n::after{content:" /";color:var(--muted)}
.sec-h h2{font-size:clamp(30px,3.6vw,42px);line-height:1.05;letter-spacing:-.035em}
.sec-h .rule{display:none}
.sub{color:var(--muted);font-size:15px;margin:-18px 0 28px}
/* hero */
.hero{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,.6fr);gap:72px;align-items:center;padding:80px 0 8px}
.hero h1{font-size:clamp(52px,7.4vw,104px);line-height:.92;font-weight:650;letter-spacing:-.055em;margin:26px 0 0;
background:linear-gradient(180deg,var(--ink) 30%,color-mix(in srgb,var(--ink) 55%,var(--accent)));-webkit-background-clip:text;background-clip:text;color:transparent}
.hero h1 .ko{display:block;font:500 15px/1 var(--mono);letter-spacing:.35em;color:var(--muted);-webkit-text-fill-color:var(--muted);margin-top:22px}
.hero .tag{display:none}
.bio{margin-top:34px}.bio p{margin:0 0 14px;color:var(--ink-2);font-size:17.5px;line-height:1.75;max-width:58ch}
.pills{display:flex;flex-wrap:wrap;gap:10px;margin-top:30px}
.pill{background:var(--card);display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:500;padding:9px 16px;border-radius:12px;border:1px solid var(--line-2);color:var(--ink-2);transition:all .15s}
.pill:hover{border-color:var(--ink);color:var(--ink);transform:translateY(-1px)}
.pill.solid{background:var(--ink);color:var(--paper);border-color:var(--ink)}.pill.solid:hover{color:var(--paper);box-shadow:0 8px 20px -8px rgba(15,23,42,.5)}
.portrait{position:relative;justify-self:end;width:100%;max-width:340px}
.portrait::before{content:"";position:absolute;inset:-14px;border-radius:30px;background:linear-gradient(135deg,var(--accent),var(--accent-2));opacity:.16;filter:blur(18px);z-index:-1}
.portrait .frame{border-radius:24px;overflow:hidden;aspect-ratio:4/5;background:var(--paper-2);border:1px solid var(--line);box-shadow:var(--shadow)}
.portrait img{width:100%;height:100%;object-fit:cover;object-position:50% 28%;display:block}
.aff{display:flex;align-items:center;gap:12px;margin-top:16px;padding:12px 14px;border-radius:16px;background:color-mix(in srgb,var(--card) 85%,transparent);border:1px solid var(--line);backdrop-filter:blur(8px)}
.aff .t{font-size:13px;line-height:1.45;color:var(--muted)}.aff .t b{display:block;font-weight:600;color:var(--ink);font-size:13.5px}
.logo{flex:none;width:44px;height:44px;border-radius:12px;background:#fff;border:1px solid var(--line);display:grid;place-items:center;overflow:hidden}
.logo img{width:80%;height:80%;object-fit:contain}.logo.lg{width:56px;height:56px;border-radius:14px}
.mono{flex:none;width:56px;height:56px;border-radius:14px;display:grid;place-items:center;font:600 13px/1 var(--mono);letter-spacing:.02em;color:var(--accent);background:var(--accent-soft);border:1px solid color-mix(in srgb,var(--accent) 18%,transparent)}
.mono.sage{color:var(--accent-2);background:color-mix(in srgb,var(--accent-2) 10%,transparent);border-color:color-mix(in srgb,var(--accent-2) 22%,transparent)}
/* research */
.themes{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.theme-item{position:relative;display:flex;flex-direction:column;justify-content:space-between;gap:36px;min-height:180px;padding:26px;border:1px solid var(--line);border-radius:var(--r);background:var(--card);overflow:hidden;transition:border-color .2s,transform .2s}
.theme-item::after{content:"";position:absolute;right:-60px;top:-60px;width:180px;height:180px;border-radius:50%;background:radial-gradient(closest-side,var(--glow1),transparent);opacity:0;transition:opacity .3s}
.theme-item:hover{border-color:var(--line-2);transform:translateY(-2px)}.theme-item:hover::after{opacity:1}
.theme-item .num{font:500 12px/1 var(--mono);color:var(--muted);letter-spacing:.06em}
.theme-item h3{font-size:24px;line-height:1.2;letter-spacing:-.03em;max-width:22ch}
/* glance */
.glance{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:1px;background:var(--line);border:1px solid var(--line);border-radius:var(--r);overflow:hidden}
.g{padding:28px 24px;background:var(--card)}
.g .v{font-family:var(--display);font-size:52px;line-height:1;font-weight:600;letter-spacing:-.05em;background:linear-gradient(135deg,var(--ink),color-mix(in srgb,var(--ink) 50%,var(--accent)));-webkit-background-clip:text;background-clip:text;color:transparent}
.g .l{font-size:14px;color:var(--ink);margin-top:14px;line-height:1.35;font-weight:550}.g .s{font:12px/1.4 var(--mono);color:var(--muted);margin-top:6px}
/* news */
.news{list-style:none;margin:0;padding:0}
.news li{display:grid;grid-template-columns:120px minmax(0,1fr);gap:28px;padding:18px 0;border-top:1px solid var(--line)}
.news li:first-child{border-top:0;padding-top:4px}
.news time{font:12.5px/1.6 var(--mono);color:var(--muted);padding-top:3px}
.news .k{display:inline-flex;align-items:center;gap:6px;font:500 11px/1 var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-bottom:8px;padding:4px 8px;border-radius:6px;background:var(--paper-2)}
.news .k.award,.news .k.grant{color:var(--gold);background:var(--gold-soft)}.news .k.paper{color:var(--accent);background:var(--accent-soft)}.news .k.talk{color:var(--sage);background:var(--sage-soft)}.news .k.milestone{color:var(--plum);background:var(--plum-soft)}
.news .txt{color:var(--ink-2)}.news .txt b{color:var(--ink);font-weight:600}
details.more{margin-top:10px}details.more>summary{cursor:pointer;list-style:none;display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:550;color:var(--ink);padding:9px 14px;border:1px solid var(--line-2);border-radius:10px;background:var(--card)}
details.more>summary:hover{border-color:var(--ink)}details.more>summary::-webkit-details-marker{display:none}details.more>summary::after{content:"↓";font-size:13px;color:var(--muted)}details.more[open]>summary::after{content:"↑"}
details.more[open]>summary{margin-bottom:8px}
/* publications */
.pubs{list-style:none;margin:0;padding:0}
.pub{display:grid;grid-template-columns:44px minmax(0,1fr);gap:12px;padding:24px 0;border-top:1px solid var(--line)}.pub:first-child{border-top:0}
.pub .idx{font:500 12.5px/1.9 var(--mono);color:var(--muted)}
.pub .ttl{font-family:var(--display);font-size:20px;line-height:1.35;font-weight:600;color:var(--ink);letter-spacing:-.02em}
.pub .au{font-size:15px;color:var(--ink-2);margin-top:8px}.pub .au b.me{font-weight:650;color:var(--ink);background:linear-gradient(transparent 62%,color-mix(in srgb,var(--accent) 22%,transparent) 62%)}
.pub .ve{font-size:14.5px;color:var(--muted);margin-top:3px}.pub .pl{font:12.5px/1.6 var(--mono);color:var(--muted)}
.badges{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px}
.badge{font:500 11.5px/1 var(--mono);padding:5px 9px;border-radius:7px;background:var(--paper-2);color:var(--ink-2);letter-spacing:.01em}
.badge.j{background:var(--accent-soft);color:var(--accent)}.badge.f{background:var(--sage-soft);color:var(--sage)}.badge.aw{background:var(--gold-soft);color:var(--gold)}.badge.acc{background:var(--plum-soft);color:var(--plum)}
.acts{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.acts .tg,.acts a{font:inherit;font-size:13px;font-weight:550;background:var(--card);padding:6px 12px;border-radius:9px;border:1px solid var(--line-2);color:var(--ink-2);cursor:pointer;line-height:1.4;transition:all .15s}
.acts .tg:hover,.acts a:hover{border-color:var(--ink);color:var(--ink)}.acts .tg[aria-expanded="true"]{background:var(--ink);border-color:var(--ink);color:var(--paper)}
.acts .panel{flex-basis:100%;margin-top:8px;padding:18px 20px;background:var(--paper-2);border-radius:14px;font-size:15px;color:var(--ink-2);line-height:1.75}.acts .panel[hidden]{display:none}
.panel pre{margin:0;white-space:pre-wrap;font:12.5px/1.65 var(--mono)}.copy{float:right;font:inherit;font-size:12px;border:1px solid var(--line-2);background:var(--card);color:var(--ink-2);border-radius:8px;padding:3px 10px;cursor:pointer}
.kw{display:flex;flex-wrap:wrap;gap:6px}.kw span{font-size:13px;padding:3px 10px;border-radius:8px;background:var(--card);border:1px solid var(--line)}
.pub.hide{display:none}[role="tabpanel"][hidden]{display:none}
.tabs{display:flex;flex-wrap:wrap;gap:4px;margin:40px 0 12px;padding:4px;background:var(--paper-2);border:1px solid var(--line);border-radius:14px;width:max-content;max-width:100%}
.tabs button{appearance:none;border:0;background:none;font:inherit;font-size:14px;font-weight:550;color:var(--muted);padding:8px 16px;border-radius:10px;cursor:pointer}
.tabs button[aria-selected="true"]{background:var(--card);color:var(--ink);box-shadow:var(--shadow)}.tabs .cnt{font:500 11.5px var(--mono);margin-left:8px;color:var(--muted)}
.seg{display:inline-flex;gap:2px;margin:10px 0 6px;padding:3px;border:1px solid var(--line);border-radius:10px}
.seg button{border:0;background:none;font:inherit;font-size:13px;color:var(--muted);cursor:pointer;padding:4px 12px;border-radius:7px}.seg button[aria-pressed="true"]{color:var(--ink);background:var(--paper-2);font-weight:600}
table.sum{width:100%;border-collapse:separate;border-spacing:0;font-size:15px;background:var(--card);border:1px solid var(--line);border-radius:var(--r);overflow:hidden}
table.sum th,table.sum td{padding:14px 20px;border-bottom:1px solid var(--line);text-align:left}
table.sum th{font:500 11.5px/1.3 var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--muted);background:var(--paper-2)}
table.sum td.num,table.sum th.num{text-align:center;width:110px}table.sum td.num{font-family:var(--display);font-size:20px;font-weight:600}
table.sum tr:last-child td{border-bottom:0}table.sum tr:last-child td:first-child{font-weight:650}table.sum .full{color:var(--muted);font-size:13px;display:block;font-weight:400}
/* academics layout */
.acad{display:grid;grid-template-columns:220px minmax(0,1fr);gap:64px;padding-top:8px}
.toc{position:sticky;top:100px;align-self:start;padding-top:96px}
.toc .me{display:flex;align-items:center;gap:12px;margin-bottom:28px;padding:10px;border:1px solid var(--line);border-radius:16px;background:var(--card)}.toc .me img{width:44px;height:44px;border-radius:12px;object-fit:cover;object-position:50% 25%}
.toc .me b{font-family:var(--display);font-weight:600;font-size:15px;display:block;line-height:1.2}.toc .me span{font:11.5px var(--mono);color:var(--muted)}
.toc ol{list-style:none;margin:0;padding:0;counter-reset:t}.toc li{counter-increment:t}
.toc a{display:flex;gap:12px;background:none;font-size:14px;color:var(--muted);padding:7px 10px;border-radius:9px}
.toc a::before{content:counter(t,decimal-leading-zero);font:11.5px/1.9 var(--mono);color:var(--line-2)}
.toc a:hover{color:var(--ink);background:var(--paper-2)}.toc a.on{color:var(--ink);background:var(--paper-2);font-weight:550}.toc a.on::before{color:var(--accent)}
.page-head{padding:80px 0 0}.page-head h1{font-size:clamp(48px,6.4vw,88px);font-weight:650;letter-spacing:-.055em;line-height:.95;margin-top:24px}
.page-head p{color:var(--ink-2);font-size:19px;margin:20px 0 0;max-width:46ch}
/* education */
.edu{display:grid;grid-template-columns:56px minmax(0,1fr) auto;gap:20px;align-items:center;padding:22px 24px;border:1px solid var(--line);border-radius:var(--r);background:var(--card);margin-bottom:12px}
.edu h4{font-size:19px;line-height:1.3}.edu .where{font-size:14.5px;color:var(--ink-2);margin-top:4px}.edu .where a{font-weight:550;background:none}.edu .adv{font-size:13.5px;color:var(--muted);margin-top:2px}
.edu .when{font:12.5px var(--mono);color:var(--muted);white-space:nowrap;padding:6px 10px;border-radius:8px;background:var(--paper-2);align-self:start}
/* awards */
.awg{margin-bottom:40px}.awg h3{font:500 12px/1 var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-bottom:10px}
.aw{list-style:none;margin:0;padding:0;border:1px solid var(--line);border-radius:var(--r);background:var(--card);overflow:hidden}
.aw li{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;padding:16px 22px;border-top:1px solid var(--line)}.aw li:first-child{border-top:0}
.aw .t{font-family:var(--display);font-size:17px;font-weight:600;letter-spacing:-.015em}.aw .who{font-size:14px;color:var(--muted);margin-top:2px}
.aw .chip{display:inline-block;margin-left:8px;font:500 11px/1 var(--mono);padding:4px 7px;border-radius:6px;vertical-align:2px;background:var(--sage-soft);color:var(--sage)}.aw .chip.pi{background:var(--gold-soft);color:var(--gold)}
.aw .d{font:12.5px var(--mono);color:var(--muted);white-space:nowrap;padding-top:4px}
/* projects */
.proj{display:grid;grid-template-columns:56px minmax(0,1fr);gap:20px;padding:26px;margin-bottom:14px;background:var(--card);border:1px solid var(--line);border-radius:var(--r)}
.proj .when{font:12.5px var(--mono);color:var(--muted)}.proj h4{font-size:20px;line-height:1.35;margin:6px 0 6px}
.proj .org{font-size:14.5px;color:var(--ink-2)}.proj ul{margin:14px 0 0;padding-left:18px;color:var(--ink-2);font-size:15px}.proj li{margin:5px 0}.proj li::marker{color:var(--accent)}
.plain{margin:0;padding:0;list-style:none;border:1px solid var(--line);border-radius:var(--r);background:var(--card);overflow:hidden}
.plain li{padding:15px 22px;border-top:1px solid var(--line);color:var(--ink-2)}.plain li:first-child{border-top:0}.plain b{color:var(--ink);font-weight:600}
.skills{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.skill{padding:20px 22px;background:var(--card);border:1px solid var(--line);border-radius:var(--r)}.skill b{display:block;font:500 11.5px/1 var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--accent);margin-bottom:10px}
/* contact */
.contact{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:48px;align-items:start;margin-top:48px}
.cbox{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:8px 28px}
.cbox dl{margin:0}.cbox .row{display:grid;grid-template-columns:120px minmax(0,1fr);gap:16px;padding:20px 0;border-top:1px solid var(--line)}.cbox .row:first-child{border-top:0}
.cbox dt{font:500 11.5px/1.9 var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}.cbox dd{margin:0}
.cbox .big{font-family:var(--display);font-size:24px;font-weight:600;letter-spacing:-.02em}
footer{margin-top:120px;border-top:1px solid var(--line)}footer .wrap{display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px 24px;padding:28px 32px;color:var(--muted);font:12.5px/1.6 var(--mono)}
footer a{color:var(--muted)}
@media (max-width:980px){.hero{grid-template-columns:1fr;gap:40px;padding-top:56px}.portrait{justify-self:start;max-width:300px}.acad{grid-template-columns:1fr;gap:0}.toc{display:none}
.glance{grid-template-columns:repeat(3,minmax(0,1fr))}.contact{grid-template-columns:1fr}}
@media (max-width:680px){.wrap{padding:0 20px}body{font-size:16px}.themes,.skills{grid-template-columns:1fr}.theme-item{min-height:0;gap:20px}.glance{grid-template-columns:repeat(2,minmax(0,1fr))}
.news li{grid-template-columns:1fr;gap:4px}.pub{grid-template-columns:1fr}.pub .idx{display:none}.edu{grid-template-columns:44px minmax(0,1fr);padding:18px}.edu .when{grid-column:2;justify-self:start}
.logo.lg,.mono{width:44px;height:44px}.proj{grid-template-columns:1fr;padding:20px}.cbox .row{grid-template-columns:1fr;gap:2px}
nav.main a{padding:7px 9px;font-size:14px}.brand{font-size:16px}.sec{padding-top:72px}.tabs{width:100%}.g .v{font-size:42px}}
@media print{body::before,header.top,.toc,.tabs,.seg,.acts,.theme,footer{display:none!important}[role="tabpanel"][hidden],.pub.hide{display:block!important}}
"""

JS = r"""
(function(){var r=document.documentElement,k='sm-theme';try{var s=localStorage.getItem(k);if(s)r.setAttribute('data-theme',s)}catch(e){}
var b=document.querySelector('.theme');if(b)b.addEventListener('click',function(){var d=r.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');var n=d==='dark'?'light':'dark';r.setAttribute('data-theme',n);try{localStorage.setItem(k,n)}catch(e){}});
document.querySelectorAll('[data-mail]').forEach(function(a){var u=a.getAttribute('data-u'),d=a.getAttribute('data-d');a.href='mailto:'+u+'@'+d;if(a.hasAttribute('data-show'))a.textContent=u+'@'+d});
document.querySelectorAll('.tabs').forEach(function(t){var bs=t.querySelectorAll('button');bs.forEach(function(x){x.addEventListener('click',function(){bs.forEach(function(y){y.setAttribute('aria-selected','false');document.getElementById(y.getAttribute('aria-controls')).hidden=true});x.setAttribute('aria-selected','true');document.getElementById(x.getAttribute('aria-controls')).hidden=false})})});
document.querySelectorAll('.seg').forEach(function(s){var bs=s.querySelectorAll('button'),list=document.getElementById(s.getAttribute('data-for'));function apply(sel){list.querySelectorAll('.pub').forEach(function(p){p.classList.toggle('hide',sel&&p.getAttribute('data-sel')!=='1')})}
bs.forEach(function(x){x.addEventListener('click',function(){bs.forEach(function(y){y.setAttribute('aria-pressed','false')});x.setAttribute('aria-pressed','true');apply(x.getAttribute('data-mode')==='sel')})});apply(true)});
document.querySelectorAll('.tg').forEach(function(b){b.addEventListener('click',function(){var p=document.getElementById(b.getAttribute('aria-controls')),o=b.getAttribute('aria-expanded')==='true';b.setAttribute('aria-expanded',o?'false':'true');p.hidden=o})});
document.querySelectorAll('.copy').forEach(function(c){c.addEventListener('click',function(){var t=c.parentNode.querySelector('pre').textContent;(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){c.textContent='Copied'},function(){c.textContent='Select & copy'});setTimeout(function(){c.textContent='Copy'},1600)})});
var toc=document.querySelectorAll('.toc a[href^="#"]');if(toc.length&&'IntersectionObserver' in window){var m={};toc.forEach(function(a){m[a.getAttribute('href').slice(1)]=a});
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){toc.forEach(function(a){a.classList.remove('on')});var a=m[e.target.id];if(a)a.classList.add('on')}})},{rootMargin:'-25% 0px -70% 0px'});
document.querySelectorAll('section.sec[id]').forEach(function(s){io.observe(s)})}})();
"""

ICON_MOON = "<svg width='17' height='17' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' aria-hidden='true'><path d='M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z'/></svg>"
FONTS = ("<link rel='preconnect' href='https://fonts.googleapis.com'><link rel='preconnect' href='https://fonts.gstatic.com' crossorigin>"
         "<link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;family=Inter+Tight:wght@500;600;700&amp;family=JetBrains+Mono:wght@400;500&amp;display=swap'>"
         "<link rel='stylesheet' href='https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css'>")

def page(fname, title, desc, body, current):
    CUR = ' aria-current="page"'
    nav = "".join(f"<a href='{u}'{CUR if current == u else ''}>{t}</a>" for t, u in [("Home", "index.html"), ("Academics", "academics.html"), ("Contact", "contact.html")])
    url = f"{SITE_URL}/{'' if fname == 'index.html' else fname}"
    same = ",".join('"' + u + '"' for _, u in PROFILE["links"][:3])
    return f"""<!doctype html>
<html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>
<title>{esc(title)}</title><meta name='description' content='{esc(desc)}'><link rel='canonical' href='{url}'>
<meta name='color-scheme' content='light dark'><meta name='theme-color' content='#ffffff'>
<meta property='og:type' content='website'><meta property='og:title' content='{esc(title)}'><meta property='og:description' content='{esc(desc)}'>
<meta property='og:url' content='{url}'><meta property='og:image' content='{SITE_URL}/{PROFILE['photo']}'>
<link rel='icon' href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='16' fill='%234338ca'/%3E%3Ctext x='32' y='43' font-family='Arial' font-size='26' font-weight='700' fill='white' text-anchor='middle'%3ES%3C/text%3E%3C/svg%3E">
<link rel='alternate' type='text/plain' href='llms-full.txt' title='Full plain-text version'>{FONTS}
<script type='application/ld+json'>{{"@context":"https://schema.org","@type":"Person","name":"{PROFILE['name']}","jobTitle":"{PROFILE['title']}","affiliation":{{"@type":"CollegeOrUniversity","name":"{PROFILE['univ']}"}},"url":"{SITE_URL}","sameAs":[{same}]}}</script>
<style>{CSS}</style></head>
<body><a class='skip' href='#main'>Skip to content</a>
<header class='top'><div class='wrap'><a class='brand' href='index.html'>Sangmin Lee</a>
<nav class='main' aria-label='Primary'>{nav}</nav><button class='theme' type='button' aria-label='Toggle dark mode'>{ICON_MOON}</button></div></header>
<main id='main'>{body}</main>
<footer><div class='wrap'><span>© 2026 {PROFILE['name']} · {PROFILE['lab']}, {PROFILE['univ']}</span><span>Updated {UPDATED} · <a href='llms-full.txt'>Plain-text version</a></span></div></footer>
<script>{JS}</script></body></html>"""

def sec(i, sid, title, inner, sub=""):
    return (f"<section class='sec' id='{sid}'><div class='sec-h'><span class='n'>{i:02d}</span><h2>{title}</h2><span class='rule'></span></div>"
            f"{f'<p class=sub>{sub}</p>' if sub else ''}{inner}</section>")

def logo(src, alt, big=True):
    return f"<span class='logo{' lg' if big else ''}'><img src='{src}' alt='{esc(alt)} logo' loading='lazy'></span>"

# ------------------------------------------------------------------ pubs
def render_pub(p, idx, kind):
    sel = "1" if p.get("selected") else "0"
    b = []
    if kind == "j":
        b.append(f"<span class='badge j'>{esc(p['jabbr'])}</span>")
        if p.get("status"): b.append(f"<span class='badge acc'>{esc(p['status'])}</span>")
        if p["first"]: b.append("<span class='badge f'>First author</span>")
    acts, panels = [], []
    uid = f"{p['key']}-{kind}"
    def add(label, inner):
        pid = f"{uid}-{label.lower()}"
        acts.append(f"<button type='button' class='tg' aria-expanded='false' aria-controls='{pid}'>{label}</button>")
        panels.append(f"<div class='panel' id='{pid}' hidden>{inner}</div>")
    if p.get("abstract"): add("Abstract", esc(p["abstract"]))
    if p.get("keywords"): add("Keywords", "<div class='kw'>" + "".join(f"<span>{esc(k)}</span>" for k in p["keywords"]) + "</div>")
    add("BibTeX", f"<button class='copy' type='button'>Copy</button><pre>{esc(bib(p, 'article' if kind == 'j' else 'inproceedings'))}</pre>")
    if p.get("doi"): acts.append(f"<a href='https://doi.org/{p['doi']}' rel='noopener'>DOI ↗</a>")
    place = f"<div class='pl'>{esc(p['place'])}</div>" if p.get("place") else ""
    return (f"<li class='pub' data-sel='{sel}'><div class='idx'>{idx}</div><div><div class='ttl'>{esc(p['title'])}</div>"
            f"<div class='au'>{bold_me(p['authors'])}</div><div class='ve'>{esc(p['venue'])}</div>{place}"
            f"{'<div class=badges>'+''.join(b)+'</div>' if b else ''}<div class='acts'>{''.join(acts + panels)}</div></div></li>")

def journal_table():
    rows = {}
    for p in JOURNALS:
        r = rows.setdefault(p["jabbr"], [0, 0]); r[0 if p["first"] else 1] += 1
    rank = list(JOURNAL_FULL.keys())
    order = sorted(rows.items(), key=lambda kv: rank.index(kv[0]) if kv[0] in rank else 99)
    body = "".join(f"<tr><td><b>{esc(k)}</b><span class='full'>{esc(JOURNAL_FULL[k])}</span></td><td class='num'>{v[0] or '–'}</td><td class='num'>{v[1] or '–'}</td><td class='num'>{sum(v)}</td></tr>" for k, v in order)
    f = sum(v[0] for v in rows.values()); c = sum(v[1] for v in rows.values())
    return f"<table class='sum'><thead><tr><th>Journal</th><th class='num'>First</th><th class='num'>Co-author</th><th class='num'>Total</th></tr></thead><tbody>{body}<tr><td>Total</td><td class='num'>{f}</td><td class='num'>{c}</td><td class='num'>{f+c}</td></tr></tbody></table>"

def news_li(n):
    d, k, t = n
    return f"<li><time datetime='{d}'>{fmt_date(d)}</time><div><span class='k {k}'>{KIND_LABEL[k]}</span><div class='txt'>{t}</div></div></li>"

# ------------------------------------------------------------------ pages
def build_home():
    pills = (f"<a class='pill solid' data-mail data-u='{PROFILE['email_user']}' data-d='{PROFILE['email_domain']}' href='contact.html'>Email</a>"
             + "".join(f"<a class='pill' href='{u}' rel='noopener'>{esc(t)}</a>" for t, u in PROFILE["links"]))
    hero = f"""<div class='wrap'><section class='hero'>
<div><span class='eyebrow'>Ph.D. Student · Kyungpook National University</span>
<h1>Sangmin Lee<span class='ko'>이상민</span></h1>
<div class='bio'>{''.join(f'<p>{p}</p>' for p in ABOUT)}</div><div class='pills'>{pills}</div></div>
<div class='portrait'><div class='frame'><img src='{PROFILE['photo']}' alt='Portrait of {PROFILE['name']}' width='354' height='472'></div>
<div class='aff'>{logo('assets/logos/knu.jpg', 'Kyungpook National University', False)}<div class='t'><b>{PROFILE['lab']}</b>{PROFILE['dept']}<br>{PROFILE['univ']}</div></div></div>
</section>"""
    themes = "".join(f"<div class='theme-item'><span class='num'>{i+1:02d}</span><h3>{esc(t)}</h3></div>" for i, (t, _) in enumerate(INTERESTS))
    glance = "".join(f"<div class='g'><div class='v'>{v}</div><div class='l'>{esc(l)}</div><div class='s'>{esc(s)}</div></div>" for v, l, s in stats())
    sel = [p for p in JOURNALS if p["selected"]]
    body = hero + sec(1, "research", "Research", f"<div class='themes'>{themes}</div>") + \
        sec(2, "glance", "At a Glance", f"<div class='glance'>{glance}</div>", f"As of {UPDATED} · full record on the <a href='academics.html'>Academics</a> page") + \
        sec(3, "news", "News", f"<ul class='news'>{''.join(news_li(n) for n in NEWS[:6])}</ul><details class='more'><summary>Earlier news ({len(NEWS)-6})</summary><ul class='news'>{''.join(news_li(n) for n in NEWS[6:])}</ul></details>") + \
        sec(4, "selected", "Selected Publications", f"<ol class='pubs'>{''.join(render_pub(p, i+1, 'j') for i, p in enumerate(sel))}</ol><p style='margin-top:18px'><a href='academics.html#publications'>All publications →</a></p>", "Highlighted name = me · * corresponding author") + "</div>"
    return page("index.html", f"{PROFILE['name']} — Ph.D. Student, KNU",
                "Sangmin Lee, Ph.D. student at Kyungpook National University (PLAYWAVE Lab): reconfigurable intelligent surfaces, Huygens' metasurfaces, series-fed and phased arrays for 6G and radar.", body, "index.html")

def build_academics():
    toc = [("education", "Education"), ("publications", "Publications"), ("awards", "Awards & Honors"), ("research", "Research Projects"),
           ("service", "Service"), ("mentoring", "Mentoring & Collaborators"), ("skills", "Skills")]
    edu = "".join(f"""<div class='edu'>{logo(e['logo'], e['school'])}<div><h4>{esc(e['degree'])}</h4>
<div class='where'><a href='{e['url']}' rel='noopener'>{esc(e['school'])}</a> · {esc(e['place'])}</div>
{f"<div class='adv'>Advisor: <a href='{e['advisor'][1]}' rel='noopener'>Prof. {esc(e['advisor'][0])}</a></div>" if e['advisor'] else ''}</div>
<div class='when'>{e['period']}</div></div>""" for e in EDUCATION)

    j_html = "".join(render_pub(p, len(JOURNALS) - i, "j") for i, p in enumerate(JOURNALS))
    c_html = "".join(render_pub(p, len(INTL_CONF) - i, "c") for i, p in enumerate(INTL_CONF))
    d_items = []
    for i, (y, m, au, t, conf, note, aw) in enumerate(DOMESTIC):
        b = "".join([f"<span class='badge aw'>{esc(aw)}</span>" if aw else "", f"<span class='badge'>{esc(note)}</span>" if note else ""])
        d_items.append(f"<li class='pub'><div class='idx'>{len(DOMESTIC)-i}</div><div><div class='ttl' style='font-size:18px'>{esc(t)}</div><div class='au'>{bold_me(au)}</div><div class='ve'>{esc(conf)}, {m} {y}</div>{'<div class=badges>'+b+'</div>' if b else ''}</div></li>")
    p_items = "".join(f"""<li class='pub'><div class='idx'>{len(PATENTS)-i}</div><div><div class='ttl'>{esc(p['title'])}</div><div class='au'>Inventors: {bold_me(p['inventors'])}</div>
<div class='ve'>{p['country']} · {'Patent No.' if p['status']=='Registered' else 'Application No.'} {p['number']} · {p['date']}</div>
<div class='badges'><span class='badge {'f' if p['status']=='Registered' else ''}'>{p['status']}</span></div>
{f"<div class='acts'><a href='{p['url']}' rel='noopener'>Google Patents ↗</a></div>" if p['url'] else ''}</div></li>""" for i, p in enumerate(PATENTS))
    tabs = [("tab-j", "Journals", len(JOURNALS)), ("tab-c", "International", len(INTL_CONF)), ("tab-d", "Domestic", len(DOMESTIC)), ("tab-p", "Patents", len(PATENTS))]
    tabbar = "<div class='tabs' role='tablist'>" + "".join(f"<button type='button' role='tab' aria-selected='{'true' if i==0 else 'false'}' aria-controls='{t}'>{n}<span class='cnt'>{c}</span></button>" for i, (t, n, c) in enumerate(tabs)) + "</div>"
    pubs = f"""{journal_table()}{tabbar}
<div id='tab-j' role='tabpanel'><div class='seg' data-for='list-j'><button type='button' data-mode='sel' aria-pressed='true'>Selected</button><button type='button' data-mode='all' aria-pressed='false'>All</button></div><ol class='pubs' id='list-j'>{j_html}</ol></div>
<div id='tab-c' role='tabpanel' hidden><ol class='pubs'>{c_html}</ol></div>
<div id='tab-d' role='tabpanel' hidden><ol class='pubs'>{''.join(d_items)}</ol></div>
<div id='tab-p' role='tabpanel' hidden><ol class='pubs'>{p_items}</ol></div>"""

    def aw_group(name, items, collapsed=False):
        lis = []
        for t, extra, org, d, own in items:
            chip = "<span class='chip pi'>PI</span>" if "Principal" in extra else ("<span class='chip'>First author</span>" if own and name.startswith(("Conference", "Institutional")) else "")
            who = esc(org) + (" · No. RS-2026-25552947" if "Principal" in extra else (" · " + esc(extra) if extra else ""))
            lis.append(f"<li><div><span class='t'>{esc(t)}</span>{chip}<div class='who'>{who}</div></div><div class='d'>{esc(d)}</div></li>")
        ul = f"<ul class='aw'>{''.join(lis)}</ul>"
        if collapsed:
            return f"<div class='awg'><details class='more'><summary>{esc(name)} ({len(items)})</summary>{ul}</details></div>"
        return f"<div class='awg'><h3>{esc(name)}</h3>{ul}</div>"
    awards = "".join(aw_group(n, it, n == "Undergraduate Competitions") for n, it in AWARDS)

    def mono(org):
        if "NRF" in org: return "<span class='mono'>NRF</span>"
        if "IITP" in org: return "<span class='mono sage'>IITP</span>"
        return "<span class='mono'>R&amp;D</span>"
    projs = "".join(f"""<div class='proj'>{mono(p['org'])}<div><div class='when'>{esc(p['period'])}</div><h4>{esc(p['title'])}</h4>
<div class='org'>{esc(p['org'])} · No. {esc(p['no'])}</div><div class='badges'><span class='badge {'aw' if p['role']=='Principal Investigator' else ''}'>{esc(p['role'])}</span></div>
<ul>{''.join(f'<li>{esc(b)}</li>' for b in p['bullets'])}</ul></div></div>""" for p in PROJECTS)
    service = "".join(f"<div class='awg'><h3>{esc(h)}</h3><ul class='plain'>{''.join(f'<li>{esc(x)}</li>' for x in xs)}</ul></div>" for h, xs in SERVICE)
    def ment(x):
        return re.sub(r"^([^—]+)—", r"<b>\1</b>—", x)
    mentoring = "".join(f"<div class='awg'><h3>{esc(h)}</h3><ul class='plain'>{''.join(f'<li>{ment(x)}</li>' for x in xs)}</ul></div>" for h, xs in MENTORING)
    skills = "<div class='skills'>" + "".join(f"<div class='skill'><b>{esc(a)}</b>{esc(b)}</div>" for a, b in SKILLS) + "</div>"

    tochtml = f"""<aside class='toc'><div class='me'><img src='{PROFILE['photo']}' alt=''><div><b>{PROFILE['name']}</b><span>{PROFILE['title']}, KNU</span></div></div>
<nav aria-label='On this page'><ol>{''.join(f"<li><a href='#{i}'>{esc(t)}</a></li>" for i, t in toc)}</ol></nav></aside>"""
    content = "<div>" + sec(1, "education", "Education", edu) + sec(2, "publications", "Publications", pubs) + sec(3, "awards", "Awards &amp; Honors", awards) + \
        sec(4, "research", "Research Projects", projs) + sec(5, "service", "Service", service) + sec(6, "mentoring", "Mentoring &amp; Collaborators", mentoring) + \
        sec(7, "skills", "Skills", skills) + "</div>"
    body = f"""<div class='wrap'><div class='page-head'><span class='eyebrow'>Academic record</span><h1>Academics</h1>
<p>Education, publications, awards and research projects.</p></div><div class='acad'>{tochtml}{content}</div></div>"""
    return page("academics.html", f"Academics — {PROFILE['name']}",
                "Education, publications (journals, conferences, patents), awards, research projects, service and mentoring of Sangmin Lee.", body, "academics.html")

def build_contact():
    links = "".join(f"<a class='pill' href='{u}' rel='noopener'>{esc(t)}</a>" for t, u in PROFILE["links"])
    body = f"""<div class='wrap'><div class='page-head'><span class='eyebrow'>Get in touch</span><h1>Contact</h1>
<p>For research collaboration or questions, email is the best way to reach me.</p></div>
<div class='contact'><div class='cbox'><dl>
<div class='row'><dt>Email</dt><dd><a class='big' data-mail data-show data-u='{PROFILE['email_user']}' data-d='{PROFILE['email_domain']}' href='#'>{PROFILE['email_user']} [at] {PROFILE['email_domain']}</a></dd></div>
<div class='row'><dt>Lab</dt><dd><a href='{PROFILE['lab_url']}' rel='noopener'>{PROFILE['lab']}</a> · Prof. Sangjo Choi</dd></div>
<div class='row'><dt>Affiliation</dt><dd>{PROFILE['dept']}<br>{PROFILE['univ']}</dd></div>
<div class='row'><dt>Office</dt><dd>{PROFILE['office']}</dd></div>
<div class='row'><dt>Profiles</dt><dd><div class='pills' style='margin:0'>{links}</div></dd></div></dl></div>
<div class='portrait' style='justify-self:stretch'><div class='frame'><img src='{PROFILE['photo']}' alt='Portrait of {PROFILE['name']}'></div>
<div class='aff'>{logo('assets/logos/knu.jpg', 'Kyungpook National University', False)}<div class='t'><b>Kyungpook National University</b>Daegu, Republic of Korea</div></div></div></div></div>"""
    return page("contact.html", f"Contact — {PROFILE['name']}", "Contact information for Sangmin Lee, Kyungpook National University.", body, "contact.html")

def plain_text():
    L = [f"# {PROFILE['name']} ({PROFILE['name_ko']})", f"{PROFILE['title']}, {PROFILE['dept']}, {PROFILE['univ']}", f"Lab: {PROFILE['lab']} ({PROFILE['lab_url']})", f"Site: {SITE_URL}", ""]
    L += ["## About"] + [re.sub("<[^>]+>", "", html.unescape(p)) for p in ABOUT] + ["", "## Research interests"] + [f"- {t}" for t, _ in INTERESTS]
    L += ["", "## Education"] + [f"- {e['period']}: {e['degree']}, {e['school']}" + (f" (advisor: Prof. {e['advisor'][0]})" if e['advisor'] else "") for e in EDUCATION]
    L += ["", "## Journal papers"] + [f"- {p['authors'].replace('**','')}, \"{p['title']},\" {p['venue']}." + (f" doi:{p['doi']}" if p.get('doi') else "") for p in JOURNALS]
    L += ["", "## International conference papers"] + [f"- {p['authors']}, \"{p['title']},\" {p['venue']}, {p['place']}." for p in INTL_CONF]
    L += ["", "## Domestic conference papers"] + [f"- {a.replace('**','')}, \"{t},\" {c}, {m} {y}." + (f" [{aw}]" if aw else "") for y, m, a, t, c, n, aw in DOMESTIC]
    L += ["", "## Patents"] + [f"- {p['title']} ({p['country']} {p['status']} {p['number']}, {p['date']}); inventors: {p['inventors']}" for p in PATENTS]
    L += ["", "## Awards & honors"]
    for n, it in AWARDS:
        L += [f"### {n}"] + [f"- {t}{' ('+x+')' if x else ''}, {o}, {d}" for t, x, o, d, _ in it]
    L += ["", "## Research projects"] + [f"- {p['period']}: {p['title']} — {p['org']}, No. {p['no']} ({p['role']})" for p in PROJECTS]
    L += ["", f"Contact: {PROFILE['email_user']} [at] {PROFILE['email_domain']}", f"Last updated: {UPDATED}"]
    return "\n".join(L) + "\n"

def main():
    os.makedirs(os.path.join(OUT, "assets", "logos"), exist_ok=True)
    files = {"index.html": build_home(), "academics.html": build_academics(), "contact.html": build_contact(), "llms-full.txt": plain_text(),
             "llms.txt": f"# {PROFILE['name']}\n> {PROFILE['title']}, {PROFILE['univ']} — RIS, Huygens' metasurfaces, antenna arrays.\n\n- [Home]({SITE_URL}/index.html)\n- [Academics]({SITE_URL}/academics.html)\n- [Contact]({SITE_URL}/contact.html)\n- [Full plain text]({SITE_URL}/llms-full.txt)\n",
             "robots.txt": f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n",
             "sitemap.xml": "<?xml version='1.0' encoding='UTF-8'?>\n<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>" + "".join(f"<url><loc>{SITE_URL}/{p}</loc></url>" for p in ["", "academics.html", "contact.html"]) + "</urlset>\n",
             "404.html": page("404.html", "Not found — Sangmin Lee", "Page not found.", "<div class='wrap'><div class='page-head'><span class='eyebrow'>404</span><h1>Page not found</h1><p><a href='index.html'>Back to home →</a></p></div></div>", "")}
    for n, c in files.items():
        with open(os.path.join(OUT, n), "w", encoding="utf-8", newline="\n") as f:
            f.write(c)
    print("built:", ", ".join(files))

if __name__ == "__main__":
    main()
