#!/usr/bin/env python3
"""Builds the static pages and the art sprite. Run: python3 build.py  (settings live in config.js, not here)."""
import math, random
from pathlib import Path
OUT = Path(__file__).parent

# ---------- art sprite ----------
def wreath(cx, cy, r, n, lr=8, lw=3.2, a0=18, span=150):
    out = []
    for side in (-1, 1):
        for i in range(n):
            th = math.radians(a0 + i * (span / (n - 1)))
            x, y = cx + side * r * math.sin(th), cy + r * math.cos(th)
            rot = math.degrees(math.atan2(-math.sin(th), side * math.cos(th)))
            for tilt in (-32, 32):
                out.append(f'<ellipse rx="{lr}" ry="{lw}" transform="translate({x:.1f} {y:.1f}) rotate({rot + tilt:.0f}) translate({lr * .8:.1f} 0)"/>')
    return "".join(out)

def splash(seed, n=20, base=58):
    rnd = random.Random(seed); pts = []
    for i in range(n):
        a = 2 * math.pi * i / n + rnd.uniform(-.08, .08)
        r = base * (1 + (rnd.uniform(.25, .7) if i % 2 else -rnd.uniform(.05, .28)))
        pts.append((r * math.cos(a), r * math.sin(a)))
    mid = lambda a, b: ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    m0 = mid(pts[-1], pts[0]); d = f"M{m0[0]:.1f} {m0[1]:.1f}"
    for i, p in enumerate(pts):
        m = mid(p, pts[(i + 1) % n]); d += f"Q{p[0]:.1f} {p[1]:.1f} {m[0]:.1f} {m[1]:.1f}"
    drops = ""
    for _ in range(9):
        a, r = rnd.uniform(0, 6.28), rnd.uniform(78, 98)
        drops += f'<circle cx="{r * math.cos(a):.1f}" cy="{r * math.sin(a):.1f}" r="{rnd.uniform(1.5, 6):.1f}"/>'
    return f'<path d="{d}Z"/>{drops}'

