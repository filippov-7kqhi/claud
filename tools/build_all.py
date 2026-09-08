import sys, os; sys.path.insert(0, '/home/user/claud/tools')
from build_site import write_site
from products import for_store
import cfg_branchforge, cfg_haulcrest
import hashlib


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

  // Optional serverless endpoint for baskets with more than one machine.
  // See stripe/README.md. Leave "" while hosting on GitHub Pages.
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
    """Written once; never overwritten, so edits survive a rebuild."""
    path = f"{root}/assets/js/site-config.js"
    if os.path.exists(path):
        return "kept"
    links = "\n".join(
        f'    "{p["sku"]}": "",{" " * max(1, 14 - len(p["sku"]))}// {p["name"]} - GBP {p["price"]:,}'
        for p in cfg["products"])
    open(path, "w").write(CONFIG_TEMPLATE.format(
        brand=cfg["brand"], links=links, passhash=ADMIN_PASS_HASH))
    return "created"


def digest(path):
    """Short content hash so a changed asset gets a new URL and can never be served stale."""
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()[:10]

ROOT = '/home/user/claud/sites'
for mod, prefix in ((cfg_branchforge, 'BF'), (cfg_haulcrest, 'HC')):
    cfg = dict(mod.CFG)
    cfg['products'] = for_store(cfg['brand'], prefix)
    key = cfg['domain'].split('.')[0]
    state = write_site_config(cfg, f'{ROOT}/{key}')
    cfg['ver_stripe'] = digest(f'{ROOT}/{key}/assets/js/site-config.js')
    cfg['ver_css'] = digest(f'{ROOT}/{key}/assets/css/style.css')
    cfg['ver_js'] = digest(f'{ROOT}/{key}/assets/js/script.js')
    pages = write_site(cfg, f'{ROOT}/{key}')
    print(f"{cfg['brand']}: {len(pages)} pages, {len(cfg['products'])} products "
          f"| css v{cfg['ver_css']} js v{cfg['ver_js']} | stripe-config {state}")
