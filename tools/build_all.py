import sys, os; sys.path.insert(0, '/home/user/claud/tools')
from build_site import write_site
from products import for_store
import cfg_branchforge, cfg_haulcrest
import hashlib


CONFIG_TEMPLATE = """\
/* ---------------------------------------------------------------------------
   Stripe configuration for {brand}.

   This file is PUBLIC. Never put a secret key (sk_live_... / sk_test_...) here.
   Payment Link URLs and publishable keys are safe to publish; secret keys are not.

   HOW TO FILL THIS IN
   1. Stripe Dashboard -> Product catalogue -> add each machine with its price
      (prices below are GBP and already include 20% VAT).
   2. For each product, create a Payment Link. On each link switch on:
        - "Collect customers' addresses" -> Shipping
        - "Let customers adjust quantity" (so a buyer can order two)
        - a custom text field named "Delivery access notes" (gate width, gradient,
          parking) so the carrier gets what it needs
   3. Paste each Payment Link URL below, next to its item code.

   Leave a link blank and that machine falls back to the enquiry route rather
   than pretending to take payment.
--------------------------------------------------------------------------- */
window.STRIPE_CONFIG = {{
  // Optional: a serverless endpoint that creates a Checkout Session.
  // Needed only for baskets holding more than one different machine.
  // See stripe/README.md. Leave "" while you are on GitHub Pages.
  checkoutEndpoint: "",

  paymentLinks: {{
{links}
  }}
}};
"""


def write_stripe_config(cfg, root):
    """Written once; never overwritten, so pasted links survive a rebuild."""
    path = f"{root}/assets/js/stripe-config.js"
    if os.path.exists(path):
        return "kept"
    links = "\n".join(
        f'    "{p["sku"]}": "",{" " * max(1, 14 - len(p["sku"]))}// {p["name"]} — £{p["price"]:,}'
        for p in cfg["products"])
    open(path, "w").write(CONFIG_TEMPLATE.format(brand=cfg["brand"], links=links))
    return "created"


def digest(path):
    """Short content hash so a changed asset gets a new URL and can never be served stale."""
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()[:10]

ROOT = '/home/user/claud/sites'
for mod, prefix in ((cfg_branchforge, 'BF'), (cfg_haulcrest, 'HC')):
    cfg = dict(mod.CFG)
    cfg['products'] = for_store(cfg['brand'], prefix)
    key = cfg['domain'].split('.')[0]
    state = write_stripe_config(cfg, f'{ROOT}/{key}')
    cfg['ver_stripe'] = digest(f'{ROOT}/{key}/assets/js/stripe-config.js')
    cfg['ver_css'] = digest(f'{ROOT}/{key}/assets/css/style.css')
    cfg['ver_js'] = digest(f'{ROOT}/{key}/assets/js/script.js')
    pages = write_site(cfg, f'{ROOT}/{key}')
    print(f"{cfg['brand']}: {len(pages)} pages, {len(cfg['products'])} products "
          f"| css v{cfg['ver_css']} js v{cfg['ver_js']} | stripe-config {state}")