flutes = "".join(f'<rect x="{13 + i * 7}" y="22" width="2.4" height="254" style="fill:var(--m2,#cfc4ad)"/>' for i in range(5))
hair = "".join(f'<circle cx="{62 + i * 9.5:.1f}" cy="{62 - 14 * math.sin(math.pi * i / 8):.1f}" r="11"/>' for i in range(9))
SYMS = {
 "mark": ('0 0 100 100', f'<g fill="currentColor">{wreath(50, 50, 38, 7)}<path d="M41 33v34l28-17z"/></g>'),
 "wreath": ('0 0 100 100', f'<g fill="currentColor">{wreath(50, 50, 40, 8)}</g>'),
 "column": ('0 0 60 300', f'<g style="fill:var(--m1,#f4efe6)"><rect width="60" height="10"/><rect x="5" y="10" width="50" height="9" rx="4"/><rect x="10" y="19" width="40" height="261"/><rect x="5" y="280" width="50" height="8" rx="3"/><rect y="288" width="60" height="12"/></g>{flutes}<rect x="42" y="19" width="8" height="261" style="fill:var(--m2,#cfc4ad)" opacity=".55"/>'),
 "pediment": ('0 0 400 90', '<path d="M0 72 200 2l200 70z" style="fill:var(--m1,#f4efe6)"/><path d="M40 66 200 12l160 54z" style="fill:var(--m2,#cfc4ad)"/><rect y="72" width="400" height="8" style="fill:var(--m1,#f4efe6)"/><rect y="80" width="400" height="10" style="fill:var(--m2,#cfc4ad)"/><circle cx="200" cy="46" r="11" style="fill:var(--m1,#f4efe6)"/>'),
 "bust": ('0 0 200 260', f'<g style="fill:var(--m1,#f7f3eb)"><rect x="52" y="226" width="96" height="34" rx="2"/><path d="M26 228q8-58 54-62h40q46 4 54 62z"/><rect x="83" y="128" width="34" height="46"/><ellipse cx="100" cy="94" rx="39" ry="49"/>{hair}<circle cx="60" cy="96" r="8"/><circle cx="140" cy="96" r="8"/></g><g style="fill:var(--m2,#d5cab4)" opacity=".45"><path d="M100 45a39 49 0 0 1 0 98z"/><rect x="100" y="128" width="17" height="40"/><path d="M100 166h20q46 4 54 62h-74z"/><rect x="100" y="226" width="48" height="34"/></g><path d="M100 96l-6 20h11" fill="none" stroke="#b9ad96" stroke-width="2.5" stroke-linecap="round"/><path d="M88 127q12 5 24 0" fill="none" stroke="#b9ad96" stroke-width="2.5" stroke-linecap="round"/><g fill="#c29a45">{wreath(100, 84, 43, 4, 9, 3.4, 100, 62)}</g><g><rect x="60" y="82" width="36" height="20" rx="7" fill="#16121b"/><rect x="104" y="82" width="36" height="20" rx="7" fill="#16121b"/><rect x="94" y="86" width="12" height="4" fill="#16121b"/><rect x="63" y="85" width="30" height="6" rx="3" style="fill:var(--neon,#ff2e88)"/><rect x="107" y="85" width="30" height="6" rx="3" style="fill:var(--neon2,#19e3d2)"/></g>'),
 "sneaker": ('0 0 240 150', '<path d="M10 112h222q5 22-17 24H30q-22 0-20-24z" fill="#fff"/><path d="M12 121h221" stroke="#16121b" stroke-width="3"/><path d="M18 112l4-54q2-20 22-20h28q8 0 12 9l12 23q34 14 74 18 44 4 60 24z" style="fill:var(--a,#ff2e88)"/><path d="M178 89q44 5 52 23h-60q-2-14 8-23z" style="fill:var(--b,#c6ff3d)"/><path d="M18 112l3-40h30q6 22-3 40z" style="fill:var(--b,#c6ff3d)"/><path d="M26 46q22-14 52-3l-4 9q-24-8-44 2z" fill="#16121b"/><circle cx="112" cy="94" r="11" style="fill:var(--c,#2d7bff)"/><g stroke="#fff" stroke-width="4" stroke-linecap="round"><path d="M86 52l14-5M94 62l15-5M104 71l15-4M118 77l14-3M133 82l13-2"/></g>'),
 "ball": ('0 0 100 100', '<circle cx="50" cy="50" r="48" fill="#ff7a1a"/><g fill="none" stroke="#16121b" stroke-width="3"><path d="M2 50h96M50 2v96M16 16q26 34 0 68M84 16q-26 34 0 68"/></g>'),
 "coin": ('0 0 100 100', f'<circle cx="50" cy="50" r="48" fill="#c29a45"/><circle cx="50" cy="50" r="42" fill="#e9cb7e"/><circle cx="50" cy="50" r="42" fill="none" stroke="#a97f2e" stroke-width="2" stroke-dasharray="2 5"/><path d="M40 30v40l32-20z" fill="#a97f2e"/>'),
 "bolt": ('0 0 60 100', '<path d="M38 0 4 56h22l-8 44 38-60H32z" style="fill:var(--a,#c6ff3d)" stroke="#16121b" stroke-width="3" stroke-linejoin="round"/>'),
 "clapper": ('0 0 120 100', '<rect x="6" y="36" width="108" height="60" rx="6" fill="#16121b"/><g transform="rotate(-12 8 30)"><rect x="6" y="14" width="108" height="20" rx="4" fill="#16121b"/><path d="M18 14l-10 20M44 14 34 34M70 14 60 34M96 14 86 34" stroke="#fff" stroke-width="9"/></g><path d="M50 52v30l26-15z" style="fill:var(--a,#ff2e88)"/>'),
 "burst": ('-100 -100 200 200', '<path d="' + "M" + "L".join(f"{(92 if i % 2 == 0 else 70) * math.cos(math.pi * i / 14):.1f} {(92 if i % 2 == 0 else 70) * math.sin(math.pi * i / 14):.1f}" for i in range(28)) + 'Z" style="fill:var(--a,#c6ff3d)"/>'),
 "splash1": ('-100 -100 200 200', f'<g fill="currentColor">{splash(4)}</g>'),
 "splash2": ('-100 -100 200 200', f'<g fill="currentColor">{splash(9)}</g>'),
 "splash3": ('-100 -100 200 200', f'<g fill="currentColor">{splash(23)}</g>'),
}
PAR = ' preserveAspectRatio="none"'
sprite = '<svg xmlns="http://www.w3.org/2000/svg" style="display:none">' + "".join(f'<symbol id="{k}" viewBox="{vb}"{PAR if k in ("column", "pediment") else ""}>{body}</symbol>' for k, (vb, body) in SYMS.items()) + "</svg>"
(OUT / "art.svg").write_text(sprite)
(OUT / "favicon.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="22" fill="#16121b"/><g color="#e9cb7e">{SYMS["mark"][1]}</g></svg>')

def use(name, cls="", style="", pres=""):
    return f'<svg class="{cls}" style="{style}" aria-hidden="true"{pres}><use href="art.svg#{name}"/></svg>'
def pop(name, cls="", **v):
    return use(name, f"pop {cls}".strip(), ";".join(f"--{k}:{val}" for k, val in v.items()))

def bg(name, scrim, eager=False, pos="50% 50%"):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img class="bg" src="img/{name}.jpg" alt="" {load} decoding="async" style="object-position:{pos}"><div class="scrim {scrim}"></div>'

# ---------- shared chrome ----------
NAV = [("work.html", "Work"), ("index.html#process", "How it works"), ("free-video.html", "Free video"), ("contact.html", "Contact")]
def page(fname, title, desc, body):
    dark_top = ' class="dark-top"' 
    cur = ' aria-current="page"'
    nav = "".join(f'<a href="{h}"{cur if h == fname else ""}>{t}</a>' for h, t in NAV)
    logo = f'<a class="logo" href="index.html" aria-label="AI Studious, home">{use("mark")}<span aria-hidden="true">AI&nbsp;<b>STVDIOVS</b></span></a>'
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#16121B">
<link rel="preload" as="image" href="img/hero.jpg" fetchpriority="high">
<link rel="canonical" href="https://aistudious.ca/{'' if fname == 'index.html' else fname}">
<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="https://aistudious.ca/{'' if fname == 'index.html' else fname}"><meta property="og:image" content="https://aistudious.ca/og.png"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Manrope:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"ProfessionalService","name":"AI Studious","url":"https://aistudious.ca","email":"contact@aistudious.ca","areaServed":"Greater Toronto Area","description":"Video studio for small businesses in the Greater Toronto Area."}}</script>
</head>
<body{dark_top}>
<div class="progress" aria-hidden="true"><i></i></div>
<div class="announce"><span><b>Small business in the GTA?</b> Get one video built only for you, free. <a href="free-video.html">Claim yours &rarr;</a></span><button aria-label="Dismiss">&times;</button></div>
<header class="head"><div class="wrap head-row">{logo}<nav class="nav" aria-label="Main">{nav}</nav>
<div class="head-cta"><a class="btn sm" data-calendly href="contact.html">Book a call</a><button class="burger" aria-label="Menu" aria-expanded="false"><i></i><i></i></button></div></div></header>
<div class="drawer">{"".join(f'<a href="{h}">{t}</a>' for h, t in NAV)}<a data-calendly href="contact.html">Book a call</a></div>
<main>{body}</main>
<footer class="foot"><div class="wrap"><div class="foot-grid">
<div>{logo}<p>A video studio for small businesses across the Greater Toronto Area.</p></div>
<div><h4>Studio</h4><ul><li><a href="work.html">Work</a></li><li><a href="index.html#process">How it works</a></li><li><a href="free-video.html">Free video</a></li></ul></div>
<div><h4>Contact</h4><ul><li><a data-email></a></li><li><a data-calendly href="contact.html">Book a call</a></li><li>2160 Hwy 7, Ste 6 #1521, Vaughan, ON</li></ul></div>
</div><div class="foot-base"><span>&copy; 2026 AI Studious</span><span>Our videos are produced with AI-assisted tools and labelled where platforms ask for it.</span><span>Paintings: Thomas Cole, The Course of Empire (1836); Giovanni Paolo Panini, Ancient Rome (1757). Public domain.</span></div></div></footer>
<dialog id="lightbox"><button class="lb-x" aria-label="Close">&times;</button><div class="lb-body"></div></dialog>
<script src="config.js"></script><script src="main.js" defer></script>
</body></html>'''

def form(kind, cta):
    return f'''<form class="inquiry rv" id="inquiry">
