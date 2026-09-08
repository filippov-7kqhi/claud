# BranchForge & HaulCrest — UK equipment stores

Two independent storefronts. **Each sells all four machines**, under its own brand and
in its own livery.

```
sites/branchforge/   branchforge.shop   green / lime livery
sites/haulcrest/     haulcrest.shop     amber / graphite livery

Cyclone 150 TD Wood Chipper        £2,899   (was £3,699)
Grindmaster 380 TX Stump Grinder   £3,449   (was £4,299)
Titan 1000 HT Tracked Dumper       £2,699   (was £3,499)
Vanguard 850 SL Compact Loader     £3,299   (was £4,199)
```

Live repos (GitHub Pages, `main` at `/ (root)`): `filippov-7kqhi/branchforge`,
`filippov-7kqhi/haulcrest`.

## Product imagery

Every machine is drawn from scratch as SVG and exists in **both** liveries, so each
store's photos carry only that store's brand — `BRANCHFORGE` or `HAULCREST` — plus the
model decal. 8 views x 4 machines x 2 stores = **64 images**.

| File | View |
|---|---|
| `01-hero` | Full machine, dark studio |
| `02-side` | Side elevation, light studio |
| `03-*` | Working end (infeed / cutter / high tip / bucket) |
| `04-engine` | Power unit with cutaway panel |
| `05-controls` | Operator controls |
| `06-dimensions` | Dimensioned technical drawing |
| `07-in-use` | On-site scene |
| `08-included` | What ships in the crate |

```bash
python3 tools/gen_all.py     # regenerates all 64
python3 tools/build_all.py   # regenerates both stores' pages
```

`tools/livery.py` holds the two colour schemes; `tools/products.py` holds the four
machines brand-neutrally and rebrands them per store.

### Swapping in photographs

Overwrite a file in `sites/<store>/assets/img/<machine>/` keeping the name, at 1200x760
(16:10) so the gallery keeps its aspect ratio. Alt text lives in the product dicts in
`tools/cfg_branchforge.py` / `tools/cfg_haulcrest.py`.

## Google Merchant Center

### Done

- **Returns policy** (`returns.html`) with return window measured from delivery, the
  procedure, who pays, refund method and 14-day timing, condition rules, exclusions and
  warranty. States explicitly that no restocking fee applies and that no digital goods
  or subscriptions are sold.
- **Delivery** (`shipping.html`), **payment and billing** (`payment.html`),
  **privacy** and **terms** pages.
- Policy links in the footer of **every** page, including cart and checkout.
- **Working basket and checkout** with a VAT breakdown; cart and checkout are `noindex`
  and excluded from the sitemap.
- **Product structured data** with price, `priceValidUntil`, availability, condition,
  `shippingDetails` and `hasMerchantReturnPolicy`; `OnlineStore` and `BreadcrumbList`
  markup alongside.
- **`feed.xml`** per store: RSS 2.0 with the `g:` namespace, `identifier_exists: no`
  (own-brand goods have no GTIN), shipping, weight and 20% VAT.
- Prices VAT-inclusive with the VAT element shown on every product page.

### Removed rather than kept

- **The countdown timer.** It reset itself every three days, so the deadline was never
  real. That is prohibited misleading urgency under Merchant Center's misrepresentation
  policy and under the Digital Markets, Competition and Consumers Act 2024.
- **The customer reviews.** They were written, not collected. Publishing invented
  reviews is banned outright by the DMCCA 2024 and by Google. The section now sets out
  the cover a buyer actually has, and says plainly that no reviews are published yet.

### Still required before submitting

1. **Real business identity.** Footers show `[Registered company name] Ltd`,
   `[Companies House number]`, `[VAT registration number]`, `[Registered address]`,
   `[Town]`, `[Postcode]` and `[Add your phone number]`. Merchant Center and Stripe both
   verify these. Set them in the `CFG` dict of each config file and rebuild.
2. **Paste the Stripe Payment Links.** See below — until they are in, checkout says
   payment is not switched on.
3. **Real stock and fulfilment.** Every page claims UK stock, 1–2 day dispatch and free
   mainland delivery. Those must be true.
4. Verify and claim each domain in Merchant Center, then submit `feed.xml`.

## Stripe

Static sites cannot hold a secret key, and Stripe removed `redirectToCheckout` from
Stripe.js, so the stores use **Payment Links** — Stripe's supported route for this case.

Paste one link per machine into `sites/<store>/assets/js/stripe-config.js`. The file is
generated once and never overwritten by a rebuild, so pasted links survive. Full setup
in `stripe/README.md`.

| Basket | Behaviour |
|---|---|
| **Buy now** on a product page | Straight to that machine's Stripe page |
| One machine in the basket | **Pay securely with Stripe** |
| Several different machines | Says so, offers a single invoice (a Payment Link covers one machine) |
| A machine with no link pasted in | Says payment is not switched on, routes to an enquiry |

For multi-machine baskets, `stripe/checkout-worker.js` is an optional Cloudflare Worker
that creates a Checkout Session; set `checkoutEndpoint` in the config and the checkout
switches to it. It reads prices from Stripe rather than the browser, so a tampered
basket cannot change what is charged.

**Never commit a secret key** (`sk_live_…`). Payment Link URLs are public by design.

## Run locally

```bash
python3 -m http.server 8000    # then open /sites/branchforge/ or /sites/haulcrest/
```
