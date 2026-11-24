# -*- coding: utf-8 -*-
"""Static site generator for sangmin2-rf.github.io  ->  docs/
Usage:  python build.py
"""
import html, os, re, shutil
from data import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
esc = html.escape

# ------------------------------------------------------------------ helpers
def bold_me(authors):
    if "**" in authors:
        return re.sub(r"\*\*(.+?)\*\*", r"<b class='me'>\1</b>", esc(authors).replace("&#x27;", "'"))
    s = esc(authors)
    for n in ["S.-M. Lee", "S. Lee"]:
        if n in s:
            return s.replace(n, f"<b class='me'>{n}</b>", 1)
    return s

def bibkey_entry(p, kind):
    a = p["authors"].replace("**", "").replace("*", "")
    a = " and ".join(x.strip() for x in re.split(r",\s*(?:and\s+)?|\s+and\s+", a) if x.strip())
    lines = [f"@{kind}{{{p['key']},", f"  title     = {{{p['title']}}},", f"  author    = {{{a}}},"]
    if kind == "article":
        lines.append(f"  journal   = {{{JOURNAL_FULL.get(p['jabbr'], p['jabbr'])}}},")
    else:
        lines.append(f"  booktitle = {{{p['venue']}}},")
    lines.append(f"  year      = {{{p['year']}}},")
    if p.get("doi"):
        lines.append(f"  doi       = {{{p['doi']}}},")
    lines.append("}")
    return "\n".join(lines)

def stats():
    j = len(JOURNALS); jf = sum(1 for p in JOURNALS if p["first"])
    aw = sum(len(v) for k, v in AWARDS if k != "Undergraduate Competitions")
    return [(j, "Journal papers", f"{jf} first-author"), (len(INTL_CONF), "Int'l conference papers", "IEEE AP-S/URSI · ISAP"),
            (len(DOMESTIC), "Domestic conference papers", "KIEES and others"), (len(PATENTS), "Korean patents", "1 registered · 1 filed"),
            (aw, "Awards & grants", "since 2020")]

def fmt_date(d):
    y, m, dd = d.split("-")
    mon = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][int(m) - 1]
    return f"{mon} {int(dd)}, {y}" if dd != "01" else f"{mon} {y}"

KIND_LABEL = {"paper": "Paper", "award": "Award", "grant": "Grant", "talk": "Talk", "milestone": "Milestone"}

