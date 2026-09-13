# -*- coding: utf-8 -*-
"""Static-store builder. Four products per store, built to Google Merchant Center rules."""
import os, html, datetime

def e(t): return html.escape(str(t), quote=True)

PRICE_VALID = (datetime.date.today() + datetime.timedelta(days=365)).isoformat()

# ---------------------------------------------------------------------------
# Region-specific tokens. Every store defaults to "GB" (cfg.get("country","GB")),
# so the four existing UK stores need no cfg change at all and render exactly
# as before. A store sets country="US" (see cfg_agrimaxx.py/cfg_groundmaxx.py)
# to pick up USD pricing, US structured data and US-appropriate copy.
# ---------------------------------------------------------------------------
REGION = {
    "GB": dict(
        # A literal character, not the &pound; entity: this string also flows
        # through head()'s title, which is html.escape()d, and escaping does
        # not know to leave "&pound;" alone -- it would double-escape the "&"
        # into "&amp;pound;", which renders as the literal text "&pound;".
        currency_code="GBP", currency_symbol="£", country_code="GB",
        html_lang="en-GB", og_locale="en_GB", area_served="GB",
    ),
    "US": dict(
        currency_code="USD", currency_symbol="$", country_code="US",
        html_lang="en-US", og_locale="en_US", area_served="US",
    ),
}

PHRASES = {
    "GB": dict(
        stock_dispatch="In stock &mdash; dispatched in 1&ndash;2 working days",
        vat1="Includes free delivery to the UK mainland.",
        vat2="New and unregistered, held in UK stock.",
        deliverysum="free to UK mainland, 7&ndash;12 working days.",
        cart_delivery_label="Delivery (UK mainland)",
        cart_formnote="Delivery is free to the UK mainland. Northern Ireland, the Highlands and "
                      "Islands and the Channel Islands are quoted separately &mdash; "
                      "<a href=\"shipping.html\">see delivery</a>.",
        track_stock="Payment cleared and your machine allocated from UK stock.",
        track_label="Delivery postcode", track_ph="SW1A 1AA",
        track_intro="Enter the reference from your confirmation email. Crated machines move on a "
                    "tail-lift vehicle, so the carrier calls to book a slot before delivery.",
        track_carrier_step="Booked onto a tail-lift vehicle. You get a call to agree a slot.",
        parts_dispatch="Parts dispatched from the UK in 48 hours.",
        machines_meta="UK stock, free mainland delivery.",
        machines_lead="Every machine below is held in UK stock, ships crated on a tail-lift "
                      "vehicle, and carries the same delivery, returns and warranty terms.",
        collection_fee="Collection from {sym}{fee:,} unless faulty",
        warranty_summary="2 years parts, 1 year engine.",
        day_word="working day",
    ),
    "US": dict(
        stock_dispatch="In stock — dispatched in 1–2 business days",
        vat1="Includes free nationwide freight shipping (curbside delivery).",
        vat2="New and unused, held in US stock.",
        deliverysum="free nationwide via freight carrier — typical transit time depends on "
                    "distance and is confirmed once your order ships, not guaranteed.",
        cart_delivery_label="Delivery (Freight, nationwide)",
        cart_formnote="Free freight shipping applies to the contiguous 48 states. Alaska, Hawaii "
                      "and offshore addresses are quoted separately &mdash; "
                      "<a href=\"shipping.html\">see delivery</a>.",
        track_stock="Payment cleared and your machine allocated from US stock.",
        track_label="Delivery ZIP code", track_ph="90210",
        track_intro="Enter the reference from your confirmation email. Freight shipments move on a "
                    "pallet, so the carrier calls to book a delivery window.",
        track_carrier_step="Booked with the freight carrier. You get a call to agree a delivery window.",
        parts_dispatch="Parts dispatched within 48 hours.",
        machines_meta="US stock, nationwide freight shipping.",
        machines_lead="Every machine below is held in US stock, ships freight on a pallet, and "
                      "carries the same delivery, returns and warranty terms.",
        collection_fee="Collection billed at cost, estimated around {sym}{fee:,}, unless faulty",
        # These are PTO implements with no engine of their own, so there is no
        # separate engine-warranty tier to state -- unlike the UK stores' petrol
        # and diesel machines.
        warranty_summary="2 years parts.",
        day_word="business day",
    ),
}


def region(cfg):
    return REGION[cfg.get("country", "GB")]


def cur(cfg):
    return region(cfg)["currency_symbol"]


def ph(cfg, key, **kw):
    text = PHRASES[cfg.get("country", "GB")][key]
    return text.format(**kw) if kw else text


def us(cfg):
    return cfg.get("country") == "US"


# Pages that must carry policy links in the footer (GMC checks home, product, cart, checkout).
NAV = [("Machines", "machines.html"), ("About", "about.html"),
       ("Contact", "contact.html"), ("Track Order", "track-order.html")]

POLICY_LINKS = [("Delivery & shipping", "shipping.html"), ("Returns & refunds", "returns.html"),
                ("Payment & billing", "payment.html"), ("Warranty", "returns.html#warranty"),
                ("Privacy", "privacy.html"), ("Terms & conditions", "terms.html")]


def crate_note(p):
    """Only stated once we have the figures. An empty " kg, crated ." reads as a
       mistake, and a made-up weight is worse than no weight."""
    w, b = str(p.get("weight_kg") or "").strip(), str(p.get("box") or "").strip()
    if w and b:
        return f" Shipping weight {w} kg, crated {b}."
    return f" Shipping weight {w} kg." if w else ""


def shipping_weight(p):
    w = str(p.get("weight_kg") or "").strip()
    return f"    <g:shipping_weight>{w} kg</g:shipping_weight>\n" if w else ""


def hero_img(p):
    """First gallery image — not a hardcoded filename, since real photos are .jpg."""
    return f"{p['dir']}/{p['images'][0][0]}" if p.get('images') else f"{p['dir']}/01-hero.svg"


def feed_img(p):
    """Merchant Center rejects SVG, so the feed and og:image always point at a raster."""
    src = hero_img(p)
    return src[:-4] + ".jpg" if src.endswith(".svg") else src


# Payment marks, drawn inline so they need no network request. These are card-scheme
# trademarks shown to indicate accepted methods; swap in the official artwork from
# Stripe's brand kit if you want the exact registered marks.
PAY_ICONS = (
  '<span class="payico" title="Visa" aria-label="Visa">'
  '<svg viewBox="0 0 48 30" role="img"><rect width="48" height="30" rx="4" fill="#fff"/>'
  '<text x="24" y="20" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" '
  'font-style="italic" font-weight="700" font-size="13" fill="#1a1f71">VISA</text></svg></span>'

  '<span class="payico" title="Mastercard" aria-label="Mastercard">'
  '<svg viewBox="0 0 48 30" role="img"><rect width="48" height="30" rx="4" fill="#fff"/>'
  '<circle cx="19" cy="15" r="8.5" fill="#eb001b"/><circle cx="29" cy="15" r="8.5" fill="#f79e1b"/>'
  '<path d="M24 8.7a8.5 8.5 0 0 0 0 12.6 8.5 8.5 0 0 0 0-12.6z" fill="#ff5f00"/></svg></span>'

  '<span class="payico" title="American Express" aria-label="American Express">'
  '<svg viewBox="0 0 48 30" role="img"><rect width="48" height="30" rx="4" fill="#2e77bc"/>'
  '<text x="24" y="19" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" '
  'font-weight="700" font-size="10" fill="#fff">AMEX</text></svg></span>'

  '<span class="payico" title="PayPal" aria-label="PayPal">'
  '<svg viewBox="0 0 48 30" role="img"><rect width="48" height="30" rx="4" fill="#fff"/>'
  '<path d="M15 22l1.8-11h5.6c2.8 0 4.3 1.4 3.9 3.8-.4 2.6-2.4 4-5.3 4h-2.2L18.2 22z" fill="#002c8a"/>'
  '<path d="M21 22l1.8-11h5.6c2.8 0 4.3 1.4 3.9 3.8-.4 2.6-2.4 4-5.3 4h-2.2L24.2 22z" fill="#009be1"/>'
  '</svg></span>'

  '<span class="payico" title="Apple Pay and Google Pay" aria-label="Apple Pay and Google Pay">'
  '<svg viewBox="0 0 48 30" role="img"><rect width="48" height="30" rx="4" fill="#111"/>'
  '<g fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round">'
  '<path d="M17 11.5a7 7 0 0 1 0 7"/><path d="M20.5 9a11 11 0 0 1 0 12"/>'
  '<path d="M24 6.5a15 15 0 0 1 0 17"/></g>'
  '<text x="35" y="19" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" '
  'font-weight="700" font-size="9" fill="#fff">PAY</text></svg></span>'
)


def company_no_row(cfg):
    """A definition row only when a company number has actually been supplied."""
    n = (cfg.get("company_no") or "").strip()
    if not n:
        return ""
    label = "Business ID" if us(cfg) else "Company number"
    return f"<div><dt>{label}</dt><dd>{e(n)}</dd></div>"


def company_no_line(cfg):
    n = (cfg.get("company_no") or "").strip()
    if not n:
        return ""
    label = "Business ID" if us(cfg) else "Company no."
    return f'<br><span class="muted">{label} {e(n)}</span>'


def company_no_clause(cfg):
    n = (cfg.get("company_no") or "").strip()
    if not n:
        return ""
    return f", business ID {e(n)}" if us(cfg) else f", company number {e(n)}"


def one_line_address(cfg):
    """Street, town/city, postcode and country on a single line, skipping
       anything not supplied. UK addresses put town and postcode together
       without a comma; a US address is written city, state ZIP."""
    if us(cfg):
        locality = ", ".join(x.strip() for x in (cfg.get("city"), cfg.get("state"))
                             if x and x.strip())
        town = " ".join(x.strip() for x in (locality, cfg.get("postcode")) if x and x.strip())
        supplied = [p.strip() for p in (cfg.get("street"), town) if p and p.strip()]
        if not supplied:
            return ""                   # a store that has not given us an address yet
        return ", ".join(supplied + ["United States"])
    town = " ".join(x.strip() for x in (cfg.get("city"), cfg.get("postcode")) if x and x.strip())
    supplied = [p.strip() for p in (cfg.get("street"), town) if p and p.strip()]
    if not supplied:
        return ""                       # a store that has not given us an address yet
    return ", ".join(supplied + ["United Kingdom"])


def phone_anchor(cfg):
    """A tel: link, or nothing when no number has been supplied for this store."""
    n = (cfg.get("phone") or "").strip()
    return f'<a href="tel:{cfg["phone_link"]}">{e(n)}</a>' if n else ""


def or_call(cfg, lead=" or call "):
    """The 'or call 01234 567890' half of a sentence, dropped when there is no number."""
    a = phone_anchor(cfg)
    return f"{lead}{a}" if a else ""


def address_row(cfg):
    a = one_line_address(cfg)
    return f"<div><dt>Registered office</dt><dd>{e(a)}</dd></div>" if a else ""


def phone_row(cfg):
    a = phone_anchor(cfg)
    return f"<div><dt>Telephone</dt><dd>{a}</dd></div>" if a else ""


def head(cfg, title, desc, path, extra="", noindex=False):
    canon = f"https://{cfg['domain']}/{path}"
    robots = '<meta name="robots" content="noindex,nofollow">' if noindex else ""
    R = region(cfg)
    return f"""<!DOCTYPE html>
<html lang="{R['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
{robots}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(cfg['brand'])}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="https://{cfg['domain']}/{feed_img(cfg['products'][0])}">
<meta property="og:locale" content="{R['og_locale']}">
<meta name="theme-color" content="{cfg['theme']}">
<link rel="icon" href="data:image/svg+xml,{cfg['favicon']}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{cfg['fonts']}" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css?v={cfg['ver_css']}">
{extra}</head>
<body>
"""