<input type="hidden" name="request" value="{kind}">
<label class="f">Your name<input name="name" autocomplete="name" required></label>
<label class="f">Business name<input name="business" autocomplete="organization" required></label>
<label class="f">Email<input name="email" type="email" autocomplete="email" required></label>
<label class="f">Phone (optional)<input name="phone" type="tel" autocomplete="tel"></label>
<label class="f">Website or Instagram<input name="website" placeholder="yourbusiness.ca or @handle"></label>
<label class="f">Type of business<select name="type"><option>Gym or fitness studio</option><option>Restaurant or cafe</option><option>Shop or retail</option><option>Salon or beauty</option><option>Other</option></select></label>
<label class="f full">What should the video promote?<textarea name="message" placeholder="An offer, a class, a new location, an event…"></textarea></label>
<label class="hp" aria-hidden="true">Leave empty<input name="company_site_url" tabindex="-1" autocomplete="off"></label>
<button class="btn pink full" type="submit" style="grid-column:1/-1">{cta}</button>
<p class="form-note" role="status">We only use these details to reply to you.</p>
</form>'''

rule = f'<div class="rule">{use("wreath")}</div>'
words = lambda s: " ".join(f'<span style="--i:{i}">{w}</span>' for i, w in enumerate(s.split()))

# ---------- home ----------
home = f'''
<section class="hero intro painted dark" data-scene="exit" data-dot="Top" id="top">
  {bg("hero","s-hero",True,"50% 62%")}
  <div class="hero-copy">
    <p class="eyebrow">Video studio &middot; Greater Toronto Area</p>
    <h1>{words("Video that")} <span style="--i:2" class="hl">stops</span> {words("the scroll").replace("--i:0","--i:3").replace("--i:1","--i:4")}</h1>
    <p class="lead">Short videos for gyms, studios, restaurants and local shops. Made for your offer, your feed and your customers.</p>
    <div class="hero-cta"><a class="btn pink" href="free-video.html">Claim your free video <span class="arrow">&rarr;</span></a><a class="btn ghost" href="work.html">See the work</a></div>
  </div>
  <p class="plate">Thomas Cole, <i>The Consummation of Empire</i>, 1836</p>
  <div class="pops" style="--z:2">
    {pop("splash1","flat",l=36,t=88,w=17,dx=-6,dy=-8,s0=1,s1=1.7,r0=-6,r1=24,i=0)[:-6].replace('class="pop flat"','class="pop flat" color="#ff2e88"')}</svg>
    {pop("splash2","flat hide-m",l=17,t=66,w=22,dx=-8,dy=-12,s1=1.7,r1=-20,i=1).replace('class="pop flat hide-m"','class="pop flat hide-m" color="#2d7bff"')}
    {pop("splash3","flat",l=85,t=60,w=20,dx=8,dy=-16,s1=1.8,r1=24,i=2).replace('class="pop flat"','class="pop flat" color="#c6ff3d"')}
  </div>
  <div class="pops" style="--z:5">
    {pop("sneaker",l=82,t=80,w=25,ar="240/150",dx=10,dy=-26,s0=1,s1=2,r0=-16,r1=-36,i=3)}
    {pop("ball","hide-m",l=14,t=50,w=8,dx=-12,dy=-34,s1=2.4,r1=140,i=4)}
    {pop("coin","hide-m",l=8,t=30,w=6,dx=-6,dy=-30,s1=2,r1=-40,i=5)}
    {pop("bolt",l=24,t=84,w=6,ar="60/100",dx=-10,dy=-20,s1=2.2,r0=-14,r1=10,i=6)}
    {pop("clapper","hide-m",l=92,t=34,w=8,ar="120/100",dx=10,dy=-30,s1=2,r0=10,r1=-18,i=7)}
  </div>