# ------------------------------------------------------------------ CSS / JS
CSS = r"""
:root{--bg:#f7f7f4;--surface:#ffffff;--ink:#15181e;--ink-2:#2b3039;--muted:#5d6472;--line:#e4e4df;--soft:#f0f0eb;
--accent:#1d4ed8;--accent-ink:#ffffff;--accent-soft:#e7edfc;--gold:#a16207;--gold-soft:#fdf3d7;--teal:#0f766e;--teal-soft:#dcf2ef;
--shadow:0 1px 2px rgba(16,24,40,.04),0 4px 16px rgba(16,24,40,.05);--radius:14px;
--font:"Pretendard Variable",Pretendard,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;
--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0e1014;--surface:#151920;--ink:#e9ecf1;--ink-2:#cdd3dc;--muted:#97a0ae;--line:#262c35;--soft:#1b2029;
--accent:#7aa7ff;--accent-ink:#0e1014;--accent-soft:#1b2a45;--gold:#f0c15c;--gold-soft:#3a2e12;--teal:#5fd1c1;--teal-soft:#123532;--shadow:none}}
:root[data-theme="dark"]{--bg:#0e1014;--surface:#151920;--ink:#e9ecf1;--ink-2:#cdd3dc;--muted:#97a0ae;--line:#262c35;--soft:#1b2029;
--accent:#7aa7ff;--accent-ink:#0e1014;--accent-soft:#1b2a45;--gold:#f0c15c;--gold-soft:#3a2e12;--teal:#5fd1c1;--teal-soft:#123532;--shadow:none}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:84px}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 var(--font);-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline;text-underline-offset:3px}
.skip{position:absolute;left:-999px}.skip:focus{left:16px;top:12px;background:var(--surface);padding:8px 12px;border-radius:8px;z-index:99}
header.top{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--bg) 86%,transparent);backdrop-filter:saturate(1.4) blur(10px);border-bottom:1px solid var(--line)}
.top .in{max-width:1180px;margin:0 auto;padding:0 20px;height:64px;display:flex;align-items:center;gap:20px}
.brand{font-weight:700;color:var(--ink);letter-spacing:-.01em;font-size:17px;white-space:nowrap}.brand span{color:var(--muted);font-weight:500;margin-left:6px;font-size:14px}
nav.main{margin-left:auto;display:flex;gap:4px;align-items:center}
nav.main a{color:var(--muted);padding:8px 12px;border-radius:999px;font-size:15px;font-weight:500}
nav.main a:hover{color:var(--ink);background:var(--soft);text-decoration:none}nav.main a[aria-current="page"]{color:var(--ink);background:var(--soft)}
.theme{border:1px solid var(--line);background:var(--surface);color:var(--muted);width:36px;height:36px;border-radius:999px;cursor:pointer;display:grid;place-items:center}
.theme:hover{color:var(--ink)}
.wrap{max-width:1180px;margin:0 auto;padding:32px 20px 64px;display:grid;grid-template-columns:270px minmax(0,1fr);gap:40px}
aside.side{position:sticky;top:88px;align-self:start}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow)}
.profile{padding:22px}.profile img{width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:10px;display:block;background:var(--soft)}
.profile h2{margin:16px 0 2px;font-size:20px;letter-spacing:-.01em}
.profile.compact{display:grid;grid-template-columns:72px minmax(0,1fr);gap:14px;align-items:center;padding:16px}.profile.compact img{width:72px;height:72px;aspect-ratio:1;object-position:50% 25%;border-radius:50%}
.profile.compact h2{margin:0;font-size:17px}.profile.compact .ko{display:none}.profile.compact .role{font-size:13px}.profile.compact .loc,.profile.compact .links{display:none}.profile .ko{color:var(--muted);font-weight:500;font-size:15px;margin-left:4px}
.profile .role{color:var(--ink-2);font-size:14.5px;line-height:1.5}.profile .loc{color:var(--muted);font-size:13.5px;margin-top:6px}
.links{list-style:none;padding:0;margin:14px 0 0;display:flex;flex-wrap:wrap;gap:6px}
.links a{display:inline-block;font-size:13px;padding:5px 10px;border:1px solid var(--line);border-radius:999px;color:var(--ink-2);background:var(--bg)}
.links a:hover{border-color:var(--accent);color:var(--accent);text-decoration:none}
.toc{margin-top:14px;padding:16px 18px}.toc h3{margin:0 0 8px;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.toc ol{margin:0;padding:0;list-style:none;counter-reset:t}.toc li{counter-increment:t}
.toc a{display:block;padding:5px 8px;border-radius:8px;color:var(--ink-2);font-size:14.5px}
.toc a::before{content:counter(t,decimal-leading-zero);color:var(--muted);font-variant-numeric:tabular-nums;margin-right:10px;font-size:12px}
.toc a:hover{background:var(--soft);text-decoration:none}.toc a.on{background:var(--accent-soft);color:var(--accent)}
main{min-width:0}
.eyebrow{font-size:13px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}
h1.hero{font-size:clamp(30px,4.2vw,44px);line-height:1.12;letter-spacing:-.025em;margin:8px 0 10px}
.lede{font-size:18px;color:var(--ink-2);max-width:62ch}
section.sec{margin-top:44px}section.sec>h2{font-size:24px;letter-spacing:-.015em;margin:0 0 6px;display:flex;align-items:baseline;gap:10px}
section.sec>h2 .n{font-size:13px;color:var(--muted);font-weight:600;font-variant-numeric:tabular-nums}
.sub{color:var(--muted);margin:0 0 18px;font-size:14.5px}
h3.grp{font-size:15px;margin:26px 0 10px;color:var(--ink-2);letter-spacing:.01em}
.prose p{margin:0 0 14px;max-width:70ch}
.interests{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin-top:8px}
.int{padding:16px 18px;display:flex;gap:14px;align-items:flex-start}.int .no{font-variant-numeric:tabular-nums;color:var(--accent);font-weight:700;font-size:14px;padding-top:2px}
.int b{display:block;font-size:15.5px;line-height:1.4}
.stats{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}
.stat{padding:16px}.stat .v{font-size:28px;font-weight:700;letter-spacing:-.02em;font-variant-numeric:tabular-nums}.stat .l{font-size:13.5px;color:var(--ink-2);line-height:1.35}.stat .s{font-size:12px;color:var(--muted);margin-top:4px}
.news{list-style:none;margin:0;padding:0}.news li{display:grid;grid-template-columns:120px 84px minmax(0,1fr);gap:12px;padding:12px 0;border-bottom:1px solid var(--line);align-items:baseline}
.news time{color:var(--muted);font-size:13.5px;font-variant-numeric:tabular-nums}
.tag{display:inline-block;font-size:11.5px;font-weight:600;letter-spacing:.03em;padding:2px 8px;border-radius:999px;background:var(--soft);color:var(--ink-2);text-align:center}
.tag.award,.tag.grant{background:var(--gold-soft);color:var(--gold)}.tag.paper{background:var(--accent-soft);color:var(--accent)}.tag.talk{background:var(--teal-soft);color:var(--teal)}
details.more{margin-top:8px}details.more>summary{cursor:pointer;color:var(--accent);font-size:14.5px;padding:8px 0;list-style:none}
details.more>summary::-webkit-details-marker{display:none}details.more>summary::before{content:"+ ";font-weight:700}details.more[open]>summary::before{content:"− "}
/* education */
.tl{position:relative;padding-left:22px}.tl::before{content:"";position:absolute;left:6px;top:8px;bottom:8px;width:2px;background:var(--line)}
.tl .item{position:relative;padding:0 0 22px}.tl .item::before{content:"";position:absolute;left:-21px;top:8px;width:12px;height:12px;border-radius:50%;background:var(--surface);border:2px solid var(--accent)}
.tl .when{font-size:13px;color:var(--muted);font-variant-numeric:tabular-nums}.tl h4{margin:2px 0;font-size:16.5px}.tl .where{font-size:14.5px;color:var(--ink-2)}.tl .adv{font-size:14px;color:var(--muted)}
.gen{padding:18px;margin-top:8px}.gen svg{width:100%;max-width:400px;height:auto;display:block;margin:0 auto}.gen .cap{font-size:13px;color:var(--muted);margin-top:8px}
/* publications */
table.sum{width:100%;border-collapse:collapse;font-size:14.5px;background:var(--surface);border:1px solid var(--line);border-radius:12px;overflow:hidden}
table.sum th,table.sum td{padding:10px 14px;border-bottom:1px solid var(--line);text-align:left}table.sum th{font-size:12.5px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);background:var(--soft)}
table.sum td.num,table.sum th.num{text-align:center;font-variant-numeric:tabular-nums;width:90px}table.sum tr:last-child td{border-bottom:0;font-weight:700}
.tabs{display:flex;flex-wrap:wrap;gap:6px;margin:22px 0 14px;border-bottom:1px solid var(--line)}
.tabs button{appearance:none;border:0;background:none;color:var(--muted);font:inherit;font-size:15px;font-weight:600;padding:10px 12px;cursor:pointer;border-bottom:2px solid transparent;margin-bottom:-1px}
.tabs button[aria-selected="true"]{color:var(--ink);border-bottom-color:var(--accent)}.tabs .cnt{font-weight:500;color:var(--muted);font-size:12.5px;margin-left:4px}
.seg{display:inline-flex;border:1px solid var(--line);border-radius:999px;padding:3px;background:var(--surface);margin-bottom:10px}
.seg button{border:0;background:none;font:inherit;font-size:13.5px;padding:5px 12px;border-radius:999px;color:var(--muted);cursor:pointer}.seg button[aria-pressed="true"]{background:var(--ink);color:var(--bg)}
ol.pubs{list-style:none;margin:0;padding:0}.pub{display:grid;grid-template-columns:44px minmax(0,1fr);gap:8px;padding:16px 0;border-bottom:1px solid var(--line)}
.pub .idx{color:var(--muted);font-variant-numeric:tabular-nums;font-size:14px;padding-top:2px}
.pub .ttl{font-weight:650;font-size:16px;line-height:1.45;color:var(--ink)}.pub .au{font-size:14.5px;color:var(--ink-2);margin-top:3px}.pub .au b.me{color:var(--ink);text-decoration:underline;text-decoration-color:var(--accent);text-underline-offset:3px}
.pub .ve{font-size:14px;color:var(--muted);font-style:italic;margin-top:2px}.pub .pl{font-size:13.5px;color:var(--muted)}
.badges{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}.badge{font-size:12px;font-weight:600;padding:3px 9px;border-radius:999px;background:var(--soft);color:var(--ink-2)}
.badge.j{background:var(--accent-soft);color:var(--accent)}.badge.aw{background:var(--gold-soft);color:var(--gold)}.badge.f{background:var(--teal-soft);color:var(--teal)}
.acts{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}.acts a,.acts .tg{font:inherit;font-size:13px;font-weight:600;padding:4px 11px;border:1px solid var(--line);border-radius:8px;color:var(--ink-2);background:var(--surface);cursor:pointer;line-height:1.5}
.acts a:hover,.acts .tg:hover{border-color:var(--accent);color:var(--accent);text-decoration:none}
.acts .tg[aria-expanded="true"]{background:var(--accent-soft);border-color:var(--accent);color:var(--accent)}
.acts .panel{flex-basis:100%;margin-top:6px;padding:14px 16px;background:var(--soft);border-radius:10px;font-size:14.5px;color:var(--ink-2)}.acts .panel[hidden]{display:none}
.panel pre{margin:0;white-space:pre-wrap;font:12.5px/1.6 var(--mono)}.copy{float:right;font:inherit;font-size:12px;border:1px solid var(--line);background:var(--surface);color:var(--ink-2);border-radius:6px;padding:2px 8px;cursor:pointer}
.kw{display:flex;flex-wrap:wrap;gap:6px}.kw span{font-size:12.5px;padding:2px 9px;border-radius:999px;background:var(--surface);border:1px solid var(--line)}
.pub.hide{display:none}[role="tabpanel"][hidden]{display:none}
/* awards */
ul.aw{list-style:none;margin:0;padding:0}.aw li{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:12px;padding:11px 0;border-bottom:1px solid var(--line)}
.aw .t{font-weight:650}.aw .note{font-size:12px;font-weight:600;color:var(--gold);background:var(--gold-soft);padding:1px 8px;border-radius:999px;margin-left:6px}
.aw .who{font-size:14px;color:var(--muted)}.aw .d{font-size:13.5px;color:var(--muted);white-space:nowrap;font-variant-numeric:tabular-nums}
/* projects */
.proj{padding:18px 20px;margin-bottom:12px}.proj .when{font-size:13px;color:var(--muted);font-variant-numeric:tabular-nums}.proj h4{margin:4px 0 4px;font-size:16.5px;line-height:1.4}
.proj .org{font-size:14px;color:var(--ink-2)}.proj .role{display:inline-block;margin-top:6px}.proj ul{margin:10px 0 0;padding-left:18px;color:var(--ink-2);font-size:14.5px}
ul.plain{margin:0;padding-left:18px}ul.plain li{margin:4px 0}
.chips{display:flex;flex-wrap:wrap;gap:8px}.chips span{padding:6px 12px;border:1px solid var(--line);border-radius:999px;background:var(--surface);font-size:14px}
.skills{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.skills .card{padding:14px 16px}.skills b{display:block;font-size:13px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}
.contact{padding:24px}.contact dl{display:grid;grid-template-columns:140px minmax(0,1fr);gap:12px 18px;margin:0}.contact dt{color:var(--muted);font-size:14px}.contact dd{margin:0}
footer{border-top:1px solid var(--line);color:var(--muted);font-size:13.5px}footer .in{max-width:1180px;margin:0 auto;padding:20px;display:flex;flex-wrap:wrap;gap:8px 20px;justify-content:space-between}
@media (max-width:960px){.wrap{grid-template-columns:1fr;gap:24px}aside.side{position:static}.profile{display:grid;grid-template-columns:110px minmax(0,1fr);gap:16px;align-items:start}.profile h2{margin-top:0}
.toc{display:none}.stats{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (max-width:640px){.interests,.skills{grid-template-columns:1fr}.stats{grid-template-columns:repeat(2,minmax(0,1fr))}.news li{grid-template-columns:1fr;gap:2px}
.pub{grid-template-columns:1fr}.pub .idx{display:none}.brand span{display:none}nav.main a{padding:8px 9px}.contact dl{grid-template-columns:1fr;gap:2px}.contact dd{margin-bottom:10px}}
@media print{header.top,aside.side,.tabs,.seg,.acts,footer,.theme{display:none!important}.wrap{display:block}[role="tabpanel"][hidden]{display:block!important}.pub.hide{display:block!important}}
"""

