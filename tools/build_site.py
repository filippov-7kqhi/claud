# -*- coding: utf-8 -*-
"""Static-store builder. Four products per store, built to Google Merchant Center rules."""
import os, html, datetime

def e(t): return html.escape(str(t), quote=True)

PRICE_VALID = (datetime.date.today() + datetime.timedelta(days=365)).isoformat()

# Pages that must carry policy links in the footer (GMC checks home, product, cart, checkout).
NAV = [("Machines", "machines.html"), ("About", "about.html"),
       ("Contact", "contact.html"), ("Track Order", "track-order.html")]

POLICY_LINKS = [("Delivery & shipping", "shipping.html"), ("Returns & refunds", "returns.html"),
                ("Payment & billing", "payment.html"), ("Warranty", "returns.html#warranty"),
                ("Privacy", "privacy.html"), ("Terms & conditions", "terms.html")]


def head(cfg, title, desc, path, extra="", noindex=False):
    canon = f"https://{cfg['domain']}/{path}"
    robots = '<meta name="robots" content="noindex,nofollow">' if noindex else ""
    return f"""<!DOCTYPE html>
<html lang="en-GB">
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
<meta property="og:image" content="https://{cfg['domain']}/{cfg['products'][0]['dir']}/01-hero.svg">
<meta property="og:locale" content="en_GB">
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
    return f"""<script type="application/ld+json">{{
 "@context":"https://schema.org","@type":"OnlineStore","name":"{e(cfg['brand'])}",
 "url":"https://{cfg['domain']}/","email":"{cfg['email']}","telephone":"{cfg['phone']}",
 "address":{{"@type":"PostalAddress","streetAddress":"{e(cfg['street'])}",
   "addressLocality":"{e(cfg['city'])}","postalCode":"{e(cfg['postcode'])}","addressCountry":"GB"}},
 "currenciesAccepted":"GBP","paymentAccepted":"Visa, Mastercard, American Express, PayPal",
 "areaServed":"GB"
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
          <strong style="color:var(--ink)" data-biz="company">{e(cfg['company'])}</strong><br>
          <span data-biz="street">{e(cfg['street'])}</span><br>
          <span data-biz="city">{e(cfg['city'])}</span> <span data-biz="postcode">{e(cfg['postcode'])}</span><br>
          United Kingdom<br>
          <a href="mailto:{cfg['email']}">{cfg['email']}</a><br>
          <a href="tel:{cfg['phone_link']}" data-biz="phone">{e(cfg['phone'])}</a><br>
          <span class="muted">Company no. <span data-biz="companyNo">{e(cfg['company_no'])}</span>
            &middot; VAT no. <span data-biz="vatNo">{e(cfg['vat_no'])}</span></span>
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
      <span class="paychip">VISA</span><span class="paychip">Mastercard</span>
      <span class="paychip">AmEx</span><span class="paychip">PayPal</span>
      <span class="paychip">Apple&nbsp;Pay</span>
    </div>
    <div class="footer__bot">
      <span>&copy; <span data-year></span> <span data-biz="company">{e(cfg['company'])}</span>. All rights reserved.</span>
      <span>All prices in GBP and include UK VAT at 20%. {e(cfg['brand'])} is an independent
        supplier and is not affiliated with any equipment manufacturer.</span>
    </div>
  </div>
</footer>
<script src="assets/js/site-config.js?v={cfg['ver_stripe']}"></script>
<script src="assets/js/script.js?v={cfg['ver_js']}"></script>
</body>
</html>
"""


# ------------------------------------------------------------------ blocks ---
def product_card(p, featured=False):
    bullets = "".join(f"<li>{e(b)}</li>" for b in p['bullets'][:3])
    return f"""<article class="card" data-reveal>
  <div class="card__media">
    <span class="card__tag">{e(p['tag'])}</span>
    <a href="{p['url']}"><img src="{p['dir']}/01-hero.svg" width="1200" height="760"
       alt="{e(p['name_full'])}" loading="lazy"></a>
  </div>
  <div class="card__body">
    <h3><a href="{p['url']}">{e(p['name'])}</a></h3>
    <p class="muted" style="font-size:.93rem;margin:0">{e(p['short_desc'])}</p>
    <ul>{bullets}</ul>
    <div class="card__price"><b>&pound;{p['price']:,}</b><s>&pound;{p['was']:,}</s>
      <span class="incvat">inc. VAT</span></div>
    <div class="card__actions">
      <a class="btn btn--primary btn--block" href="{p['url']}">View machine</a>
      <button class="btn btn--ghost btn--block" data-add="{p['sku']}"
        data-name="{e(p['name_full'])}" data-price="{p['price']}"
        data-img="{p['dir']}/01-hero.svg" data-url="{p['url']}">Add to basket</button>
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
      <img src="{p['dir']}/01-hero.svg" width="1200" height="760"
           alt="{e(p['name_full'])} — {e(p['short_desc'])}">
    </div>
  </div>
</section>"""


def range_section(cfg, heading=None, lead=None):
    cards = "".join(product_card(p) for p in cfg['products'])
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
    <p class="muted">Your statutory rights under UK consumer law, and the terms we add on top.
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
    return (head(cfg, f"All machines — {cfg['brand']}",
                 f"All four {cfg['brand']} machines: wood chipper, stump grinder, tracked dumper and "
                 f"compact loader. UK stock, free mainland delivery.", "machines.html")
            + header(cfg, "machines.html")
            + f"""<section class="pagehead"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / <span>Machines</span></nav>
  <h1>All four machines</h1>
  <p class="muted" style="max-width:64ch">Every machine below is held in UK stock, ships crated on a
     tail-lift vehicle, and carries the same delivery, returns and warranty terms. Prices include VAT.</p>
</div></section>"""
            + range_section(cfg, "The full range", cfg['range_lead']) + cta(cfg) + footer(cfg))


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
    feats = "".join(f'<div class="tile" data-reveal><h3>{e(t)}</h3><p>{e(d)}</p></div>'
                    for t, d in p['features'])
    others = "".join(product_card(q) for q in cfg['products'] if q['sku'] != p['sku'])

    ld = f"""<script type="application/ld+json">{{
 "@context":"https://schema.org","@type":"Product",
 "name":"{e(p['name_full'])}",
 "image":[{",".join(f'"https://{cfg["domain"]}/{p["dir"]}/{f}"' for f, _ in p['images'][:4])}],
 "description":"{e(p['meta_desc'])}",
 "sku":"{p['sku']}","mpn":"{p['mpn']}",
 "brand":{{"@type":"Brand","name":"{e(cfg['brand'])}"}},
 "offers":{{"@type":"Offer","url":"https://{cfg['domain']}/{p['url']}",
   "priceCurrency":"GBP","price":"{p['price']}","priceValidUntil":"{PRICE_VALID}",
   "availability":"https://schema.org/InStock","itemCondition":"https://schema.org/NewCondition",
   "seller":{{"@type":"Organization","name":"{e(cfg['company'])}"}},
   "shippingDetails":{{"@type":"OfferShippingDetails",
     "shippingRate":{{"@type":"MonetaryAmount","value":"0","currency":"GBP"}},
     "shippingDestination":{{"@type":"DefinedRegion","addressCountry":"GB"}},
     "deliveryTime":{{"@type":"ShippingDeliveryTime",
       "handlingTime":{{"@type":"QuantitativeValue","minValue":1,"maxValue":2,"unitCode":"DAY"}},
       "transitTime":{{"@type":"QuantitativeValue","minValue":2,"maxValue":5,"unitCode":"DAY"}}}}}},
   "hasMerchantReturnPolicy":{{"@type":"MerchantReturnPolicy",
     "applicableCountry":"GB","returnPolicyCategory":"https://schema.org/MerchantReturnFiniteReturnWindow",
     "merchantReturnDays":30,"returnMethod":"https://schema.org/ReturnByMail",
     "returnFees":"https://schema.org/ReturnShippingFees",
     "returnShippingFeesAmount":{{"@type":"MonetaryAmount","value":"{cfg['return_fee']}","currency":"GBP"}}}}}}
}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
 {{"@type":"ListItem","position":1,"name":"Home","item":"https://{cfg['domain']}/"}},
 {{"@type":"ListItem","position":2,"name":"Machines","item":"https://{cfg['domain']}/machines.html"}},
 {{"@type":"ListItem","position":3,"name":"{e(p['name'])}"}}]}}</script>"""

    return (head(cfg, f"{p['name_full']} — £{p['price']:,} inc. VAT", p['meta_desc'], p['url'], ld)
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
    <span class="stockline"><i class="dot"></i>In stock &mdash; dispatched in 1&ndash;2 working days</span>
    <h1>{e(p['name_full'])}</h1>
    <p class="muted">{e(p['lede'])}</p>

    <div class="priceblock">
      <div class="priceblock__row">
        <span class="price">&pound;{p['price']:,}</span>
        <s class="was">&pound;{p['was']:,}</s>
        <span class="save">SAVE {round((1-p['price']/p['was'])*100)}%</span>
      </div>
      <p class="vatline">Price includes UK VAT at 20% (&pound;{round(p['price']-p['price']/1.2):,})
         and free delivery to the UK mainland.</p>
      <p class="vatline">Item code {p['sku']} &middot; new, unregistered, UK stock</p>
    </div>

    <div class="specgrid">{specs_hi}</div>

    <div class="buyrow">
      <label class="qty"><span class="sr">Quantity</span>
        <input type="number" id="qty" value="1" min="1" max="5" inputmode="numeric"></label>
      <button class="btn btn--primary btn--lg btn--grow" data-add="{p['sku']}" data-buynow
        data-name="{e(p['name_full'])}" data-price="{p['price']}"
        data-img="{p['dir']}/01-hero.svg" data-url="{p['url']}" data-qty="#qty">
        Buy now &mdash; &pound;{p['price']:,}</button>
    </div>
    <button class="btn btn--ghost btn--lg btn--block" style="margin-top:.7rem" data-add="{p['sku']}"
      data-name="{e(p['name_full'])}" data-price="{p['price']}"
      data-img="{p['dir']}/01-hero.svg" data-url="{p['url']}" data-qty="#qty">Add to basket</button>
    <p class="added" data-added hidden>Added to your basket. <a href="cart.html">View basket</a></p>
    <p class="buynote">Buy now takes you straight to checkout with this machine in your basket.</p>

    <ul class="delivery-summary">
      <li><strong>Delivery:</strong> free to UK mainland, 3&ndash;7 working days.
        <a href="shipping.html">Delivery details</a></li>
      <li><strong>Returns:</strong> 30 days from delivery. Collection from &pound;{cfg['return_fee']}
        unless faulty. <a href="returns.html">Returns policy</a></li>
      <li><strong>Warranty:</strong> 2 years parts, 1 year engine.
        <a href="returns.html#warranty">Warranty terms</a></li>
      <li><strong>Payment:</strong> card, PayPal or Apple Pay at checkout.
        <a href="payment.html">Payment terms</a></li>
    </ul>

    <ul class="keypoints">{bullets}</ul>
  </div>
</div></div></section>

<section class="band"><div class="wrap">
  <div class="sec-head" data-reveal><p class="eyebrow">Built for the job</p><h2>{e(p['features_h2'])}</h2></div>
  <div class="grid-3">{feats}</div>
</div></section>

<section><div class="wrap" style="max-width:900px">
  <div class="sec-head" data-reveal><p class="eyebrow">Full specification</p>
    <h2>{e(p['short'])} technical data</h2></div>
  <table class="spectable" data-reveal><tbody>{rows}</tbody></table>
  <p class="formnote" style="margin-top:1rem">Specifications are nominal and may vary slightly by
     production batch. Shipping weight {p['weight_kg']} kg, crated {p['box']}.</p>
</div></section>

{faq_block(p['faq'], 'About the ' + p['short'])}

<section><div class="wrap">
  <div class="sec-head center"><p class="eyebrow">The rest of the range</p><h2>Also available</h2></div>
  <div class="grid-3 cards">{others}</div>
</div></section>

<div class="stickybuy">
  <div><b>&pound;{p['price']:,}</b> <span class="muted" style="font-size:.8rem">inc. VAT</span></div>
  <div class="stickybuy__btns">
    <button class="btn btn--ghost" data-add="{p['sku']}" data-name="{e(p['name_full'])}"
      data-price="{p['price']}" data-img="{p['dir']}/01-hero.svg" data-url="{p['url']}">Basket</button>
    <button class="btn btn--primary" data-add="{p['sku']}" data-buynow data-name="{e(p['name_full'])}"
      data-price="{p['price']}" data-img="{p['dir']}/01-hero.svg" data-url="{p['url']}">Buy now</button>
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
    <div id="cartItems" class="cartitems"></div>
    <p id="cartEmpty" class="empty">Your basket is empty.
       <a href="machines.html">Browse the four machines</a>.</p>
  </div>
  <aside class="summary" id="cartSummary" hidden>
    <h2>Order summary</h2>
    <dl>
      <div><dt>Subtotal (ex. VAT)</dt><dd data-sum-net>&pound;0</dd></div>
      <div><dt>VAT at 20%</dt><dd data-sum-vat>&pound;0</dd></div>
      <div><dt>Delivery (UK mainland)</dt><dd>Free</dd></div>
      <div class="total"><dt>Total to pay</dt><dd data-sum-total>&pound;0</dd></div>
    </dl>
    <a class="btn btn--primary btn--block btn--lg" href="checkout.html">Proceed to checkout</a>
    <p class="formnote">Delivery is free to the UK mainland. Northern Ireland, the Highlands and
      Islands and the Channel Islands are quoted separately &mdash;
      <a href="shipping.html">see delivery</a>.</p>
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
        <li>A VAT invoice is emailed with your dispatch confirmation</li>
      </ul>
    </div>
    <p class="formnote">Questions before you pay? Email
      <a href="mailto:{cfg['email']}">{cfg['email']}</a> or call
      <a href="tel:{cfg['phone_link']}">{e(cfg['phone'])}</a>.</p>
  </div>
  <aside class="summary">
    <h2>Order summary</h2>
    <dl>
      <div><dt>Subtotal (ex. VAT)</dt><dd data-sum-net>&pound;0</dd></div>
      <div><dt>VAT at 20%</dt><dd data-sum-vat>&pound;0</dd></div>
      <div><dt>Delivery (UK mainland)</dt><dd>Free</dd></div>
      <div class="total"><dt>Total to pay</dt><dd data-sum-total>&pound;0</dd></div>
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
          "<p><strong>Dispatch:</strong> 1&ndash;2 working days from cleared payment. Orders placed "
          "before 2pm on a working day are picked the same day.</p>"
          "<p><strong>Transit:</strong> 2&ndash;5 working days on the UK mainland, so "
          "<strong>3&ndash;7 working days from order to doorstep</strong>. Off-mainland addresses add "
          "3&ndash;5 working days.</p>"
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
    return _policy_page(cfg, "payment.html", "Payment & billing",
        "Accepted payment methods, currency, VAT, invoicing and finance.",
        "All prices on this site are in pounds sterling and include UK VAT at 20%. What you see is "
        "what you pay &mdash; we add nothing at checkout.",
        [("methods", "How you can pay",
          "<p>We accept Visa, Mastercard and American Express credit and debit cards, PayPal, "
          "Apple&nbsp;Pay and Google&nbsp;Pay.</p>"
          "<p>Card payments are processed by our payment provider on their own secure, PCI-DSS "
          "compliant systems. <strong>Card numbers are never entered on this website and are never "
          "stored by us</strong> &mdash; we receive only a confirmation that payment succeeded.</p>"
          "<p>Bank transfer is available for orders over &pound;5,000 and for trade accounts; email "
          f"<a href='mailto:{cfg['email']}'>{cfg['email']}</a> and we will issue a proforma invoice.</p>"),
         ("vat", "VAT and invoicing",
          f"<p>{e(cfg['company'])} is registered for VAT in the United Kingdom under number "
          f"<strong>{e(cfg['vat_no'])}</strong>. Every displayed price includes VAT at the prevailing "
          "standard rate of 20%.</p>"
          "<p>A full VAT invoice is emailed with your dispatch confirmation and a paper copy travels "
          "in the crate. VAT-registered businesses can reclaim the VAT element in the normal way.</p>"),
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
          "<p><strong>To meet legal duties</strong> &mdash; legal obligation, mainly keeping VAT and "
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
         ("cookies", "Cookies",
          "<p>This site sets <strong>no advertising, analytics or tracking cookies</strong>. Your "
          "basket is held in your own browser using local storage, which never leaves your device and "
          "is not readable by us. Clearing your browser data clears your basket.</p>"
          "<p>If we add analytics later, this page will be updated first and you will be asked to "
          "consent before any non-essential cookie is set.</p>"),
         ("rights", "Your rights",
          "<p>Under UK GDPR you may ask for a copy of your data, ask us to correct or delete it, "
          "object to or restrict how we use it, ask for it in a portable format, and withdraw consent "
          "at any time.</p>"
          f"<p>Email <a href='mailto:{cfg['support_email']}'>{cfg['support_email']}</a> and we will "
          "respond within one month, free of charge. If you are unhappy with our response you can "
          "complain to the Information Commissioner's Office at ico.org.uk or on 0303 123 1113.</p>")])


def build_terms(cfg):
    return _policy_page(cfg, "terms.html", "Terms & conditions",
        "The terms on which we sell machines through this website.",
        "These terms govern every order placed through this website. Please read them before you buy. "
        "Nothing here limits your statutory rights.",
        [("who", "Who you are buying from",
          f"<p>You are buying from <strong>{e(cfg['company'])}</strong>, a company registered in "
          f"England and Wales, company number {e(cfg['company_no'])}, VAT number {e(cfg['vat_no'])}, "
          f"registered office {e(cfg['street'])}, {e(cfg['city'])} {e(cfg['postcode'])}.</p>"
          f"<p>Contact us at <a href='mailto:{cfg['email']}'>{cfg['email']}</a> or "
          f"<a href='tel:{cfg['phone_link']}'>{e(cfg['phone'])}</a>.</p>"
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
          "<p>Prices are in pounds sterling and include UK VAT at 20%. The price you see when you "
          "place the order is the price you pay; we do not add fees at checkout.</p>"
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
    return (head(cfg, f"About — {cfg['brand']}", cfg['about_desc'], "about.html")
            + header(cfg, "about.html")
            + f"""<section class="pagehead"><div class="wrap" style="max-width:820px">
  <nav class="crumbs"><a href="index.html">Home</a> / <span>About</span></nav>
  <p class="eyebrow">About us</p><h1>{e(cfg['about_h1'])}</h1>
  <div class="muted" style="font-size:1.05rem">{paras}</div>
  <div class="idcard">
    <h3>Business details</h3>
    <dl>
      <div><dt>Registered name</dt><dd>{e(cfg['company'])}</dd></div>
      <div><dt>Company number</dt><dd>{e(cfg['company_no'])}</dd></div>
      <div><dt>VAT number</dt><dd>{e(cfg['vat_no'])}</dd></div>
      <div><dt>Registered office</dt><dd>{e(cfg['street'])}, {e(cfg['city'])} {e(cfg['postcode'])}, United Kingdom</dd></div>
      <div><dt>Email</dt><dd><a href="mailto:{cfg['email']}">{cfg['email']}</a></dd></div>
      <div><dt>Telephone</dt><dd><a href="tel:{cfg['phone_link']}">{e(cfg['phone'])}</a></dd></div>
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
     finance? A specialist replies the same working day. Lines are open Monday to Friday,
     8am&ndash;6pm.</p>
