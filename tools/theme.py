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
STYLE = {
  "rootvexx": [
    ("/* BranchForge — branchforge.shop */", "/* RootVexx — rootvexx.shop */"),
    ("--bg:#0b0f0d; --bg-2:#111815; --bg-3:#18211d; --line:#243029;",
     "--bg:#0f0b0c; --bg-2:#171112; --bg-3:#201819; --line:#33262a;"),
    ("--ink:#f2f6f3; --ink-2:#a8b6ad; --ink-3:#7c8b83;",
     "--ink:#f7f2f3; --ink-2:#b8a9ac; --ink-3:#8d7d81;"),
    ("--brand:#a3e635; --brand-2:#78c116; --brand-ink:#0d1a05;",
     "--brand:#ef4444; --brand-2:#dc2626; --brand-ink:#ffffff;"),
    ("--green:#1f5c39;", "--green:#7f1d1d;"),
    ("--brand-soft:rgba(163,230,53,.10);", "--brand-soft:rgba(239,68,68,.12);"),
    ('--head:"Barlow Condensed","Arial Narrow",Impact,sans-serif;',
     '--head:"Archivo Narrow","Arial Narrow",Impact,sans-serif;'),
    (".btn--primary:hover{background:#b6f04f", ".btn--primary:hover{background:#f56565"),
    ("background:rgba(11,15,13,.94)", "background:rgba(15,11,12,.94)"),
    ("rgba(163,230,53,.11),transparent 60%)", "rgba(239,68,68,.13),transparent 60%)"),
    ("rgba(31,92,57,.34),transparent 62%)", "rgba(127,29,29,.42),transparent 62%)"),
    (".card:hover{border-color:#3c5a3f", ".card:hover{border-color:#5e3238"),
    ("background:rgba(163,230,53,.12);display:grid", "background:rgba(239,68,68,.14);display:grid"),
    ("box-shadow:0 0 0 4px rgba(163,230,53,.18)", "box-shadow:0 0 0 4px rgba(239,68,68,.2)"),
    ("linear-gradient(120deg,var(--green),#0f3a24)", "linear-gradient(120deg,var(--green),#4a1414)"),
    ("border:1px solid #2c5f42}", "border:1px solid #7a2a2a}"),
    (".cta p{color:#cfe6d6", ".cta p{color:#f2d8d8"),
    ("background:rgba(17,24,21,.97)", "background:rgba(23,17,18,.97)"),
  ],
  "lawnstride": [
    ("/* BranchForge — branchforge.shop */", "/* LawnStride — lawnstride.shop */"),
    ("--bg:#0b0f0d; --bg-2:#111815; --bg-3:#18211d; --line:#243029;",
     "--bg:#081311; --bg-2:#0f1c19; --bg-3:#162622; --line:#22352f;"),
    ("--ink:#f2f6f3; --ink-2:#a8b6ad; --ink-3:#7c8b83;",
     "--ink:#eff7f5; --ink-2:#a4b8b3; --ink-3:#7a8d89;"),
    ("--brand:#a3e635; --brand-2:#78c116; --brand-ink:#0d1a05;",
     "--brand:#2dd4bf; --brand-2:#14b8a6; --brand-ink:#04211f;"),
    ("--green:#1f5c39;", "--green:#0f766e;"),
    ("--brand-soft:rgba(163,230,53,.10);", "--brand-soft:rgba(45,212,191,.10);"),
    ('--head:"Barlow Condensed","Arial Narrow",Impact,sans-serif;',
     '--head:"Saira Condensed","Arial Narrow",Impact,sans-serif;'),
    (".btn--primary:hover{background:#b6f04f", ".btn--primary:hover{background:#4ce0cd"),
    ("background:rgba(11,15,13,.94)", "background:rgba(8,19,17,.94)"),
    ("rgba(163,230,53,.11),transparent 60%)", "rgba(45,212,191,.12),transparent 60%)"),
    ("rgba(31,92,57,.34),transparent 62%)", "rgba(15,118,110,.36),transparent 62%)"),
    (".card:hover{border-color:#3c5a3f", ".card:hover{border-color:#2a5c52"),
    ("background:rgba(163,230,53,.12);display:grid", "background:rgba(45,212,191,.13);display:grid"),
    ("box-shadow:0 0 0 4px rgba(163,230,53,.18)", "box-shadow:0 0 0 4px rgba(45,212,191,.18)"),
    ("linear-gradient(120deg,var(--green),#0f3a24)", "linear-gradient(120deg,var(--green),#0b3b36)"),
    ("border:1px solid #2c5f42}", "border:1px solid #1d6b60}"),
    (".cta p{color:#cfe6d6", ".cta p{color:#cdeae4"),
    ("background:rgba(17,24,21,.97)", "background:rgba(15,28,25,.97)"),
  ],
}

ADMIN = {
  "rootvexx":   [("--acc:#4d7c0f; --acc-2:#65a30d;", "--acc:#b91c1c; --acc-2:#dc2626;")],
  "lawnstride": [("--acc:#4d7c0f; --acc-2:#65a30d;", "--acc:#0f766e; --acc-2:#14b8a6;")],
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
        _swap(css, STYLE[key], f"{key} style.css"))
    acss = open(f"{SRC}/assets/css/admin.css", encoding="utf-8").read()
    open(f"{root}/assets/css/admin.css", "w", encoding="utf-8").write(
        _swap(acss, ADMIN[key], f"{key} admin.css"))
    for js in ("script.js", "admin.js"):      # identical on every store
        shutil.copyfile(f"{SRC}/assets/js/{js}", f"{root}/assets/js/{js}")
    return "derived"