JS = r"""
(function(){var r=document.documentElement,k='sm-theme';try{var s=localStorage.getItem(k);if(s)r.setAttribute('data-theme',s)}catch(e){}
var b=document.querySelector('.theme');if(b)b.addEventListener('click',function(){var d=r.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');var n=d==='dark'?'light':'dark';r.setAttribute('data-theme',n);try{localStorage.setItem(k,n)}catch(e){}});
document.querySelectorAll('[data-mail]').forEach(function(a){var u=a.getAttribute('data-u'),d=a.getAttribute('data-d');a.href='mailto:'+u+'@'+d;a.textContent=u+'@'+d});
document.querySelectorAll('.tabs').forEach(function(t){var bs=t.querySelectorAll('button');bs.forEach(function(x){x.addEventListener('click',function(){bs.forEach(function(y){y.setAttribute('aria-selected','false');document.getElementById(y.getAttribute('aria-controls')).hidden=true});x.setAttribute('aria-selected','true');document.getElementById(x.getAttribute('aria-controls')).hidden=false})})});
document.querySelectorAll('.seg').forEach(function(s){var bs=s.querySelectorAll('button'),list=document.getElementById(s.getAttribute('data-for'));function apply(sel){list.querySelectorAll('.pub').forEach(function(p){p.classList.toggle('hide',sel&&p.getAttribute('data-sel')!=='1')})}
bs.forEach(function(x){x.addEventListener('click',function(){bs.forEach(function(y){y.setAttribute('aria-pressed','false')});x.setAttribute('aria-pressed','true');apply(x.getAttribute('data-mode')==='sel')})});apply(true)});
document.querySelectorAll('.tg').forEach(function(b){b.addEventListener('click',function(){var p=document.getElementById(b.getAttribute('aria-controls')),o=b.getAttribute('aria-expanded')==='true';b.setAttribute('aria-expanded',o?'false':'true');p.hidden=o})});
document.querySelectorAll('.copy').forEach(function(c){c.addEventListener('click',function(){var t=c.parentNode.querySelector('pre').textContent;(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){c.textContent='Copied'},function(){c.textContent='Select & copy'});setTimeout(function(){c.textContent='Copy'},1600)})});
var toc=document.querySelectorAll('.toc a');if(toc.length&&'IntersectionObserver' in window){var m={};toc.forEach(function(a){m[a.getAttribute('href').slice(1)]=a});
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){toc.forEach(function(a){a.classList.remove('on')});var a=m[e.target.id];if(a)a.classList.add('on')}})},{rootMargin:'-30% 0px -65% 0px'});
document.querySelectorAll('section.sec[id]').forEach(function(s){io.observe(s)})}})();
"""

