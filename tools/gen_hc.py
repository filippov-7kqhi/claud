import sys, os, math
sys.path.insert(0,'/home/user/claud/tools')
from svgkit import *
from hc_dumper import dumper, PAINT, BRAND, AMBER, SUN, GRAPH
from hc_loader import loader

AC = AMBER
def zoom(cx, cy, k, inner):
    return f'<g transform="translate({600-k*cx:.1f},{380-k*cy:.1f}) scale({k})">{inner}</g>'
def frame(light=False):
    c="#0f172a" if light else "#ffffff"
    return f'<rect x="26" y="26" width="{W-52}" height="{H-52}" rx="16" fill="none" stroke="{c}" stroke-width="1.5" opacity=".14"/>'
def wm(light=False):
    c="#0f172a" if light else "#ffffff"
    return (f'<text x="{W-56}" y="{H-42}" text-anchor="end" font-family="Arial,Helvetica,sans-serif" '
            f'font-weight="800" font-size="17" letter-spacing="3.5" fill="{c}" opacity=".38">HAULCREST</text>')
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
def kit_tile(x,y,label,inner):
    return (f'<rect x="{x}" y="{y}" width="250" height="196" rx="14" fill="#fff" stroke="#d8dee7" stroke-width="2"/>'
            f'<g transform="translate({x+125},{y+86})">{inner}</g>'
            f'<text x="{x+125}" y="{y+172}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" '
            f'font-weight="700" font-size="16" fill="#0f172a">{esc(label)}</text>')