</div></section>
<section><div class="wrap grid-2" style="align-items:start">
  <div>
    <form class="form" data-demo="Thanks — your enquiry has been noted. A specialist will reply by email within one working day." novalidate>
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
         <a href="tel:{cfg['phone_link']}">{e(cfg['phone'])}</a><br>
         <span class="muted">Mon&ndash;Fri, 8am&ndash;6pm</span></p></div>
    <div class="tile" style="margin-bottom:1rem"><h3>Orders, returns &amp; parts</h3>
      <p><a href="mailto:{cfg['support_email']}">{cfg['support_email']}</a><br>
         <span class="muted">Replies within one working day. Parts dispatched from the UK in 48 hours.</span></p></div>
    <div class="tile"><h3>Registered office</h3>
      <p>{e(cfg['company'])}<br>{e(cfg['street'])}<br>{e(cfg['city'])} {e(cfg['postcode'])}<br>United Kingdom<br>
      <span class="muted">Company no. {e(cfg['company_no'])}<br>VAT no. {e(cfg['vat_no'])}</span></p>
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
  <p class="muted">Enter the reference from your confirmation email. Crated machines move on a
     tail-lift vehicle, so the carrier calls to book a slot before delivery.</p>
  <form class="form" data-demo="No live order was found for that reference. Email {cfg['support_email']} with your order number and we will trace it the same working day." style="margin-top:1.6rem" novalidate>
    <div class="field"><label for="ref">Order reference</label>
      <input id="ref" name="ref" placeholder="{cfg['ref_prefix']}-000000" required></div>
    <div class="field"><label for="pc">Delivery postcode</label>
      <input id="pc" name="postcode" placeholder="SW1A 1AA" required></div>
    <button class="btn btn--primary btn--lg" type="submit">Track order</button>
  </form>
  <div class="result" role="status"></div>
