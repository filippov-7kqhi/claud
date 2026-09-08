# -*- coding: utf-8 -*-
"""Static-site builder shared by BranchForge and HaulCrest."""
import os, html

def e(t): return html.escape(str(t), quote=True)


def head(cfg, title, desc, path, extra=""):
    canon = f"https://{cfg['domain']}/{path}".rstrip('/')
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(cfg['brand'])}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="https://{cfg['domain']}/{cfg['products'][0]['dir']}/01-hero.svg">
<meta name="theme-color" content="{cfg['theme']}">
<link rel="icon" href="data:image/svg+xml,{cfg['favicon']}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
{extra}</head>
<body>
"""


def header(cfg, current=""):
    cur = ' aria-current="page"'
    links = "".join(
        '<a href="%s"%s>%s</a>' % (l[1], cur if l[1] == current else "", e(l[0]))
        for l in cfg['nav'])
    bar = "".join(f"<span>{b}</span>" for b in cfg['topbar'])
    return f"""<div class="topbar"><div class="wrap topbar__in">{bar}</div></div>
<header class="header">
  <div class="wrap header__in">
    <a class="logo" href="index.html">{cfg['logomark']}<span>{cfg['brand_a']}<b>{cfg['brand_b']}</b></span></a>
    <nav class="nav" id="nav">{links}<a class="btn btn--primary" href="{cfg['products'][0]['url']}">Shop now</a></nav>
    <button class="burger" id="burger" aria-label="Menu" aria-expanded="false" aria-controls="nav">
      <span></span><span></span><span></span></button>
  </div>
</header>
"""


def footer(cfg):
    cols = ""
    for title, items in cfg['footer_cols']:
        li = "".join(f'<li><a href="{u}">{e(t)}</a></li>' for t, u in items)
        cols += f'<div><h4>{e(title)}</h4><ul>{li}</ul></div>'
    return f"""<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div>
        <a class="logo" href="index.html">{cfg['logomark']}<span>{cfg['brand_a']}<b>{cfg['brand_b']}</b></span></a>
        <p class="muted" style="margin-top:1rem;max-width:38ch;font-size:.93rem">{e(cfg['footer_blurb'])}</p>
        <p class="muted" style="font-size:.88rem">{e(cfg['company'])}<br>{e(cfg['address'])}<br>
          <a href="mailto:{cfg['email']}">{cfg['email']}</a></p>
      </div>
      {cols}
    </div>
    <div class="footer__bot">
      <span>&copy; <span data-year></span> {e(cfg['brand'])}. All rights reserved.</span>
      <span>Prices in GBP and include UK VAT. {e(cfg['brand'])} is not affiliated with any equipment manufacturer.</span>
    </div>
  </div>
</footer>
<script src="assets/js/script.js"></script>
</body>
</html>
"""


# ------------------------------------------------------------------ sections --
def hero(cfg):
    p = cfg['products'][0]
    pills = "".join(f'<span>{t}</span>' for t in cfg['hero_pills'])
    return f"""<section class="hero">
  <div class="wrap hero__grid">
    <div data-reveal>
      <p class="eyebrow">{e(cfg['hero_eyebrow'])}</p>
      <h1>{cfg['hero_h1']}</h1>
      <p class="lead">{e(cfg['hero_lead'])}</p>
      <div class="hero__cta">
        <a class="btn btn--primary btn--lg" href="{p['url']}">Shop the {e(p['short'])}</a>
        <a class="btn btn--ghost btn--lg" href="#range">See both machines</a>
      </div>
      <div class="hero__pills">{pills}</div>
    </div>
    <div class="hero__media" data-reveal>
      <img src="{p['dir']}/01-hero.svg" width="1200" height="760"
           alt="{e(p['name'])} — {e(p['short_desc'])}">
    </div>
  </div>
