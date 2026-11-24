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
--paper:#fbf8f3;--paper-2:#f4efe6;--card:#ffffff;--ink:#1f1c18;--ink-2:#3d3832;--muted:#7a7166;--line:#e8e0d3;--line-2:#d9cfbf;
--accent:#a8432b;--accent-ink:#ffffff;--accent-soft:#f6e6df;--sage:#4f6f5f;--sage-soft:#e3ece6;--gold:#9a6b10;--gold-soft:#f6ecd4;--plum:#6a4a6e;--plum-soft:#efe5f0;
--serif:"Fraunces","Noto Serif KR",Georgia,"Times New Roman",serif;
--sans:"Pretendard Variable",Pretendard,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;
--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--r:18px;--shadow:0 1px 1px rgba(60,40,20,.04),0 8px 30px -12px rgba(60,40,20,.12)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
--paper:#16140f;--paper-2:#1d1a15;--card:#211e18;--ink:#f1ebe1;--ink-2:#d8d0c3;--muted:#a39886;--line:#322d25;--line-2:#423b31;
--accent:#e38a6f;--accent-ink:#16140f;--accent-soft:#3a241c;--sage:#9cc0ab;--sage-soft:#1f2c25;--gold:#e5bd62;--gold-soft:#342913;--plum:#cfa9d3;--plum-soft:#2c2130;--shadow:none}}
:root[data-theme="dark"]{--paper:#16140f;--paper-2:#1d1a15;--card:#211e18;--ink:#f1ebe1;--ink-2:#d8d0c3;--muted:#a39886;--line:#322d25;--line-2:#423b31;
--accent:#e38a6f;--accent-ink:#16140f;--accent-soft:#3a241c;--sage:#9cc0ab;--sage-soft:#1f2c25;--gold:#e5bd62;--gold-soft:#342913;--plum:#cfa9d3;--plum-soft:#2c2130;--shadow:none}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:90px;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.75 var(--sans);-webkit-font-smoothing:antialiased;letter-spacing:-.003em}
a{color:inherit;text-decoration:underline;text-decoration-color:color-mix(in srgb,var(--accent) 45%,transparent);text-underline-offset:3px;text-decoration-thickness:1px}
a:hover{color:var(--accent);text-decoration-color:var(--accent)}
::selection{background:var(--accent-soft)}
.skip{position:absolute;left:-999px}.skip:focus{left:16px;top:12px;background:var(--card);padding:8px 12px;border-radius:8px;z-index:99}
.wrap{max-width:1120px;margin:0 auto;padding:0 28px}
/* header */
header.top{position:sticky;top:0;z-index:30;background:color-mix(in srgb,var(--paper) 82%,transparent);backdrop-filter:blur(14px) saturate(1.3)}
header.top .wrap{height:72px;display:flex;align-items:center;gap:24px}
.brand{font-family:var(--serif);font-size:21px;font-weight:600;letter-spacing:-.01em;text-decoration:none;color:var(--ink);font-variation-settings:"opsz" 36}
.brand i{font-style:italic;font-weight:400;color:var(--accent)}
nav.main{margin-left:auto;display:flex;gap:2px;align-items:center}
nav.main a{text-decoration:none;color:var(--muted);font-size:15px;font-weight:500;padding:8px 14px;border-radius:999px}
nav.main a:hover{color:var(--ink);background:var(--paper-2)}nav.main a[aria-current="page"]{color:var(--ink);background:var(--card);box-shadow:var(--shadow)}
.theme{margin-left:6px;width:38px;height:38px;border-radius:999px;border:1px solid var(--line);background:transparent;color:var(--muted);cursor:pointer;display:grid;place-items:center}
.theme:hover{color:var(--ink);border-color:var(--line-2)}
/* type */
.eyebrow{font-size:12.5px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--accent)}
h1,h2,h3,h4{font-family:var(--serif);font-weight:500;letter-spacing:-.015em;font-variation-settings:"opsz" 72;margin:0}
.sec{padding:72px 0 0}.sec-h{display:flex;align-items:baseline;gap:16px;margin-bottom:26px}
.sec-h h2{font-size:34px;line-height:1.1}.sec-h .n{font-family:var(--serif);font-style:italic;color:var(--accent);font-size:18px}
.sec-h .rule{flex:1;height:1px;background:var(--line);transform:translateY(-6px)}
.sub{color:var(--muted);font-size:15px;margin:-14px 0 24px}
/* hero */
.hero{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,.65fr);gap:64px;align-items:center;padding:56px 0 8px}
.hero h1{font-size:clamp(46px,6.6vw,84px);line-height:.98;font-weight:400;letter-spacing:-.035em;margin:14px 0 6px}
.hero h1 .ko{display:block;font-family:var(--sans);font-size:17px;letter-spacing:.3em;color:var(--muted);font-weight:500;margin-top:14px}
.hero .tag{font-family:var(--serif);font-style:italic;font-size:clamp(21px,2.3vw,26px);line-height:1.4;color:var(--ink-2);margin:26px 0 22px;max-width:30ch;font-weight:400}
.hero .tag em{color:var(--accent);font-style:italic}
.bio p{margin:0 0 14px;color:var(--ink-2);max-width:62ch}
.pills{display:flex;flex-wrap:wrap;gap:8px;margin-top:22px}
.pill{display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:500;text-decoration:none;padding:8px 16px;border-radius:999px;border:1px solid var(--line-2);color:var(--ink-2);background:var(--card)}
.pill:hover{border-color:var(--accent);color:var(--accent)}.pill.solid{background:var(--ink);color:var(--paper);border-color:var(--ink)}.pill.solid:hover{background:var(--accent);border-color:var(--accent);color:var(--accent-ink)}
.portrait{position:relative;justify-self:end;width:100%;max-width:360px}
.portrait .frame{border-radius:999px 999px 28px 28px;overflow:hidden;aspect-ratio:3/4;background:var(--paper-2);box-shadow:var(--shadow);outline:1px solid var(--line);outline-offset:8px}
.portrait img{width:100%;height:100%;object-fit:cover;object-position:50% 30%;display:block}
.aff{display:flex;align-items:center;gap:12px;margin-top:26px;padding:12px 14px;border-radius:16px;background:var(--card);border:1px solid var(--line)}
.aff .t{font-size:13.5px;line-height:1.45;color:var(--ink-2)}.aff .t b{display:block;font-weight:600;color:var(--ink)}
.logo{flex:none;width:46px;height:46px;border-radius:12px;background:#fff;border:1px solid var(--line);display:grid;place-items:center;overflow:hidden}
.logo img{width:82%;height:82%;object-fit:contain}.logo.lg{width:58px;height:58px;border-radius:14px}
.mono{flex:none;width:58px;height:58px;border-radius:14px;display:grid;place-items:center;font-family:var(--serif);font-weight:600;font-size:15px;letter-spacing:.02em;color:var(--accent);background:var(--accent-soft)}
.mono.sage{color:var(--sage);background:var(--sage-soft)}
/* research */
.themes{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 48px}
.theme-item{display:grid;grid-template-columns:64px minmax(0,1fr);gap:8px;padding:24px 0;border-top:1px solid var(--line)}
.theme-item .num{font-family:var(--serif);font-style:italic;font-size:30px;color:var(--accent);line-height:1}
.theme-item h3{font-size:22px;line-height:1.3}
/* glance */
.glance{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));background:var(--card);border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--shadow);overflow:hidden}
.g{padding:26px 22px;border-left:1px solid var(--line)}.g:first-child{border-left:0}
.g .v{font-family:var(--serif);font-size:48px;line-height:1;font-weight:400;letter-spacing:-.03em;color:var(--ink)}
.g .l{font-size:14px;color:var(--ink-2);margin-top:10px;line-height:1.35;font-weight:500}.g .s{font-size:12.5px;color:var(--muted);margin-top:4px}
/* news */
.news{list-style:none;margin:0;padding:0;position:relative}
.news li{display:grid;grid-template-columns:130px minmax(0,1fr);gap:24px;padding:16px 0;border-top:1px solid var(--line)}
.news li:first-child{border-top:0}
.news time{font-size:13.5px;color:var(--muted);font-variant-numeric:tabular-nums;padding-top:3px}
.news .k{display:inline-flex;align-items:center;gap:6px;font-size:11.5px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:2px}
.news .k::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--muted)}
.news .k.award::before,.news .k.grant::before{background:var(--gold)}.news .k.paper::before{background:var(--accent)}.news .k.talk::before{background:var(--sage)}.news .k.milestone::before{background:var(--plum)}
.news .txt{color:var(--ink-2)}.news .txt b{color:var(--ink);font-weight:600}
details.more{margin-top:6px}details.more>summary{cursor:pointer;list-style:none;display:inline-flex;align-items:center;gap:8px;font-size:14.5px;font-weight:600;color:var(--accent);padding:10px 0}
details.more>summary::-webkit-details-marker{display:none}details.more>summary::after{content:"+";font-family:var(--serif);font-size:20px;line-height:1}details.more[open]>summary::after{content:"–"}
/* publications */
.pubs{list-style:none;margin:0;padding:0}
.pub{display:grid;grid-template-columns:52px minmax(0,1fr);gap:10px;padding:22px 0;border-top:1px solid var(--line)}.pub:first-child{border-top:0}
.pub .idx{font-family:var(--serif);font-style:italic;color:var(--muted);font-size:16px;padding-top:2px}
.pub .ttl{font-family:var(--serif);font-size:20px;line-height:1.35;font-weight:500;color:var(--ink);letter-spacing:-.01em}
.pub .au{font-size:15px;color:var(--ink-2);margin-top:6px}.pub .au b.me{font-weight:700;color:var(--ink);box-shadow:inset 0 -.42em 0 var(--accent-soft)}
.pub .ve{font-size:14.5px;color:var(--muted);font-style:italic;margin-top:2px}.pub .pl{font-size:13.5px;color:var(--muted)}
.badges{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.badge{font-size:12px;font-weight:600;padding:3px 10px;border-radius:999px;background:var(--paper-2);color:var(--ink-2);letter-spacing:.01em}
.badge.j{background:var(--accent-soft);color:var(--accent)}.badge.f{background:var(--sage-soft);color:var(--sage)}.badge.aw{background:var(--gold-soft);color:var(--gold)}.badge.acc{background:var(--plum-soft);color:var(--plum)}
.acts{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
.acts .tg,.acts a{font:inherit;font-size:13px;font-weight:600;text-decoration:none;padding:5px 13px;border-radius:999px;border:1px solid var(--line-2);background:transparent;color:var(--ink-2);cursor:pointer;line-height:1.5}
.acts .tg:hover,.acts a:hover{border-color:var(--accent);color:var(--accent)}.acts .tg[aria-expanded="true"]{background:var(--ink);border-color:var(--ink);color:var(--paper)}
.acts .panel{flex-basis:100%;margin-top:6px;padding:18px 20px;background:var(--card);border:1px solid var(--line);border-radius:14px;font-size:15px;color:var(--ink-2);line-height:1.7}.acts .panel[hidden]{display:none}
.panel pre{margin:0;white-space:pre-wrap;font:12.5px/1.65 var(--mono)}.copy{float:right;font:inherit;font-size:12px;border:1px solid var(--line-2);background:var(--paper);color:var(--ink-2);border-radius:999px;padding:3px 10px;cursor:pointer}
.kw{display:flex;flex-wrap:wrap;gap:6px}.kw span{font-size:13px;padding:3px 11px;border-radius:999px;background:var(--paper-2)}
.pub.hide{display:none}[role="tabpanel"][hidden]{display:none}
.tabs{display:flex;flex-wrap:wrap;gap:6px;margin:34px 0 10px;padding:5px;background:var(--paper-2);border-radius:999px;width:max-content;max-width:100%}
.tabs button{appearance:none;border:0;background:none;font:inherit;font-size:14.5px;font-weight:600;color:var(--muted);padding:8px 16px;border-radius:999px;cursor:pointer}
.tabs button[aria-selected="true"]{background:var(--card);color:var(--ink);box-shadow:var(--shadow)}.tabs .cnt{font-weight:500;font-size:12px;margin-left:6px;color:var(--muted)}
.seg{display:inline-flex;gap:4px;margin:8px 0 4px;font-size:13.5px}
.seg button{border:0;background:none;font:inherit;color:var(--muted);cursor:pointer;padding:4px 10px;border-radius:999px}.seg button[aria-pressed="true"]{color:var(--accent);background:var(--accent-soft);font-weight:600}
table.sum{width:100%;border-collapse:separate;border-spacing:0;font-size:15px;background:var(--card);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;box-shadow:var(--shadow)}
table.sum th,table.sum td{padding:13px 18px;border-bottom:1px solid var(--line);text-align:left}
table.sum th{font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);font-weight:600;background:var(--paper-2)}
table.sum td.num,table.sum th.num{text-align:center;width:96px;font-variant-numeric:tabular-nums}table.sum td.num{font-family:var(--serif);font-size:19px}
table.sum tr:last-child td{border-bottom:0;font-weight:700}table.sum .full{color:var(--muted);font-size:13.5px;display:block}
/* academics layout */
.acad{display:grid;grid-template-columns:220px minmax(0,1fr);gap:56px;padding-top:8px}
.toc{position:sticky;top:100px;align-self:start;padding-top:72px}
.toc .me{display:flex;align-items:center;gap:12px;margin-bottom:26px}.toc .me img{width:52px;height:52px;border-radius:50%;object-fit:cover;object-position:50% 25%}
.toc .me b{font-family:var(--serif);font-weight:500;font-size:17px;display:block;line-height:1.2}.toc .me span{font-size:12.5px;color:var(--muted)}
.toc ol{list-style:none;margin:0;padding:0;border-left:1px solid var(--line)}
.toc a{display:block;text-decoration:none;font-size:14.5px;color:var(--muted);padding:7px 0 7px 16px;margin-left:-1px;border-left:2px solid transparent}
.toc a:hover{color:var(--ink)}.toc a.on{color:var(--ink);border-left-color:var(--accent);font-weight:600}
.page-head{padding:56px 0 0}.page-head h1{font-size:clamp(44px,6vw,72px);font-weight:400;letter-spacing:-.035em;line-height:1;margin-top:12px}
.page-head p{font-family:var(--serif);font-style:italic;color:var(--ink-2);font-size:21px;margin:16px 0 0;max-width:40ch}
/* education */
.edu{display:grid;grid-template-columns:58px minmax(0,1fr) auto;gap:20px;align-items:start;padding:22px 0;border-top:1px solid var(--line)}.edu:first-child{border-top:0}
.edu h4{font-size:21px;line-height:1.3}.edu .where{font-size:15px;color:var(--ink-2);margin-top:3px}.edu .where a{font-weight:600}.edu .adv{font-size:14px;color:var(--muted);margin-top:2px}
.edu .when{font-size:13.5px;color:var(--muted);font-variant-numeric:tabular-nums;white-space:nowrap;padding-top:4px}
/* awards */
.awg{margin-bottom:34px}.awg h3{font-size:14px;font-family:var(--sans);font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:6px}
.aw{list-style:none;margin:0;padding:0}.aw li{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;padding:14px 0;border-top:1px solid var(--line)}
.aw .t{font-family:var(--serif);font-size:18.5px;font-weight:500}.aw .who{font-size:14px;color:var(--muted);margin-top:1px}
.aw .chip{display:inline-block;margin-left:8px;font-family:var(--sans);font-size:11.5px;font-weight:600;padding:2px 9px;border-radius:999px;vertical-align:3px;background:var(--sage-soft);color:var(--sage)}.aw .chip.pi{background:var(--gold-soft);color:var(--gold)}
.aw .d{font-size:13.5px;color:var(--muted);white-space:nowrap;font-variant-numeric:tabular-nums;padding-top:4px}
/* projects */
.proj{display:grid;grid-template-columns:58px minmax(0,1fr);gap:20px;padding:24px;margin-bottom:14px;background:var(--card);border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--shadow)}
.proj .when{font-size:13px;color:var(--muted);font-variant-numeric:tabular-nums}.proj h4{font-size:21px;line-height:1.35;margin:4px 0 6px}
.proj .org{font-size:14.5px;color:var(--ink-2)}.proj ul{margin:12px 0 0;padding-left:18px;color:var(--ink-2);font-size:15px}.proj li{margin:4px 0}
.plain{margin:0;padding:0;list-style:none}.plain li{padding:12px 0;border-top:1px solid var(--line);color:var(--ink-2)}.plain li:first-child{border-top:0}
.plain b{color:var(--ink);font-weight:600}
.skills{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
.skill{padding:18px 20px;background:var(--card);border:1px solid var(--line);border-radius:16px}.skill b{display:block;font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin-bottom:4px}
/* contact */
.contact{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:48px;align-items:start;margin-top:40px}
.cbox{background:var(--card);border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--shadow);padding:10px 28px}
.cbox dl{margin:0}.cbox .row{display:grid;grid-template-columns:120px minmax(0,1fr);gap:16px;padding:18px 0;border-top:1px solid var(--line)}.cbox .row:first-child{border-top:0}
.cbox dt{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-weight:600;padding-top:4px}.cbox dd{margin:0}
.cbox .big{font-family:var(--serif);font-size:24px}
footer{margin-top:96px;border-top:1px solid var(--line)}footer .wrap{display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px 24px;padding:28px;color:var(--muted);font-size:13.5px}
footer a{color:var(--muted)}
@media (max-width:980px){.hero{grid-template-columns:1fr;gap:36px}.portrait{justify-self:start;max-width:300px}.acad{grid-template-columns:1fr;gap:0}.toc{display:none}
.glance{grid-template-columns:repeat(3,minmax(0,1fr))}.g:nth-child(4){border-left:0}.g:nth-child(n+4){border-top:1px solid var(--line)}.contact{grid-template-columns:1fr}}
@media (max-width:680px){.wrap{padding:0 18px}body{font-size:16px}.themes,.skills{grid-template-columns:1fr}.glance{grid-template-columns:repeat(2,minmax(0,1fr))}
.g{border-left:0!important;border-top:1px solid var(--line)}.g:nth-child(-n+2){border-top:0}.g:nth-child(even){border-left:1px solid var(--line)!important}
.news li{grid-template-columns:1fr;gap:2px}.pub{grid-template-columns:1fr}.pub .idx{display:none}.edu{grid-template-columns:46px minmax(0,1fr)}.edu .when{grid-column:2;padding:0}
.logo.lg,.mono{width:46px;height:46px}.proj{grid-template-columns:1fr;padding:20px}.cbox .row{grid-template-columns:1fr;gap:2px}
nav.main a{padding:8px 10px;font-size:14px}.brand{font-size:18px}.sec{padding-top:56px}.sec-h h2{font-size:28px}.tabs{width:100%;border-radius:16px}}
@media print{header.top,.toc,.tabs,.seg,.acts,.theme,footer{display:none!important}[role="tabpanel"][hidden],.pub.hide{display:block!important}}
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
         "<link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..700&amp;family=Noto+Serif+KR:wght@400;500&amp;display=swap'>"
         "<link rel='stylesheet' href='https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css'>")

