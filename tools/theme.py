# -*- coding: utf-8 -*-
"""Derive a store's stylesheet from the BranchForge one.

script.js, admin.js and the structure of both stylesheets are identical across
stores -- only the palette and the display face change. Rather than keep four
near-copies in sync by hand, the BranchForge files are the source and each new
store is a list of literal colour swaps applied to them. Every swap is asserted
to fire, so a change to the source stylesheet that renames a colour fails the
build instead of silently leaving a store on the wrong palette.
"""
import os, shutil

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "sites", "branchforge")

# (old, new) literal swaps. Order matters only in that no `new` may contain an
# `old` that has not yet been applied -- none do.
# Both of these stores are LIGHT designs, so the swaps go further than a recolour:
# the ground, the ink, the shadow and the display face all change. Brand colours
# are chosen to clear 4.5:1 on white, because --brand is used as a text colour in
# roughly thirty rules and is a button and topbar fill in several more.
STYLE = {
  # RootVexx -- light industrial. Warm concrete ground, oxide orange, a tall
  # condensed display face.
  "rootvexx": [
    ("/* BranchForge — branchforge.shop */", "/* RootVexx — rootvexx.shop */"),
    ("--bg:#0b0f0d; --bg-2:#111815; --bg-3:#18211d; --line:#243029;",
     "--bg:#f5f3f0; --bg-2:#ffffff; --bg-3:#eceae5; --line:#ded9d1;"),
    ("--ink:#f2f6f3; --ink-2:#a8b6ad; --ink-3:#7c8b83;",
     "--ink:#171310; --ink-2:#5b534c; --ink-3:#8b8279;"),
    ("--brand:#a3e635; --brand-2:#78c116; --brand-ink:#0d1a05;",
     "--brand:#c2410c; --brand-2:#9a3412; --brand-ink:#ffffff;"),
    ("--green:#1f5c39;", "--green:#1c1917;"),
    ("--brand-soft:rgba(163,230,53,.10);", "--brand-soft:rgba(194,65,12,.08);"),
    ("--shadow:0 18px 44px rgba(0,0,0,.44);", "--shadow:0 14px 34px rgba(28,25,23,.10);"),
    ('--head:"Barlow Condensed","Arial Narrow",Impact,sans-serif;',
     '--head:"Big Shoulders Display","Arial Narrow",Impact,sans-serif;'),
    (".btn--primary:hover{background:#b6f04f", ".btn--primary:hover{background:#9a3412"),
    ("background:rgba(11,15,13,.94)", "background:rgba(245,243,240,.93)"),
    ("rgba(163,230,53,.11),transparent 60%)", "rgba(194,65,12,.10),transparent 60%)"),
    ("rgba(31,92,57,.34),transparent 62%)", "rgba(120,113,108,.16),transparent 62%)"),
    (".card:hover{border-color:#3c5a3f", ".card:hover{border-color:#c7c0b6"),
    ("background:rgba(163,230,53,.12);display:grid", "background:rgba(194,65,12,.11);display:grid"),
    ("box-shadow:0 0 0 4px rgba(163,230,53,.18)", "box-shadow:0 0 0 4px rgba(194,65,12,.16)"),
    ("linear-gradient(120deg,var(--green),#0f3a24)", "linear-gradient(120deg,var(--green),#3b3532)"),
    ("border:1px solid #2c5f42}", "border:1px solid #443d39}"),
    (".cta p{color:#cfe6d6", ".cta p{color:#e8e3dd"),
    ("background:rgba(17,24,21,.97)", "background:rgba(255,255,255,.97)"),
    ("box-shadow:0 0 0 1px rgba(255,255,255,.14)", "box-shadow:0 0 0 1px rgba(0,0,0,.14)"),
  ],
  # AgriMaxx (US) -- a dark, agricultural recolour of the BranchForge original:
  # same near-black structure, but a deep field-green ground and a harvest-gold
  # accent instead of lime, so a dark store still has its own hue family rather
  # than reusing BranchForge's or HaulCrest's.
  "agrimax": [
    ("/* BranchForge — branchforge.shop */", "/* AgriMaxx — agrimax.shop */"),
    ("--bg:#0b0f0d; --bg-2:#111815; --bg-3:#18211d; --line:#243029;",
     "--bg:#0a120c; --bg-2:#0f1a12; --bg-3:#142415; --line:#1f3322;"),
    ("--ink:#f2f6f3; --ink-2:#a8b6ad; --ink-3:#7c8b83;",
     "--ink:#f3f7f0; --ink-2:#a9b0a3; --ink-3:#7d8578;"),
    ("--brand:#a3e635; --brand-2:#78c116; --brand-ink:#0d1a05;",
     "--brand:#d4a017; --brand-2:#a8790a; --brand-ink:#1a1206;"),
    ("--green:#1f5c39;", "--green:#1c3d20;"),
    ("--brand-soft:rgba(163,230,53,.10);", "--brand-soft:rgba(212,160,23,.12);"),
    ('--head:"Barlow Condensed","Arial Narrow",Impact,sans-serif;',
     '--head:"Oswald","Arial Narrow",Impact,sans-serif;'),
    (".btn--primary:hover{background:#b6f04f", ".btn--primary:hover{background:#e8b636"),
    ("background:rgba(11,15,13,.94)", "background:rgba(10,18,12,.94)"),
    ("rgba(163,230,53,.11),transparent 60%)", "rgba(212,160,23,.11),transparent 60%)"),
    ("rgba(31,92,57,.34),transparent 62%)", "rgba(28,61,32,.34),transparent 62%)"),
    (".card:hover{border-color:#3c5a3f", ".card:hover{border-color:#3a4f3c"),
    ("background:rgba(163,230,53,.12);display:grid", "background:rgba(212,160,23,.12);display:grid"),
    ("box-shadow:0 0 0 4px rgba(163,230,53,.18)", "box-shadow:0 0 0 4px rgba(212,160,23,.18)"),
    ("linear-gradient(120deg,var(--green),#0f3a24)", "linear-gradient(120deg,var(--green),#0d2e19)"),
    ("border:1px solid #2c5f42}", "border:1px solid #2a4a2e}"),
    (".cta p{color:#cfe6d6", ".cta p{color:#d7e6d2"),
    ("background:rgba(17,24,21,.97)", "background:rgba(15,26,18,.97)"),
  ],
  # GroundMaxx (US) -- a dark, slate/charcoal recolour with a safety-yellow
  # accent, distinct from AgriMaxx's green and from HaulCrest's amber.
  "groundmax": [
    ("/* BranchForge — branchforge.shop */", "/* GroundMaxx — groundmax.shop */"),
    ("--bg:#0b0f0d; --bg-2:#111815; --bg-3:#18211d; --line:#243029;",
     "--bg:#101114; --bg-2:#16181c; --bg-3:#1d2025; --line:#2a2d33;"),
    ("--ink:#f2f6f3; --ink-2:#a8b6ad; --ink-3:#7c8b83;",
     "--ink:#f5f6f7; --ink-2:#a7abb3; --ink-3:#7d8189;"),
    ("--brand:#a3e635; --brand-2:#78c116; --brand-ink:#0d1a05;",
     "--brand:#eab308; --brand-2:#ca8a04; --brand-ink:#1c1502;"),
    # No green identity here, so --green (only ever used as the CTA band's dark
    # gradient stop) is repointed to a slate tone rather than left green.
    ("--green:#1f5c39;", "--green:#2a2e35;"),
    ("--brand-soft:rgba(163,230,53,.10);", "--brand-soft:rgba(234,179,8,.12);"),
    ('--head:"Barlow Condensed","Arial Narrow",Impact,sans-serif;',
     '--head:"Anton","Arial Narrow",Impact,sans-serif;'),
    (".btn--primary:hover{background:#b6f04f", ".btn--primary:hover{background:#f4c430"),
    ("background:rgba(11,15,13,.94)", "background:rgba(16,17,20,.94)"),
    ("rgba(163,230,53,.11),transparent 60%)", "rgba(234,179,8,.11),transparent 60%)"),
    ("rgba(31,92,57,.34),transparent 62%)", "rgba(42,46,53,.34),transparent 62%)"),
    (".card:hover{border-color:#3c5a3f", ".card:hover{border-color:#3d4149"),
    ("background:rgba(163,230,53,.12);display:grid", "background:rgba(234,179,8,.12);display:grid"),
    ("box-shadow:0 0 0 4px rgba(163,230,53,.18)", "box-shadow:0 0 0 4px rgba(234,179,8,.18)"),
    ("linear-gradient(120deg,var(--green),#0f3a24)", "linear-gradient(120deg,var(--green),#15171b)"),
    ("border:1px solid #2c5f42}", "border:1px solid #33373f}"),
    (".cta p{color:#cfe6d6", ".cta p{color:#e3e6ea"),
    ("background:rgba(17,24,21,.97)", "background:rgba(22,24,28,.97)"),
  ],
  # LawnStride -- light editorial. Cream ground, moss green, a slab serif with
  # the uppercase heading transform dropped so it reads as prose, not signage.
  "lawnstride": [
    ("/* BranchForge — branchforge.shop */", "/* LawnStride — lawnstride.shop */"),
    ("--bg:#0b0f0d; --bg-2:#111815; --bg-3:#18211d; --line:#243029;",
     "--bg:#faf8f2; --bg-2:#ffffff; --bg-3:#f0ede3; --line:#e2ddce;"),
    ("--ink:#f2f6f3; --ink-2:#a8b6ad; --ink-3:#7c8b83;",
     "--ink:#18220f; --ink-2:#55604b; --ink-3:#87907c;"),
    ("--brand:#a3e635; --brand-2:#78c116; --brand-ink:#0d1a05;",
     "--brand:#4d7c0f; --brand-2:#3f6212; --brand-ink:#ffffff;"),
    ("--green:#1f5c39;", "--green:#1f2d16;"),
    ("--brand-soft:rgba(163,230,53,.10);", "--brand-soft:rgba(77,124,15,.08);"),
    ("--shadow:0 18px 44px rgba(0,0,0,.44);", "--shadow:0 14px 34px rgba(24,34,15,.10);"),
    ('--head:"Barlow Condensed","Arial Narrow",Impact,sans-serif;',
     '--head:"Bitter",Georgia,"Times New Roman",serif;'),
    ("letter-spacing:-.01em;margin:0 0 .5em;text-transform:uppercase}",
     "letter-spacing:-.015em;margin:0 0 .5em}"),
    (".btn--primary:hover{background:#b6f04f", ".btn--primary:hover{background:#3f6212"),
    ("background:rgba(11,15,13,.94)", "background:rgba(250,248,242,.93)"),
    ("rgba(163,230,53,.11),transparent 60%)", "rgba(101,163,13,.12),transparent 60%)"),
    ("rgba(31,92,57,.34),transparent 62%)", "rgba(120,133,95,.16),transparent 62%)"),
    (".card:hover{border-color:#3c5a3f", ".card:hover{border-color:#c6cdb2"),
    ("background:rgba(163,230,53,.12);display:grid", "background:rgba(77,124,15,.11);display:grid"),
    ("box-shadow:0 0 0 4px rgba(163,230,53,.18)", "box-shadow:0 0 0 4px rgba(77,124,15,.16)"),
    ("linear-gradient(120deg,var(--green),#0f3a24)", "linear-gradient(120deg,var(--green),#35492a)"),
    ("border:1px solid #2c5f42}", "border:1px solid #405632}"),
    (".cta p{color:#cfe6d6", ".cta p{color:#e4edda"),
    ("background:rgba(17,24,21,.97)", "background:rgba(255,255,255,.97)"),
    ("box-shadow:0 0 0 1px rgba(255,255,255,.14)", "box-shadow:0 0 0 1px rgba(0,0,0,.14)"),
  ],
}

