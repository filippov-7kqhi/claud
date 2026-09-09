# Four UK equipment stores

Four independent storefronts, each generated from the same code and each selling
**four machines** under its own brand, livery and theme.

| Store | Domain | Look | Range |
|---|---|---|---|
| BranchForge | branchforge.shop | dark, lime on near-black | photographed |
| HaulCrest | haulcrest.shop | dark, amber on graphite | photographed |
| RootVexx | rootvexx.shop | light, oxide orange on warm concrete | compact plant |
| LawnStride | lawnstride.shop | light, moss green on cream, slab serif | compact plant |

Live repos (GitHub Pages, `main` at `/ (root)`): `filippov-7kqhi/branchforge`,
`filippov-7kqhi/haulcrest`, `filippov-7kqhi/rootvexx`, `filippov-7kqhi/lawnstride`.

## The two ranges

BranchForge and HaulCrest sell the machines there are photographs of:

```
HC15H Towable Wood Chipper          £2,899   (was £3,699)
CREX10-K Mini Excavator             £3,449   (was £4,299)
MD-500HPRO Tracked Mini Dumper      £2,699   (was £3,499)
Mini Skid Steer Loader              £3,299   (was £4,199)
```

RootVexx and LawnStride sell compact plant, drawn rather than photographed:

```
EX10 1 Tonne Mini Excavator         £4,999   (was £6,199)
TD500 500 kg Tracked Mini Dumper    £2,499   (was £3,099)
LS22 22 Tonne Petrol Log Splitter   £2,199   (was £2,749)
FM150 15 hp ATV Flail Mower         £2,599   (was £3,199)
```

`tools/products.py` maps a store to its range. `tools/cat_compact.py` holds the compact
four brand-neutrally, with `%BRAND%` substituted per store; the photographed four live
in `OVERRIDES` in `tools/products.py`.

## Rebuilding

```bash
python3 tools/gen_all.py     # all machine imagery, every store
python3 tools/build_all.py   # every store's pages, feed, sitemap and catalogue
python3 tools/deploy.py      # copy each built store into its repo working tree
```

`build_all.py` calls `theme.py` first, so a derived store's CSS is always current. It
also rasterises a JPEG twin of every SVG, because Merchant Center rejects SVG.

`deploy.py` does not commit or push — read the diff, then commit in each repo. It
deliberately leaves `README.md` and `stripe/` alone, and ships only the galleries a
product on that store actually references.

## Product imagery

Every machine is drawn from scratch as SVG in `tools/m_*.py` and `tools/bf_*.py` /
`tools/hc_*.py`, and rendered once per store livery, so a machine only ever carries the
brand of the store selling it. 8 views x 4 machines x 4 stores = **128 images**, plus a
JPEG twin of each for the feed.

| File | View |
|---|---|
| `01-hero` | Full machine, studio |
| `02-side` | Side elevation, light studio |
| `03-*` | Working end (dig / tip / wedge / rotor) |
| `04-*` | Power unit with cutaway panel |
| `05-*` | Controls, undercarriage or hitch |
| `06-dimensions` | Dimensioned technical drawing |
| `07-in-use` | On-site scene |
| `08-included` | What ships in the crate |

`gen_all.py` asserts that no other store's brand appears in any file it writes, and
removes generated galleries for machines a store no longer sells. A gallery containing
photographs is never touched.

### Swapping in photographs

Drop files into `sites/<store>/assets/img/<machine>/` at 1200x760 (16:10) so the gallery
keeps its aspect ratio. `products.py` reads the directory at build time, so no code
change is needed; alt text goes in `alt.json` alongside them.

## Themes

`tools/livery.py` holds each store's machine paint. `tools/theme.py` derives a store's
`style.css` and `admin.css` from the BranchForge originals by literal colour swap, each
swap asserted to fire, so a rename in the source stylesheet fails the build instead of
silently leaving a store on the wrong palette. `script.js` and `admin.js` are identical
everywhere and are copied verbatim.

RootVexx and LawnStride are light designs, not recolours: ground, ink, shadow and
display face all change, their machines are painted to suit, and their studio shots use
a light backdrop. Their brand colours are chosen to clear 4.5:1 on their own ground,
because `--brand` is a text colour in about thirty rules as well as a button and topbar
fill.

## Google Merchant Center