</section>"""


def range_section(cfg):
    cards = ""
    for p in cfg['products']:
        bullets = "".join(f"<li>{e(b)}</li>" for b in p['bullets'][:3])
        cards += f"""
      <article class="card" data-reveal>
        <div class="card__media">
          <span class="card__tag">{e(p['tag'])}</span>
          <img src="{p['dir']}/01-hero.svg" width="1200" height="760" alt="{e(p['name'])}">
        </div>
        <div class="card__body">
          <h3>{e(p['name'])}</h3>
          <p class="muted" style="font-size:.95rem;margin:0">{e(p['short_desc'])}</p>
          <ul>{bullets}</ul>
          <div class="card__price"><b>&pound;{p['price']:,}</b><s>&pound;{p['was']:,}</s></div>
          <a class="btn btn--primary btn--block" href="{p['url']}">View machine &amp; specs</a>
        </div>
      </article>"""
    return f"""<section id="range">
  <div class="wrap">
    <div class="sec-head center" data-reveal>
      <p class="eyebrow">The range</p>
      <h2>{cfg['range_h2']}</h2>
      <p class="muted">{e(cfg['range_lead'])}</p>
    </div>
    <div class="grid-2">{cards}</div>
  </div>
</section>"""


def why(cfg):
    tiles = "".join(f"""<div class="tile" data-reveal><div class="tile__ico">{ico}</div>
      <h3>{e(t)}</h3><p>{e(d)}</p></div>""" for ico, t, d in cfg['why'])
    return f"""<section style="background:var(--bg-2);border-block:1px solid var(--line)">
  <div class="wrap">
    <div class="sec-head center" data-reveal><p class="eyebrow">Why buy from us</p>
      <h2>{cfg['why_h2']}</h2><p class="muted">{e(cfg['why_lead'])}</p></div>
    <div class="grid-4">{tiles}</div>
  </div>
</section>"""


def steps(cfg):
    s = "".join(f'<div class="step" data-reveal><h3>{e(t)}</h3><p>{e(d)}</p></div>'
                for t, d in cfg['steps'])
    return f"""<section><div class="wrap">
  <div class="sec-head center" data-reveal><p class="eyebrow">How it works</p>
  <h2>From order to first job in a week</h2></div>
  <div class="steps">{s}</div></div></section>"""


def reviews(cfg):
    r = "".join(f"""<div class="review" data-reveal><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
      <p>&ldquo;{e(q)}&rdquo;</p><footer>{e(n)}</footer></div>""" for q, n in cfg['reviews'])
    return f"""<section style="background:var(--bg-2);border-block:1px solid var(--line)"><div class="wrap">
  <div class="sec-head center" data-reveal><p class="eyebrow">Owner feedback</p>
  <h2>What UK operators tell us</h2>
  <p class="muted">Verified reviews collected after delivery. We publish the average, not the highlights.</p></div>
  <div class="grid-3">{r}</div></div></section>"""


def cta(cfg):
    p = cfg['products'][0]
    return f"""<section><div class="wrap"><div class="cta" data-reveal>
  <h2>{cfg['cta_h2']}</h2>
  <p>{e(cfg['cta_lead'])}</p>
  <p style="margin-top:1.6rem">
    <a class="btn btn--primary btn--lg" href="{p['url']}">Shop the {e(p['short'])}</a>
    <a class="btn btn--ghost btn--lg" href="contact.html">Talk to a specialist</a></p>