def org_ld(cfg):
    # Google penalises structured data that contradicts the page, so a field we have
    # nothing for is left out rather than emitted empty.
    R = region(cfg)
    tel = (cfg.get("phone") or "").strip()
    tel = f'\n "telephone":"{e(tel)}",' if tel else ""
    addr = ""
    if one_line_address(cfg):
        if us(cfg):
            addr = (f'\n "address":{{"@type":"PostalAddress","streetAddress":"{e(cfg["street"])}",'
                    f'\n   "addressLocality":"{e(cfg["city"])}",'
                    f'"addressRegion":"{e(cfg.get("state", ""))}",'
                    f'\n   "postalCode":"{e(cfg["postcode"])}","addressCountry":"US"}},')
        else:
            addr = (f'\n "address":{{"@type":"PostalAddress","streetAddress":"{e(cfg["street"])}",'
                    f'\n   "addressLocality":"{e(cfg["city"])}","postalCode":"{e(cfg["postcode"])}",'
                    f'\n   "addressCountry":"GB"}},')
    return f"""<script type="application/ld+json">{{
 "@context":"https://schema.org","@type":"OnlineStore","name":"{e(cfg['brand'])}",
 "url":"https://{cfg['domain']}/","email":"{cfg['email']}",{tel}{addr}
 "currenciesAccepted":"{R['currency_code']}","paymentAccepted":"Visa, Mastercard, American Express, PayPal",
 "areaServed":"{R['area_served']}"
}}</script>"""


def header(cfg, current=""):
    cur = ' aria-current="page"'
    links = "".join('<a href="%s"%s>%s</a>' % (u, cur if u == current else "", e(t)) for t, u in NAV)
    bar = "".join(f"<span>{b}</span>" for b in cfg['topbar'])
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap topbar__in">{bar}</div></div>
<header class="header">
  <div class="wrap header__in">
    <a class="logo" href="index.html">{cfg['logomark']}<span>{cfg['brand_a']}<b>{cfg['brand_b']}</b></span></a>
    <nav class="nav" id="nav" aria-label="Main">{links}
      <a class="btn btn--primary nav__cart" href="cart.html">Basket <span data-cart-count>0</span></a></nav>
    <div class="header__right">
      <a class="cartlink" href="cart.html" aria-label="Basket">&#128722;<span class="cartbadge" data-cart-count>0</span></a>
      <button class="burger" id="burger" aria-label="Menu" aria-expanded="false" aria-controls="nav">
        <span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<main id="main">
"""


def footer(cfg):
    machines = "".join(f'<li><a href="{p["url"]}">{e(p["short"])}</a></li>' for p in cfg['products'])
    policies = "".join(f'<li><a href="{u}">{e(t)}</a></li>' for t, u in POLICY_LINKS)
    return f"""</main>
<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div>
        <a class="logo" href="index.html">{cfg['logomark']}<span>{cfg['brand_a']}<b>{cfg['brand_b']}</b></span></a>
        <p class="muted" style="margin-top:1rem;max-width:38ch;font-size:.93rem">{e(cfg['footer_blurb'])}</p>
        <p class="muted" style="font-size:.88rem;line-height:1.8">
          <strong style="color:var(--ink)" data-biz="company">{e(cfg['company'])}</strong>
          <span data-biz-addr data-hide-if-unset>{e(one_line_address(cfg))}</span>
          <a href="mailto:{cfg['email']}">{cfg['email']}</a>
          <a {'href="tel:' + cfg['phone_link'] + '" ' if cfg['phone_link'] else ''}data-biz="phone" data-hide-if-unset>{e(cfg['phone'])}</a>
          <span class="muted" data-biz="companyNo" data-hide-if-unset
                data-prefix="Company no. ">{e(cfg['company_no'])}</span>
        </p>
      </div>
      <div><h4>Machines</h4><ul>{machines}</ul></div>
      <div><h4>Customer service</h4><ul>
        <li><a href="contact.html">Contact us</a></li>
        <li><a href="track-order.html">Track your order</a></li>
        <li><a href="about.html">About us</a></li>
        <li><a href="machines.html">All machines</a></li></ul></div>
      <div><h4>Policies</h4><ul>{policies}</ul></div>
    </div>
    <div class="footer__pay">
      <span class="muted">We accept</span>
      {PAY_ICONS}
    </div>
    <div class="footer__bot">
      <span>&copy; <span data-year></span> <span data-biz="company">{e(cfg['company'])}</span>. All rights reserved.</span>
      <span>All prices in {region(cfg)['currency_code']}. {e(cfg['brand'])} is an independent
        supplier and is not affiliated with any equipment manufacturer.</span>
    </div>
  </div>
</footer>
<script src="assets/js/site-config.js?v={cfg['ver_stripe']}"></script>
<script src="assets/js/catalogue.js?v={cfg['ver_cat']}"></script>
<script src="assets/js/script.js?v={cfg['ver_js']}"></script>
</body>
</html>
"""


# ------------------------------------------------------------------ blocks ---
def product_card(p, cfg, featured=False):
    sym = cur(cfg)
    bullets = "".join(f"<li>{e(b)}</li>" for b in p['bullets'][:3])
    return f"""<article class="card" data-reveal>
  <div class="card__media">
    <span class="card__tag">{e(p['tag'])}</span>
    <a href="{p['url']}"><img src="{hero_img(p)}" width="1200" height="760"
       alt="{e(p['name_full'])}" loading="lazy"></a>
  </div>
  <div class="card__body">
    <h3><a href="{p['url']}">{e(p['name'])}</a></h3>
    <p class="muted" style="font-size:.93rem;margin:0">{e(p['short_desc'])}</p>
    <ul>{bullets}</ul>
    <div class="card__price"><b>{sym}{p['price']:,}</b><s>{sym}{p['was']:,}</s></div>
    <div class="card__actions">
      <a class="btn btn--primary btn--block" href="{p['url']}">View machine</a>
      <button class="btn btn--ghost btn--block" data-add="{p['sku']}">Add to basket</button>
    </div>
  </div>
</article>"""


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
        <a class="btn btn--primary btn--lg" href="machines.html">Shop all four machines</a>
        <a class="btn btn--ghost btn--lg" href="{p['url']}">Start with the {e(p['short'])}</a>
      </div>
      <div class="hero__pills">{pills}</div>
    </div>
    <div class="hero__media" data-reveal>
      <img src="{hero_img(p)}" width="1200" height="760"
           alt="{e(p['name_full'])} — {e(p['short_desc'])}">
    </div>
  </div>
</section>"""


def range_section(cfg, heading=None, lead=None):
    cards = "".join(product_card(p, cfg) for p in cfg['products'])
    return f"""<section id="range">
  <div class="wrap">
    <div class="sec-head center" data-reveal>
      <p class="eyebrow">The range</p>
      <h2>{heading or cfg['range_h2']}</h2>
      <p class="muted">{e(lead or cfg['range_lead'])}</p>
    </div>
    <div class="grid-4 cards">{cards}</div>
  </div>
</section>"""


def why(cfg):
    tiles = "".join(f'<div class="tile" data-reveal><div class="tile__ico">{i}</div>'
                    f'<h3>{e(t)}</h3><p>{e(d)}</p></div>' for i, t, d in cfg['why'])
    return f"""<section class="band">
  <div class="wrap">
    <div class="sec-head center" data-reveal><p class="eyebrow">Why buy from us</p>
      <h2>{cfg['why_h2']}</h2><p class="muted">{e(cfg['why_lead'])}</p></div>
    <div class="grid-4">{tiles}</div>
  </div>
</section>"""


