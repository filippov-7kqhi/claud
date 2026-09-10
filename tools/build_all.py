import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_site import write_site
from products import for_store
import cfg_branchforge, cfg_haulcrest, cfg_rootvexx, cfg_lawnstride
import theme
import hashlib, re


CONFIG_TEMPLATE = """\
/* ---------------------------------------------------------------------------
   Runtime configuration for {brand}. Edited through /admin.html, or by hand.

   THIS FILE IS PUBLIC. Everything in it ships to every visitor.
   Payment Link URLs, business details and the admin hash are all fine to publish.
   A Stripe SECRET key (sk_live_... / sk_test_...) is NOT. Never put one here.
--------------------------------------------------------------------------- */
window.SITE_CONFIG = {{
  // SHA-256 of the admin passphrase. This only hides the form from a casual
  // visitor -- anyone can read this file and bypass it. Nothing behind it is
  // secret; the real gate on changing the live site is your GitHub login.
  admin: {{ passHash: "{passhash}" }},

  // Shown in the footer of every page. Google and Stripe both verify these.
  business: {{
    company:   "",
    companyNo: "",
    vatNo:     "",
    street:    "",
    city:      "",
    postcode:  "",
    phone:     ""
  }},

  // Data collector that feeds the admin dashboard. Without it the dashboard
  // shows nothing rather than inventing figures. See stripe/README.md.
  analyticsEndpoint: "",

  // Optional: Checkout Sessions for baskets with more than one machine.
  checkoutEndpoint: "",

  // One Stripe Payment Link per machine. Blank = that machine routes to an
  // enquiry instead of pretending to take payment.
  paymentLinks: {{
{links}
  }}
}};
"""

ADMIN_PASS_HASH = "5b9e9741342f4f8a87a03b52634853031e9478d49220cadd57e189392e0b7bb3"


def write_site_config(cfg, root):
    """Never overwrites anything the owner has filled in. A file where every
       value is still blank is regenerated, so a store that changes its range
       gets a payment-link slot per machine it actually sells."""
    path = f"{root}/assets/js/site-config.js"
    links = "\n".join(
        f'    "{p["sku"]}": "",{" " * max(1, 14 - len(p["sku"]))}// {p["name"]} - GBP {p["price"]:,}'
        for p in cfg["products"])
    body = CONFIG_TEMPLATE.format(brand=cfg["brand"], links=links, passhash=ADMIN_PASS_HASH)

    if os.path.exists(path):
        cur = open(path).read()
        skus = [p["sku"] for p in cfg["products"]]
        if all(f'"{s}"' in cur for s in skus):
            return "kept"
        # values the owner may have set: anything between quotes after a colon,
        # excluding the admin hash which we write ourselves
        filled = [v for k, v in re.findall(r'(\w+):\s*"([^"]*)"', cur)
                  if v and k != "passHash"]
        if filled:
            print(f"  ! {cfg['brand']}: site-config.js lists a different range but has "
                  f"values set. Left alone -- add slots for {', '.join(skus)} by hand.")
            return "kept (stale range)"
        open(path, "w").write(body)
        return "regenerated"

    open(path, "w").write(body)
    return "created"


def rasterise(root):
    """Merchant Center rejects SVG. Emit a JPEG twin of every product SVG so the
       feed, structured data and og:image always have a raster to point at."""
    import glob, cairosvg
    from PIL import Image
    made = 0
    for svg in glob.glob(f"{root}/assets/img/*/*.svg"):
        jpg = svg[:-4] + ".jpg"
        if os.path.exists(jpg) and os.path.getmtime(jpg) >= os.path.getmtime(svg):
            continue
        cairosvg.svg2png(url=svg, write_to="/tmp/_r.png", output_width=1200)
        im = Image.open("/tmp/_r.png").convert("RGB")
        im.save(jpg, "JPEG", quality=86, optimize=True, progressive=True)
        made += 1
    return made


def digest(path):
    """Short content hash so a changed asset gets a new URL and can never be served stale."""
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()[:10]

# the sites/ directory beside tools/, wherever this repo is checked out
ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'sites')
STORES = ((cfg_branchforge, 'BF'), (cfg_haulcrest, 'HC'),
          (cfg_rootvexx, 'RV'), (cfg_lawnstride, 'LS'))

for mod, prefix in STORES:
    cfg = dict(mod.CFG)
    key0 = cfg['domain'].split('.')[0]
    themed = theme.derive(key0, f'{ROOT}/{key0}')
    rasterised = rasterise(f'{ROOT}/{key0}')
    cfg['products'] = for_store(cfg['brand'], prefix, key0, f'{ROOT}/{key0}')
    key = key0
    state = write_site_config(cfg, f'{ROOT}/{key}')
    cfg['ver_stripe'] = digest(f'{ROOT}/{key}/assets/js/site-config.js')
    cfg['ver_css'] = digest(f'{ROOT}/{key}/assets/css/style.css')
    cfg['ver_admin_css'] = digest(f'{ROOT}/{key}/assets/css/admin.css')
    cfg['ver_admin_js'] = digest(f'{ROOT}/{key}/assets/js/admin.js')
    # catalogue is written by write_site, so hash the previous copy if present
    catp = f'{ROOT}/{key}/assets/js/catalogue.js'
    cfg['ver_cat'] = digest(catp) if os.path.exists(catp) else '0'
    cfg['ver_js'] = digest(f'{ROOT}/{key}/assets/js/script.js')
    pages = write_site(cfg, f'{ROOT}/{key}')
    cfg['ver_cat'] = digest(catp)          # now it exists; rebuild so the URL matches
    pages = write_site(cfg, f'{ROOT}/{key}')
    print(f"{cfg['brand']}: {len(pages)} pages, {len(cfg['products'])} products "
          f"| css v{cfg['ver_css']} js v{cfg['ver_js']} | stripe-config {state}"
          f" | rasterised {rasterised} svg | css {themed}")