ICON_MOON = "<svg width='17' height='17' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' aria-hidden='true'><path d='M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z'/></svg>"

# ------------------------------------------------------------------ layout
def page(fname, title, desc, body, current, toc=None):
    CUR = ' aria-current="page"'
    nav = "".join(f"<a href='{u}'{CUR if current == u else ''}>{t}</a>"
                  for t, u in [("Home", "index.html"), ("Academics", "academics.html"), ("Contact", "contact.html")])
    links = "".join(f"<li><a href='{u}' rel='noopener'>{esc(t)}</a></li>" for t, u in PROFILE["links"])
    toc_html = ""
    if toc:
        toc_html = "<nav class='card toc' aria-label='On this page'><h3>On this page</h3><ol>" + \
                   "".join(f"<li><a href='#{i}'>{esc(t)}</a></li>" for i, t in toc) + "</ol></nav>"
    side = f"""<aside class='side'><div class='card profile{' compact' if toc else ''}'><img src='{PROFILE['photo']}' alt='Portrait of {PROFILE['name']}' width='354' height='472'>
<div><h2>{PROFILE['name']}<span class='ko'>{PROFILE['name_ko']}</span></h2>
<div class='role'>{PROFILE['title']}<br>{PROFILE['dept']}<br>{PROFILE['univ']}</div>
<div class='loc'>{PROFILE['lab']} · {PROFILE['location']}</div>
<ul class='links'>{links}</ul></div></div>{toc_html}</aside>"""
    url = f"{SITE_URL}/{'' if fname == 'index.html' else fname}"
    return f"""<!doctype html>
<html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>
<title>{esc(title)}</title><meta name='description' content='{esc(desc)}'><link rel='canonical' href='{url}'>
<meta name='color-scheme' content='light dark'><meta name='theme-color' content='#f7f7f4'>
<meta property='og:type' content='website'><meta property='og:title' content='{esc(title)}'><meta property='og:description' content='{esc(desc)}'>
<meta property='og:url' content='{url}'><meta property='og:image' content='{SITE_URL}/{PROFILE['photo']}'>
<link rel='icon' href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%231d4ed8'/%3E%3Ctext x='32' y='42' font-family='Arial' font-size='28' font-weight='700' fill='white' text-anchor='middle'%3ESL%3C/text%3E%3C/svg%3E">
<link rel='alternate' type='text/plain' href='llms-full.txt' title='Full plain-text version'>
<link rel='stylesheet' href='https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css'>
<script type='application/ld+json'>{{"@context":"https://schema.org","@type":"Person","name":"{PROFILE['name']}","jobTitle":"{PROFILE['title']}","affiliation":{{"@type":"CollegeOrUniversity","name":"{PROFILE['univ']}"}},"url":"{SITE_URL}","sameAs":[{",".join('"'+u+'"' for _,u in PROFILE['links'][:3])}]}}</script>
<style>{CSS}</style></head>
<body><a class='skip' href='#main'>Skip to content</a>
<header class='top'><div class='in'><a class='brand' href='index.html'>{PROFILE['name']}<span>RF · Metasurfaces · Antenna Arrays</span></a>
<nav class='main' aria-label='Primary'>{nav}</nav><button class='theme' type='button' aria-label='Toggle dark mode'>{ICON_MOON}</button></div></header>
<div class='wrap'>{side}<main id='main'>{body}</main></div>
<footer><div class='in'><span>© 2026 {PROFILE['name']} · {PROFILE['lab']}, {PROFILE['univ']}</span><span>Last updated {UPDATED} · <a href='llms-full.txt'>Plain-text version</a></span></div></footer>
<script>{JS}</script></body></html>"""