### Done

- **Returns** (`returns.html`) — window measured from delivery, procedure, who pays,
  refund method and 14-day timing, condition rules, exclusions, warranty. States that no
  restocking fee applies and that no digital goods or subscriptions are sold.
- **Delivery** (`shipping.html`, 7–12 working days), **payment and billing**
  (`payment.html`), **privacy** and **terms** pages.
- Policy links in the footer of **every** page, including cart and checkout.
- **Working basket and checkout.** The basket stores only `{sku, qty}` and resolves
  name, price and image from `catalogue.js` at render time, so a withdrawn machine or a
  changed price can never be carried in a stale basket. Cart and checkout are `noindex`
  and excluded from the sitemap.
- **Product structured data** with price, `priceValidUntil`, availability, condition,
  `shippingDetails` and `hasMerchantReturnPolicy`; `OnlineStore` and `BreadcrumbList`
  alongside. Fields with nothing behind them are omitted rather than emitted empty.
- **`feed.xml`** per store: RSS 2.0 with the `g:` namespace, `identifier_exists: no`
  (own-brand goods have no GTIN), shipping and weight. Item IDs carry a store prefix, so
  the four feeds never collide.

### Removed rather than kept

- **The countdown timer.** It reset every three days, so the deadline was never real —
  prohibited misleading urgency under Merchant Center policy and under the Digital
  Markets, Competition and Consumers Act 2024.
- **The customer reviews and star ratings.** They were written, not collected.
  Publishing invented reviews or ratings is banned outright by the DMCCA 2024 and by
  Google. The section now sets out the cover a buyer actually has and says plainly that
  no reviews are published yet. Add real ones and `AggregateRating` can go in.
- **VAT.** All VAT text was removed on the owner's instruction. If any company is or
  becomes VAT registered, the number must be shown and prices must state VAT is
  included — see below.

### Still required before submitting

1. **Companies House numbers** for all four companies. Set `company_no` in the `CFG`
   dict of the store's config module and rebuild; the row appears automatically.
2. **VAT status.** Currently no store shows a VAT number or a VAT-inclusive statement,
   which is only correct if none of them is registered.
3. **Stripe Payment Links** — 16 of them, four per store. Until they are in, checkout
   says payment is not switched on.
4. **Real stock and fulfilment.** Every page claims UK stock, 1–2 day dispatch and free
   mainland delivery. Those must be true.
5. **Enforce HTTPS** in each repo's Pages settings.
6. Verify and claim each domain in Merchant Center, then submit `feed.xml`.

## Stripe

Static sites cannot hold a secret key, and Stripe removed `redirectToCheckout` from
Stripe.js, so the stores use **Payment Links** — Stripe's supported route for this case.

Paste one link per machine into `sites/<store>/assets/js/site-config.js`, or through
`/admin.html`. That file is generated once and a rebuild never overwrites values you
have set, so pasted links survive. Full setup in `stripe/README.md`.

| Basket | Behaviour |
|---|---|
| **Buy now** on a product page | Straight to that machine's Stripe page |
| One machine in the basket | **Pay securely with Stripe** |
| Several different machines | Says so, offers a single invoice (a Payment Link covers one machine) |
| A machine with no link pasted in | Says payment is not switched on, routes to an enquiry |

`stripe/analytics-worker.js` is an optional Cloudflare Worker serving three routes:
`POST /event` and `GET /stats` feed the admin dashboard, and `POST /checkout` creates a
Checkout Session for multi-machine baskets. It reads prices from Stripe rather than the
browser, so a tampered basket cannot change what is charged. Set `analyticsEndpoint` and
`checkoutEndpoint` in `site-config.js` to switch them on; without an endpoint the
dashboard shows nothing rather than inventing figures.

**Never commit a secret key** (`sk_live_…`). Put it in `wrangler secret put`. Payment
Link URLs are public by design and are fine in `site-config.js`.

## Admin

`/admin.html` on each store. The passphrase is hashed with SHA-256 into
`site-config.js`; that only hides the form from a casual visitor, since anyone can read
the file and bypass it. Nothing behind it is secret — the real gate on changing a live
site is the GitHub login. Change the passphrase from the dashboard's hash tool.

## Run locally

```bash
python3 -m http.server 8000    # then open /sites/rootvexx/ etc.
```