</section>

<section class="sec offer painted dark" data-scene="through" data-dot="Free video" id="offer">
  {bg("gallery","s-purple")}
  <div class="wrap offer-grid">
    <div>
      <p class="eyebrow rv">For small businesses</p>
      <h2 class="rv" style="--d:60ms;margin:14px 0 18px">One video. Built only for you. <em>Free.</em></h2>
      <p class="lead rv" style="--d:120ms">We make one short video for your business so you can see what we do before you spend anything.</p>
      <ul class="rv" style="--d:180ms"><li>Made around your own offer, colours and style</li><li>Sized for Reels, TikTok and Shorts</li><li>No card, no contract</li></ul>
      <a class="btn gold rv" style="--d:240ms" href="free-video.html">Claim your free video <span class="arrow">&rarr;</span></a>
    </div>
    <div class="ticket" aria-hidden="true">
      {pop("splash2","flat",w=34,s0=.7,s1=1.2,r0=-30,r1=30).replace('class="pop flat"','class="pop flat" color="#ff2e88"')}
      {pop("burst","",w=24,s0=.6,s1=1.15,r0=-40,r1=20)}
      <div class="pop" style="--w:24;--s0:.6;--s1:1.15;--r0:-18;--r1:-6;display:grid;place-content:center;text-align:center;color:#16121b;filter:none"><b class="display" style="font-size:clamp(34px,5.4vw,76px);font-weight:900;line-height:.9">Free</b><span style="font-weight:700;letter-spacing:.14em;font-size:clamp(10px,1vw,14px);text-transform:uppercase">one video</span></div>
      {pop("coin","",l=84,t=20,w=6,s0=.6,s1=1.6,dy=-10,r1=90)}
      {pop("bolt","",l=14,t=78,w=5,ar="60/100",s0=.6,s1=1.7,dy=-8,r0=-20,r1=14)}
    </div>
  </div>