def steps(cfg):
    s = "".join(f'<div class="step" data-reveal><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in cfg['steps'])
    return f"""<section><div class="wrap">
  <div class="sec-head center" data-reveal><p class="eyebrow">How it works</p>
  <h2>From order to first job in a week</h2></div>
  <div class="steps">{s}</div></div></section>"""


def assurance(cfg):
    """Replaces the old testimonial block: verifiable facts, not invented quotes."""
    rows = "".join(f'<div class="tile" data-reveal><h3>{e(t)}</h3><p>{e(d)}</p></div>'
                   for t, d in cfg['assurance'])
    return f"""<section class="band"><div class="wrap">
  <div class="sec-head center" data-reveal><p class="eyebrow">Buying with confidence</p>
    <h2>What you are covered by</h2>
    <p class="muted">{"Your rights under applicable law, and the terms we add on top." if us(cfg)
      else "Your statutory rights under UK consumer law, and the terms we add on top."}
      Every claim below is written out in full on our policy pages.</p></div>
  <div class="grid-3">{rows}</div>
  <p class="center muted" style="margin-top:2rem;font-size:.92rem">
    We do not publish customer reviews on this site. When we have collected enough verified,
    post-delivery feedback to be representative, it will appear here through an independent
    review platform &mdash; not written by us.</p>
</div></section>"""


def faq_block(items, heading="Frequently asked"):
    d = "".join(f'<details><summary>{e(q)}</summary><div class="acc__body">{a}</div></details>'
                for q, a in items)
    ld = ",".join('{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'
                  % (e(q), e(__import__("re").sub("<[^>]+>", "", a))) for q, a in items)
    return f"""<section><div class="wrap" style="max-width:900px">
  <div class="sec-head center" data-reveal><p class="eyebrow">Questions</p><h2>{e(heading)}</h2></div>
  <div class="acc" data-reveal>{d}</div>
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{ld}]}}</script>
</div></section>"""


def cta(cfg):
    return f"""<section><div class="wrap"><div class="cta" data-reveal>
  <h2>{cfg['cta_h2']}</h2><p>{e(cfg['cta_lead'])}</p>
  <p style="margin-top:1.6rem">
    <a class="btn btn--primary btn--lg" href="machines.html">See all four machines</a>
    <a class="btn btn--ghost btn--lg" href="contact.html">Talk to a specialist</a></p>
</div></div></section>"""


# ------------------------------------------------------------------- pages ---
def build_index(cfg):
    return (head(cfg, cfg['title'], cfg['desc'], "index.html", org_ld(cfg))
            + header(cfg, "index.html") + hero(cfg) + range_section(cfg) + why(cfg)
            + steps(cfg) + assurance(cfg) + faq_block(cfg['faq']) + cta(cfg) + footer(cfg))


def build_machines(cfg):
    # named from the range this store actually sells, not a fixed list
    names = ", ".join(p["short_desc"].split(" — ")[0].split(" that ")[0].split(" with ")[0].lower()
                      for p in cfg["products"][:-1])
    last = cfg["products"][-1]["short_desc"].split(" — ")[0].split(" that ")[0].split(" with ")[0].lower()
    return (head(cfg, f"All machines — {cfg['brand']}",
                 f"All four {cfg['brand']} machines: {names} and {last}. "
                 f"{ph(cfg, 'machines_meta')}", "machines.html")
            + header(cfg, "machines.html")
            + f"""<section class="pagehead"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / <span>Machines</span></nav>
  <h1>All four machines</h1>
  <p class="muted" style="max-width:64ch">{ph(cfg, 'machines_lead')}</p>
</div></section>"""
            + range_section(cfg, "The full range", cfg['range_lead']) + cta(cfg) + footer(cfg))


def attachments_block(p, cfg):
    """Only rendered for machines that actually have a published attachment list."""
    items = p.get("attachments")
    if not items:
        return ""
    sym = cur(cfg)
    rows = "".join(f'<tr><th>{e(n)}</th><td><strong>{sym}{v:,}</strong></td></tr>' for n, v in items)
    return f"""<section class="band"><div class="wrap" style="max-width:900px">
  <div class="sec-head" data-reveal><p class="eyebrow">Attachments</p>
    <h2>What else it will run</h2>
    <p class="muted">All change over on the quick hitch. Tell us which you want
      and we will add them to your order &mdash; they ship in the same crate.</p></div>
  <table class="spectable" data-reveal><tbody>{rows}</tbody></table>
</div></section>"""


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
    # A feature tuple is (title, text) everywhere already shipping, or
    # (title, text, (image_src, image_alt)) for a store that supplies photos
    # to illustrate each point -- the image is optional so every existing
    # store's features list, and its rendered markup, is untouched.
    has_feat_imgs = any(len(f) == 3 for f in p['features'])
    feat_style = ("<style>.tile--img img{width:100%;aspect-ratio:4/3;object-fit:cover;"
                  "border-radius:10px;margin-bottom:14px}</style>") if has_feat_imgs else ""

    def _feat(f):
        if len(f) == 3:
            t, d, (src, alt) = f
            return (f'<div class="tile tile--img" data-reveal>'
                    f'<img src="{p["dir"]}/{src}" alt="{e(alt)}" loading="lazy">'
                    f'<h3>{e(t)}</h3><p>{e(d)}</p></div>')
        t, d = f
        return f'<div class="tile" data-reveal><h3>{e(t)}</h3><p>{e(d)}</p></div>'
    feats = "".join(_feat(f) for f in p['features'])
    others = "".join(product_card(q, cfg) for q in cfg['products'] if q['sku'] != p['sku'])
    R = region(cfg)
    sym = R['currency_symbol']
    # A US freight transit time varies far more by distance than a UK tail-lift
    # delivery does, so it is omitted rather than guessed -- handlingTime alone
    # is still valid and GMC does not require transitTime.
    if us(cfg):
        delivery_time = ('"deliveryTime":{"@type":"ShippingDeliveryTime",\n'
                          '       "handlingTime":{"@type":"QuantitativeValue","minValue":1,'
                          '"maxValue":2,"unitCode":"DAY"}}},')
    else:
        delivery_time = ('"deliveryTime":{"@type":"ShippingDeliveryTime",\n'
                          '       "handlingTime":{"@type":"QuantitativeValue","minValue":1,'
                          '"maxValue":2,"unitCode":"DAY"},\n'
                          '       "transitTime":{"@type":"QuantitativeValue","minValue":6,'
                          '"maxValue":10,"unitCode":"DAY"}}},')

    ld = f"""<script type="application/ld+json">{{
 "@context":"https://schema.org","@type":"Product",
 "name":"{e(p['name_full'])}",
 "image":[{",".join(f'"https://{cfg["domain"]}/{p["dir"]}/{(f[:-4] + ".jpg") if f.endswith(".svg") else f}"' for f, _ in p['images'][:4])}],
 "description":"{e(p['meta_desc'])}",
 "sku":"{p['sku']}","mpn":"{p['mpn']}",
 "brand":{{"@type":"Brand","name":"{e(cfg['brand'])}"}},
 "offers":{{"@type":"Offer","url":"https://{cfg['domain']}/{p['url']}",
   "priceCurrency":"{R['currency_code']}","price":"{p['price']}","priceValidUntil":"{PRICE_VALID}",
   "availability":"https://schema.org/InStock","itemCondition":"https://schema.org/NewCondition",
   "seller":{{"@type":"Organization","name":"{e(cfg['company'])}"}},
   "shippingDetails":{{"@type":"OfferShippingDetails",
     "shippingRate":{{"@type":"MonetaryAmount","value":"0","currency":"{R['currency_code']}"}},
     "shippingDestination":{{"@type":"DefinedRegion","addressCountry":"{R['country_code']}"}},
     {delivery_time}
   "hasMerchantReturnPolicy":{{"@type":"MerchantReturnPolicy",
     "applicableCountry":"{R['country_code']}",
     "returnPolicyCategory":"https://schema.org/MerchantReturnFiniteReturnWindow",
     "merchantReturnDays":30,"returnMethod":"https://schema.org/ReturnByMail",
     "returnFees":"https://schema.org/ReturnShippingFees",
     "returnShippingFeesAmount":{{"@type":"MonetaryAmount","value":"{cfg['return_fee']}","currency":"{R['currency_code']}"}}}}}}
}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
 {{"@type":"ListItem","position":1,"name":"Home","item":"https://{cfg['domain']}/"}},
 {{"@type":"ListItem","position":2,"name":"Machines","item":"https://{cfg['domain']}/machines.html"}},
 {{"@type":"ListItem","position":3,"name":"{e(p['name'])}"}}]}}</script>"""

    return (head(cfg, f"{p['name_full']} — {sym}{p['price']:,}", p['meta_desc'], p['url'], ld)
            + header(cfg, p['url'])
            + f"""<section class="pdp"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> /
    <a href="machines.html">Machines</a> / <span>{e(p['short'])}</span></nav>
  <div class="pdp__grid">
  <div class="gallery">
    <div class="gallery__main"><img id="galMain" src="{p['dir']}/{p['images'][0][0]}"
      alt="{e(p['images'][0][1])}" width="1200" height="760"></div>
    <div class="gallery__thumbs" id="galThumbs" role="tablist" aria-label="{e(p['name'])} images">{thumbs}</div>
    <p class="muted" style="font-size:.8rem;margin-top:.7rem">{len(p['images'])} views &mdash; tap a thumbnail to enlarge.</p>
  </div>

  <div class="buybox">
    <span class="stockline"><i class="dot"></i>{ph(cfg, 'stock_dispatch')}</span>
    <h1>{e(p['name_full'])}</h1>
    <p class="muted">{e(p['lede'])}</p>

    <div class="priceblock">
      <div class="priceblock__row">
        <span class="price">{sym}{p['price']:,}</span>
        <s class="was">{sym}{p['was']:,}</s>
        <span class="save">SAVE {round((1-p['price']/p['was'])*100)}%</span>
      </div>
      <p class="vatline">{ph(cfg, 'vat1')}</p>
      <p class="vatline">{ph(cfg, 'vat2')}</p>
    </div>

    <div class="specgrid">{specs_hi}</div>

    <div class="buyrow">
      <label class="qty"><span class="sr">Quantity</span>
        <input type="number" id="qty" value="1" min="1" max="5" inputmode="numeric"></label>
      <button class="btn btn--primary btn--lg btn--grow" data-add="{p['sku']}" data-buynow
        data-qty="#qty">Buy now &mdash; {sym}{p['price']:,}</button>
    </div>
    <button class="btn btn--ghost btn--lg btn--block" style="margin-top:.7rem"
      data-add="{p['sku']}" data-qty="#qty">Add to basket</button>
    <p class="added" data-added hidden>Added to your basket. <a href="cart.html">View basket</a></p>
    <p class="buynote">Buy now takes you straight to checkout with this machine in your basket.</p>

    <ul class="delivery-summary">
      <li><strong>Delivery:</strong> {ph(cfg, 'deliverysum')}
        <a href="shipping.html">Delivery details</a></li>
      <li><strong>Returns:</strong> 30 days from delivery. {ph(cfg, 'collection_fee', sym=sym, fee=cfg['return_fee'])}.
        <a href="returns.html">Returns policy</a></li>
      <li><strong>Warranty:</strong> {ph(cfg, 'warranty_summary')}
        <a href="returns.html#warranty">Warranty terms</a></li>
      <li><strong>Payment:</strong> card, PayPal or Apple Pay at checkout.
        <a href="payment.html">Payment terms</a></li>
    </ul>

    <ul class="keypoints">{bullets}</ul>
  </div>
</div></div></section>

{feat_style}
<section class="band"><div class="wrap">
  <div class="sec-head" data-reveal><p class="eyebrow">Built for the job</p><h2>{e(p['features_h2'])}</h2></div>
  <div class="grid-3">{feats}</div>
</div></section>

<section><div class="wrap" style="max-width:900px">
  <div class="sec-head" data-reveal><p class="eyebrow">Full specification</p>
    <h2>{e(p['short'])} technical data</h2></div>
  <table class="spectable" data-reveal><tbody>{rows}</tbody></table>
  <p class="formnote" style="margin-top:1rem">Specifications are nominal and may vary slightly by
     production batch.{crate_note(p)}</p>
</div></section>

{attachments_block(p, cfg)}

{faq_block(p['faq'], 'About the ' + p['short'])}

<section><div class="wrap">
  <div class="sec-head center"><p class="eyebrow">The rest of the range</p><h2>Also available</h2></div>
  <div class="grid-3 cards">{others}</div>
</div></section>

<div class="stickybuy">
  <div><b>{sym}{p['price']:,}</b></div>
  <div class="stickybuy__btns">
    <button class="btn btn--ghost" data-add="{p['sku']}">Basket</button>
    <button class="btn btn--primary" data-add="{p['sku']}" data-buynow>Buy now</button>
  </div>
</div>
""" + footer(cfg))


def build_cart(cfg):
    return (head(cfg, f"Your basket — {cfg['brand']}", "Review the machines in your basket before checkout.",
                 "cart.html", noindex=True)
            + header(cfg)
            + f"""<section class="pagehead"><div class="wrap">
  <nav class="crumbs"><a href="index.html">Home</a> / <span>Basket</span></nav>
  <h1>Your basket</h1></div></section>
<section><div class="wrap cartlayout">
  <div>
    <p class="cartnotice" id="cartNotice" hidden></p>
    <div id="cartItems" class="cartitems"></div>
    <p id="cartEmpty" class="empty">Your basket is empty.
       <a href="machines.html">Browse the four machines</a>.</p>
  </div>
  <aside class="summary" id="cartSummary" hidden>
    <h2>Order summary</h2>
    <dl>
      <div><dt>Subtotal</dt><dd data-sum-net>{cur(cfg)}0</dd></div>
      <div><dt>{ph(cfg, 'cart_delivery_label')}</dt><dd>Free</dd></div>
      <div class="total"><dt>Total to pay</dt><dd data-sum-total>{cur(cfg)}0</dd></div>
    </dl>
    <a class="btn btn--primary btn--block btn--lg" href="checkout.html">Proceed to checkout</a>
    <p class="formnote">{ph(cfg, 'cart_formnote')}</p>
    <ul class="minipolicy">
      <li><a href="returns.html">30-day returns</a></li>
      <li><a href="shipping.html">Delivery &amp; shipping</a></li>
      <li><a href="terms.html">Terms &amp; conditions</a></li>
    </ul>
  </aside>
</div></section>""" + footer(cfg))


def build_checkout(cfg):
    return (head(cfg, f"Checkout — {cfg['brand']}", "Secure checkout, powered by Stripe.",
                 "checkout.html", noindex=True)
            + header(cfg)
            + f"""<section class="pagehead"><div class="wrap">
  <nav class="crumbs"><a href="index.html">Home</a> / <a href="cart.html">Basket</a> / <span>Checkout</span></nav>
  <h1>Checkout</h1>
  <p class="muted" style="max-width:64ch">Payment is handled by Stripe. You will enter your delivery
     address, contact details and card on Stripe's secure page &mdash; no card details are entered on
     or stored by this website.</p>
</div></section>
<section><div class="wrap cartlayout">
  <div>
    <div class="checkout-panel">
      <h2>Your order</h2>
      <div id="checkoutItems" class="checkitems"></div>
      <div id="payReady" hidden>
        <button class="btn btn--primary btn--lg btn--block" id="payBtn">
          Pay securely with Stripe</button>
        <p class="formnote" style="margin-top:.9rem">You will be taken to Stripe to complete payment.
          Your order is not placed until payment succeeds. Stripe collects your delivery address there.</p>
      </div>
      <div class="result" id="ckResult" role="status"></div>
      <ul class="paylist">
        <li>Card, Apple&nbsp;Pay and Google&nbsp;Pay accepted</li>
        <li>Payment taken in full at checkout &mdash; no deposits, no recurring charges</li>
        <li>An invoice is emailed with your dispatch confirmation</li>
      </ul>
    </div>
    <p class="formnote">Questions before you pay? Email
      <a href="mailto:{cfg['email']}">{cfg['email']}</a>{or_call(cfg)}.</p>
  </div>
  <aside class="summary">
    <h2>Order summary</h2>
    <dl>
      <div><dt>Subtotal</dt><dd data-sum-net>{cur(cfg)}0</dd></div>
      <div><dt>{ph(cfg, 'cart_delivery_label')}</dt><dd>Free</dd></div>
      <div class="total"><dt>Total to pay</dt><dd data-sum-total>{cur(cfg)}0</dd></div>
    </dl>
    <a class="btn btn--ghost btn--block" href="cart.html">Back to basket</a>
    <ul class="minipolicy">
      <li><a href="returns.html">30-day returns</a></li>
      <li><a href="shipping.html">Delivery &amp; shipping</a></li>
      <li><a href="payment.html">Payment &amp; billing</a></li>
      <li><a href="terms.html">Terms</a></li>
      <li><a href="privacy.html">Privacy</a></li>
    </ul>
  </aside>
</div></section>""" + footer(cfg))


def _policy_page(cfg, slug, title, desc, intro, sections):
    body = "".join(f'<h2 id="{i}">{e(t)}</h2>{b}' for i, t, b in sections)
    toc = "".join(f'<li><a href="#{i}">{e(t)}</a></li>' for i, t, _ in sections)
    return (head(cfg, f"{title} — {cfg['brand']}", desc, slug)
            + header(cfg, slug)
            + f"""<section class="pagehead"><div class="wrap">
  <nav class="crumbs"><a href="index.html">Home</a> / <span>{e(title)}</span></nav>
  <h1>{e(title)}</h1><p class="muted" style="max-width:66ch">{intro}</p>
  <p class="muted" style="font-size:.85rem">Last updated {datetime.date.today().strftime('%d %B %Y')}.</p>
</div></section>
<section><div class="wrap policy">
  <nav class="policy__toc"><h4>On this page</h4><ul>{toc}</ul></nav>
  <div class="policy__body">{body}</div>
</div></section>""" + footer(cfg))


def build_returns(cfg):
    f = cfg['return_fee']
    if us(cfg):
        return _policy_page(cfg, "returns.html", "Returns, refunds & warranty",
            "How to return a machine, what it costs, how long a refund takes, and what the "
            "warranty covers.",
            "You may return most machines within 30 days of delivery. This page sets out the "
            "window, the procedure, who pays, and when you get your money back. Written "
            "warranties on this site are also subject to the federal Magnuson-Moss Warranty Act.",
            [("window", "Return window",
              "<p><strong>You have 30 calendar days from the day you receive the machine</strong> "
              "to tell us you want to return it. The window runs from the delivery date, not the "
              "order date.</p>"
              "<p>Once you have told us, you have a further 14 days to make the machine available "
              "for freight pickup. Contact us on or before day 30 even if pickup falls later.</p>"),
             ("how", "How to start a return",
              f"<ol><li>Email <a href='mailto:{cfg['email']}'>{cfg['email']}</a> with your order "
              "reference and the reason for return, or use the form on our "
              "<a href='contact.html'>contact page</a>.</li>"
              "<li>We reply within one business day with a return reference and a freight pickup "
              "form.</li>"
              "<li>We book a freight pickup from the delivery address. You do not arrange your own "
              "carrier &mdash; these machines are too heavy for a parcel network.</li>"
              "<li>Have the machine palletized and accessible at ground level on the agreed "
              "day.</li></ol>"
              "<p>No return is refused for want of the original packaging, but keep the pallet and "
              "crating if you can; it protects the machine in transit and protects your "
              "refund.</p>"),
             ("cost", "Who pays for the return",
              f"<table class='spectable'><tbody>"
              f"<tr><th>Faulty, damaged or not as described</th><td><strong>We pay.</strong> "
              f"Pickup is free and you receive a full refund including any shipping you "
              f"paid.</td></tr>"
              f"<tr><th>Changed your mind</th><td>Pickup is billed at the freight carrier's actual "
              f"cost for your location &mdash; typically around <strong>{cur(cfg)}{f}</strong>, but "
              f"it varies with distance and weight &mdash; deducted from your refund. We confirm "
              f"the figure before booking so there are no surprises.</td></tr>"
              f"<tr><th>Restocking fee</th><td><strong>None.</strong> We do not charge a "
              f"restocking fee in any circumstances.</td></tr></tbody></table>"),
             ("condition", "Condition of returned machines",
              "<p>You may inspect and test a machine as you would in a store: check the fit, the "
              "controls and the hitch or PTO connection against your tractor. That is expected and "
              "does not affect your refund.</p>"
              "<p>Use in the field does. If a machine comes back with wear on blades, teeth or "
              "cutting edges, or damage beyond reasonable inspection, we may reduce the refund to "
              "reflect the loss in value, and we will tell you the amount and the reason in "
              "writing before we process it.</p>"
              "<p>Freight carriers can refuse a machine with fuel or fluids not drained or "
              "declared, which delays your refund.</p>"),
             ("refund", "Refunds and timing",
              "<p>Refunds go back to the original payment method &mdash; the same card or account "
              "you paid from. We cannot refund to a different method, and we do not issue store "
              "credit unless you ask for it.</p>"
              "<p><strong>We refund within 14 days</strong> of the machine reaching our warehouse, "
              "or of you giving us proof it was shipped, whichever is sooner. Card refunds usually "
              "clear in a further 3&ndash;10 business days depending on your bank.</p>"),
             ("exclusions", "What is not returnable",
              "<p>Consumable and wear parts are non-returnable once fitted or used: blades, "
              "carbide teeth, belts, filters, cutting edges and driveline shafts. Unopened, "
              "unfitted spares can be returned within 30 days on the same terms as machines.</p>"
              "<p>We do not sell digital goods, downloads or subscriptions, so no digital-content "
              "or subscription-cancellation terms apply to anything on this site.</p>"),
             ("warranty", "Warranty",
              "<p>Every machine carries a <strong>two-year written warranty on parts we "
              "supply</strong>, starting on the delivery date and transferring with the machine if "
              "you sell it. As a written warranty on a consumer product, it is also subject to the "
              "federal Magnuson-Moss Warranty Act.</p>"
              "<p><strong>Covered:</strong> manufacturing defects, premature failure of a component "
              "under normal use, and anything that was already wrong when the machine arrived.</p>"
              "<p><strong>Not covered:</strong> wear items (blades, teeth, belts, filters, cutting "
              "edges, driveline shafts); damage from feeding stone, wire, metal or frozen material "
              "into a machine; running the PTO above the machine's rated speed; overloading beyond "
              "rated capacity; and damage from repairs carried out by someone other than an "
              "approved service provider. The post hole digger's auger is sold separately and is "
              "not part of this listing's warranty.</p>"
              f"<p>To claim, email <a href='mailto:{cfg['support_email']}'>{cfg['support_email']}"
              "</a> with your order reference, the serial number and photographs or video of the "
              "fault. We repair by dispatching parts or by arranging a service visit, at our "
              "discretion.</p>"),
             ("rights", "Your rights under state law",
              "<p>This warranty is in addition to, and does not replace, any rights you may have "
              "under your state's consumer protection laws. Some states do not allow limits on how "
              "long an implied warranty lasts or on incidental or consequential damages, so the "
              "limits above may not apply to you.</p>"
              "<p>Business customers buy on our <a href='terms.html'>terms of sale</a>. Our 30-day "
              "return window and two-year parts warranty apply to business purchases on the same "
              "terms as to individual buyers.</p>")])
    return _policy_page(cfg, "returns.html", "Returns, refunds & warranty",
        "How to return a machine, what it costs, how long a refund takes, and what the warranty covers.",
        "You may return any machine within 30 days of delivery. This page sets out the window, the "
        "procedure, who pays, and when you get your money back. Nothing here affects your statutory "
        "rights under the Consumer Rights Act 2015 or the Consumer Contracts Regulations 2013.",
        [("window", "Return window",
          "<p><strong>You have 30 calendar days from the day you receive the machine</strong> to tell us "
          "you want to return it. The window runs from the delivery date, not the order date.</p>"
          "<p>Once you have told us, you have a further 14 days to make the machine available for "
          "collection. Contact us on or before day 30 even if collection falls later.</p>"),
         ("how", "How to start a return",
          f"<ol><li>Email <a href='mailto:{cfg['email']}'>{cfg['email']}</a> with your order reference "
          "and the reason for return, or use the form on our "
          "<a href='contact.html'>contact page</a>.</li>"
          "<li>We reply within one working day with a returns reference and a collection booking form.</li>"
          "<li>We book a tail-lift collection from the delivery address. You do not arrange your own "
          "carrier &mdash; these machines are too heavy for a parcel network.</li>"
          "<li>Have the machine palletised and accessible at kerbside on the agreed day.</li></ol>"
          "<p>No return is refused for want of the original packaging, but keep the crate if you can; "
          "it protects the machine in transit and protects your refund.</p>"),
         ("cost", "Who pays for the return",
          f"<table class='spectable'><tbody>"
          f"<tr><th>Faulty, damaged or not as described</th><td><strong>We pay.</strong> Collection is "
          f"free and you receive a full refund including any delivery you paid.</td></tr>"
          f"<tr><th>Changed your mind</th><td>Collection is charged at <strong>&pound;{f}</strong> "
          f"for UK mainland addresses, deducted from your refund. Off-mainland collections are quoted "
          f"before we book them.</td></tr>"
          f"<tr><th>Restocking fee</th><td><strong>None.</strong> We do not charge a restocking fee "
          f"in any circumstances.</td></tr></tbody></table>"),
         ("condition", "Condition of returned machines",
          "<p>You may inspect and test a machine as you would in a shop: start it, check the controls, "
          "confirm it fits your access. That is expected and does not affect your refund.</p>"
          "<p>Commercial use does. If a machine comes back with hours on it, damaged blades or teeth, "
          "or wear beyond reasonable inspection, we may reduce the refund to reflect the loss in value, "
          "and we will tell you the amount and the reason in writing before we process it.</p>"
          "<p>Please drain or declare fuel before collection. Carriers can refuse a machine with a "
          "full tank, which delays your refund.</p>"),
         ("refund", "Refunds and timing",
          "<p>Refunds go back to the original payment method &mdash; the same card, PayPal account or "
          "bank account you paid from. We cannot refund to a different method, and we do not issue "
          "store credit unless you ask for it.</p>"
          "<p><strong>We refund within 14 days</strong> of the machine reaching our warehouse, or of "
          "you giving us proof it was sent, whichever is sooner. Card refunds usually clear in a "
          "further 3&ndash;5 working days depending on your bank.</p>"),
         ("exclusions", "What is not returnable",
          "<p>Consumable and wear parts are non-returnable once fitted or used: blades, carbide teeth, "
          "belts, filters, cutting edges and rubber tracks. Unopened, unfitted spares can be returned "
          "within 30 days on the same terms as machines.</p>"
          "<p>We do not sell digital goods, downloads or subscriptions, so no digital-content or "
          "subscription-cancellation terms apply to anything on this site.</p>"),
         ("warranty", "Warranty",
          "<p>Every machine carries a <strong>two-year warranty on parts we supply</strong> and a "
          "<strong>one-year engine warranty</strong> honoured through the engine manufacturer's UK "
          "service network. The warranty starts on the delivery date and transfers with the machine "
          "if you sell it.</p>"
          "<p><strong>Covered:</strong> manufacturing defects, premature failure of a component under "
          "normal use, and anything that was already wrong when the machine arrived.</p>"
          "<p><strong>Not covered:</strong> wear items (blades, teeth, belts, filters, tracks, tyres, "
          "cutting edges); damage from feeding stone, wire, metal or frozen material into a machine; "
          "overloading beyond the rated capacity; operating across a slope; missed servicing; and "
          "damage from repairs carried out by someone other than an approved engineer.</p>"
          f"<p>To claim, email <a href='mailto:{cfg['support_email']}'>{cfg['support_email']}</a> with "
          "your order reference, the serial number and photographs or video of the fault. We repair by "
          "dispatching parts or by sending an engineer, at our discretion. Keep your service records "
          "&mdash; we will ask for them on any engine or hydraulic claim.</p>"),
         ("rights", "Your statutory rights",
          "<p>Under the Consumer Rights Act 2015 goods must be of satisfactory quality, fit for purpose "
          "and as described. If they are not, you have a 30-day right to reject for a full refund, and "
          "after that a right to repair or replacement. These rights sit alongside everything above and "
          "are not replaced by it.</p>"
          "<p>Business customers buy on our <a href='terms.html'>terms of sale</a>; the Consumer Rights "
          "Act does not apply to business-to-business purchases, but our 30-day return and two-year "
          "warranty do.</p>")])


def build_shipping(cfg):
    if us(cfg):
        return _policy_page(cfg, "shipping.html", "Delivery & shipping",
            "Delivery costs, typical timescales, coverage and what to check when your machine "
            "arrives.",
            "Every machine ships freight on a pallet. Delivery is free to the contiguous 48 "
            "states; everywhere else is quoted before you order.",
            [("cost", "Delivery costs",
              "<table class='spectable'><tbody>"
              "<tr><th>Contiguous 48 states</th><td><strong>Free</strong></td></tr>"
              "<tr><th>Alaska &amp; Hawaii</th><td>Quoted individually</td></tr>"
              "<tr><th>US territories (Puerto Rico, etc.)</th><td>Quoted individually</td></tr>"
              "<tr><th>Outside the United States</th><td>Not currently served</td></tr>"
              "</tbody></table>"
              "<p>Ask us for an exact figure before ordering and we will confirm it in writing. We "
              "never add a delivery charge after an order is placed. Sales tax, where applicable, "
              "is calculated and shown at checkout.</p>"),
             ("time", "How long it takes",
              "<p>Handling is typically 1&ndash;2 business days before a machine leaves us. "
              "<strong>Freight transit time after that depends on distance and the carrier's "
              "schedule</strong> &mdash; it is estimated, not guaranteed, and we will give you the "
              "carrier's current estimate once your order ships rather than promise a fixed "
              "date.</p>"
              "<p>The carrier calls you to schedule a delivery window before the truck arrives. We "
              "do not send a machine without that call being made first.</p>"),
             ("access", "What we need at your end",
              "<p>Delivery is curbside by freight truck, typically to a driveway or the nearest "
              "point a semi-trailer can safely reach. You need firm, level ground, and an adult "
              "present to sign.</p>"
              "<p>Most carriers do not include a forklift or loader at the delivery end. If you do "
              "not have equipment to move the pallet off the truck, ask about liftgate service when "
              "you order &mdash; many carriers offer it for an added fee. Carriers may also refuse "
              "steep, narrow or unpaved access; tell us at checkout in the access notes box and we "
              "will plan for it.</p>"),
             ("check", "Checking your delivery",
              "<p><strong>Inspect the shipment before you sign the delivery receipt.</strong> If "
              "anything is damaged, note it on the carrier's paperwork before signing &mdash; that "
              "note is what makes a freight claim straightforward. Photograph it and email us the "
              "same day.</p>"
              "<p>If damage only becomes apparent after unpacking, tell us within 48 hours and we "
              "will still put it right. Signing clean does not remove your rights, but it does make "
              "a freight claim slower.</p>"),
             ("track", "Tracking",
              "<p>You get a dispatch email with a carrier reference as soon as the machine leaves "
              "us. You can also use our <a href='track-order.html'>order tracking page</a> or reply "
              "to your confirmation email and we will chase the carrier for you.</p>")])
    return _policy_page(cfg, "shipping.html", "Delivery & shipping",
        "Delivery costs, timescales, coverage and what to check when your machine arrives.",
        "Every machine ships crated on a pallet by tail-lift vehicle. Delivery is free to the UK "
        "mainland; everywhere else is quoted before you order.",
        [("cost", "Delivery costs",
          "<table class='spectable'><tbody>"
          "<tr><th>UK mainland (incl. mainland Scotland)</th><td><strong>Free</strong></td></tr>"
          "<tr><th>Scottish Highlands &amp; Islands</th><td>Quoted individually, typically &pound;95&ndash;&pound;180</td></tr>"
          "<tr><th>Northern Ireland</th><td>Quoted individually, typically &pound;120&ndash;&pound;200</td></tr>"
          "<tr><th>Isle of Man, Isle of Wight, Channel Islands</th><td>Quoted individually</td></tr>"
          "<tr><th>Outside the UK</th><td>Not currently served</td></tr></tbody></table>"
          "<p>Ask us for an exact figure before ordering and we will confirm it in writing. We never "
          "add a delivery charge after an order is placed.</p>"),
         ("time", "How long it takes",
          "<p><strong>7&ndash;12 working days from order to doorstep</strong> on the UK mainland. "
          "That covers picking and the pre-delivery inspection at our end, and transit on a "
          "tail-lift vehicle at the carrier's.</p>"
          "<p>Off-mainland addresses add roughly 3&ndash;5 working days. If a machine is going to "
          "miss the window we tell you before the window closes, not after.</p>"
          "<p>The carrier telephones you to agree a delivery slot. We do not send a machine without "
          "that call being made first.</p>"),
         ("access", "What we need at your end",
          "<p>Delivery is kerbside by tail-lift. You need firm, level ground the pallet truck can "
          "cross, and an adult present to sign.</p>"
          "<p>Carriers may refuse soft verges, loose gravel, steep or narrow drives and unmade tracks. "
          "If you are unsure, tell us at checkout in the access notes box and we will plan for it "
          "&mdash; a refused delivery costs a redelivery fee we would rather you did not pay.</p>"),
         ("check", "Checking your delivery",
          "<p><strong>Inspect the crate before you sign.</strong> If anything is damaged, write it on "
          "the carrier's paperwork before signing &mdash; that note is what makes a claim "
          "straightforward. Photograph it and email us the same day.</p>"
          "<p>If damage only becomes apparent after unpacking, tell us within 48 hours and we will "
          "still put it right. Signing clean does not remove your rights, but it does make a carrier "
          "claim slower.</p>"),
         ("track", "Tracking",
          "<p>You get a dispatch email with a carrier reference as soon as the machine leaves us. "
          "You can also use our <a href='track-order.html'>order tracking page</a> or reply to your "
          "confirmation email and we will chase the carrier for you.</p>")])


def build_payment(cfg):
    if us(cfg):
        return _policy_page(cfg, "payment.html", "Payment & billing",
            "Accepted payment methods, currency, invoicing and finance.",
            "All prices on this site are in US dollars. What you see is what you pay before tax "
            "&mdash; we add nothing at checkout beyond sales tax where it applies.",
            [("methods", "How you can pay",
              "<p>We accept Visa, Mastercard, American Express and Discover credit and debit "
              "cards, PayPal, Apple&nbsp;Pay and Google&nbsp;Pay.</p>"
              "<p>Card payments are processed by our payment provider on their own secure, "
              "PCI-DSS compliant systems. <strong>Card numbers are never entered on this website "
              "and are never stored by us</strong> &mdash; we receive only a confirmation that "
              "payment succeeded.</p>"
              "<p>Bank transfer (ACH or wire) is available for orders over "
              f"{cur(cfg)}5,000 and for trade accounts; email "
              f"<a href='mailto:{cfg['email']}'>{cfg['email']}</a> and we will issue a proforma "
              "invoice.</p>"),
             ("tax", "Sales tax",
              "<p>Sales tax is calculated at checkout based on your delivery address, where the "
              "law requires us to collect it. The amount is shown before you pay &mdash; it is "
              "never added afterward.</p>"),
             ("invoicing", "Invoicing",
              "<p>An invoice is emailed with your dispatch confirmation and a paper copy travels "
              "with the machine.</p>"
              "<p>If you need it made out to a company name, or a purchase order number on it, "
              "tell us when you order and we will raise it that way.</p>"),
             ("when", "When you are charged",
              "<p>Payment is taken in full when you place the order. We do not take deposits, we "
              "do not store card details for later, and there are no recurring or subscription "
              "charges of any kind on this site.</p>"
              "<p>If a machine turns out to be unavailable after you have paid, we tell you within "
              "one business day and refund in full immediately &mdash; we do not hold your money "
              "against future stock.</p>"),
             ("finance", "Financing",
              "<p>Equipment financing is available through an independent, third-party finance "
              "provider. Monthly figures shown on product pages are indicative illustrations, not "
              "quotations or offers of credit, and assume a representative term with no down "
              "payment.</p>"
              f"<p>{e(cfg['company'])} introduces customers to the provider and is not the lender. "
              "Approval, rate and term are decided entirely by the provider's own underwriting; the "
              "financing agreement is between you and them.</p>"),
             ("security", "Security",
              "<p>This site is served over HTTPS. Payment is handled entirely on the provider's "
              "systems, so no card data passes through, or is retained by, this website.</p>"
              "<p>We will never call or email you to ask for card details, a PIN or a one-time "
              "passcode. If someone does, it is not us &mdash; contact us using the email in the "
              "footer.</p>")])
    return _policy_page(cfg, "payment.html", "Payment & billing",
        "Accepted payment methods, currency, invoicing and finance.",
        "All prices on this site are in pounds sterling. What you see is what you pay &mdash; we "
        "add nothing at checkout.",
        [("methods", "How you can pay",
          "<p>We accept Visa, Mastercard and American Express credit and debit cards, PayPal, "
          "Apple&nbsp;Pay and Google&nbsp;Pay.</p>"
          "<p>Card payments are processed by our payment provider on their own secure, PCI-DSS "
          "compliant systems. <strong>Card numbers are never entered on this website and are never "
          "stored by us</strong> &mdash; we receive only a confirmation that payment succeeded.</p>"
          "<p>Bank transfer is available for orders over &pound;5,000 and for trade accounts; email "
          f"<a href='mailto:{cfg['email']}'>{cfg['email']}</a> and we will issue a proforma invoice.</p>"),
         ("invoicing", "Invoicing",
          "<p>An invoice is emailed with your dispatch confirmation and a paper copy travels in the "
          "crate with the machine.</p>"
          "<p>If you need it made out to a company name, or a purchase order number on it, tell us "
          "when you order and we will raise it that way.</p>"),
         ("when", "When you are charged",
          "<p>Payment is taken in full when you place the order. We do not take deposits, we do not "
          "store card details for later, and there are no recurring or subscription charges of any "
          "kind on this site.</p>"
          "<p>If a machine turns out to be unavailable after you have paid, we tell you within one "
          "working day and refund in full immediately &mdash; we do not hold your money against "
          "future stock.</p>"),
         ("finance", "Finance",
          "<p>Business asset finance is available over 24 to 48 months through an independent, "
          "FCA-authorised UK finance provider. Monthly figures shown on product pages are indicative "
          "illustrations, not quotations, and assume a 48-month term with no deposit.</p>"
          f"<p>{e(cfg['company'])} introduces customers to the provider and is not a lender or a "
          "credit broker for consumer credit. Finance is subject to status and to the provider's own "
          "terms; the agreement is between you and them.</p>"),
         ("security", "Security",
          "<p>This site is served over HTTPS. Payment is handled entirely on the provider's systems, "
          "so no card data passes through, or is retained by, this website.</p>"
          "<p>We will never telephone or email you to ask for card details, a PIN or a one-time "
          "passcode. If someone does, it is not us &mdash; hang up and contact us on the number in "
          "the footer.</p>")])


def build_privacy(cfg):
    if us(cfg):
        return _policy_page(cfg, "privacy.html", "Privacy policy",
            "What personal data we collect, why, how long we keep it and your rights.",
            f"{e(cfg['company'])} collects what we need to sell and deliver a machine, and "
            "nothing else.",
            [("collect", "What we collect",
              "<table class='spectable'><tbody>"
              "<tr><th>Order data</th><td>Name, email, phone, delivery and billing address, order "
              "history, access notes you give us</td></tr>"
              "<tr><th>Enquiry data</th><td>Whatever you type into the contact form and the emails "
              "you send us</td></tr>"
              "<tr><th>Technical data</th><td>IP address and browser type in standard server "
              "logs</td></tr>"
              "<tr><th>Payment data</th><td>None. Card details go directly to our payment provider "
              "and are never seen or stored by us</td></tr></tbody></table>"),
             ("why", "Why we use it",
              "<p><strong>To fulfil your order</strong> &mdash; we cannot sell or deliver you a "
              "machine without it.</p>"
              "<p><strong>To answer enquiries</strong> &mdash; responding to people who contact "
              "us.</p>"
              "<p><strong>To meet legal and accounting duties</strong> &mdash; mainly keeping "
              "order and tax records.</p>"
              "<p><strong>Marketing email</strong> &mdash; only if you opt in. Every marketing "
              "email carries a one-click unsubscribe that works immediately.</p>"),
             ("share", "Who we share it with",
              "<p>Only those who need it to complete your order: our freight carrier (name, "
              "address, phone so they can schedule your delivery), our payment provider, our "
              "accountants, and our IT and email providers.</p>"
              "<p><strong>We do not sell, rent or trade your personal data</strong>, and we do not "
              "share it for anyone else's marketing.</p>"),
             ("keep", "How long we keep it",
              "<p>Order and invoice records: kept for as long as required for accounting and tax "
              "purposes, typically several years. Warranty records: for the life of the warranty "
              "plus one year. Enquiries that do not become orders: two years. Marketing consent: "
              "until you withdraw it.</p>"),
             ("cookies", "Cookies and analytics",
              "<p>This site sets <strong>no advertising or cross-site tracking cookies</strong>, "
              "and we do not use Google Analytics, Meta Pixel or any third-party tracker. Your "
              "basket is held in your own browser using local storage, which never leaves your "
              "device. Clearing your browser data clears your basket.</p>"
              "<p>We do count visits, so we know which machines people are looking at. Each visit "
              "is given a random reference that lives only for that browser session and is "
              "discarded when you close the tab. Against it we record only the page you viewed, "
              "the machine you looked at, and whether a basket or checkout was started.</p>"
              "<p><strong>We do not record your name, email, IP address, device fingerprint or "
              "anything that identifies you</strong>, and the reference cannot be linked back to "
              "you or followed onto any other website. Counts are deleted after seven days.</p>"),
             ("rights", "Your privacy rights",
              "<p>Depending on your state, you may have the right to know what personal data a "
              "business holds about you, to request its deletion, and to opt out of the sale or "
              "sharing of personal data. We do not sell personal data to third parties.</p>"
              f"<p>Email <a href='mailto:{cfg['support_email']}'>{cfg['support_email']}</a> to "
              "make a request and we will respond within a reasonable time.</p>")])
    return _policy_page(cfg, "privacy.html", "Privacy policy",
        "What personal data we collect, why, how long we keep it and your rights under UK GDPR.",
        f"{e(cfg['company'])} is the data controller for the personal data described here. We collect "
        "what we need to sell and deliver a machine, and nothing else.",
        [("collect", "What we collect",
          "<table class='spectable'><tbody>"
          "<tr><th>Order data</th><td>Name, email, phone, delivery and billing address, order history, "
          "access notes you give us</td></tr>"
          "<tr><th>Enquiry data</th><td>Whatever you type into the contact form and the emails you send us</td></tr>"
          "<tr><th>Technical data</th><td>IP address and browser type in standard server logs</td></tr>"
          "<tr><th>Payment data</th><td>None. Card details go directly to our payment provider and are "
          "never seen or stored by us</td></tr></tbody></table>"),
         ("why", "Why we use it and our lawful basis",
          "<p><strong>To fulfil your order</strong> &mdash; performance of a contract. Without this we "
          "cannot sell or deliver you a machine.</p>"
          "<p><strong>To answer enquiries</strong> &mdash; legitimate interests in responding to people "
          "who contact us.</p>"
          "<p><strong>To meet legal duties</strong> &mdash; legal obligation, mainly keeping "
          "accounting records for six years.</p>"
          "<p><strong>Marketing email</strong> &mdash; consent, and only if you opt in. Every marketing "
          "email carries a one-click unsubscribe that works immediately.</p>"),
         ("share", "Who we share it with",
          "<p>Only those who need it to complete your order: our delivery carrier (name, address, phone "
          "so they can book your slot), our payment provider, our accountants, and our IT and email "
          "providers.</p>"
          "<p><strong>We never sell, rent or trade personal data</strong>, and we do not share it for "
          "anyone else's marketing. Where a provider processes data outside the UK, the transfer is "
          "covered by the UK International Data Transfer Addendum or adequacy regulations.</p>"),
         ("keep", "How long we keep it",
          "<p>Order and invoice records: six years after the end of the tax year, as HMRC requires. "
          "Warranty records: for the life of the warranty plus one year. Enquiries that do not become "
          "orders: two years. Marketing consent: until you withdraw it.</p>"),
         ("cookies", "Cookies and analytics",
          "<p>This site sets <strong>no advertising or cross-site tracking cookies</strong>, and we do "
          "not use Google Analytics, Meta Pixel or any third-party tracker. Your basket is held in your "
          "own browser using local storage, which never leaves your device. Clearing your browser data "
          "clears your basket.</p>"
          "<p>We do count visits, so we know which machines people are looking at. Each visit is given a "
          "random reference that lives only for that browser session and is discarded when you close the "
          "tab. Against it we record only the page you viewed, the machine you looked at, and whether a "
          "basket or checkout was started.</p>"
          "<p><strong>We do not record your name, email, IP address, device fingerprint or anything that "
          "identifies you</strong>, and the reference cannot be linked back to you or followed onto any "
          "other website. Counts are deleted after seven days. Because none of it identifies a person, "
          "no consent banner is required &mdash; but if you would rather not be counted at all, any "
          "browser setting that blocks background requests will stop it, with no effect on the site.</p>"),
         ("rights", "Your rights",
          "<p>Under UK GDPR you may ask for a copy of your data, ask us to correct or delete it, "
          "object to or restrict how we use it, ask for it in a portable format, and withdraw consent "
          "at any time.</p>"
          f"<p>Email <a href='mailto:{cfg['support_email']}'>{cfg['support_email']}</a> and we will "
          "respond within one month, free of charge. If you are unhappy with our response you can "
          "complain to the Information Commissioner's Office at ico.org.uk or on 0303 123 1113.</p>")])


def build_terms(cfg):
    if us(cfg):
        return _policy_page(cfg, "terms.html", "Terms & conditions",
            "The terms on which we sell machines through this website.",
            "These terms govern every order placed through this website. Please read them before "
            "you buy.",
            [("who", "Who you are buying from",
              f"<p>You are buying from <strong>{e(cfg['company'])}</strong>"
              f"{company_no_clause(cfg)}"
              f"{', located at ' + e(one_line_address(cfg)) if one_line_address(cfg) else ''}.</p>"
              f"<p>Contact us at <a href='mailto:{cfg['email']}'>{cfg['email']}</a>"
              f"{or_call(cfg)}.</p>"
              f"<p>{e(cfg['brand'])} is an independent retailer. We are not affiliated with, "
              "endorsed by, or an agent of any equipment manufacturer, and any manufacturer name "
              "on this site is used only to identify a component.</p>"),
             ("contract", "How the contract is formed",
              "<p>Your order is an offer to buy. The contract forms when we send you a dispatch "
              "confirmation email, not when you pay. If we cannot fulfil an order we tell you "
              "within one business day and refund in full.</p>"
              "<p>We reserve the right to decline an order where a price or specification has been "
              "published in obvious error. Where that happens you are refunded in full and owe us "
              "nothing.</p>"),
             ("prices", "Prices and specification",
              "<p>Prices are in US dollars and do not include sales tax, which is calculated at "
              "checkout where applicable. The price you see when you place the order is the price "
              "you pay; we do not add fees afterward.</p>"
              "<p>Specifications are nominal and may vary slightly between production batches. "
              "Where a variation would materially affect your intended use, tell us within 30 days "
              "and the <a href='returns.html'>returns policy</a> applies in full.</p>"),
             ("title", "Title and risk",
              "<p>Risk in a machine passes to you on delivery. Title passes when we have received "
              "payment in full. Until then the machine remains ours, and you must not sell, modify "
              "or dispose of it.</p>"),
             ("use", "Safe use and operator competence",
              "<p>These are powerful, PTO-driven implements. You are responsible for reading the "
              "operator's manual, following standard PTO and tractor-attachment safety practice, "
              "and ensuring anyone who operates a machine is trained and competent to do so.</p>"
              "<p>There is no license required to purchase or operate this equipment on private "
              "property. We supply the manual and the machine; we do not provide operator "
              "certification, and we are not liable for loss arising from untrained or unsafe "
              "use.</p>"),
             ("liability", "Liability",
              "<p>We are responsible for loss you suffer that is a direct and foreseeable result "
              "of our breaking this contract or failing to use reasonable care.</p>"
              "<p>We do not disclaim liability for death or personal injury caused by our "
              "negligence, or for fraud, to the extent such liability cannot be limited under "
              "applicable law. Otherwise, our total liability for any claim relating to a purchase "
              "is limited to the amount you paid for the product, and we are not liable for "
              "indirect, incidental or consequential damages, including lost profits.</p>"),
             ("law", "Complaints and governing law",
              f"<p>If something goes wrong, email <a href='mailto:{cfg['support_email']}'>"
              f"{cfg['support_email']}</a>. We acknowledge complaints within one business day and "
              "aim to resolve them within ten.</p>"
              "<p>These terms are governed by the laws of the <strong>[Governing state &mdash; "
              "TBD]</strong>, without regard to its conflict-of-laws principles, once that is "
              "finalized alongside our business registration.</p>")])
    return _policy_page(cfg, "terms.html", "Terms & conditions",
        "The terms on which we sell machines through this website.",
        "These terms govern every order placed through this website. Please read them before you buy. "
        "Nothing here limits your statutory rights.",
        [("who", "Who you are buying from",
          f"<p>You are buying from <strong>{e(cfg['company'])}</strong>, a company registered in "
          f"England and Wales{company_no_clause(cfg)}"
          f"{', registered office ' + e(one_line_address(cfg)) if one_line_address(cfg) else ''}.</p>"
          f"<p>Contact us at <a href='mailto:{cfg['email']}'>{cfg['email']}</a>"
          f"{or_call(cfg)}.</p>"
          f"<p>{e(cfg['brand'])} is an independent supplier. We are not affiliated with, endorsed by, "
          "or an agent of any equipment manufacturer, and any manufacturer name on this site is used "
          "only to identify a component.</p>"),
         ("contract", "How the contract is formed",
          "<p>Your order is an offer to buy. The contract forms when we send you a dispatch "
          "confirmation email, not when you pay. If we cannot fulfil an order we tell you within one "
          "working day and refund in full.</p>"
          "<p>We reserve the right to decline an order where a price or specification has been "
          "published in obvious error. Where that happens you are refunded in full and owe us "
          "nothing.</p>"),
         ("prices", "Prices and specification",
          "<p>Prices are in pounds sterling. The price you see when you place the order is the "
          "price you pay; we do not add fees at checkout.</p>"
          "<p>Specifications are nominal and may vary slightly between production batches. Where a "
          "variation would materially affect your intended use, tell us within 30 days and the "
          "<a href='returns.html'>returns policy</a> applies in full.</p>"),
         ("title", "Title and risk",
          "<p>Risk in a machine passes to you on delivery. Title passes when we have received payment "
          "in full. Until then the machine remains ours, and you must not sell, modify or dispose of "
          "it.</p>"),
         ("use", "Safe use and operator competence",
          "<p>These are powerful machines. You are responsible for reading the manual, wearing the "
          "protective equipment supplied, and ensuring anyone who operates a machine is trained and "
          "competent to do so.</p>"
          "<p>For commercial use, HSE expects operators to be trained and competent, and most "
          "principal contractors require a CPCS or NPORS card for compact plant. We supply the manual "
          "and the machine; we do not provide operator certification, and we are not liable for loss "
          "arising from untrained use.</p>"),
         ("liability", "Liability",
          "<p>We are responsible for loss you suffer that is a foreseeable result of our breaking this "
          "contract or failing to use reasonable care and skill.</p>"
          "<p>We do not limit liability for death or personal injury caused by our negligence, for "
          "fraud, or for anything else that cannot lawfully be limited. For business customers, our "
          "total liability is limited to the price paid for the machine, and we are not liable for "
          "loss of profit, loss of contract or business interruption.</p>"),
         ("law", "Complaints and governing law",
          f"<p>If something goes wrong, email <a href='mailto:{cfg['support_email']}'>"
          f"{cfg['support_email']}</a>. We acknowledge complaints within one working day and aim to "
          "resolve them within ten.</p>"
          "<p>These terms are governed by the law of England and Wales, and the courts of England and "
          "Wales have jurisdiction. If you live in Scotland or Northern Ireland you may also bring "
          "proceedings in your own courts.</p>")])


def build_about(cfg):
    tiles = "".join(f'<div class="tile" data-reveal><h3>{e(t)}</h3><p>{e(d)}</p></div>'
                    for t, d in cfg['about_tiles'])
    paras = "".join(f"<p>{e(x)}</p>" for x in cfg['about_paras'])
    # Opt-in: only stores that set about_images get a gallery, and its CSS is
    # scoped inline right here rather than added to the shared stylesheet, so
    # a store that doesn't set it renders byte-identical to before.
    gallery = ""
    if cfg.get('about_images'):
        imgs = "".join(f'<img src="{src}" alt="{e(alt)}" loading="lazy">'
                       for src, alt in cfg['about_images'])
        gallery = f"""<style>
.about-gallery{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:28px 0}}
.about-gallery img{{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:10px;
  border:1px solid var(--line)}}
@media (max-width:640px){{.about-gallery{{grid-template-columns:repeat(2,1fr)}}}}
</style>
<div class="about-gallery" data-reveal>{imgs}</div>"""
    return (head(cfg, f"About — {cfg['brand']}", cfg['about_desc'], "about.html")
            + header(cfg, "about.html")
            + f"""<section class="pagehead"><div class="wrap" style="max-width:820px">
  <nav class="crumbs"><a href="index.html">Home</a> / <span>About</span></nav>
  <p class="eyebrow">About us</p><h1>{e(cfg['about_h1'])}</h1>
  <div class="muted" style="font-size:1.05rem">{paras}</div>
  {gallery}
  <div class="idcard">
    <h3>Business details</h3>
    <dl>
      <div><dt>Registered name</dt><dd>{e(cfg['company'])}</dd></div>
      {company_no_row(cfg)}
      {address_row(cfg)}
      <div><dt>Email</dt><dd><a href="mailto:{cfg['email']}">{cfg['email']}</a></dd></div>
      {phone_row(cfg)}
    </dl>
  </div>
</div></section>
<section class="band"><div class="wrap">
  <div class="sec-head center" data-reveal><h2>How we operate</h2></div>
  <div class="grid-3">{tiles}</div></div></section>"""
            + cta(cfg) + footer(cfg))


def build_contact(cfg):
    opts = "".join(f'<option>{e(q["name_full"])}</option>' for q in cfg['products'])
    return (head(cfg, f"Contact — {cfg['brand']}",
                 f"Contact {cfg['brand']} about specification, delivery, returns or finance. "
                 f"Email {cfg['email']} or call {cfg['phone']}.", "contact.html")
            + header(cfg, "contact.html")
            + f"""<section class="pagehead"><div class="wrap">
  <nav class="crumbs"><a href="index.html">Home</a> / <span>Contact</span></nav>
  <h1>Contact us</h1>
  <p class="muted" style="max-width:62ch">Questions on specification, access, delivery, returns or
     finance? A specialist replies the same {ph(cfg, 'day_word')}. Lines are open Monday to Friday,
     8am&ndash;6pm.</p>
</div></section>
<section><div class="wrap grid-2" style="align-items:start">
  <div>
    <form class="form" data-demo="Thanks — your enquiry has been noted. A specialist will reply by email within one {ph(cfg, 'day_word')}." novalidate>
      <div class="field"><label for="cname">Your name</label><input id="cname" name="name" required autocomplete="name"></div>
      <div class="field"><label for="cmail">Email</label><input id="cmail" name="email" type="email" required autocomplete="email"></div>
      <div class="field"><label for="cphone">Phone (optional)</label><input id="cphone" name="phone" type="tel" autocomplete="tel"></div>
      <div class="field"><label for="cmachine">Machine</label>
        <select id="cmachine" name="machine">{opts}
          <option>An existing order</option><option>A return or warranty claim</option>
          <option>Not sure yet — help me choose</option></select></div>
      <div class="field"><label for="cmsg">How can we help?</label><textarea id="cmsg" name="message" rows="5" required></textarea></div>
      <button class="btn btn--primary btn--lg" type="submit">Send enquiry</button>
      <p class="formnote">By sending this you agree to our <a href="privacy.html">privacy policy</a>.</p>
    </form>
    <div class="result" role="status"></div>
  </div>
  <div>
    <div class="tile" style="margin-bottom:1rem"><h3>Sales &amp; specification</h3>
      <p><a href="mailto:{cfg['email']}">{cfg['email']}</a><br>
         {phone_anchor(cfg) + "<br>" if phone_anchor(cfg) else ""}
         <span class="muted">Mon&ndash;Fri, 8am&ndash;6pm</span></p></div>
    <div class="tile" style="margin-bottom:1rem"><h3>Orders, returns &amp; parts</h3>
      <p><a href="mailto:{cfg['support_email']}">{cfg['support_email']}</a><br>
         <span class="muted">Replies within one {ph(cfg, 'day_word')}. {ph(cfg, 'parts_dispatch')}</span></p></div>
    <div class="tile"><h3>Registered office</h3>
      <p>{e(cfg['company'])}{"<br>" + e(one_line_address(cfg)) if one_line_address(cfg) else ""}{company_no_line(cfg)}</p>
      <p class="muted" style="font-size:.86rem">Warehouse address &mdash; not a retail showroom.
        Please email before visiting.</p></div>
  </div>
</div></section>""" + footer(cfg))


def build_track(cfg):
    return (head(cfg, f"Track your order — {cfg['brand']}",
                 "Track a delivery and see what each stage means.", "track-order.html")
            + header(cfg, "track-order.html")
            + f"""<section class="pagehead"><div class="wrap" style="max-width:760px">
  <nav class="crumbs"><a href="index.html">Home</a> / <span>Track order</span></nav>
  <h1>Where is my machine?</h1>
  <p class="muted">{ph(cfg, 'track_intro')}</p>
  <form class="form" data-demo="No live order was found for that reference. Email {cfg['support_email']} with your order number and we will trace it the same {ph(cfg, 'day_word')}." style="margin-top:1.6rem" novalidate>
    <div class="field"><label for="ref">Order reference</label>
      <input id="ref" name="ref" placeholder="{cfg['ref_prefix']}-000000" required></div>
    <div class="field"><label for="pc">{ph(cfg, 'track_label')}</label>
      <input id="pc" name="postcode" placeholder="{ph(cfg, 'track_ph')}" required></div>
    <button class="btn btn--primary btn--lg" type="submit">Track order</button>
  </form>
  <div class="result" role="status"></div>
</div></section>
<section class="band"><div class="wrap">
  <div class="sec-head center"><h2>What each stage means</h2></div>
  <div class="steps">
    <div class="step"><h3>Order placed</h3><p>{ph(cfg, 'track_stock')}</p></div>
    <div class="step"><h3>Pre-delivery check</h3><p>Fluids, fasteners and a running test before the crate is sealed.</p></div>
    <div class="step"><h3>With the carrier</h3><p>{ph(cfg, 'track_carrier_step')}</p></div>
    <div class="step"><h3>Delivered</h3><p>Signed for kerbside. Inspect before signing and note any damage.</p></div>
  </div>
  <p class="center muted" style="margin-top:2rem">Still stuck? Email
    <a href="mailto:{cfg['support_email']}">{cfg['support_email']}</a>{or_call(cfg)}.</p>
</div></section>""" + footer(cfg))


def build_feed(cfg):
    """Google Merchant Center product feed (RSS 2.0 + g: namespace)."""
    items = ""
    R = region(cfg)
    for p in cfg['products']:
        d = cfg['domain']
        items += f"""
  <item>
    <g:id>{p['sku']}</g:id>
    <g:title>{e(p['name_full'])}</g:title>
    <g:description>{e(p['meta_desc'])}</g:description>
    <g:link>https://{d}/{p['url']}</g:link>
    <g:image_link>https://{d}/{feed_img(p)}</g:image_link>
    {"".join(f'<g:additional_image_link>https://{d}/{p["dir"]}/{(f[:-4] + ".jpg") if f.endswith(".svg") else f}</g:additional_image_link>' for f, _ in p['images'][1:6])}
    <g:availability>in_stock</g:availability>
    <g:condition>new</g:condition>
    <g:price>{p['price']}.00 {R['currency_code']}</g:price>
    <g:brand>{e(cfg['brand'])}</g:brand>
    <g:mpn>{p['mpn']}</g:mpn>
    <g:identifier_exists>no</g:identifier_exists>
    <g:product_type>{e(p['category'])}</g:product_type>
    <g:google_product_category>{p['gpc']}</g:google_product_category>
    <g:shipping><g:country>{R['country_code']}</g:country><g:service>Standard</g:service><g:price>0.00 {R['currency_code']}</g:price></g:shipping>
{shipping_weight(p)}
  </item>"""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">
<channel>
  <title>{e(cfg['brand'])} product feed</title>
  <link>https://{cfg['domain']}/</link>
  <description>{e(cfg['desc'])}</description>{items}
</channel>
</rss>
"""


def build_catalogue(cfg):
    """The live product list. The basket stores only an item code and a quantity and
       resolves everything else from here, so a renamed, repriced or withdrawn machine
       can never linger in someone's basket at a stale name, price or image."""
    rows = ",\n".join(
        '  "%s": { "name": "%s", "price": %d, "img": "%s", "url": "%s" }'
        % (p["sku"], e(p["name_full"]).replace('"', '\\"'), p["price"], hero_img(p), p["url"])
        for p in cfg["products"])
    return "/* Generated by tools/build_all.py — do not edit by hand. */\nwindow.CATALOGUE = {\n%s\n};\n" % rows


def write_site(cfg, root):
    os.makedirs(root, exist_ok=True)
    pages = {
        "index.html": build_index(cfg), "machines.html": build_machines(cfg),
        "cart.html": build_cart(cfg), "checkout.html": build_checkout(cfg),
        "about.html": build_about(cfg), "contact.html": build_contact(cfg),
        "track-order.html": build_track(cfg), "returns.html": build_returns(cfg),
        "shipping.html": build_shipping(cfg), "payment.html": build_payment(cfg),
        "privacy.html": build_privacy(cfg), "terms.html": build_terms(cfg),
        "admin.html": build_admin(cfg),
    }
    for p in cfg['products']:
        pages[p['url']] = build_product(cfg, p)

    # Remove pages from an earlier build that this one no longer produces,
    # so a renamed product does not leave its old URL live.
    for existing in os.listdir(root):
        if existing.endswith(".html") and existing not in pages:
            os.remove(os.path.join(root, existing))

    for name, content in pages.items():
        open(os.path.join(root, name), "w", encoding="utf-8").write(content)

    open(os.path.join(root, "feed.xml"), "w", encoding="utf-8").write(build_feed(cfg))
    open(os.path.join(root, "assets", "js", "catalogue.js"), "w", encoding="utf-8").write(build_catalogue(cfg))
    open(os.path.join(root, "CNAME"), "w").write(cfg['domain'] + "\n")

    indexable = [n for n in pages if n not in ("cart.html", "checkout.html", "admin.html")]
    today = datetime.date.today().isoformat()
    urls = "".join(f"<url><loc>https://{cfg['domain']}/{n}</loc><lastmod>{today}</lastmod></url>"
                   for n in sorted(indexable))
    open(os.path.join(root, "sitemap.xml"), "w").write(
        f'<?xml version="1.0" encoding="UTF-8"?>'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    open(os.path.join(root, "robots.txt"), "w").write(
        "User-agent: *\nAllow: /\nDisallow: /cart.html\nDisallow: /checkout.html\n"
        "Disallow: /admin.html\n"
        f"Sitemap: https://{cfg['domain']}/sitemap.xml\n")
    return sorted(pages)


def build_admin(cfg):
    """Standalone admin dashboard. Live figures come from the analytics worker;
    without one configured, every panel says so rather than inventing numbers."""
    sym = cur(cfg)
    linkrows = "".join(f"""
      <div class="field">
        <label for="pl-{p['sku']}">{e(p['name'])} <span class="muted">&mdash; {sym}{p['price']:,} &middot; {p['sku']}</span></label>
        <input id="pl-{p['sku']}" data-link="{p['sku']}" type="url"
               placeholder="https://buy.stripe.com/…" autocomplete="off" spellcheck="false"></div>"""
        for p in cfg['products'])

    if us(cfg):
        biz = [("company", "Legal business name"), ("companyNo", "Business registration / EIN (optional)"),
               ("street", "Street address"), ("city", "City"), ("state", "State"),
               ("postcode", "ZIP code"), ("phone", "Phone number")]
    else:
        biz = [("company", "Registered company name"), ("companyNo", "Companies House number"),
               ("street", "Registered address"),
               ("city", "Town or city"), ("postcode", "Postcode"), ("phone", "Phone number")]
    bizrows = "".join(f"""<div class="field"><label for="bz-{k}">{e(l)}</label>
        <input id="bz-{k}" data-biz-field="{k}" autocomplete="off" spellcheck="false"></div>"""
        for k, l in biz)

    tabs = [("live", "Live"), ("orders", "Orders"), ("customers", "Customers"),
            ("abandoned", "Abandoned"), ("insights", "Insights"), ("settings", "Settings")]
    tabbtns = "".join(
        f'<button role="tab" data-tab="{k}" aria-selected="{"true" if i == 0 else "false"}">{e(l)}</button>'
        for i, (k, l) in enumerate(tabs))

    return f"""<!DOCTYPE html>
<html lang="{region(cfg)['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Store admin &mdash; {e(cfg['brand'])}</title>
<meta name="robots" content="noindex,nofollow">
<link rel="icon" href="data:image/svg+xml,{cfg['favicon']}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/admin.css?v={cfg['ver_admin_css']}">
</head>
<body>

<form class="gate" id="gate">
  <h1>Store admin</h1>
  <p>{e(cfg['brand'])} &mdash; {e(cfg['domain'])}</p>
  <div class="field"><label for="pass">Passphrase</label>
    <input id="pass" type="password" autocomplete="current-password"></div>
  <button class="btn btn--primary" type="submit" style="width:100%;justify-content:center">Unlock</button>
  <p class="gmsg" id="gateMsg"></p>
</form>

<div id="app" hidden>
  <header class="abar"><div class="wrap abar__in">
    <div><p class="abrand">{e(cfg['brand'])}</p><p class="atitle">Store admin</p></div>
    <div class="row">
      <a class="btn btn--sm" href="index.html">View store</a>
      <button class="btn btn--sm" id="signout">Sign out</button>
    </div>
  </div></header>

  <div class="wrap">
    <div class="tabs" role="tablist">{tabbtns}</div>

    <div class="notice danger" id="httpWarn" hidden>
      <strong>This store is being served over plain HTTP.</strong> Switch on
      <em>Enforce HTTPS</em> in Settings &rarr; Pages. Customers currently see
      &ldquo;Not secure&rdquo;, and Merchant Center will not approve the store.
    </div>

    <div class="notice" id="noData" hidden>
      <strong>No data source connected, so every figure below is empty rather than made up.</strong>
      This store is static hosting &mdash; it has no server, so it cannot count visitors, hold
      orders or total revenue on its own. Deploy the collector in
      <code>stripe/analytics-worker.js</code> and put its URL in <code>analyticsEndpoint</code>
      on the Settings tab. Setup is in <code>stripe/README.md</code>.
    </div>

    <!-- LIVE -->
    <section data-panel="live">
      <div class="grid g4">
        <div class="card"><p class="stat__l">On the site now</p>
          <p class="stat__v" data-k="active">&mdash;</p><p class="stat__s">Active in the last 5 minutes</p></div>
        <div class="card"><p class="stat__l">Page views (24h)</p>
          <p class="stat__v" data-k="pageViews">&mdash;</p><p class="stat__s">All pages</p></div>
        <div class="card"><p class="stat__l">Checkouts started (24h)</p>
          <p class="stat__v" data-k="checkoutStarted">&mdash;</p><p class="stat__s">Reached checkout</p></div>
        <div class="card"><p class="stat__l">Revenue (24h)</p>
          <p class="stat__v" data-k="revenue">&mdash;</p><p class="stat__s"><span data-k="orders">0</span> orders</p></div>
      </div>

      <div class="card" style="margin-top:1rem">
        <div class="card__h"><h2>Conversion funnel &mdash; last 24 hours</h2>
          <button class="btn btn--sm" id="refresh">Refresh</button></div>
        <div class="funnel">
          <div class="fstep"><b data-k="pageViews">&mdash;</b><span>Page views</span></div>
          <div class="fstep"><b data-k="productViews">&mdash;</b><span>Product views</span></div>
          <div class="fstep"><b data-k="addToCart">&mdash;</b><span>Add to basket</span></div>
          <div class="fstep"><b data-k="checkoutStarted">&mdash;</b><span>Checkout started</span></div>
          <div class="fstep"><b data-k="purchased">&mdash;</b><span>Purchased</span></div>
        </div>
        <div class="frates">
          <span>View &rarr; basket: <b data-k="r1">&mdash;</b></span>
          <span>Basket &rarr; checkout: <b data-k="r2">&mdash;</b></span>
          <span>Checkout &rarr; paid: <b data-k="r3">&mdash;</b></span>
        </div>
      </div>

      <div class="grid g2" style="margin-top:1rem">
        <div class="card"><div class="card__h"><h2>Visitors right now</h2></div>
          <div id="visitors"><p class="empty">Nobody browsing at the moment.</p></div></div>
        <div class="card"><div class="card__h"><h2>Latest activity</h2></div>
          <div class="feed" id="feed"><p class="empty">No activity recorded.</p></div></div>
      </div>
    </section>

    <!-- ORDERS -->
    <section data-panel="orders" hidden>
      <div class="card">
        <div class="card__h"><h2>Orders</h2>
          <a class="btn btn--sm" href="https://dashboard.stripe.com/payments" target="_blank" rel="noopener">Open in Stripe</a></div>
        <div id="ordersBody"><p class="empty">No orders to show.</p></div>
        <p class="muted" style="font-size:.8rem;margin-top:1rem">Stripe is the record of every
          payment, refund and payout. This table mirrors it; the Dashboard is authoritative.</p>
      </div>
    </section>

    <!-- CUSTOMERS -->
    <section data-panel="customers" hidden>
      <div class="card"><div class="card__h"><h2>Customers</h2></div>
        <div id="customersBody"><p class="empty">No customers yet.</p></div></div>
    </section>

    <!-- ABANDONED -->
    <section data-panel="abandoned" hidden>
      <div class="card"><div class="card__h"><h2>Abandoned baskets (7 days)</h2></div>
        <div id="abandonedBody"><p class="empty">No abandoned baskets recorded.</p></div>
        <p class="muted" style="font-size:.8rem;margin-top:1rem">A basket counts as abandoned once
          checkout was reached but no payment followed within an hour.</p></div>
    </section>

    <!-- INSIGHTS -->
    <section data-panel="insights" hidden>
      <div class="card"><div class="card__h"><h2>Machines by interest (7 days)</h2></div>
        <div id="insightsBody"><p class="empty">No product data yet.</p></div></div>
    </section>

    <!-- SETTINGS -->
    <section data-panel="settings" hidden>
      <div class="card">
        <h3 class="sec">Stripe Payment Links</h3>
        <p class="sub">One per machine. Create them in the Stripe Dashboard with shipping address
          collection and adjustable quantity on, and tax behaviour set to <em>inclusive</em>.
          Leave one blank and that machine routes to an enquiry instead of taking payment.</p>
        {linkrows}

        <h3 class="sec">Business identity</h3>
        <p class="sub">Shown in the footer of every page. Google Merchant Center and Stripe both
          {"check these against your real business details." if us(cfg) else
           "verify these against Companies House, so they must be your real details."}</p>
        <div class="f2">{bizrows}</div>

        <h3 class="sec">Data collector</h3>
        <p class="sub">URL of the analytics worker that feeds the tabs above, and of the optional
          checkout endpoint for baskets holding more than one machine.</p>
        <div class="field"><label for="an-ep">Analytics endpoint</label>
          <input id="an-ep" data-cfg="analyticsEndpoint" type="url" placeholder="https://…workers.dev" spellcheck="false"></div>
        <div class="field"><label for="ck-ep">Checkout endpoint (optional)</label>
          <input id="ck-ep" data-cfg="checkoutEndpoint" type="url" placeholder="https://…workers.dev/checkout" spellcheck="false"></div>

        <h3 class="sec">Save</h3>
        <p class="sub">This produces <code>assets/js/site-config.js</code>. Copy it, replace that file
          on GitHub, and commit. The site picks it up on the next load &mdash; no rebuild needed.
          <strong>Never put a Stripe secret key in it.</strong></p>
        <div class="row" style="margin-bottom:.8rem">
          <button class="btn btn--primary" id="copyBtn" type="button">Copy file contents</button>
          <button class="btn" id="dlBtn" type="button">Download</button>
          <span class="muted" id="saveMsg" style="font-size:.83rem"></span>
        </div>
        <textarea class="out" id="out" rows="16" readonly spellcheck="false"></textarea>

        <h3 class="sec">Change the passphrase</h3>
        <p class="sub">This gate runs in the browser and anyone can read past it &mdash; it keeps a
          casual visitor out, nothing more. Nothing here is confidential; committing to GitHub is
          what actually authorises a change.</p>
        <div class="row">
          <input id="newpass" placeholder="New passphrase" spellcheck="false"
                 style="flex:1;min-width:220px;padding:.6rem .75rem;border:1px solid var(--line);border-radius:8px">
          <button class="btn" id="hashBtn" type="button">Show hash</button>
        </div>
        <p class="muted" id="hashOut" style="font-family:ui-monospace,monospace;font-size:.8rem;margin-top:.6rem"></p>
      </div>
    </section>
  </div>
  <div style="height:3rem"></div>
</div>

<script src="assets/js/site-config.js?v={cfg['ver_stripe']}"></script>
<script src="assets/js/admin.js?v={cfg['ver_admin_js']}"></script>
</body>
</html>
"""
