# Working on this repo

Read `STORES.md` first — it is the reference for what the four stores are and what
still has to be supplied. This file is the working context: how the code fits
together, what to run, and the mistakes already made once.

## What is in here

The repository root is a **different project** — a coaching site for `skillore.shop`
(`index.html`, `assets/`, `CNAME`, and a `README.md` that describes only that). The four
UK equipment stores live entirely in:

```
tools/     the generator
sites/     the four built stores (generated output, committed)
stripe/    Payment Link tooling and the Cloudflare Worker
```

Do not assume the root files relate to the stores. They do not.

## The four stores

`branchforge.shop`, `haulcrest.shop`, `rootvexx.shop`, `lawnstride.shop`. Each is its
own public GitHub Pages repo under `filippov-7kqhi/`, served from `main` at `/ (root)`.
This repo generates them; those repos only receive built output.

## Setup

```bash
pip install -r requirements.txt
python3 -m playwright install chromium     # skip if PLAYWRIGHT_BROWSERS_PATH is set
```

`cairosvg` needs system Cairo (`libcairo2` on Debian/Ubuntu, `brew install cairo` on
macOS). `libarchive-c` is only for unpacking supplied RAR5 photo archives — `7z` creates
the files but cannot decode RAR5 entries, which looks like success and is not.

## The loop

```bash
python3 tools/gen_all.py     # machine imagery: 8 views per machine, per store livery
python3 tools/build_all.py   # pages, feed, sitemap, catalogue, per-store CSS
python3 tools/deploy.py      # copy each built store into its repo working tree
```

Every path is worked out from the file's own location, so it does not matter where this
is checked out. `deploy.py` looks for the four store clones beside this repo; pass
`--repos DIR` if they live somewhere else.

`build_all.py` calls `theme.py` first, so derived CSS is always current, and rasterises a
JPEG twin of every SVG because Merchant Center rejects SVG.

`deploy.py` does **not** commit or push. Read the diff, then commit in each store repo.

## Verifying before you push

There is no test suite. Two scripts do the work, and both must be green:

- a **render lint** over every page at 1360px and 390px — console errors, page errors,
  missing local assets, horizontal overflow, unresolved template braces
- a **functional pass** per store — add to basket, Buy now, cart hydration, checkout,
  admin unlock / re-lock / wrong passphrase

They are not committed; write them into the scratch directory when needed. Points that
cost time before:

- Google Fonts is unreachable in a sandbox. Fulfil the stylesheet request with empty CSS
  in a Playwright route handler, or `load` never fires and every page times out.
- A `file://` requestfailed is usually the previous page's image cancelled by the
  navigation. Check the path on disk before believing it.
- Cards below the fold are `loading="lazy"`, so they are blank in a full-page
  screenshot. That is the screenshot, not the site.
- `[data-reveal]` is opacity 0 until it scrolls into view. Force it visible when
  capturing a full page.

## How the generator fits together

- `livery.py` — each store's machine paint, plus `studio` ("light" stores get light
  studio backdrops). Machine modules read `livery.CUR`.
- `m_*.py`, `bf_*.py`, `hc_*.py` — one machine each, drawn from scratch, parametric so a
  boom angle or a tip is an argument. `svgkit.py` holds the shared primitives.
- `gen_all.py` — scene sets, and which four machines each store generates. Asserts no
  other store's brand appears in anything it writes. Removes generated galleries a store
  no longer sells; never touches a gallery containing photographs.
- `products.py` — `CATALOGUE` maps a store to its range; `OVERRIDES` swaps a drawn entry
  for a photographed machine. `_images_on_disk` reads galleries off disk, so adding a
  photo needs no code change.
- `cat_compact.py` (drawn), `cat_photo.py` (photographed) — brand-neutral product data,
  `%BRAND%` substituted per store.
- `cfg_<store>.py` — one store's identity and copy.
- `theme.py` — derives a store's CSS from the BranchForge original by literal colour
  swap, each swap asserted to fire, plus an `EXTRA` block per light store.
- `build_site.py` — every page. `photos.py` fits supplied photographs to 1200x760.

## Conventions that matter

**Never invent a figure.** Every spec on a photographed machine was read off a badge, a
data plate or a dimension in the shot. Where a figure was not visible it is absent and
the FAQ says to ask. `crate_note()` and `shipping_weight()` omit themselves rather than
render an empty value.

**Never publish an unsubstantiated claim.** No star ratings, no invented reviews, no
countdown timers, no "best seller" badges without sales. The DMCCA 2024 bans these and
Merchant Center suspends for them. Product badges state a fact about the machine.

**The basket stores only `{sku, qty}`** and resolves everything else from
`catalogue.js` at render time. It used to snapshot name, price and image at add-time,
which left withdrawn machines and stale prices in people's baskets.

**`site-config.js` is public and written once.** A rebuild never overwrites values the
owner has set; it regenerates only when the range changed and nothing is filled in yet.
Payment Link URLs are fine in it. A secret key never is.

**A contrast check is not optional on the light stores.** `--brand` is a text colour in
about thirty rules as well as a button and topbar fill, so it has to clear 4.5:1 on its
own ground.

## Deploying

`deploy.py` leaves `README.md` and `stripe/` alone in each store repo, and ships only the
galleries a product on that store references. A plain `cp -r` would delete the Worker
source and add several megabytes of unused artwork — that nearly happened once.

## Secrets

Scan before every push:

```bash
grep -rInE "sk_(live|test)_[A-Za-z0-9]{6,}" .
```

The admin passphrase is stored only as a SHA-256 hash. All four store repos are public.