</section>

<section class="pin dark" data-scene="pin" data-dot="Showreel" id="reel">
  <div class="pin-inner painted">
    {bg("fall","s-dark")}
    <div class="pops back">
      {pop("splash1","flat fade",l=50,t=56,w=40,s0=.3,s1=2.3,r0=0,r1=40,o=.3).replace('class="pop flat fade"','class="pop flat fade" color="#ff2e88"')}
      {pop("splash3","flat fade",l=50,t=56,w=30,s0=.3,s1=2,dx=-30,dy=-16,r1=-60,o=1).replace('class="pop flat fade"','class="pop flat fade" color="#2d7bff"')}
      {pop("splash2","flat fade",l=50,t=56,w=28,s0=.3,s1=2,dx=32,dy=18,r1=70,o=1.6).replace('class="pop flat fade"','class="pop flat fade" color="#c6ff3d"')}
    </div>
    <p class="eyebrow">Showreel</p>
    <h2>See it <span class="hl lime">move</span></h2>
    <div class="screen"><div class="vslot" data-slot="reel" data-inline></div></div>
    <div class="pops">
      {pop("sneaker","fade",l=50,t=60,w=20,ar="240/150",dx=44,dy=30,s0=.2,s1=2.1,r0=20,r1=-24,o=1.2)}
      {pop("ball","fade",l=50,t=60,w=8,dx=-46,dy=-32,s0=.2,s1=2.6,r1=220,o=1.8)}
      {pop("coin","fade",l=50,t=60,w=6,dx=44,dy=-36,s0=.2,s1=2.4,r1=-120,o=2.4)}
      {pop("bolt","fade",l=50,t=60,w=6,ar="60/100",dx=-44,dy=34,s0=.2,s1=2.4,r0=-40,r1=16,o=2.8)}
      {pop("clapper","fade hide-m",l=50,t=60,w=9,ar="120/100",dx=-50,dy=2,s0=.2,s1=1.8,r0=30,r1=-14,o=3.4)}
    </div>
  </div>
</section>

<section class="sec marble" data-dot="What we make" id="services">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow rv">What we make</p><h2 class="rv" style="--d:60ms">Video for the places people <span class="hl blue">actually</span> scroll</h2></div>
    <div class="cards">
      <article class="card tilt rv" style="--c:var(--pink)"><span class="num">I</span><h3>Social video ads</h3><p>Vertical videos for Reels, TikTok and Shorts, built around one clear offer.</p></article>
      <article class="card tilt rv" style="--c:var(--blue);--d:100ms"><span class="num">II</span><h3>Promo and launch videos</h3><p>A new location, a new class, a seasonal deal. One video that says it fast.</p></article>
      <article class="card tilt rv" style="--c:var(--lime);--d:200ms"><span class="num">III</span><h3>Monthly content</h3><p>Fresh videos every month, so your page never goes quiet.</p></article>
    </div>
  </div>
</section>

