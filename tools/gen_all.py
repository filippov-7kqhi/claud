# -*- coding: utf-8 -*-
"""Generate all product imagery: 8 views per machine, per store livery.

   Two stores sell the original four machines and two sell the compact-plant four,
   so SETS is chosen per store rather than shared."""
import sys, os, math
sys.path.insert(0, '/home/user/claud/tools')
import livery
from svgkit import *
from bf_chipper import chipper
from bf_grinder import grinder
from hc_dumper import dumper, GRAPH
from hc_loader import loader
from m_excavator import excavator
from m_minidumper import minidumper
from m_splitter import splitter
from m_flail import flail

ROOT = '/home/user/claud/sites'


def zoom(cx, cy, k, inner):
    return f'<g transform="translate({600-k*cx:.1f},{380-k*cy:.1f}) scale({k})">{inner}</g>'


def frame(light=False):
    c = "#0f172a" if light else "#ffffff"
    return (f'<rect x="26" y="26" width="{W-52}" height="{H-52}" rx="16" fill="none" '
            f'stroke="{c}" stroke-width="1.5" opacity=".14"/>')


def wm(L, light=False):
    c = "#0f172a" if light else "#ffffff"
    return (f'<text x="{W-56}" y="{H-42}" text-anchor="end" font-family="Arial,Helvetica,sans-serif" '
            f'font-weight="800" font-size="17" letter-spacing="3.5" fill="{c}" opacity=".38">'
            f'{L["brand"]}</text>')


def glow(L):
    return f'<ellipse cx="600" cy="325" rx="470" ry="250" fill="{L["glow"]}" opacity=".06"/>'


def studio(L):
    """The backdrop the studio shots use. A light-themed store gets light shots,
       or its hero images sit on the page like holes cut in it."""
    return L.get("studio", "dark")


def lit(L):
    return studio(L) == "light"


def wash(L):
    """The soft brand wash behind a studio shot, in whichever direction reads."""
    return (f'<ellipse cx="600" cy="325" rx="470" ry="250" fill="{L["glow"]}" '
            f'opacity="{".05" if lit(L) else ".06"}"/>')


def panel(L, x, y, w, h, title, lines, art=""):
    body = "".join(f'<text x="{x+32}" y="{y+h-56+i*26}" font-family="Arial,Helvetica,sans-serif" '
                   f'font-size="17" fill="#cbd5e1">{esc(t)}</text>' for i, t in enumerate(lines))
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#0d1117" '
            f'stroke="{L["acc"]}" stroke-width="2.5"/>'
            f'<text x="{x+32}" y="{y+42}" font-family="Arial,Helvetica,sans-serif" font-weight="800" '
            f'font-size="20" fill="{L["acc"]}">{esc(title)}</text>{art}{body}')


def engine_card(L, x, y, w=452, h=330):
    art = (f'<g transform="translate({x+32},{y+64})">' + engine_block(0, 0, w-64, h-158) +
           f'<circle cx="{w-120}" cy="{(h-158)/2}" r="32" fill="#2a2f38" stroke="#6b7280" stroke-width="3"/>'
           f'<circle cx="{w-120}" cy="{(h-158)/2}" r="12" fill="#9aa2ad"/></g>')
    return art


def site_bg():
    return (f'<rect width="{W}" height="{H}" fill="url(#skyG)"/>'
            + "".join(f'<rect x="{i*84}" y="426" width="78" height="140" rx="3" fill="#8fa3b2" opacity=".45"/>'
                      for i in range(15))
            + f'<rect y="418" width="{W}" height="10" fill="#7c8fa0" opacity=".6"/>'
            + f'<rect y="560" width="{W}" height="200" fill="#8a7a62"/>'
            + f'<rect y="560" width="{W}" height="22" fill="#9d8b6f"/>'
            + f'<ellipse cx="600" cy="720" rx="740" ry="96" fill="#7a6a54" opacity=".6"/>')


def heap(x, y, w, h, c="#6b5a42", c2="#8a7554"):
    return (f'<path d="M{x-w/2} {y} q{w*0.25} -{h} {w/2} -{h} q{w*0.25} 0 {w/2} {h} z" fill="{c}"/>'
            f'<path d="M{x-w*0.3} {y} q{w*0.15} -{h*0.6} {w*0.3} -{h*0.6} q{w*0.15} 0 {w*0.3} {h*0.6} z" fill="{c2}"/>')


def stump(x, y, r=60, h=42):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r*0.34}" fill="#c9a978"/>'
            f'<path d="M{x-r} {y} v{h} a{r} {r*0.34} 0 0 0 {2*r} 0 v-{h} z" fill="#8a6b45"/>'
            + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{r-i*11}" ry="{(r-i*11)*0.34}" fill="none" '
                      f'stroke="#a8895f" stroke-width="2"/>' for i in range(1, 5)))


# ----------------------------------------------------------------- kit art ---
def kit_tile(x, y, label, inner):
    return (f'<rect x="{x}" y="{y}" width="250" height="196" rx="14" fill="#fff" stroke="#d8dee7" stroke-width="2"/>'
            f'<g transform="translate({x+125},{y+86})">{inner}</g>'
            f'<text x="{x+125}" y="{y+172}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" '
            f'font-weight="700" font-size="16" fill="#0f172a">{esc(label)}</text>')