# ------------------------------------------------------------------ pub renderers
def render_pub(p, idx, kind):
    sel = "1" if p.get("selected") else "0"
    badges = []
    if kind == "j":
        badges.append(f"<span class='badge j'>{esc(p['jabbr'])}</span>")
        if p["first"]:
            badges.append("<span class='badge f'>1st author</span>")
    acts, panels = [], []
    uid = f"{p['key']}-{kind}"
    def add(label, inner):
        pid = f"{uid}-{label.lower()}"
        acts.append(f"<button type='button' class='tg' aria-expanded='false' aria-controls='{pid}'>{label}</button>")
        panels.append(f"<div class='panel' id='{pid}' hidden>{inner}</div>")
    if p.get("abstract"):
        add("Abstract", esc(p["abstract"]))
    if p.get("keywords"):
        add("Keywords", "<div class='kw'>" + "".join(f"<span>{esc(k)}</span>" for k in p["keywords"]) + "</div>")
    add("BibTeX", f"<button class='copy' type='button'>Copy</button><pre>{esc(bibkey_entry(p, 'article' if kind == 'j' else 'inproceedings'))}</pre>")
    if p.get("doi"):
        acts.append(f"<a href='https://doi.org/{p['doi']}' rel='noopener'>DOI</a>")
    acts = acts + panels
    place = f"<div class='pl'>{esc(p['place'])}</div>" if p.get("place") else ""
    return f"""<li class='pub' data-sel='{sel}'><div class='idx'>[{idx}]</div><div>
<div class='ttl'>{esc(p['title'])}</div><div class='au'>{bold_me(p['authors'])}</div><div class='ve'>{esc(p['venue'])}</div>{place}
<div class='badges'>{''.join(badges)}</div><div class='acts'>{''.join(acts)}</div></div></li>"""

def journal_table():
    rows = {}
    for p in JOURNALS:
        r = rows.setdefault(p["jabbr"], [0, 0]); r[0 if p["first"] else 1] += 1
    rank = list(JOURNAL_FULL.keys())
    order = sorted(rows.items(), key=lambda kv: rank.index(kv[0]) if kv[0] in rank else 99)
    body = "".join(f"<tr><td>{esc(k)} <span style='color:var(--muted)'>· {esc(JOURNAL_FULL[k])}</span></td><td class='num'>{v[0] or '–'}</td><td class='num'>{v[1] or '–'}</td><td class='num'>{sum(v)}</td></tr>" for k, v in order)
    f = sum(v[0] for v in rows.values()); c = sum(v[1] for v in rows.values())
    return f"<table class='sum'><thead><tr><th>Journal</th><th class='num'>1st author</th><th class='num'>Co-author</th><th class='num'>Total</th></tr></thead><tbody>{body}<tr><td>Total</td><td class='num'>{f}</td><td class='num'>{c}</td><td class='num'>{f + c}</td></tr></tbody></table>"