</div></section>
<section class="band"><div class="wrap">
  <div class="sec-head center"><h2>What each stage means</h2></div>
  <div class="steps">
    <div class="step"><h3>Order placed</h3><p>Payment cleared and your machine allocated from UK stock.</p></div>
    <div class="step"><h3>Pre-delivery check</h3><p>Fluids, fasteners and a running test before the crate is sealed.</p></div>
    <div class="step"><h3>With the carrier</h3><p>Booked onto a tail-lift vehicle. You get a call to agree a slot.</p></div>
    <div class="step"><h3>Delivered</h3><p>Signed for kerbside. Inspect before signing and note any damage.</p></div>
  </div>
  <p class="center muted" style="margin-top:2rem">Still stuck? Email
    <a href="mailto:{cfg['support_email']}">{cfg['support_email']}</a> or call
    <a href="tel:{cfg['phone_link']}">{e(cfg['phone'])}</a>.</p>
</div></section>""" + footer(cfg))


def build_feed(cfg):
    """Google Merchant Center product feed (RSS 2.0 + g: namespace)."""
    items = ""
    for p in cfg['products']:
        d = cfg['domain']
        items += f"""
  <item>
    <g:id>{p['sku']}</g:id>
    <g:title>{e(p['name_full'])}</g:title>
    <g:description>{e(p['meta_desc'])}</g:description>
    <g:link>https://{d}/{p['url']}</g:link>
    <g:image_link>https://{d}/{p['dir']}/01-hero.svg</g:image_link>
    {"".join(f'<g:additional_image_link>https://{d}/{p["dir"]}/{f}</g:additional_image_link>' for f, _ in p['images'][1:6])}
    <g:availability>in_stock</g:availability>
    <g:condition>new</g:condition>
    <g:price>{p['price']}.00 GBP</g:price>
    <g:brand>{e(cfg['brand'])}</g:brand>
    <g:mpn>{p['mpn']}</g:mpn>
    <g:identifier_exists>no</g:identifier_exists>
    <g:product_type>{e(p['category'])}</g:product_type>
    <g:google_product_category>{p['gpc']}</g:google_product_category>
    <g:shipping><g:country>GB</g:country><g:service>Standard</g:service><g:price>0.00 GBP</g:price></g:shipping>
    <g:shipping_weight>{p['weight_kg']} kg</g:shipping_weight>
    <g:tax><g:country>GB</g:country><g:rate>20</g:rate><g:tax_ship>n</g:tax_ship></g:tax>
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

    for name, content in pages.items():
        open(os.path.join(root, name), "w", encoding="utf-8").write(content)

    open(os.path.join(root, "feed.xml"), "w", encoding="utf-8").write(build_feed(cfg))
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
    """Config editor. Deliberately holds nothing secret — see the notice on the page."""
    rows = "".join(f"""
      <div class="field">
        <label for="pl-{p['sku']}">{e(p['name'])} <span class="muted">— &pound;{p['price']:,} · {p['sku']}</span></label>
        <input id="pl-{p['sku']}" data-link="{p['sku']}" type="url" placeholder="https://buy.stripe.com/…"
               autocomplete="off" spellcheck="false">
      </div>""" for p in cfg['products'])

    biz = [("company", "Registered company name"), ("companyNo", "Companies House number"),
           ("vatNo", "VAT registration number"), ("street", "Registered address"),
           ("city", "Town or city"), ("postcode", "Postcode"), ("phone", "Phone number")]
    bizrows = "".join(f"""
      <div class="field"><label for="bz-{k}">{e(label)}</label>
        <input id="bz-{k}" data-biz-field="{k}" autocomplete="off" spellcheck="false"></div>""" for k, label in biz)

    return (head(cfg, f"Admin — {cfg['brand']}", "Store configuration.", "admin.html", noindex=True)
            + header(cfg)
            + f"""<section class="pagehead"><div class="wrap" style="max-width:860px">
  <h1>Store admin</h1>
  <div class="warnbox">
    <strong>Read this once.</strong> This page is a <em>configuration editor</em>, not a
    control panel. It cannot change the live site on its own: it produces a file that you
    commit to GitHub, and your GitHub login is what actually authorises the change.
    <br><br>
    The passphrase below only hides the form from a casual visitor. This is a static site,
    so the check runs in your browser and anyone can read it or skip it. Nothing on this
    page is confidential &mdash; Payment Links, business details and prices are all public
    anyway. <strong>Never put a Stripe secret key here or anywhere in the repository.</strong>
  </div>
</div></section>

<section><div class="wrap" style="max-width:860px">
  <form id="gate" class="form" style="max-width:420px">
    <div class="field"><label for="pass">Passphrase</label>
      <input id="pass" type="password" autocomplete="current-password"></div>
    <button class="btn btn--primary btn--lg" type="submit">Unlock</button>
    <p class="formnote" id="gateMsg"></p>
  </form>

  <div id="panel" hidden>
    <h2>Stripe Payment Links</h2>
    <p class="muted">One per machine. Create them in the Stripe Dashboard under
      <em>Payment Links</em>, with shipping address collection and adjustable quantity
      switched on, and tax behaviour set to <em>inclusive</em>. Leave one blank and that
      machine routes to an enquiry instead.</p>
    <form class="form">{rows}</form>

    <h2 style="margin-top:2.4rem">Business identity</h2>
    <p class="muted">Shown in the footer of every page. Google Merchant Center and Stripe
      both verify these against Companies House, so they must be your real details.</p>
    <form class="form">{bizrows}</form>

    <h2 style="margin-top:2.4rem">Save your changes</h2>
    <p class="muted">This produces the contents of <code>assets/js/site-config.js</code>.
      Copy it, open that file on GitHub, replace everything, and commit. The site picks it
      up on the next load — no rebuild needed.</p>
    <div class="btnrow">
      <button class="btn btn--primary btn--lg" id="copyBtn" type="button">Copy file contents</button>
      <button class="btn btn--ghost btn--lg" id="dlBtn" type="button">Download file</button>
    </div>
    <p class="formnote" id="saveMsg"></p>
    <textarea id="out" class="outbox" rows="18" readonly spellcheck="false"></textarea>

    <h2 style="margin-top:2.4rem">Where everything else lives</h2>
    <ul class="adminlinks">
      <li><strong>Orders, refunds and payouts</strong> —
        <a href="https://dashboard.stripe.com/payments" target="_blank" rel="noopener">Stripe Dashboard</a>.
        A static site cannot hold order data; Stripe is your order admin.</li>
      <li><strong>Product feed status</strong> —
        <a href="https://merchants.google.com/" target="_blank" rel="noopener">Google Merchant Center</a>.</li>
      <li><strong>Prices, specs, copy and images</strong> — these are built into the pages.
        Ask for a change and it ships as a commit.</li>
      <li><strong>Changing this passphrase</strong> — paste a new one below to get its hash,
        then replace <code>admin.passHash</code> in the file above.</li>
    </ul>
    <form class="form" style="max-width:420px" id="hashForm">
      <div class="field"><label for="newpass">New passphrase</label>
        <input id="newpass" type="text" autocomplete="off" spellcheck="false"></div>
      <button class="btn btn--ghost" type="submit">Show hash</button>
      <p class="formnote" id="hashOut"></p>
    </form>
  </div>
</div></section>""" + footer(cfg))