# Rules that only a light store needs, appended after the swaps. The CTA is the
# one band that stays dark on a light page, so everything inside it has to be
# told its foreground explicitly instead of inheriting the page's dark ink.
EXTRA = {
  "rootvexx": """
/* ---- light-theme corrections ---- */
.cta{color:#f7f4f1}
.cta h2{color:#f7f4f1}
.cta .btn--ghost{border-color:#f7f4f1;color:#f7f4f1;background:rgba(255,255,255,.10)}
.cta .btn--ghost:hover{background:#f7f4f1;color:#1c1917}
""",
  "lawnstride": """
/* ---- light-theme corrections ---- */
.cta{color:#f4f7ef}
.cta h2{color:#f4f7ef}
.cta .btn--ghost{border-color:#f4f7ef;color:#f4f7ef;background:rgba(255,255,255,.10)}
.cta .btn--ghost:hover{background:#f4f7ef;color:#1f2d16}
""",
}

ADMIN = {
  "rootvexx":   [("--acc:#4d7c0f; --acc-2:#65a30d;", "--acc:#9a3412; --acc-2:#c2410c;")],
  "lawnstride": [("--acc:#4d7c0f; --acc-2:#65a30d;", "--acc:#3f6212; --acc-2:#4d7c0f;")],
  "agrimax":    [("--acc:#4d7c0f; --acc-2:#65a30d;", "--acc:#a8790a; --acc-2:#d4a017;")],
  "groundmax":  [("--acc:#4d7c0f; --acc-2:#65a30d;", "--acc:#ca8a04; --acc-2:#eab308;")],
}