def genealogy_svg():
    W, bh, gap = 520, 58, 26
    H = len(GENEALOGY) * bh + (len(GENEALOGY) - 1) * gap
    parts = [f"<svg viewBox='0 0 {W} {H}' role='img' aria-label='Academic genealogy: " + " → ".join(n for n, _ in GENEALOGY) + "'>"]
    for i, (n, sub) in enumerate(GENEALOGY):
        y = i * (bh + gap); me = i == len(GENEALOGY) - 1
        fill = "var(--accent-soft)" if me else "var(--surface)"; stroke = "var(--accent)" if me else "var(--line)"
        parts.append(f"<rect x='80' y='{y}' width='{W-160}' height='{bh}' rx='12' fill='{fill}' stroke='{stroke}' stroke-width='1.5'/>")
        parts.append(f"<text x='{W/2}' y='{y+25}' text-anchor='middle' font-size='16' font-weight='700' fill='var(--ink)' font-family='inherit'>{esc(n)}</text>")
        parts.append(f"<text x='{W/2}' y='{y+45}' text-anchor='middle' font-size='12.5' fill='var(--muted)' font-family='inherit'>{esc(sub)}</text>")
        if i < len(GENEALOGY) - 1:
            y2 = y + bh
            parts.append(f"<line x1='{W/2}' y1='{y2+3}' x2='{W/2}' y2='{y2+gap-6}' stroke='var(--muted)' stroke-width='1.5'/>")
            parts.append(f"<path d='M{W/2-5} {y2+gap-11} L{W/2} {y2+gap-4} L{W/2+5} {y2+gap-11}' fill='none' stroke='var(--muted)' stroke-width='1.5'/>")
    parts.append("</svg>")
    return "".join(parts)

# ------------------------------------------------------------------ pages
def build_home():
    interests = "".join(f"<div class='card int'><span class='no'>{i+1:02d}</span><b>{esc(t)}</b></div>" for i, (t, _) in enumerate(INTERESTS))
    st = "".join(f"<div class='card stat'><div class='v'>{v}</div><div class='l'>{esc(l)}</div><div class='s'>{esc(s)}</div></div>" for v, l, s in stats())
    def news_li(n):
        d, k, t = n
        return f"<li><time datetime='{d}'>{fmt_date(d)}</time><span class='tag {k}'>{KIND_LABEL[k]}</span><span>{t}</span></li>"
    news = "".join(news_li(n) for n in NEWS[:7])
    older = "".join(news_li(n) for n in NEWS[7:])
    sel = [p for p in JOURNALS if p["selected"]]
    sel_html = "".join(render_pub(p, i + 1, "j") for i, p in enumerate(sel))
    body = f"""<p class='eyebrow'>Ph.D. Student · Kyungpook National University</p>
<h1 class='hero'>Wave control with metasurfaces and antenna arrays for 6G and radar.</h1>
<section class='sec' id='about' style='margin-top:20px'><div class='prose'>{''.join(f'<p>{p}</p>' for p in ABOUT)}</div></section>
<section class='sec' id='interests'><h2>Research Interests</h2><div class='interests'>{interests}</div></section>
<section class='sec' id='glance'><h2>At a Glance</h2><p class='sub'>Counts as of {UPDATED}. Full record on the <a href='academics.html'>Academics</a> page.</p><div class='stats'>{st}</div></section>
<section class='sec' id='news'><h2>Recent News</h2><ul class='news'>{news}</ul>
<details class='more'><summary>Earlier news ({len(NEWS)-7})</summary><ul class='news'>{older}</ul></details></section>
<section class='sec' id='selected'><h2>Selected Publications</h2><p class='sub'>Underlined name = me · * corresponding author</p><ol class='pubs'>{sel_html}</ol>
<p style='margin-top:14px'><a href='academics.html#publications'>All publications →</a></p></section>"""
    return page("index.html", f"{PROFILE['name']} — Ph.D. Student, KNU",
                "Sangmin Lee, Ph.D. student at Kyungpook National University (PLAYWAVE Lab). Reconfigurable intelligent surfaces, Huygens' metasurfaces, series-fed and phased arrays for 6G and radar.",
                body, "index.html")