<section class="sec dark painted" data-scene="through" data-dot="How it works" id="process">
  {bg("gallery","s-darker")}
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow rv">How it works</p><h2 class="rv" style="--d:60ms">Four steps, start to post</h2></div>
    <div class="steps4">
      <div class="st rv"><span class="num">I</span><h3>Brief</h3><p>Tell us what you want to promote. Your business name is enough to start.</p></div>
      <div class="st rv" style="--d:100ms"><span class="num">II</span><h3>Concept</h3><p>We write the idea and show it to you before anything is produced.</p></div>
      <div class="st rv" style="--d:200ms"><span class="num">III</span><h3>Production</h3><p>We make the video in your colours, your style and your words.</p></div>
      <div class="st rv" style="--d:300ms"><span class="num">IV</span><h3>Delivery</h3><p>You get files sized for each platform, ready to post or run as ads.</p></div>
    </div>
  </div>
</section>

<section class="sec marble" data-dot="Work" id="work">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow rv">Work</p><h2 class="rv" style="--d:60ms">Recent videos</h2></div>
    <div class="grid3"><div class="vslot rv" data-slot="w1"></div><div class="vslot rv" style="--d:100ms" data-slot="w2"></div><div class="vslot rv" style="--d:200ms" data-slot="w3"></div></div>
    <p class="rv" style="margin-top:28px"><a class="btn ghost" href="work.html">All work <span class="arrow">&rarr;</span></a></p>
  </div>
</section>

<section class="sec marble" style="background:var(--marble2)" id="faq">
  <div class="wrap">
    <div class="sec-head" style="text-align:center;justify-items:center">{rule.replace('class="rule"','class="rule" style="width:min(320px,70%)"')}<h2 class="rv">Questions</h2></div>
    <div class="faq rv">
      <details><summary>Is the free video really free?</summary><p>Yes. One video per business, no card and no contract. If you like it, we can talk about more.</p></details>
      <details><summary>Who can get one?</summary><p>Small businesses in the Greater Toronto Area: gyms, studios, restaurants, shops, salons and similar.</p></details>
      <details><summary>What do you need from me?</summary><p>Your business name and what you want to promote. A website or Instagram page helps us match your style.</p></details>
      <details><summary>How long does it take?</summary><p>It depends on the video. We give you a date when we reply to your request.</p></details>
      <details><summary>How are the videos made?</summary><p>We produce them with AI-assisted tools, directed and checked by a person, and we label them where platforms ask for it. We never present AI-generated people as your real customers.</p></details>
    </div>
  </div>
</section>

<section class="sec cta painted" data-scene="through" id="cta">
  {bg("hero","s-darker",False,"50% 70%")}
  <div class="pops back" style="--z:0">{pop("splash3","flat",l=12,t=30,w=26,s0=.5,s1=1.4,r1=60).replace('class="pop flat"','class="pop flat" color="#4e1a60"')}{pop("splash1","flat",l=90,t=74,w=30,s0=.5,s1=1.4,r1=-50).replace('class="pop flat"','class="pop flat" color="#a3231c"')}</div>
  <div class="wrap" style="position:relative">
    <p class="eyebrow rv">Ready when you are</p>
    <h2 class="rv" style="--d:60ms">Let&rsquo;s make your first video</h2>
    <p class="lead rv" style="--d:120ms">Book a short call or send us a few details. A real person answers every message.</p>
    <div class="cta-row rv" style="--d:180ms"><a class="btn pink" data-calendly href="contact.html">Book a call</a><a class="btn ghost" href="contact.html#inquiry">Send an inquiry</a></div>
  </div>