# script.js and admin.js are otherwise identical on every store (see CLAUDE.md),
# but a US store needs its money formatter and its client-side business-address
# composer to stop hard-coding "£"/en-GB/"United Kingdom". These are applied on
# top of BranchForge's copy for a store's own derived files only -- BranchForge
# itself is never touched, so the four existing stores render exactly as before.
_US_SCRIPT_JS = [
    ("return '£' + n.toLocaleString('en-GB', { minimumFractionDigits: 0, maximumFractionDigits: 0 });",
     "return '$' + n.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 });"),
    ("      // Town and postcode sit together without a comma, as UK addresses are written.\n"
     "      var town = [(biz.city || '').trim(), (biz.postcode || '').trim()].filter(Boolean).join(' ');",
     "      // City, state and ZIP are written together, US-style: \"City, ST 00000\".\n"
     "      var town = [[(biz.city || '').trim(), (biz.state || '').trim()].filter(Boolean).join(', '), "
     "(biz.postcode || '').trim()].filter(Boolean).join(' ');"),
    ("        addr.textContent = supplied.concat('United Kingdom').join(', ');",
     "        addr.textContent = supplied.join(', ');"),
]
_US_ADMIN_JS = [
    ("var nf = new Intl.NumberFormat('en-GB');", "var nf = new Intl.NumberFormat('en-US');"),
    ("return '£' + (pence / 100).toLocaleString('en-GB', { minimumFractionDigits: 2, maximumFractionDigits: 2 });",
     "return '$' + (pence / 100).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });"),
    ("return isNaN(d) ? '' : d.toLocaleString('en-GB',", "return isNaN(d) ? '' : d.toLocaleString('en-US',"),
]
JS_SCRIPT = {"agrimax": _US_SCRIPT_JS, "groundmax": _US_SCRIPT_JS}
JS_ADMIN = {"agrimax": _US_ADMIN_JS, "groundmax": _US_ADMIN_JS}