</div></div></section>"""


def faq_block(items, heading="Frequently asked"):
    d = "".join(f"""<details><summary>{e(q)}</summary><div class="acc__body">{a}</div></details>"""
                for q, a in items)
    return f"""<section><div class="wrap" style="max-width:900px">
  <div class="sec-head center" data-reveal><p class="eyebrow">Questions</p><h2>{e(heading)}</h2></div>
  <div class="acc" data-reveal>{d}</div></div></section>"""


# ------------------------------------------------------------------- pages ----
def build_index(cfg):
    return (head(cfg, cfg['title'], cfg['desc'], "index.html")
            + header(cfg, "index.html") + hero(cfg) + range_section(cfg) + why(cfg)
            + steps(cfg) + reviews(cfg) + faq_block(cfg['faq']) + cta(cfg) + footer(cfg))


def build_product(cfg, p):
    thumbs = ""
    for i, (f, alt) in enumerate(p['images']):
        sel = "true" if i == 0 else "false"
        thumbs += (f'<button type="button" role="tab" aria-selected="{sel}" data-full="{p["dir"]}/{f}" '
                   f'data-alt="{e(alt)}"><img src="{p["dir"]}/{f}" alt="{e(alt)}" loading="lazy" '
                   f'width="1200" height="760"></button>')
    specs_hi = "".join(f'<div><small>{e(k)}</small><b>{e(v)}</b></div>' for k, v in p['spec_hi'])
    rows = "".join(f'<tr><th>{e(k)}</th><td>{e(v)}</td></tr>' for k, v in p['specs'])
    bullets = "".join(f"<li>{e(b)}</li>" for b in p['bullets'])
    feats = "".join(f"""<div class="tile" data-reveal><h3>{e(t)}</h3><p>{e(d)}</p></div>"""
                    for t, d in p['features'])
    other = [q for q in cfg['products'] if q is not p][0]
    jsonld = f"""<script type="application/ld+json">{{
 "@context":"https://schema.org","@type":"Product","name":"{e(p['name'])}",
 "image":["https://{cfg['domain']}/{p['dir']}/01-hero.svg"],
 "description":"{e(p['meta_desc'])}","sku":"{p['sku']}","brand":{{"@type":"Brand","name":"{e(cfg['brand'])}"}},
 "offers":{{"@type":"Offer","url":"https://{cfg['domain']}/{p['url']}","priceCurrency":"GBP",
 "price":"{p['price']}","availability":"https://schema.org/InStock",
 "itemCondition":"https://schema.org/NewCondition"}}
}}</script>"""
    return (head(cfg, f"{p['name']} — {cfg['brand']}", p['meta_desc'], p['url'], jsonld)
            + header(cfg, p['url'])
            + f"""<section class="pdp"><div class="wrap pdp__grid">
  <div class="gallery">
    <div class="gallery__main"><img id="galMain" src="{p['dir']}/{p['images'][0][0]}"
      alt="{e(p['images'][0][1])}" width="1200" height="760"></div>
    <div class="gallery__thumbs" id="galThumbs" role="tablist" aria-label="{e(p['name'])} images">{thumbs}</div>
    <p class="muted" style="font-size:.8rem;margin-top:.7rem">{len(p['images'])} views &mdash; tap a thumbnail to enlarge.</p>
  </div>

  <div class="buybox">
    <span class="stockline"><i class="dot"></i>{e(p['stockline'])}</span>
    <h1>{e(p['name'])}</h1>
    <p class="muted">{e(p['lede'])}</p>

    <div class="priceblock">
      <div class="priceblock__row">
        <span class="price">&pound;{p['price']:,}</span>
        <s class="was">&pound;{p['was']:,}</s>
        <span class="save">SAVE {round((1-p['price']/p['was'])*100)}%</span>
      </div>
      <p class="vatline">Includes UK VAT &amp; mainland delivery. Finance from &pound;{p['finance']}/month.</p>
      <div class="countdown">
        <span class="countdown__lab">Offer ends in</span>
        <div class="cd" id="cd">
          <div><b data-d>00</b><small>DAYS</small></div><div><b data-h>00</b><small>HRS</small></div>
          <div><b data-m>00</b><small>MIN</small></div><div><b data-s>00</b><small>SEC</small></div>
        </div>
      </div>
    </div>

    <div class="specgrid">{specs_hi}</div>
    <a class="btn btn--primary btn--block btn--lg" href="contact.html?enquiry={p['sku']}">Reserve yours &mdash; &pound;{p['price']:,}</a>
    <p class="formnote" style="margin-top:.7rem">Secure checkout is handled by our sales team &mdash; no card details are taken on this site.</p>
    <div class="trustrow">
      <div><b>Free delivery</b>UK mainland</div><div><b>30-day</b>returns</div><div><b>2-year</b>warranty</div>
    </div>
    <ul style="margin-top:1.4rem;color:var(--ink-2);font-size:.95rem;padding-left:1.1rem">{bullets}</ul>
  </div>
</div></section>

