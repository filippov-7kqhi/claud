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

SRC = "/home/user/claud/sites/branchforge"

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
}


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
    for js in ("script.js", "admin.js"):      # identical on every store
        shutil.copyfile(f"{SRC}/assets/js/{js}", f"{root}/assets/js/{js}")
    return "derived"