</section>'''

work = f'''
<section class="page-hero painted dark" data-scene="exit">{bg("gallery","s-dark",True)}<div class="wrap"><p class="eyebrow">Work</p><h1>Videos we&rsquo;ve <span class="hl">made</span></h1><p class="lead">New pieces are added here as they are finished.</p></div></section>
<section class="sec marble" style="padding-top:0"><div class="wrap"><div class="grid3">
<div class="vslot wide rv" data-slot="reel"></div>
{"".join(f'<div class="vslot rv" style="--d:{(i % 3) * 100}ms" data-slot="w{i + 1}"></div>' for i in range(9))}
</div></div></section>
<section class="sec cta painted" data-scene="through">{bg("fall","s-darker")}<div class="wrap"><h2 class="rv">Want one for your business?</h2><div class="cta-row rv"><a class="btn pink" href="free-video.html">Claim your free video</a><a class="btn ghost" data-calendly href="contact.html">Book a call</a></div></div></section>'''

free = f'''
<section class="page-hero offer sec painted dark" data-scene="exit">{bg("gallery","s-purple",True)}<div class="wrap offer-grid">
<div><p class="eyebrow">For small businesses in the GTA</p><h1>One video. Built for you. <span class="hl lime">Free.</span></h1><p class="lead">See what we can do for your business before you spend anything.</p></div>
<div class="ticket" aria-hidden="true">{pop("burst","",w=26,s0=1,s1=1.5,r0=-10,r1=40)}<div class="pop" style="--w:26;--s0:1;--s1:1.5;--r0:-12;--r1:6;display:grid;place-content:center;text-align:center;color:#16121b;filter:none"><b class="display" style="font-size:clamp(36px,5.6vw,80px);font-weight:900;line-height:.9">Free</b><span style="font-weight:700;letter-spacing:.14em;font-size:clamp(10px,1vw,14px);text-transform:uppercase">one video</span></div>{pop("sneaker","",l=80,t=84,w=16,ar="240/150",s1=1.6,dx=6,dy=-10,r0=-14,r1=-30)}</div>
</div></section>
<section class="sec marble"><div class="wrap two">
<div><h2 class="rv">How the offer works</h2>
<dl class="facts rv"><div><dt>Who</dt><dd>Small businesses in the Greater Toronto Area.</dd></div><div><dt>What</dt><dd>One short video made for one thing you want to promote.</dd></div><div><dt>Cost</dt><dd>Nothing. No card, no contract.</dd></div><div><dt>Limit</dt><dd>One free video per business.</dd></div><div><dt>After</dt><dd>If you like it, we can talk about more. If not, no hard feelings.</dd></div></dl></div>
{form("Free video", "Claim my free video")}
</div></section>'''

contact = f'''
<section class="page-hero painted dark" data-scene="exit">{bg("fall","s-dark",True,"50% 40%")}<div class="wrap"><p class="eyebrow">Contact</p><h1>Let&rsquo;s <span class="hl blue">talk</span></h1><p class="lead">Send an inquiry or pick a time for a call. A real person answers every message. You can also write to <a data-email style="border-bottom:1px solid"></a>.</p></div></section>
<section class="sec marble" style="padding-top:0"><div class="wrap two">
<div><h2 class="rv" style="font-size:clamp(24px,3vw,36px);margin-bottom:18px">Send an inquiry</h2>{form("Inquiry", "Send inquiry")}</div>
<div><h2 class="rv" style="font-size:clamp(24px,3vw,36px);margin-bottom:18px">Book a call</h2><div class="cal-inline rv"></div></div>
</div></section>'''

nf = '<section class="page-hero painted dark" style="min-height:80vh">{bg("fall","s-dark",True)}<div class="wrap"><p class="eyebrow">Error CDIV</p><h1>Page not <span class="hl">found</span></h1><p class="lead">That page does not exist.</p><p style="margin-top:24px"><a class="btn gold" href="index.html">Back to home</a></p></div></section>'

PAGES = [
 ("index.html", "AI Studious · Video studio for small businesses in the GTA", "Short videos for gyms, studios, restaurants and local shops in the Greater Toronto Area. Small businesses get one video built only for them, free.", home),
 ("work.html", "Work · AI Studious", "Videos made by AI Studious for small businesses in the Greater Toronto Area.", work),
 ("free-video.html", "Free video for small businesses · AI Studious", "Small businesses in the GTA can get one video built only for them, free. No card, no contract.", free),
 ("contact.html", "Contact · AI Studious", "Send an inquiry or book a call with AI Studious, a video studio in the Greater Toronto Area.", contact),
 ("404.html", "Page not found · AI Studious", "Page not found.", nf),
]
for f, t, d, b in PAGES: (OUT / f).write_text(page(f, t, d, b))
(OUT / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://aistudious.ca/sitemap.xml\n")
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>https://aistudious.ca/{'' if f == 'index.html' else f}</loc></url>" for f, *_ in PAGES[:4]) + "</urlset>")
print("built", [f for f, *_ in PAGES])