<section style="background:var(--bg-2);border-block:1px solid var(--line)"><div class="wrap">
  <div class="sec-head" data-reveal><p class="eyebrow">Built for the job</p><h2>{e(p['features_h2'])}</h2></div>
  <div class="grid-3">{feats}</div>
</div></section>

<section><div class="wrap" style="max-width:900px">
  <div class="sec-head" data-reveal><p class="eyebrow">Full specification</p><h2>{e(p['short'])} technical data</h2></div>
  <table class="spectable" data-reveal><tbody>{rows}</tbody></table>
  <p class="formnote" style="margin-top:1rem">Specifications are nominal and may vary by production batch.</p>
</div></section>

{faq_block(p['faq'], 'About the ' + p['short'])}

<section><div class="wrap"><div class="cta" data-reveal>
  <h2>Also in the range</h2>
  <p>{e(other['short_desc'])}</p>
  <p style="margin-top:1.4rem"><a class="btn btn--primary btn--lg" href="{other['url']}">View the {e(other['short'])}</a></p>
</div></div></section>

<div class="stickybuy">
  <div><b>&pound;{p['price']:,}</b> <span class="muted" style="font-size:.8rem">inc. VAT</span></div>
  <a class="btn btn--primary" href="contact.html?enquiry={p['sku']}">Reserve yours</a>
</div>
"""
            + footer(cfg))


def build_about(cfg):
    tiles = "".join(f'<div class="tile" data-reveal><h3>{e(t)}</h3><p>{e(d)}</p></div>'
                    for t, d in cfg['about_tiles'])
    paras = "".join(f"<p>{e(x)}</p>" for x in cfg['about_paras'])
    return (head(cfg, f"About — {cfg['brand']}", cfg['about_desc'], "about.html")
            + header(cfg, "about.html")
            + f"""<section><div class="wrap" style="max-width:820px">
  <p class="eyebrow">About us</p><h1>{e(cfg['about_h1'])}</h1>
  <div class="muted" style="font-size:1.05rem">{paras}</div>
</div></section>
<section style="background:var(--bg-2);border-block:1px solid var(--line)"><div class="wrap">
  <div class="sec-head center" data-reveal><h2>How we operate</h2></div>
  <div class="grid-3">{tiles}</div></div></section>"""
            + cta(cfg) + footer(cfg))


def build_contact(cfg):
    return (head(cfg, f"Contact — {cfg['brand']}", f"Talk to the {cfg['brand']} team about specification, delivery or finance.", "contact.html")
            + header(cfg, "contact.html")
            + f"""<section><div class="wrap" style="max-width:900px">
  <p class="eyebrow">Contact</p><h1>Talk to someone who runs these machines</h1>
  <p class="muted" style="max-width:60ch">Questions on spec, access, delivery or finance? Send a note and a
     specialist replies the same working day. Phone lines are open Monday to Friday, 8am&ndash;6pm.</p>
  <div class="grid-2" style="margin-top:2.4rem;align-items:start">
    <div>
      <form class="form" data-demo="Thanks — your enquiry has been noted. A specialist will reply by email within one working day."
            novalidate>
        <div class="field"><label for="cname">Your name</label><input id="cname" name="name" required autocomplete="name"></div>
        <div class="field"><label for="cmail">Email</label><input id="cmail" name="email" type="email" required autocomplete="email"></div>
        <div class="field"><label for="cphone">Phone (optional)</label><input id="cphone" name="phone" type="tel" autocomplete="tel"></div>
        <div class="field"><label for="cmachine">Machine</label>
          <select id="cmachine" name="machine">
            {"".join(f'<option>{e(q["name"])}</option>' for q in cfg['products'])}
            <option>Not sure yet — help me choose</option>
          </select></div>
        <div class="field"><label for="cmsg">How can we help?</label><textarea id="cmsg" name="message" rows="5" required></textarea></div>
        <button class="btn btn--primary btn--lg" type="submit">Send enquiry</button>
        <p class="formnote">This demo form does not transmit data. Email us directly at
          <a href="mailto:{cfg['email']}">{cfg['email']}</a>.</p>
      </form>
      <div class="result" role="status"></div>
    </div>
    <div>
      <div class="tile" style="margin-bottom:1rem"><h3>Sales &amp; specification</h3>
        <p><a href="mailto:{cfg['email']}">{cfg['email']}</a><br>{e(cfg['phone'])}</p></div>
      <div class="tile" style="margin-bottom:1rem"><h3>After-sales &amp; parts</h3>
        <p><a href="mailto:{cfg['support_email']}">{cfg['support_email']}</a><br>Parts dispatched from the UK within 48 hours.</p></div>
      <div class="tile"><h3>Registered office</h3><p>{e(cfg['company'])}<br>{e(cfg['address'])}</p></div>
    </div>
  </div>