def grid(tiles):
    return "".join(kit_tile(56+(i%4)*274, 200+(i//4)*224, l, a) for i,(l,a) in enumerate(tiles))

TOOLROLL = ('<rect x="-64" y="-24" width="128" height="58" rx="8" fill="#b45309"/>'
            '<rect x="-64" y="-24" width="128" height="14" rx="7" fill="#f59e0b"/>'
            '<rect x="-16" y="-38" width="32" height="16" rx="7" fill="#3d434b"/>'
            '<rect x="-44" y="-4" width="24" height="6" rx="3" fill="#c9ced6"/>'
            '<rect x="-8" y="-4" width="40" height="6" rx="3" fill="#c9ced6"/>')
PPE = ('<path d="M-46 12 a46 40 0 0 1 92 0 z" fill="#f5b400"/><rect x="-52" y="12" width="104" height="12" rx="6" fill="#d19a00"/>'
       '<rect x="-40" y="-30" width="80" height="12" rx="6" fill="#22262c"/>')
MANUAL = ('<rect x="-44" y="-52" width="88" height="106" rx="6" fill="#fff" stroke="#94a3b8" stroke-width="2"/>'
          '<rect x="-44" y="-52" width="88" height="26" rx="6" fill="#b45309"/>'
          + "".join(f'<rect x="-30" y="{-14+i*16}" width="{60-i*8}" height="6" rx="3" fill="#cbd5e1"/>' for i in range(4)))
RAMPS = ('<path d="M-70 30 L10 -34 L44 -34 L-36 30 Z" fill="url(#steelLite)" stroke="#5c636d" stroke-width="2"/>'
         '<path d="M-40 30 L40 -34 L74 -34 L-6 30 Z" fill="url(#steelLite)" stroke="#5c636d" stroke-width="2"/>')
GREASE = ('<rect x="-18" y="-44" width="36" height="76" rx="6" fill="#b45309"/>'
          '<rect x="-30" y="32" width="60" height="14" rx="6" fill="#3d434b"/>'
          '<path d="M0 -44 l40 -18" stroke="#6b7280" stroke-width="8" stroke-linecap="round"/>')
WARRANTY = ('<rect x="-56" y="-40" width="112" height="80" rx="9" fill="#fff" stroke="#f59e0b" stroke-width="3"/>'
            '<circle cx="0" cy="-6" r="20" fill="#f59e0b"/>'
            '<path d="M-9 -6 l7 8 l13 -16" stroke="#7c2d12" stroke-width="5" fill="none" stroke-linecap="round"/>'
            '<rect x="-34" y="20" width="68" height="7" rx="3" fill="#cbd5e1"/>')
STRAPS = ('<path d="M-64 -30 q64 40 128 0" fill="none" stroke="#f59e0b" stroke-width="14"/>'
          '<rect x="-18" y="6" width="36" height="30" rx="6" fill="#4b5563"/>'
          '<rect x="-30" y="34" width="60" height="10" rx="5" fill="#3d434b"/>')
TRACKS = ('<rect x="-66" y="-22" width="132" height="46" rx="23" fill="url(#rubber)" stroke="#5c636d" stroke-width="2"/>'
          + "".join(f'<rect x="{-56+i*22}" y="14" width="13" height="9" rx="3" fill="#0c0e11"/>' for i in range(6)))

# ============================================================ DUMPER ==========
def build_dumper(OUT):
    os.makedirs(OUT, exist_ok=True)
    M = lambda **kw: dumper(**kw)
    S={}
    S['01-hero'] = doc(f'<ellipse cx="600" cy="330" rx="470" ry="250" fill="#f59e0b" opacity=".06"/>' + M()
        + caption("Titan 1000 HT", "1-tonne tracked hydraulic high-tip dumper")
        + badge(56, 148, "IN STOCK — UK WAREHOUSE", AC)
        + badge(56, 198, "1000 kg PAYLOAD · 700 mm WIDE", "#1f2937", "#e5e7eb")
        + frame() + wm(), defs=PAINT, bg="dark")

    S['02-side'] = doc(M() + caption("Full side profile", "Low centre of gravity, high tip", light=True)
        + frame(True) + wm(True), defs=PAINT, bg="light")

    S['03-hightip'] = doc(f'<ellipse cx="600" cy="330" rx="470" ry="250" fill="#f59e0b" opacity=".06"/>'
        + M(tip_deg=40, load=True, lift=176)
        + callout(452, 176, 430, 116, "1300 mm tip height", col=AC)
        + callout(626, 396, 800, 470, "Hydraulic scissor lift", col=AC)
        + callout(330, 300, 360, 214, "Tips clear of a skip wall", col=AC)
        + caption("High tip, over the wall", "Discharges straight into a builder's skip — no shovelling twice")
        + frame() + wm(), defs=PAINT, bg="dark")

    S['04-engine'] = doc(zoom(760, 400, 1.26, M(brand=False))
        + f'<rect x="76" y="150" width="450" height="326" rx="16" fill="#0d1117" stroke="{AC}" stroke-width="2.5"/>'
        + f'<text x="108" y="192" font-family="Arial,Helvetica,sans-serif" font-weight="800" font-size="20" fill="{AC}">POWER PACK</text>'
        + f'<g transform="translate(108,214)">' + engine_block(0,0,386,172) + '</g>'
        + f'<g transform="translate(108,214)"><circle cx="330" cy="86" r="32" fill="#2a2f38" stroke="#6b7280" stroke-width="3"/>'
          f'<circle cx="330" cy="86" r="12" fill="#9aa2ad"/><rect x="22" y="-14" width="110" height="14" rx="7" fill="#3d434b"/></g>'
        + f'<text x="108" y="426" font-family="Arial,Helvetica,sans-serif" font-size="17" fill="#cbd5e1">13 hp OHV petrol · electric start</text>'
        + f'<text x="108" y="452" font-family="Arial,Helvetica,sans-serif" font-size="17" fill="#cbd5e1">Hydrostatic drive · 6 L tank</text>'
        + callout(756, 424, 852, 336, "Vented steel cowl", col=AC)
        + callout(700, 556, 830, 636, "Sealed hydraulic pump", col=AC)
        + caption("Power pack", "13 hp electric-start petrol — turns over cold, every time")
        + frame() + wm(), defs=PAINT, bg="dark")

    S['05-controls'] = doc(zoom(858, 388, 1.16, M(brand=False))
        + callout(768, 232, 430, 150, "Twist-grip throttle", col=AC)
        + callout(690, 300, 400, 262, "Tip / lower lever", col=AC)
        + callout(690, 356, 840, 402, "Dead-man safety bar", col=AC)
        + caption("Walk-behind controls", "Everything reachable without letting go of the bars")
        + frame() + wm(), defs=PAINT, bg="dark")

    S['06-dimensions'] = doc(f'<g opacity=".92">{M()}</g>'
        + dim_h(272, 1024, 676, "2.28 m")
        + dim_v(224, 622, 1116, "1.24 m")
        + dim_h(300, 706, 190, "700 mm width")
        + f'<text x="56" y="716" font-family="Arial,Helvetica,sans-serif" font-size="17" fill="#7fb7d8">'
          f'Unladen 385 kg · 1000 kg payload · 700 mm across the tracks</text>'
        + caption("Dimensions", "Through a standard doorway, down a terrace alley")
        + frame() + wm(), defs=PAINT, bg="blueprint")

    S['07-in-use'] = doc(site_bg()
        + heap(180, 600, 300, 130) + heap(1050, 596, 260, 110)
        + f'<g transform="translate(150,110) scale(0.76)">{dumper(load=True)}</g>'
        + caption("Twelve barrow loads in one run", "One tonne up the garden without a plank in sight", light=True)
        + wm(True), defs=PAINT, bg="scene")

    S['08-included'] = doc(caption("In the crate","Everything below ships with every Titan 1000 HT",light=True)
        + grid([("Tool & spanner roll",TOOLROLL),("Folding loading ramps",RAMPS),("Ratchet transport straps",STRAPS),
                ("Helmet, gloves & ear kit",PPE),("Printed UK manual",MANUAL),("Spare rubber track",TRACKS),
                ("Grease gun & cartridge",GREASE),("1-year parts warranty",WARRANTY)])
        + wm(True), defs=PAINT, bg="flat")
    for n,s in S.items(): open(f'{OUT}/{n}.svg','w').write(s)
    return len(S)


# ============================================================ LOADER ==========
def build_loader(OUT):
    os.makedirs(OUT, exist_ok=True)
    M = lambda **kw: loader(**kw)
    S={}
    S['01-hero'] = doc(f'<ellipse cx="600" cy="330" rx="470" ry="250" fill="#f59e0b" opacity=".06"/>' + M()
        + caption("Vanguard 850 SL", "Stand-on compact tracked loader")
        + badge(56, 148, "IN STOCK — UK WAREHOUSE", AC)
        + badge(56, 198, "850 kg LIFT · QUICK-ATTACH", "#1f2937", "#e5e7eb")
        + frame() + wm(), defs=PAINT, bg="dark")

    S['02-side'] = doc(M() + caption("Full side profile", "Short wheelbase, tight turning circle", light=True)
        + frame(True) + wm(True), defs=PAINT, bg="light")

    S['03-bucket'] = doc(zoom(300, 430, 1.6, M(brand=False))
        + callout(500, 240, 660, 168, "Universal quick-attach plate", col=AC)
        + callout(430, 560, 620, 630, "Bolt-on cutting teeth", col=AC)
        + callout(760, 330, 880, 262, "850 kg lift at full height", col=AC)
        + caption("Bucket & attachments", "Standard skid-steer plate — takes forks, grapples and augers")
        + frame() + wm(), defs=PAINT, bg="dark")

    S['04-engine'] = doc(zoom(700, 430, 1.3, M(brand=False))
        + f'<rect x="76" y="150" width="450" height="326" rx="16" fill="#0d1117" stroke="{AC}" stroke-width="2.5"/>'
        + f'<text x="108" y="192" font-family="Arial,Helvetica,sans-serif" font-weight="800" font-size="20" fill="{AC}">POWER UNIT</text>'
        + f'<g transform="translate(108,214)">' + engine_block(0,0,386,172) + '</g>'
        + f'<g transform="translate(108,214)"><circle cx="330" cy="86" r="32" fill="#2a2f38" stroke="#6b7280" stroke-width="3"/>'
          f'<circle cx="330" cy="86" r="12" fill="#9aa2ad"/><rect x="22" y="-14" width="110" height="14" rx="7" fill="#3d434b"/></g>'
        + f'<text x="108" y="426" font-family="Arial,Helvetica,sans-serif" font-size="17" fill="#cbd5e1">23 hp V-twin petrol · electric start</text>'
        + f'<text x="108" y="452" font-family="Arial,Helvetica,sans-serif" font-size="17" fill="#cbd5e1">Twin hydraulic pumps · 30 L/min</text>'
        + callout(800, 340, 866, 250, "Vented engine bay", col=AC)
        + callout(720, 560, 800, 640, "Hydrostatic track drive", col=AC)
        + caption("Power unit", "23 hp and 30 L/min — enough flow to run an auger")
        + frame() + wm(), defs=PAINT, bg="dark")

    S['05-controls'] = doc(zoom(800, 340, 1.36, M(brand=False))
        + callout(420, 190, 300, 128, "Twin joysticks", col=AC)
        + callout(500, 300, 330, 300, "Backlit status panel", col=AC)
        + callout(760, 520, 880, 596, "Sprung stand-on platform", col=AC)
        + caption("Operator station", "Stand-on, not sit-in — step off at every gate without shutting down")
        + frame() + wm(), defs=PAINT, bg="dark")

    S['06-dimensions'] = doc(f'<g opacity=".92">{M()}</g>'
        + dim_h(134, 926, 676, "2.42 m")
        + dim_v(212, 620, 1090, "1.28 m")
        + dim_h(452, 782, 200, "890 mm width")
        + f'<text x="56" y="716" font-family="Arial,Helvetica,sans-serif" font-size="17" fill="#7fb7d8">'
          f'Operating weight 738 kg · 850 kg rated lift · 890 mm across the tracks</text>'
        + caption("Dimensions", "Fits a double gate and a standard plant trailer")
        + frame() + wm(), defs=PAINT, bg="blueprint")

    S['07-in-use'] = doc(site_bg()
        + heap(1020, 600, 320, 140) + heap(140, 594, 220, 96)
        + f'<g transform="translate(120,116) scale(0.76)">{loader()}</g>'
        + caption("Moves what a gang of three can't", "Muck away, hardcore in — one operator, one machine", light=True)
        + wm(True), defs=PAINT, bg="scene")

    S['08-included'] = doc(caption("In the crate","Everything below ships with every Vanguard 850 SL",light=True)
        + grid([("600 mm general bucket",TOOLROLL),("Pallet fork set",RAMPS),("Ratchet transport straps",STRAPS),
                ("Helmet, gloves & ear kit",PPE),("Printed UK manual",MANUAL),("Spare rubber track",TRACKS),
                ("Grease gun & cartridge",GREASE),("1-year parts warranty",WARRANTY)])
        + wm(True), defs=PAINT, bg="flat")
    for n,s in S.items(): open(f'{OUT}/{n}.svg','w').write(s)
    return len(S)


if __name__ == "__main__":
    r = '/home/user/claud/haulcrest/assets/img'
    print("dumper", build_dumper(r+'/titan-1000'), "| loader", build_loader(r+'/vanguard-850'))