def build_academics():
    toc = [("education", "Education"), ("publications", "Publications"), ("awards", "Awards & Honors"), ("research", "Research Projects"),
           ("service", "Academic Service"), ("mentoring", "Mentoring & Collaborators"), ("coursework", "Coursework & Skills")]
    edu = "".join(f"""<div class='item'><div class='when'>{e['period']}</div><h4>{esc(e['degree'])}</h4>
<div class='where'><a href='{e['url']}' rel='noopener'>{esc(e['school'])}</a> · {esc(e['place'])}</div>
{f"<div class='adv'>Advisor: <a href='{e['advisor'][1]}' rel='noopener'>Prof. {esc(e['advisor'][0])}</a></div>" if e['advisor'] else ''}</div>""" for e in EDUCATION)
    gen = f"<details class='more'><summary>Academic genealogy</summary><div class='card gen'>{genealogy_svg()}<div class='cap'>Doctoral lineage via the Radiation Laboratory, University of Michigan.</div></div></details>"

    j_html = "".join(render_pub(p, len(JOURNALS) - i, "j") for i, p in enumerate(JOURNALS))
    c_html = "".join(render_pub(p, len(INTL_CONF) - i, "c") for i, p in enumerate(INTL_CONF))
    d_items = []
    for i, (y, m, au, t, conf, note, aw) in enumerate(DOMESTIC):
        b = "".join([f"<span class='badge aw'>{esc(aw)}</span>" if aw else "", f"<span class='badge'>{esc(note)}</span>" if note else ""])
        d_items.append(f"<li class='pub'><div class='idx'>[{len(DOMESTIC)-i}]</div><div><div class='ttl'>{esc(t)}</div><div class='au'>{bold_me(au)}</div><div class='ve'>{esc(conf)}, {m} {y}</div>{'<div class=badges>'+b+'</div>' if b else ''}</div></li>")
    p_items = "".join(f"""<li class='pub'><div class='idx'>[{len(PATENTS)-i}]</div><div><div class='ttl'>{esc(p['title'])}</div><div class='au'>Inventors: {bold_me(p['inventors'])}</div>
<div class='ve'>{p['country']} · {'Patent No.' if p['status']=='Registered' else 'Application No.'} {p['number']} · {p['status']} {p['date']}</div>
<div class='badges'><span class='badge {'f' if p['status']=='Registered' else ''}'>{p['status']}</span></div>
{f"<div class='acts'><a href='{p['url']}' rel='noopener'>Google Patents</a></div>" if p['url'] else ''}</div></li>""" for i, p in enumerate(PATENTS))
    tabs = [("tab-j", "Journals", len(JOURNALS)), ("tab-c", "Int'l Conferences", len(INTL_CONF)), ("tab-d", "Domestic Conferences", len(DOMESTIC)), ("tab-p", "Patents", len(PATENTS))]
    tabbar = "<div class='tabs' role='tablist'>" + "".join(f"<button type='button' role='tab' aria-selected='{'true' if i==0 else 'false'}' aria-controls='{t}'>{n}<span class='cnt'>{c}</span></button>" for i, (t, n, c) in enumerate(tabs)) + "</div>"
    pubs = f"""{journal_table()}<p class='sub' style='margin-top:8px'>Published journal papers. Underlined name = me · * corresponding author.</p>{tabbar}
<div id='tab-j' role='tabpanel'><div class='seg' data-for='list-j'><button type='button' data-mode='sel' aria-pressed='true'>Selected</button><button type='button' data-mode='all' aria-pressed='false'>All</button></div><ol class='pubs' id='list-j'>{j_html}</ol></div>
<div id='tab-c' role='tabpanel' hidden><ol class='pubs'>{c_html}</ol></div>
<div id='tab-d' role='tabpanel' hidden><ol class='pubs'>{''.join(d_items)}</ol></div>
<div id='tab-p' role='tabpanel' hidden><ol class='pubs'>{p_items}</ol></div>"""

    def aw_group(name, items, collapsed=False):
        lis = "".join(f"<li><div><span class='t'>{esc(t)}</span>{'<span class=note>1st author</span>' if own and name.startswith(('Conference','Institutional')) else ''}{'<span class=note>PI</span>' if 'Principal' in extra else ''}<div class='who'>{esc(org)}{' · '+esc(extra) if extra and 'Principal' not in extra else ''}{' · No. RS-2026-25552947' if 'Principal' in extra else ''}</div></div><div class='d'>{esc(d)}</div></li>" for t, extra, org, d, own in items)
        if collapsed:
            return f"<details class='more'><summary>{esc(name)} ({len(items)})</summary><ul class='aw'>{lis}</ul></details>"
        return f"<h3 class='grp'>{esc(name)}</h3><ul class='aw'>{lis}</ul>"
    awards = "".join(aw_group(n, it, n == "Undergraduate Competitions") for n, it in AWARDS)

    projs = "".join(f"""<div class='card proj'><div class='when'>{esc(p['period'])}</div><h4>{esc(p['title'])}</h4>
<div class='org'>{esc(p['org'])} · No. {esc(p['no'])}</div><span class='badge {'aw' if p['role']=='Principal Investigator' else ''} role'>{esc(p['role'])}</span>
<ul>{''.join(f'<li>{esc(b)}</li>' for b in p['bullets'])}</ul></div>""" for p in PROJECTS)
    service = "".join(f"<h3 class='grp'>{esc(h)}</h3><ul class='plain'>{''.join(f'<li>{esc(x)}</li>' for x in xs)}</ul>" for h, xs in SERVICE)
    mentoring = "".join(f"<h3 class='grp'>{esc(h)}</h3><ul class='plain'>{''.join(f'<li>{x}</li>' for x in xs)}</ul>" for h, xs in MENTORING)
    course = "<h3 class='grp'>Graduate coursework (KNU)</h3><div class='chips'>" + "".join(f"<span>{esc(c)}</span>" for c in COURSEWORK) + "</div>"
    skills = "<h3 class='grp'>Tools & Skills</h3><div class='skills'>" + "".join(f"<div class='card'><b>{esc(a)}</b>{esc(b)}</div>" for a, b in SKILLS) + "</div>"

    def sec(i, sid, title, sub, inner):
        return f"<section class='sec' id='{sid}'><h2><span class='n'>{i:02d}</span>{title}</h2>{f'<p class=sub>{sub}</p>' if sub else ''}{inner}</section>"
    body = "<p class='eyebrow'>Academic record</p><h1 class='hero'>Academics</h1><p class='lede'>Education, publications, awards, research projects, service, and coursework.</p>" + \
        sec(1, "education", "Education", "", f"<div class='tl'>{edu}</div>{gen}") + \
        sec(2, "publications", "Publications", "", pubs) + \
        sec(3, "awards", "Awards &amp; Honors", "", awards) + \
        sec(4, "research", "Research Projects", "Government-funded projects.", projs) + \
        sec(5, "service", "Academic Service", "", service) + \
        sec(6, "mentoring", "Mentoring &amp; Collaborators", "", mentoring) + \
        sec(7, "coursework", "Coursework &amp; Skills", "", course + skills)
    return page("academics.html", f"Academics — {PROFILE['name']}",
                "Education, publications (journals, conferences, patents), awards, research projects, academic service, mentoring, and coursework of Sangmin Lee.",
                body, "academics.html", toc)