def _swap(text, subs, what):
    for old, new in subs:
        if old not in text:
            raise SystemExit(f"theme: {what}: source no longer contains {old!r}")
        text = text.replace(old, new)
    return text


def derive(key, root):
    """Write the four shared front-end assets for one store."""
    if key not in STYLE:
        return "source"                      # branchforge/haulcrest own their files
    os.makedirs(f"{root}/assets/css", exist_ok=True)
    os.makedirs(f"{root}/assets/js", exist_ok=True)
    css = open(f"{SRC}/assets/css/style.css", encoding="utf-8").read()
    open(f"{root}/assets/css/style.css", "w", encoding="utf-8").write(
        _swap(css, STYLE[key], f"{key} style.css") + EXTRA.get(key, ""))
    acss = open(f"{SRC}/assets/css/admin.css", encoding="utf-8").read()
    open(f"{root}/assets/css/admin.css", "w", encoding="utf-8").write(
        _swap(acss, ADMIN[key], f"{key} admin.css"))
    for js, swaps in (("script.js", JS_SCRIPT.get(key)), ("admin.js", JS_ADMIN.get(key))):
        if swaps:
            text = open(f"{SRC}/assets/js/{js}", encoding="utf-8").read()
            open(f"{root}/assets/js/{js}", "w", encoding="utf-8").write(
                _swap(text, swaps, f"{key} {js}"))
        else:                                 # identical on every other store
            shutil.copyfile(f"{SRC}/assets/js/{js}", f"{root}/assets/js/{js}")
    return "derived"