def page(fname, title, desc, body, current):
    CUR = ' aria-current="page"'
    nav = "".join(f"<a href='{u}'{CUR if current == u else ''}>{t}</a>" for t, u in [("Home", "index.html"), ("Academics", "academics.html"), ("Contact", "contact.html")])
    url = f"{SITE_URL}/{'' if fname == 'index.html' else fname}"
    same = ",".join('"' + u + '"' for _, u in PROFILE["links"][:3])
    return f"""<!doctype html>
<html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>
<title>{esc(title)}</title><meta name='description' content='{esc(desc)}'><link rel='canonical' href='{url}'>
<meta name='color-scheme' content='light dark'><meta name='theme-color' content='#fbf8f3'>
<meta property='og:type' content='website'><meta property='og:title' content='{esc(title)}'><meta property='og:description' content='{esc(desc)}'>
<meta property='og:url' content='{url}'><meta property='og:image' content='{SITE_URL}/{PROFILE['photo']}'>
<link rel='icon' href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='32' fill='%23a8432b'/%3E%3Ctext x='32' y='43' font-family='Georgia' font-size='30' font-style='italic' fill='white' text-anchor='middle'%3ES%3C/text%3E%3C/svg%3E">
<link rel='alternate' type='text/plain' href='llms-full.txt' title='Full plain-text version'>{FONTS}
<script type='application/ld+json'>{{"@context":"https://schema.org","@type":"Person","name":"{PROFILE['name']}","jobTitle":"{PROFILE['title']}","affiliation":{{"@type":"CollegeOrUniversity","name":"{PROFILE['univ']}"}},"url":"{SITE_URL}","sameAs":[{same}]}}</script>
<style>{CSS}</style></head>
<body><a class='skip' href='#main'>Skip to content</a>
<header class='top'><div class='wrap'><a class='brand' href='index.html'>Sangmin <i>Lee</i></a>
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
<p class='tag'>Shaping electromagnetic waves with <em>metasurfaces</em> and <em>antenna arrays</em> — for 6G links and radar.</p>
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