def build_contact():
    links = "".join(f"<li><a href='{u}' rel='noopener'>{esc(t)}</a></li>" for t, u in PROFILE["links"])
    body = f"""<p class='eyebrow'>Get in touch</p><h1 class='hero'>Contact</h1>
<p class='lede'>For research collaboration or inquiries, email is the best way to reach me.</p>
<div class='card contact' style='margin-top:24px'><dl>
<dt>Email</dt><dd><a data-mail data-u='{PROFILE['email_user']}' data-d='{PROFILE['email_domain']}' href='#'>{PROFILE['email_user']} [at] {PROFILE['email_domain']}</a></dd>
<dt>Lab</dt><dd><a href='{PROFILE['lab_url']}' rel='noopener'>{PROFILE['lab']}</a> (Prof. Sangjo Choi)</dd>
<dt>Affiliation</dt><dd>{PROFILE['dept']}, {PROFILE['univ']}</dd>
<dt>Office</dt><dd>{PROFILE['office']}</dd>
<dt>Profiles</dt><dd><ul class='links'>{links}</ul></dd></dl></div>"""
    return page("contact.html", f"Contact — {PROFILE['name']}", "Contact information for Sangmin Lee, Kyungpook National University.", body, "contact.html")

def plain_text():
    L = [f"# {PROFILE['name']} ({PROFILE['name_ko']})", f"{PROFILE['title']}, {PROFILE['dept']}, {PROFILE['univ']}", f"Lab: {PROFILE['lab']} ({PROFILE['lab_url']})", f"Site: {SITE_URL}", ""]
    L += ["## About"] + [re.sub("<[^>]+>", "", html.unescape(p)) for p in ABOUT] + ["", "## Research interests"] + [f"- {t}" for t, _ in INTERESTS]
    L += ["", "## Education"] + [f"- {e['period']}: {e['degree']}, {e['school']}" + (f" (advisor: Prof. {e['advisor'][0]})" if e['advisor'] else "") for e in EDUCATION]
    L += ["", "## Journal papers"] + [f"- {p['authors'].replace('**','')}, \"{p['title']},\" {p['venue']}. doi:{p['doi']}" for p in JOURNALS]
    L += ["", "## International conference papers"] + [f"- {p['authors']}, \"{p['title']},\" {p['venue']}, {p['place']}." for p in INTL_CONF]
    L += ["", "## Domestic conference papers"] + [f"- {a.replace('**','')}, \"{t},\" {c}, {m} {y}." + (f" [{aw}]" if aw else "") for y, m, a, t, c, n, aw in DOMESTIC]
    L += ["", "## Patents"] + [f"- {p['title']} ({p['country']} {p['status']} {p['number']}, {p['date']}); inventors: {p['inventors']}" for p in PATENTS]
    L += ["", "## Awards & honors"]
    for n, it in AWARDS:
        L += [f"### {n}"] + [f"- {t}{' ('+x+')' if x else ''}, {o}, {d}" for t, x, o, d, _ in it]
    L += ["", "## Research projects"] + [f"- {p['period']}: {p['title']} — {p['org']}, No. {p['no']} ({p['role']})" for p in PROJECTS]
    L += ["", "## Coursework"] + [f"- {c}" for c in COURSEWORK]
    L += ["", f"Contact: {PROFILE['email_user']} [at] {PROFILE['email_domain']}", f"Last updated: {UPDATED}"]
    return "\n".join(L) + "\n"

def main():
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    files = {"index.html": build_home(), "academics.html": build_academics(), "contact.html": build_contact(),
             "llms-full.txt": plain_text(),
             "llms.txt": f"# {PROFILE['name']}\n> {PROFILE['title']}, {PROFILE['univ']} — RIS, Huygens' metasurfaces, antenna arrays.\n\n- [Home]({SITE_URL}/index.html)\n- [Academics]({SITE_URL}/academics.html)\n- [Contact]({SITE_URL}/contact.html)\n- [Full plain text]({SITE_URL}/llms-full.txt)\n",
             "robots.txt": f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n",
             "sitemap.xml": "<?xml version='1.0' encoding='UTF-8'?>\n<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>" + "".join(f"<url><loc>{SITE_URL}/{p}</loc></url>" for p in ["", "academics.html", "contact.html"]) + "</urlset>\n",
             ".nojekyll": "",
             "404.html": page("404.html", "Not found — Sangmin Lee", "Page not found.", "<h1 class='hero'>Page not found</h1><p class='lede'><a href='index.html'>Back to home →</a></p>", "")}
    for n, c in files.items():
        with open(os.path.join(OUT, n), "w", encoding="utf-8", newline="\n") as f:
            f.write(c)
    print("built:", ", ".join(files))

if __name__ == "__main__":
    main()