</div></section>"""
            + footer(cfg))


def build_track(cfg):
    return (head(cfg, f"Track your order — {cfg['brand']}", "Track a delivery and see what each stage means.", "track-order.html")
            + header(cfg, "track-order.html")
            + f"""<section><div class="wrap" style="max-width:760px">
  <p class="eyebrow">Order tracking</p><h1>Where is my machine?</h1>
  <p class="muted">Enter the reference from your confirmation email. Crated machines move on a
     tail-lift vehicle, so the carrier calls to book a slot before delivery.</p>
  <form class="form" data-demo="No live order was found for that reference on this demo site. Email {cfg['support_email']} and we will trace it."
        style="margin-top:1.6rem" novalidate>
    <div class="field"><label for="ref">Order reference</label>
      <input id="ref" name="ref" placeholder="{cfg['ref_prefix']}-000000" required></div>
    <div class="field"><label for="pc">Delivery postcode</label><input id="pc" name="postcode" placeholder="SW1A 1AA" required></div>
    <button class="btn btn--primary btn--lg" type="submit">Track order</button>
  </form>
  <div class="result" role="status"></div>
</div></section>
<section style="background:var(--bg-2);border-block:1px solid var(--line)"><div class="wrap">
  <div class="sec-head center"><h2>What each stage means</h2></div>
  <div class="steps">
    <div class="step"><h3>Order placed</h3><p>Payment cleared and your machine is allocated from UK stock.</p></div>
    <div class="step"><h3>Pre-delivery check</h3><p>Fluids, fasteners and a running test before the crate is sealed.</p></div>
    <div class="step"><h3>With the carrier</h3><p>Booked onto a tail-lift vehicle. You get a call to agree a slot.</p></div>
    <div class="step"><h3>Delivered</h3><p>Signed for kerbside. Inspect before signing and note any damage.</p></div>
  </div>
</div></section>"""
            + footer(cfg))


def build_policies(cfg):
    secs = "".join(f"""<h2 id="{i}">{e(t)}</h2>{b}""" for i, t, b in cfg['policies'])
    return (head(cfg, f"Policies — {cfg['brand']}", "Delivery, returns, warranty, privacy and terms.", "policies.html")
            + header(cfg, "policies.html")
            + f"""<section><div class="wrap" style="max-width:820px">
  <p class="eyebrow">Legal &amp; policies</p><h1>Delivery, returns &amp; terms</h1>
  <div class="muted" style="font-size:1rem">{secs}</div>
</div></section>"""
            + footer(cfg))


def write_site(cfg, root):
    os.makedirs(root, exist_ok=True)
    pages = {"index.html": build_index(cfg), "about.html": build_about(cfg),
             "contact.html": build_contact(cfg), "track-order.html": build_track(cfg),
             "policies.html": build_policies(cfg)}
    for p in cfg['products']:
        pages[p['url']] = build_product(cfg, p)
    for name, content in pages.items():
        open(os.path.join(root, name), "w", encoding="utf-8").write(content)
    open(os.path.join(root, "CNAME"), "w").write(cfg['domain'] + "\n")
    urls = "".join(f"<url><loc>https://{cfg['domain']}/{n}</loc></url>" for n in pages)
    open(os.path.join(root, "sitemap.xml"), "w").write(
        f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    open(os.path.join(root, "robots.txt"), "w").write(
        f"User-agent: *\nAllow: /\nSitemap: https://{cfg['domain']}/sitemap.xml\n")
    return sorted(pages)