def kit_grid(tiles):
    return "".join(kit_tile(56 + (i % 4) * 274, 200 + (i // 4) * 224, l, a) for i, (l, a) in enumerate(tiles))


def art(L):
    o = "#f97316"
    return dict(
        blades=('<rect x="-58" y="-30" width="52" height="62" rx="5" fill="url(#steelLite)" stroke="#5c636d" stroke-width="2"/>'
                '<rect x="6" y="-30" width="52" height="62" rx="5" fill="url(#steelLite)" stroke="#5c636d" stroke-width="2"/>'
                '<circle cx="-32" cy="-12" r="5" fill="#3d434b"/><circle cx="-32" cy="14" r="5" fill="#3d434b"/>'
                '<circle cx="32" cy="-12" r="5" fill="#3d434b"/><circle cx="32" cy="14" r="5" fill="#3d434b"/>'),
        toolroll=(f'<rect x="-64" y="-24" width="128" height="58" rx="8" fill="{L["g2"]}"/>'
                  f'<rect x="-64" y="-24" width="128" height="14" rx="7" fill="{L["g1"]}"/>'
                  '<rect x="-16" y="-38" width="32" height="16" rx="7" fill="#3d434b"/>'
                  '<rect x="-44" y="-4" width="24" height="6" rx="3" fill="#c9ced6"/>'
                  '<rect x="-8" y="-4" width="40" height="6" rx="3" fill="#c9ced6"/>'),
        push=(f'<rect x="-10" y="-46" width="20" height="78" rx="6" fill="{o}"/>'
              f'<rect x="-34" y="26" width="68" height="18" rx="6" fill="{L["g2"]}"/>'),
        ppe=('<path d="M-46 12 a46 40 0 0 1 92 0 z" fill="#f5b400"/>'
             '<rect x="-52" y="12" width="104" height="12" rx="6" fill="#d19a00"/>'
             '<rect x="-40" y="-30" width="80" height="12" rx="6" fill="#22262c"/>'),
        manual=('<rect x="-44" y="-52" width="88" height="106" rx="6" fill="#fff" stroke="#94a3b8" stroke-width="2"/>'
                f'<rect x="-44" y="-52" width="88" height="26" rx="6" fill="{L["g2"]}"/>'
                + "".join(f'<rect x="-30" y="{-14+i*16}" width="{60-i*8}" height="6" rx="3" fill="#cbd5e1"/>' for i in range(4))),
        lock=('<path d="M-26 -6 v-16 a26 26 0 0 1 52 0 v16" fill="none" stroke="#6b7280" stroke-width="12"/>'
              f'<rect x="-38" y="-8" width="76" height="58" rx="9" fill="{o}"/>'
              '<circle cx="0" cy="20" r="8" fill="#7c2d12"/>'),
        grease=(f'<rect x="-18" y="-44" width="36" height="76" rx="6" fill="{L["g2"]}"/>'
                '<rect x="-30" y="32" width="60" height="14" rx="6" fill="#3d434b"/>'
                '<path d="M0 -44 l40 -18" stroke="#6b7280" stroke-width="8" stroke-linecap="round"/>'),
        warranty=(f'<rect x="-56" y="-40" width="112" height="80" rx="9" fill="#fff" stroke="{L["acc"]}" stroke-width="3"/>'
                  f'<circle cx="0" cy="-6" r="20" fill="{L["acc"]}"/>'
                  f'<path d="M-9 -6 l7 8 l13 -16" stroke="{L["g3"]}" stroke-width="5" fill="none" stroke-linecap="round"/>'
                  '<rect x="-34" y="20" width="68" height="7" rx="3" fill="#cbd5e1"/>'),
        ramps=('<path d="M-70 30 L10 -34 L44 -34 L-36 30 Z" fill="url(#steelLite)" stroke="#5c636d" stroke-width="2"/>'
               '<path d="M-40 30 L40 -34 L74 -34 L-6 30 Z" fill="url(#steelLite)" stroke="#5c636d" stroke-width="2"/>'),
        straps=(f'<path d="M-64 -30 q64 40 128 0" fill="none" stroke="{L["acc"]}" stroke-width="14"/>'
                '<rect x="-18" y="6" width="36" height="30" rx="6" fill="#4b5563"/>'
                '<rect x="-30" y="34" width="60" height="10" rx="5" fill="#3d434b"/>'),
        tracks=('<rect x="-66" y="-22" width="132" height="46" rx="23" fill="url(#rubber)" stroke="#5c636d" stroke-width="2"/>'
                + "".join(f'<rect x="{-56+i*22}" y="14" width="13" height="9" rx="3" fill="#0c0e11"/>' for i in range(6))),
        teeth=("".join(f'<rect x="{-60+i*30}" y="-18" width="24" height="24" rx="5" fill="{o}" stroke="#7c2d12" stroke-width="2"/>' for i in range(5))
               + "".join(f'<rect x="{-60+i*30}" y="14" width="24" height="24" rx="5" fill="{o}" stroke="#7c2d12" stroke-width="2"/>' for i in range(5))),
        handset=(f'<rect x="-32" y="-46" width="64" height="92" rx="10" fill="#1b1f25" stroke="#3d434b" stroke-width="3"/>'
                 f'<rect x="-24" y="-37" width="48" height="23" rx="4" fill="#0b0e13"/>'
                 f'<rect x="-20" y="-31" width="26" height="4" rx="2" fill="{L["acc"]}"/>'
                 f'<circle cx="-15" cy="3" r="11" fill="#2a2f38" stroke="#5c636d" stroke-width="2"/>'
                 f'<circle cx="15" cy="3" r="11" fill="#2a2f38" stroke="#5c636d" stroke-width="2"/>'
                 '<circle cx="-15" cy="31" r="7" fill="#dc2626"/><circle cx="15" cy="31" r="7" fill="#4b5563"/>'),
        bucket=(f'<path d="M-52 -30 L44 -34 L62 30 Q0 48 -52 30 Z" fill="url(#paint)" stroke="{L["edge"]}" stroke-width="3"/>'
                '<path d="M44 -34 L62 30" stroke="#c9ced6" stroke-width="7" stroke-linecap="round"/>'),
        forks=('<rect x="-52" y="-36" width="16" height="72" rx="4" fill="url(#steelLite)" stroke="#5c636d" stroke-width="2"/>'
               '<rect x="-52" y="24" width="70" height="14" rx="4" fill="url(#steelLite)" stroke="#5c636d" stroke-width="2"/>'
               '<rect x="20" y="-36" width="16" height="72" rx="4" fill="url(#steelLite)" stroke="#5c636d" stroke-width="2"/>'
               '<rect x="20" y="24" width="46" height="14" rx="4" fill="url(#steelLite)" stroke="#5c636d" stroke-width="2"/>'),
    )


# ============================================================ SCENE SETS =====
def scenes_chipper(L):
    D, K, A = livery_defs(L), art(L), L["acc"]
    M = lambda **kw: chipper(**kw)
    return "cyclone-150", {
    '01-hero': doc(glow(L) + M() + caption("Cyclone 150 TD", "6″ road-towable diesel wood chipper")
        + badge(56, 148, "IN STOCK — UK WAREHOUSE", A) + badge(56, 198, "750 kg · CAR TOWABLE", "#1f2937", "#e5e7eb")
        + frame() + wm(L), defs=D, bg="dark"),
    '02-side': doc(M() + caption("Full side profile", "Compact 3.1 m towing length", light=True)
        + frame(True) + wm(L, True), defs=D, bg="light"),
    '03-infeed': doc(zoom(892, 374, 1.46, M(brand=False))
        + callout(430, 214, 300, 150, "1120 mm wide funnel", col=A)
        + callout(520, 470, 320, 566, "Twin hydraulic feed rollers", col=A)
        + callout(700, 176, 840, 140, "Red no-stress stop bar", col="#f87171")
        + callout(828, 428, 946, 520, "Hi-vis edge guard", col="#f97316")
        + caption("Wide-mouth infeed", "Swallows a 150 mm limb without pre-trimming")
        + frame() + wm(L), defs=D, bg="dark"),
    '04-engine': doc(zoom(600, 400, 1.34, M(brand=False))
        + panel(L, 640, 150, 452, 330, "ENGINE BAY — CUTAWAY",
                ["3-cylinder · liquid-cooled · 1123 cc", "Electric start · 12 V · 30 L tank"],
                engine_card(L, 640, 150))
        + callout(300, 300, 200, 214, "Hinged sealed bay", col=A)
        + callout(360, 500, 250, 576, "Ground-level service", col=A)
        + caption("Power unit", "25 hp Stage V diesel — no red-diesel restrictions")
        + frame() + wm(L), defs=D, bg="dark"),
    '05-controls': doc(zoom(560, 300, 1.34, M(brand=False))
        + callout(614, 118, 770, 96, "360° rotating chute", col=A)
        + callout(590, 210, 790, 210, "Adjustable chip deflector", col=A)
        + callout(430, 402, 250, 466, "Feed / reverse / e-stop", col=A)
        + callout(690, 470, 830, 520, "Lockable engine panel", col=A)
        + caption("Chute & operator controls", "Place the chip exactly where you want it, from the ground")
        + frame() + wm(L), defs=D, bg="dark"),
    '06-dimensions': doc(f'<g opacity=".92">{M()}</g>'
        + dim_h(78, 1062, 668, "3.12 m") + dim_v(108, 622, 1120, "1.42 m") + dim_h(400, 744, 236, "1.18 m")
        + f'<text x="56" y="714" font-family="Arial,Helvetica,sans-serif" font-size="17" fill="#7fb7d8">'
          f'Gross weight 748 kg — legal behind a standard car tow bar on a B licence</text>'
        + caption("Dimensions", "Fits through a standard single-garage opening")
        + frame() + wm(L), defs=D, bg="blueprint"),
    '07-in-use': doc(f'<rect width="{W}" height="{H}" fill="url(#skyG)"/>'
        + tree(105, 600, 415, 118, leaf="#33562f") + tree(1105, 600, 480, 118, leaf="#3a6135")
        + tree(255, 592, 300, 78, leaf="#41703a", op=".75") + scene_ground()
        + f'<g transform="translate(150,120) scale(0.78)">{M()}</g>'
        + f'<ellipse cx="262" cy="690" rx="128" ry="30" fill="#b8955f"/>'
        + f'<ellipse cx="262" cy="679" rx="94" ry="22" fill="#cba871"/>'
        + "".join(f'<rect x="{946+i*12}" y="{636+i*17}" width="164" height="15" rx="7" fill="#6b5238"/>' for i in range(3))
        + caption("Built for the arb round", "Four tonnes of chip an hour, all day", light=True)
        + wm(L, True), defs=D, bg="scene"),
    '08-included': doc(caption("In the crate", "Everything below ships with every Cyclone 150 TD", light=True)
        + kit_grid([("Spare blade set ×2", K['blades']), ("Tool & spanner roll", K['toolroll']),
                    ("Timber push paddle", K['push']), ("Helmet, visor & ear kit", K['ppe']),
                    ("Printed UK manual", K['manual']), ("Hitch lock & road pins", K['lock']),
                    ("Grease gun & cartridge", K['grease']), ("2-year parts warranty", K['warranty'])])
        + wm(L, True), defs=D, bg="flat")}


def scenes_grinder(L):
    D, K, A = livery_defs(L), art(L), L["acc"]
    M = lambda **kw: f'<g transform="translate(58,10)">{grinder(**kw)}</g>'
    return "grindmaster-380", {
    '01-hero': doc(glow(L) + M() + caption("Grindmaster 380 TX", "Tracked, self-propelled stump grinder")
        + badge(56, 148, "IN STOCK — UK WAREHOUSE", A) + badge(56, 198, "760 mm WIDE · FITS SIDE GATES", "#1f2937", "#e5e7eb")
        + frame() + wm(L), defs=D, bg="dark"),
    '02-side': doc(M() + caption("Full side profile", "Low, narrow and gate-friendly", light=True)
        + frame(True) + wm(L, True), defs=D, bg="light"),
    '03-cutter': doc(zoom(330, 500, 1.62, M(brand=False))
        + callout(430, 430, 600, 320, "16″ carbide cutter wheel", col=A)
        + callout(470, 560, 660, 620, "12 reversible teeth", col=A)
        + callout(240, 300, 340, 200, "Hinged debris shield", col=A)
        + caption("Cutting head", "Grinds 300 mm below grade in a single pass")
        + frame() + wm(L), defs=D, bg="dark"),
    '04-engine': doc(zoom(700, 350, 1.28, M(brand=False))
        + panel(L, 628, 150, 460, 322, "POWER UNIT",
                ["38 hp V-twin petrol · electric start", "Cyclonic pre-filter · 24 L tank"],
                engine_card(L, 628, 150, 460, 322))
        + callout(330, 250, 220, 176, "Vented steel cowl", col=A)
        + callout(330, 500, 356, 608, "Hydrostatic drive", col=A)
        + caption("Power unit", "38 hp V-twin — full torque into the wheel")
        + frame() + wm(L), defs=D, bg="dark"),
    '05-controls': doc(zoom(830, 330, 1.3, M(brand=False))
        + panel(L, 612, 128, 470, 500, "WALK-BESIDE HANDSET", ["Proportional twin-joystick · 25 m range"],
                f'<g transform="translate(848,340) scale(2.1)">{K["handset"]}</g>')
        + callout(300, 300, 262, 206, "Twin control levers", col=A)
        + callout(340, 484, 372, 578, "Stand clear of the wheel", col=A)
        + caption("Controls", "Work from a safe distance — never over the wheel")
        + frame() + wm(L), defs=D, bg="dark"),
    '06-dimensions': doc(f'<g opacity=".92">{M()}</g>'
        + dim_h(210, 1000, 676, "1.94 m") + dim_v(200, 622, 1112, "1.18 m") + dim_h(450, 874, 190, "760 mm width")
        + f'<text x="56" y="716" font-family="Arial,Helvetica,sans-serif" font-size="17" fill="#7fb7d8">'
          f'Operating weight 412 kg · 760 mm across the tracks — through a standard side gate</text>'
        + caption("Dimensions", "Narrow enough for back-garden access")
        + frame() + wm(L), defs=D, bg="blueprint"),
    '07-in-use': doc(f'<rect width="{W}" height="{H}" fill="url(#skyG)"/>'
        + tree(96, 596, 400, 112, leaf="#33562f") + tree(1116, 598, 452, 120, leaf="#3a6135") + scene_ground()
        + f'<g transform="translate(196,132) scale(0.74)">{grinder()}</g>'
        + stump(392, 594, 58, 40)
        + f'<ellipse cx="402" cy="656" rx="150" ry="30" fill="#c2a173" opacity=".95"/>'
        + f'<ellipse cx="402" cy="646" rx="106" ry="21" fill="#d8bd8f"/>'
        + caption("Ten stumps a day, no hire fees", "Pays for itself inside a season", light=True)
        + wm(L, True), defs=D, bg="scene"),
    '08-included': doc(caption("In the crate", "Everything below ships with every Grindmaster 380 TX", light=True)
        + kit_grid([("Spare carbide teeth ×10", K['teeth']), ("Radio handset + charger", K['handset']),
                    ("Tool & spanner roll", K['toolroll']), ("Helmet, visor & ear kit", K['ppe']),
                    ("Printed UK manual", K['manual']), ("Folding loading ramps", K['ramps']),
                    ("Grease gun & cartridge", K['grease']), ("2-year parts warranty", K['warranty'])])
        + wm(L, True), defs=D, bg="flat")}


def scenes_dumper(L):
    D, K, A = livery_defs(L), art(L), L["acc"]
    M = lambda **kw: dumper(**kw)
    return "titan-1000", {
    '01-hero': doc(glow(L) + M() + caption("Titan 1000 HT", "1-tonne tracked hydraulic high-tip dumper")
        + badge(56, 148, "IN STOCK — UK WAREHOUSE", A) + badge(56, 198, "1000 kg PAYLOAD · 700 mm WIDE", "#1f2937", "#e5e7eb")
        + frame() + wm(L), defs=D, bg="dark"),
    '02-side': doc(M() + caption("Full side profile", "Low centre of gravity, high tip", light=True)
        + frame(True) + wm(L, True), defs=D, bg="light"),
    '03-hightip': doc(glow(L) + M(tip_deg=40, load=True, lift=176)
        + callout(452, 176, 430, 116, "1300 mm tip height", col=A)
        + callout(626, 396, 800, 470, "Hydraulic scissor lift", col=A)
        + callout(330, 300, 360, 214, "Tips clear of a skip wall", col=A)
        + caption("High tip, over the wall", "Discharges straight into a builder's skip — no shovelling twice")
        + frame() + wm(L), defs=D, bg="dark"),
    '04-engine': doc(zoom(760, 400, 1.26, M(brand=False))
        + panel(L, 76, 150, 450, 326, "POWER PACK",
                ["13 hp OHV petrol · electric start", "Hydrostatic drive · 6.5 L tank"],
                engine_card(L, 76, 150, 450, 326))
        + callout(800, 300, 852, 200, "Vented steel cowl", col=A)
        + callout(700, 556, 830, 636, "Sealed hydraulic pump", col=A)
        + caption("Power pack", "13 hp electric-start petrol — turns over cold, every time")
        + frame() + wm(L), defs=D, bg="dark"),
    '05-controls': doc(zoom(858, 388, 1.16, M(brand=False))
        + callout(768, 232, 430, 150, "Twist-grip throttle", col=A)
        + callout(690, 300, 400, 262, "Tip / lower lever", col=A)
        + callout(690, 356, 840, 402, "Dead-man safety bar", col=A)
        + caption("Walk-behind controls", "Everything reachable without letting go of the bars")
        + frame() + wm(L), defs=D, bg="dark"),
    '06-dimensions': doc(f'<g opacity=".92">{M()}</g>'
        + dim_h(272, 1024, 676, "2.28 m") + dim_v(224, 622, 1116, "1.24 m") + dim_h(300, 706, 190, "700 mm width")
        + f'<text x="56" y="716" font-family="Arial,Helvetica,sans-serif" font-size="17" fill="#7fb7d8">'
          f'Unladen 385 kg · 1000 kg payload · 700 mm across the tracks</text>'
        + caption("Dimensions", "Through a standard doorway, down a terrace alley")
        + frame() + wm(L), defs=D, bg="blueprint"),
    '07-in-use': doc(site_bg() + heap(180, 600, 300, 130) + heap(1050, 596, 260, 110)
        + f'<g transform="translate(150,110) scale(0.76)">{dumper(load=True)}</g>'
        + caption("Twelve barrow loads in one run", "One tonne up the garden without a plank in sight", light=True)
        + wm(L, True), defs=D, bg="scene"),
    '08-included': doc(caption("In the crate", "Everything below ships with every Titan 1000 HT", light=True)
        + kit_grid([("Tool & spanner roll", K['toolroll']), ("Folding loading ramps", K['ramps']),
                    ("Ratchet transport straps", K['straps']), ("Helmet, gloves & ear kit", K['ppe']),
                    ("Printed UK manual", K['manual']), ("Spare rubber track", K['tracks']),
                    ("Grease gun & cartridge", K['grease']), ("2-year parts warranty", K['warranty'])])
        + wm(L, True), defs=D, bg="flat")}


def scenes_loader(L):
    D, K, A = livery_defs(L), art(L), L["acc"]
    M = lambda **kw: loader(**kw)
    return "vanguard-850", {
    '01-hero': doc(glow(L) + M() + caption("Vanguard 850 SL", "Stand-on compact tracked loader")
        + badge(56, 148, "IN STOCK — UK WAREHOUSE", A) + badge(56, 198, "850 kg LIFT · QUICK-ATTACH", "#1f2937", "#e5e7eb")
        + frame() + wm(L), defs=D, bg="dark"),
    '02-side': doc(M() + caption("Full side profile", "Short wheelbase, tight turning circle", light=True)
        + frame(True) + wm(L, True), defs=D, bg="light"),
    '03-bucket': doc(zoom(300, 430, 1.6, M(brand=False))
        + callout(500, 240, 660, 168, "Universal quick-attach plate", col=A)
        + callout(430, 560, 620, 630, "Bolt-on cutting teeth", col=A)
        + callout(760, 330, 880, 262, "850 kg lift at full height", col=A)
        + caption("Bucket & attachments", "Standard skid-steer plate — takes forks, grapples and augers")
        + frame() + wm(L), defs=D, bg="dark"),
    '04-engine': doc(zoom(700, 430, 1.3, M(brand=False))
        + panel(L, 76, 150, 450, 326, "POWER UNIT",
                ["23 hp V-twin petrol · electric start", "Twin hydraulic pumps · 30 L/min"],
                engine_card(L, 76, 150, 450, 326))
        + callout(800, 340, 866, 250, "Vented engine bay", col=A)
        + callout(720, 560, 800, 640, "Hydrostatic track drive", col=A)
        + caption("Power unit", "23 hp and 30 L/min — enough flow to run an auger")
        + frame() + wm(L), defs=D, bg="dark"),
    '05-controls': doc(zoom(800, 340, 1.36, M(brand=False))
        + callout(420, 190, 300, 128, "Twin joysticks", col=A)
        + callout(500, 300, 330, 300, "Backlit status panel", col=A)
        + callout(760, 520, 880, 596, "Sprung stand-on platform", col=A)
        + caption("Operator station", "Stand-on, not sit-in — step off at every gate without shutting down")
        + frame() + wm(L), defs=D, bg="dark"),
    '06-dimensions': doc(f'<g opacity=".92">{M()}</g>'
        + dim_h(134, 926, 676, "2.42 m") + dim_v(212, 620, 1090, "1.28 m") + dim_h(452, 782, 200, "890 mm width")
        + f'<text x="56" y="716" font-family="Arial,Helvetica,sans-serif" font-size="17" fill="#7fb7d8">'
          f'Operating weight 738 kg · 850 kg rated lift · 890 mm across the tracks</text>'
        + caption("Dimensions", "Fits a double gate and a standard plant trailer")
        + frame() + wm(L), defs=D, bg="blueprint"),
    '07-in-use': doc(site_bg() + heap(1020, 600, 320, 140) + heap(140, 594, 220, 96)
        + f'<g transform="translate(120,116) scale(0.76)">{loader()}</g>'
        + caption("Moves what a gang of three can't", "Muck away, hardcore in — one operator, one machine", light=True)
        + wm(L, True), defs=D, bg="scene"),
    '08-included': doc(caption("In the crate", "Everything below ships with every Vanguard 850 SL", light=True)
        + kit_grid([("600 mm general bucket", K['bucket']), ("Pallet fork set", K['forks']),
                    ("Ratchet transport straps", K['straps']), ("Helmet, gloves & ear kit", K['ppe']),
                    ("Printed UK manual", K['manual']), ("Spare rubber track", K['tracks']),
                    ("Grease gun & cartridge", K['grease']), ("2-year parts warranty", K['warranty'])])
        + wm(L, True), defs=D, bg="flat")}




# ====================================================== COMPACT PLANT SETS ===
def scenes_excavator(L):
    D, K, A = livery_defs(L), art(L), L["acc"]
    M = lambda **kw: excavator(**kw)
    return "ex10-excavator", {
    '01-hero': doc(wash(L) + M() + caption("EX10 Mini Excavator", "1 tonne rubber-tracked digger with a dozer blade", light=lit(L))
        + badge(56, 148, "IN STOCK — UK WAREHOUSE", A) + badge(56, 198, "930 mm RETRACTED · 1.75 m DIG", "#1f2937", "#e5e7eb")
        + frame(lit(L)) + wm(L, lit(L)), defs=D, bg=studio(L)),
    '02-side': doc(M() + caption("Full side profile", "Arm folded for transport", light=True)
        + frame(True) + wm(L, True), defs=D, bg="light"),
    '03-dig': doc(wash(L) + M(boom=16, curl=-26, blade=0)
        + callout(300, 420, 224, 300, "300 mm digging bucket", col=A)
        + callout(400, 300, 560, 200, "3.2 m reach at ground level", col=A)
        + callout(520, 452, 700, 540, "360° slew with boom offset", col=A)
        + caption("Dig depth and reach", "1.75 m down, 3.2 m out, 2.3 m to the dump height", light=lit(L))
        + frame(lit(L)) + wm(L, lit(L)), defs=D, bg=studio(L)),
    '04-cab': doc(zoom(596, 300, 1.42, M(brand=False))
        + callout(528, 288, 300, 176, "Twin pilot joysticks", col=A)
        + callout(600, 226, 812, 150, "ROPS/FOPS canopy", col=A)
        + callout(700, 400, 880, 470, "Sealed engine bay", col=A)
        + caption("Operator station", "Open canopy — step on and off at every gate", light=lit(L))
        + frame(lit(L)) + wm(L, lit(L)), defs=D, bg=studio(L)),
    '05-undercarriage': doc(zoom(500, 540, 1.42, M(brand=False))
        + callout(300, 570, 250, 660, "930–1200 mm variable width", col=A)
        + callout(262, 572, 300, 470, "930 mm dozer blade", col=A)
        + callout(640, 580, 830, 640, "180 mm rubber tracks", col=A)
        + caption("Undercarriage & blade", "Retract to get in, expand to dig, blade to backfill", light=lit(L))
        + frame(lit(L)) + wm(L, lit(L)), defs=D, bg=studio(L)),
    '06-dimensions': doc(f'<g opacity=".92">{M()}</g>'
        + dim_h(216, 906, 672, "3.10 m") + dim_v(212, 620, 1084, "2.28 m") + dim_h(322, 808, 706, "930 mm retracted")
        + f'<text x="56" y="734" font-family="Arial,Helvetica,sans-serif" font-size="17" fill="#7fb7d8">'
          f'Operating weight 1050 kg · dig depth 1.75 m · 2000 kg plant trailer moves it legally</text>'
        + caption("Dimensions", "Through a wide gate, onto a car-towed plant trailer", light=lit(L))
        + frame(lit(L)) + wm(L, lit(L)), defs=D, bg="blueprint"),
    '07-in-use': doc(site_bg() + heap(1040, 600, 300, 128)
        + f'<rect x="150" y="596" width="330" height="76" rx="10" fill="#5a4b38"/>'
        + f'<g transform="translate(120,110) scale(0.76)">{excavator(boom=10, curl=-20)}</g>'
        + caption("A day's trench, not a week's", "Footings, drainage and service runs without a gang", light=True)
        + wm(L, True), defs=D, bg="scene"),
    '08-included': doc(caption("In the crate", "Everything below ships with every EX10", light=True)
        + kit_grid([("300 mm digging bucket", K['bucket']), ("Auxiliary hose couplers", K['grease']),
                    ("Ratchet transport straps", K['straps']), ("Helmet, gloves & ear kit", K['ppe']),
                    ("Printed UK manual", K['manual']), ("Tool & spanner roll", K['toolroll']),
                    ("Spare rubber track", K['tracks']), ("2-year parts warranty", K['warranty'])])
        + wm(L, True), defs=D, bg="flat")}


def scenes_minidumper(L):
    D, K, A = livery_defs(L), art(L), L["acc"]
    M = lambda **kw: minidumper(**kw)
    return "td500-dumper", {
    '01-hero': doc(wash(L) + M() + caption("TD500 Mini Dumper", "500 kg tracked dumper with a hydraulic tip", light=lit(L))
        + badge(56, 148, "IN STOCK — UK WAREHOUSE", A) + badge(56, 198, "500 kg PAYLOAD · 780 mm WIDE", "#1f2937", "#e5e7eb")
        + frame(lit(L)) + wm(L, lit(L)), defs=D, bg=studio(L)),
    '02-side': doc(M() + caption("Full side profile", "Low skip lip, high ground clearance", light=True)
        + frame(True) + wm(L, True), defs=D, bg="light"),
    '03-tip': doc(wash(L) + M(tip_deg=36, load=True)
        + callout(430, 250, 620, 172, "Hydraulic tip on one lever", col=A)
        + callout(600, 470, 790, 546, "Front pivot — the load runs out", col=A)
        + caption("Tips itself empty", "You never shovel the same spoil twice", light=lit(L))
        + frame(lit(L)) + wm(L, lit(L)), defs=D, bg=studio(L)),
    '04-engine': doc(zoom(716, 440, 1.3, M(brand=False))
        + panel(L, 76, 150, 450, 326, "POWER PACK",
                ["9 hp OHV petrol · recoil start", "Hydrostatic drive · 6.5 L tank"],
                engine_card(L, 76, 150, 450, 326))
        + callout(790, 300, 856, 210, "Vented steel cowl", col=A)
        + callout(700, 540, 812, 620, "Sealed hydraulic pump", col=A)
        + caption("Power pack", "9 hp petrol — starts on the pull after a month standing", light=lit(L))
        + frame(lit(L)) + wm(L, lit(L)), defs=D, bg=studio(L)),
    '05-controls': doc(zoom(880, 350, 1.22, M(brand=False))
        + callout(770, 240, 420, 152, "Twist-grip throttle", col=A)
        + callout(700, 320, 400, 272, "Tip / lower lever", col=A)
        + callout(720, 380, 860, 430, "Dead-man safety bar", col=A)
        + caption("Walk-behind controls", "Everything reachable without letting go of the bars", light=lit(L))
        + frame(lit(L)) + wm(L, lit(L)), defs=D, bg=studio(L)),
    '06-dimensions': doc(f'<g opacity=".92">{M()}</g>'
        + dim_h(240, 970, 676, "1.95 m") + dim_v(300, 620, 1092, "1.05 m") + dim_h(300, 690, 706, "780 mm width")
        + f'<text x="56" y="734" font-family="Arial,Helvetica,sans-serif" font-size="17" fill="#7fb7d8">'
          f'Unladen 265 kg · 500 kg payload · 720 mm loading height · 780 mm across the tracks</text>'
        + caption("Dimensions", "Through a standard doorway, down a terrace alley", light=lit(L))
        + frame(lit(L)) + wm(L, lit(L)), defs=D, bg="blueprint"),
    '07-in-use': doc(site_bg() + heap(170, 600, 280, 120) + heap(1060, 596, 240, 100)
        + f'<g transform="translate(140,116) scale(0.76)">{minidumper(load=True)}</g>'
        + caption("Twelve barrow loads in one run", "Half a tonne up the garden without a plank", light=True)
        + wm(L, True), defs=D, bg="scene"),
    '08-included': doc(caption("In the crate", "Everything below ships with every TD500", light=True)
        + kit_grid([("Tool & spanner roll", K['toolroll']), ("Folding loading ramps", K['ramps']),
                    ("Ratchet transport straps", K['straps']), ("Helmet, gloves & ear kit", K['ppe']),
                    ("Printed UK manual", K['manual']), ("Grease gun & cartridge", K['grease']),
                    ("Spare drive belt", K['tracks']), ("2-year parts warranty", K['warranty'])])
        + wm(L, True), defs=D, bg="flat")}


def scenes_splitter(L):
    D, K, A = livery_defs(L), art(L), L["acc"]
    M = lambda **kw: splitter(**kw)
    return "ls22-splitter", {
    '01-hero': doc(wash(L) + M(log=True) + caption("LS22 Log Splitter", "22 tonne towable petrol splitter", light=lit(L))
        + badge(56, 148, "IN STOCK — UK WAREHOUSE", A) + badge(56, 198, "22 TONNES · 14 SECOND CYCLE", "#1f2937", "#e5e7eb")
        + frame(lit(L)) + wm(L, lit(L)), defs=D, bg=studio(L)),
    '02-side': doc(M() + caption("Full side profile", "Horizontal beam on its own road chassis", light=True)
        + frame(True) + wm(L, True), defs=D, bg="light"),
    '03-wedge': doc(zoom(420, 400, 1.5, M(brand=False, log=True, stroke=120))
        + callout(318, 340, 520, 216, "Hardened two-way wedge", col=A)
        + callout(268, 392, 180, 268, "Cradle wings hold the halves", col=A)
        + callout(600, 380, 800, 300, "Push plate, 22 tonnes behind it", col=A)
        + caption("Working end", "650 mm long, 400 mm across — rolled on, not lifted", light=lit(L))
        + frame(lit(L)) + wm(L, lit(L)), defs=D, bg=studio(L)),
    '04-engine': doc(zoom(900, 340, 1.24, M(brand=False))
        + panel(L, 76, 150, 450, 326, "ENGINE & HYDRAULICS",
                ["15 hp OHV petrol · recoil start", "Two-stage pump · 26 L reservoir"],
                engine_card(L, 76, 150, 450, 326))
        + callout(820, 300, 900, 208, "Two-stage gear pump", col=A)
        + callout(880, 520, 960, 604, "Road chassis and axle", col=A)
        + caption("Engine & hydraulics", "Fast on approach, slow and hard into the wood", light=lit(L))
        + frame(lit(L)) + wm(L, lit(L)), defs=D, bg=studio(L)),
    '05-controls': doc(zoom(640, 400, 1.36, M(brand=False))
        + callout(700, 336, 880, 246, "Two-hand valve lever", col=A)
        + callout(190, 486, 300, 590, "50 mm ball hitch", col=A)
        + callout(186, 540, 320, 640, "Jockey leg", col=A)
        + caption("Controls & towing", "Both hands on levers while the wedge moves", light=lit(L))
        + frame(lit(L)) + wm(L, lit(L)), defs=D, bg=studio(L)),
    '06-dimensions': doc(f'<g opacity=".92">{M(log=True)}</g>'
        + dim_h(92, 1000, 676, "2.45 m towing length") + dim_v(286, 620, 1094, "0.80 m working height")
        + dim_h(336, 636, 712, "650 mm log")
        + f'<text x="56" y="738" font-family="Arial,Helvetica,sans-serif" font-size="17" fill="#7fb7d8">'
          f'22 tonnes of force · 14 second cycle · 285 kg on its own single-axle chassis</text>'
        + caption("Dimensions", "Beam at working height, hitch at the front", light=lit(L))
        + frame(lit(L)) + wm(L, lit(L)), defs=D, bg="blueprint"),
    '07-in-use': doc(f'<rect width="{W}" height="{H}" fill="url(#skyG)"/>'
        + tree(104, 596, 400, 112, leaf="#33562f") + tree(1112, 598, 448, 118, leaf="#3a6135") + scene_ground()
        + "".join(f'<rect x="{910+ (i%3)*54}" y="{560 - (i//3)*40}" width="48" height="36" rx="6" '
                  f'fill="#a8895f" stroke="#7c6242" stroke-width="2"/>' for i in range(9))
        + f'<g transform="translate(40,120) scale(0.74)">{splitter(log=True, stroke=90)}</g>'
        + caption("A winter of firewood in a weekend", "Twenty-two tonnes takes what is in a UK log pile", light=True)
        + wm(L, True), defs=D, bg="scene"),
    '08-included': doc(caption("In the crate", "Everything below ships with every LS22", light=True)
        + kit_grid([("Log cradle wings", K['forks']), ("Tool & spanner roll", K['toolroll']),
                    ("Timber push paddle", K['push']), ("Helmet, visor & ear kit", K['ppe']),
                    ("Printed UK manual", K['manual']), ("Hitch lock & jockey leg", K['lock']),
                    ("Grease gun & cartridge", K['grease']), ("2-year parts warranty", K['warranty'])])
        + wm(L, True), defs=D, bg="flat")}


def scenes_flail(L):
    D, K, A = livery_defs(L), art(L), L["acc"]
    M = lambda **kw: flail(**kw)
    return "fm150-flail", {
    '01-hero': doc(wash(L) + M() + caption("FM150 ATV Flail Mower", "1200 mm trailed flail with its own 15 hp engine", light=lit(L))
        + badge(56, 148, "IN STOCK — UK WAREHOUSE", A) + badge(56, 198, "1200 mm CUT · 40 FLAILS", "#1f2937", "#e5e7eb")
        + frame(lit(L)) + wm(L, lit(L)), defs=D, bg=studio(L)),
    '02-side': doc(M() + caption("Full side profile", "Drawbar forward, roller behind", light=True)
        + frame(True) + wm(L, True), defs=D, bg="light"),
    '03-rotor': doc(zoom(540, 500, 1.5, M(brand=False, cutaway=True))
        + callout(540, 500, 760, 380, "40 swinging hammer flails", col=A)
        + callout(430, 590, 300, 680, "Mulched and dropped under the deck", col=A)
        + caption("Inside the housing", "Hammers swing back off a stone instead of bending", light=lit(L))
        + frame(lit(L)) + wm(L, lit(L)), defs=D, bg=studio(L)),
    '04-engine': doc(zoom(584, 320, 1.34, M(brand=False))
        + panel(L, 76, 150, 450, 326, "POWER UNIT",
                ["15 hp OHV petrol · electric start", "Guarded belt drive to the rotor"],
                engine_card(L, 76, 150, 450, 326))
        + callout(700, 300, 856, 214, "Guarded belt drive", col=A)
        + callout(600, 214, 800, 140, "Key start, recoil back-up", col=A)
        + caption("Power unit", "Its own engine — full rotor speed behind any quad", light=lit(L))
        + frame(lit(L)) + wm(L, lit(L)), defs=D, bg=studio(L)),
    '05-hitch': doc(zoom(500, 520, 1.3, M(brand=False))
        + callout(180, 470, 300, 350, "Pin hitch drawbar", col=A)
        + callout(848, 596, 940, 500, "Rear roller sets the cut", col=A)
        + callout(303, 596, 240, 690, "Flotation wheels", col=A)
        + caption("Hitch & height setting", "25–100 mm on a pin, not a spanner", light=lit(L))
        + frame(lit(L)) + wm(L, lit(L)), defs=D, bg=studio(L)),
    '06-dimensions': doc(f'<g opacity=".92">{M()}</g>'
        + dim_h(96, 878, 678, "1.98 m with drawbar") + dim_v(192, 626, 1090, "0.86 m")
        + dim_h(300, 822, 712, "1200 mm cutting width")
        + f'<text x="56" y="738" font-family="Arial,Helvetica,sans-serif" font-size="17" fill="#7fb7d8">'
          f'245 kg · cutting height 25–100 mm on the rear roller · pin hitch for ATV, UTV or compact tractor</text>'
        + caption("Dimensions", "Cuts wider than the wheel tracks of the quad pulling it", light=lit(L))
        + frame(lit(L)) + wm(L, lit(L)), defs=D, bg="blueprint"),
    '07-in-use': doc(f'<rect width="{W}" height="{H}" fill="url(#skyG)"/>'
        + tree(96, 596, 392, 110, leaf="#33562f") + tree(1120, 598, 440, 116, leaf="#3a6135") + scene_ground()
        + "".join(f'<path d="M{60+i*38} 700 q5 -30 12 -44" fill="none" stroke="#6f8f45" '
                  f'stroke-width="6" stroke-linecap="round"/>' for i in range(30))
        + f'<g transform="translate(150,96) scale(0.76)">{flail(cut=True)}</g>'
        + caption("Two years of neglect, one afternoon", "Brambles, nettles and saplings to 25 mm", light=True)
        + wm(L, True), defs=D, bg="scene"),
    '08-included': doc(caption("In the crate", "Everything below ships with every FM150", light=True)
        + kit_grid([("Spare hammer flails ×10", K['teeth']), ("Tool & spanner roll", K['toolroll']),
                    ("Spare drive belt", K['tracks']), ("Helmet, visor & ear kit", K['ppe']),
                    ("Printed UK manual", K['manual']), ("Hitch pin & linch set", K['lock']),
                    ("Grease gun & cartridge", K['grease']), ("2-year parts warranty", K['warranty'])])
        + wm(L, True), defs=D, bg="flat")}


CLASSIC = (scenes_chipper, scenes_grinder, scenes_dumper, scenes_loader)
COMPACT = (scenes_excavator, scenes_minidumper, scenes_splitter, scenes_flail)

# which four machines each store sells
SETS = {"branchforge": CLASSIC, "haulcrest": CLASSIC,
        "rootvexx": COMPACT, "lawnstride": COMPACT}


def build():
    total = 0
    for L in livery.ALL:
        livery.use(L)
        wanted = set()
        for fn in SETS[L['key']]:
            slug, scenes = fn(L)
            wanted.add(slug)
            out = f"{ROOT}/{L['key']}/assets/img/{slug}"
            os.makedirs(out, exist_ok=True)
            for name, svg in scenes.items():
                assert "{" not in svg, (L['key'], slug, name)
                for other in livery.ALL:
                    if other is not L:
                        assert other['brand'] not in svg, (L['key'], slug, name, "brand leak")
                open(f"{out}/{name}.svg", "w").write(svg)
                total += 1
        # a store that changed catalogue must not keep the old machines' galleries
        import shutil
        img = f"{ROOT}/{L['key']}/assets/img"
        for d in sorted(os.listdir(img)) if os.path.isdir(img) else []:
            if os.path.isdir(f"{img}/{d}") and d not in wanted and _generated(f"{img}/{d}"):
                shutil.rmtree(f"{img}/{d}")
                print("  removed stale gallery", L['key'], d)
    return total


def _generated(d):
    """True for a directory this script owns -- an 01-hero.svg and nothing a
       photographer put there. Photographed galleries are never touched."""
    names = os.listdir(d)
    return "01-hero.svg" in names and not any(n.endswith((".jpeg", ".webp", ".png")) for n in names)


if __name__ == "__main__":
    print("wrote", build(), "images")
