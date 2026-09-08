import sys, os, math
sys.path.insert(0,'/home/user/claud/tools')
from svgkit import *
from bf_chipper import chipper, PAINT, BRAND, MODEL, LIME, ORANGE

OUT = sys.argv[1] if len(sys.argv)>1 else '/home/user/claud/branchforge/assets/img/cyclone-150'
os.makedirs(OUT, exist_ok=True)

def zoom(cx, cy, k, inner):
    return f'<g transform="translate({600-k*cx:.1f},{380-k*cy:.1f}) scale({k})">{inner}</g>'

def frame(light=False):
    c = "#0f172a" if light else "#ffffff"
    return (f'<rect x="26" y="26" width="{W-52}" height="{H-52}" rx="16" fill="none" '
            f'stroke="{c}" stroke-width="1.5" opacity=".14"/>')

def wm(light=False):
    c = "#0f172a" if light else "#ffffff"
    return (f'<text x="{W-56}" y="{H-42}" text-anchor="end" font-family="Arial,Helvetica,sans-serif" '
            f'font-weight="800" font-size="17" letter-spacing="3.5" fill="{c}" opacity=".38">BRANCHFORGE</text>')

S = {}

# 1 - hero -------------------------------------------------------------------
S['01-hero'] = doc(
    f'<ellipse cx="600" cy="300" rx="470" ry="250" fill="#a3e635" opacity=".05"/>'
    + chipper()
    + caption("Cyclone 150 TD", "6″ road-towable diesel wood chipper")
    + badge(56, 148, "IN STOCK — UK WAREHOUSE", LIME)
    + badge(56, 198, "750 kg · CAR TOWABLE", "#1f2937", "#e5e7eb")
    + frame() + wm(), defs=PAINT, bg="dark")

# 2 - side profile -----------------------------------------------------------
S['02-side'] = doc(
    chipper() + caption("Full side profile", "Compact 3.1 m towing length", light=True)
    + frame(True) + wm(True), defs=PAINT, bg="light")

# 3 - infeed hopper ----------------------------------------------------------
S['03-infeed'] = doc(
    zoom(892, 374, 1.46, chipper(brand=False))
    + callout(430, 214, 300, 150, "1120 mm wide funnel")
    + callout(520, 470, 320, 566, "Twin hydraulic feed rollers")
    + callout(700, 176, 840, 140, "Red no-stress stop bar", col="#f87171")
    + callout(828, 428, 946, 520, "Hi-vis edge guard", col=ORANGE)
    + caption("Wide-mouth infeed", "Swallows a 150 mm limb without pre-trimming")
    + frame() + wm(), defs=PAINT, bg="dark")

# 4 - engine bay -------------------------------------------------------------
S['04-engine'] = doc(
    zoom(600, 400, 1.34, chipper(brand=False))
    + f'<rect x="640" y="150" width="452" height="330" rx="16" fill="#0d1117" stroke="{LIME}" stroke-width="2.5" opacity=".97"/>'
    + f'<text x="672" y="192" font-family="Arial,Helvetica,sans-serif" font-weight="800" font-size="20" fill="{LIME}">ENGINE BAY — CUTAWAY</text>'
    + f'<g transform="translate(672,214)">' + engine_block(0, 0, 388, 176) + '</g>'
    + f'<g transform="translate(672,214)">'
      f'<circle cx="330" cy="88" r="34" fill="#2a2f38" stroke="#6b7280" stroke-width="3"/>'
      f'<circle cx="330" cy="88" r="13" fill="#9aa2ad"/>'
      f'<rect x="20" y="-16" width="120" height="16" rx="8" fill="#3d434b"/></g>'
    + f'<text x="672" y="432" font-family="Arial,Helvetica,sans-serif" font-size="17" fill="#cbd5e1">'
      f'3-cylinder · liquid-cooled · 1123 cc</text>'
    + f'<text x="672" y="458" font-family="Arial,Helvetica,sans-serif" font-size="17" fill="#cbd5e1">'
      f'Electric start · 12 V · 30 L tank</text>'
    + callout(300, 300, 200, 214, "Hinged sealed bay")
    + callout(360, 500, 250, 576, "Ground-level service")
    + caption("Power unit", "25 hp Stage V diesel — no red-diesel restrictions")
    + frame() + wm(), defs=PAINT, bg="dark")

# 5 - chute & controls -------------------------------------------------------
S['05-controls'] = doc(
    zoom(560, 300, 1.34, chipper(brand=False))
    + callout(614, 118, 770, 96, "360° rotating chute")
    + callout(590, 210, 790, 210, "Adjustable chip deflector")
    + callout(430, 402, 250, 466, "Feed / reverse / e-stop")
    + callout(690, 470, 830, 520, "Lockable engine panel")
    + caption("Chute & operator controls", "Place the chip exactly where you want it, from the ground")
    + frame() + wm(), defs=PAINT, bg="dark")

# 6 - dimensions -------------------------------------------------------------
S['06-dimensions'] = doc(
    f'<g opacity=".92">{chipper()}</g>'
    + dim_h(78, 1062, 668, "3.12 m")
    + dim_v(108, 622, 1120, "1.42 m")
    + dim_h(400, 744, 236, "1.18 m")
    + f'<text x="56" y="714" font-family="Arial,Helvetica,sans-serif" font-size="17" fill="#7fb7d8">'
      f'Gross weight 748 kg — legal behind a standard car tow bar on a B licence</text>'
    + caption("Dimensions", "Fits through a standard single-garage opening")
    + frame() + wm(), defs=PAINT, bg="blueprint")

# 7 - on site ----------------------------------------------------------------
S['07-in-use'] = doc(
    f'<rect width="{W}" height="{H}" fill="url(#skyG)"/>'
    + tree(105, 600, 415, 118, leaf="#33562f") + tree(1105, 600, 480, 118, leaf="#3a6135")
    + tree(255, 592, 300, 78, leaf="#41703a", op=".75")
    + scene_ground()
    + f'<g transform="translate(150,120) scale(0.78)">{chipper()}</g>'
    + f'<ellipse cx="262" cy="690" rx="128" ry="30" fill="#b8955f"/>'
    + f'<ellipse cx="262" cy="679" rx="94" ry="22" fill="#cba871"/>'
    + "".join(f'<rect x="{946+i*12}" y="{636+i*17}" width="164" height="15" rx="7" fill="#6b5238"/>' for i in range(3))
    + caption("Built for the arb round", "Four tonnes of chip an hour, all day", light=True)
    + wm(True), defs=PAINT, bg="scene")

# 8 - what's included --------------------------------------------------------
def kit_tile(x, y, label, inner):
    return (f'<rect x="{x}" y="{y}" width="250" height="196" rx="14" fill="#fff" stroke="#d8dee7" stroke-width="2"/>'
            f'<g transform="translate({x+125},{y+86})">{inner}</g>'
            f'<text x="{x+125}" y="{y+172}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" '
            f'font-weight="700" font-size="16" fill="#0f172a">{esc(label)}</text>')

blades = ('<rect x="-58" y="-30" width="52" height="62" rx="5" fill="url(#steelLite)" stroke="#5c636d" stroke-width="2"/>'
          '<rect x="6" y="-30" width="52" height="62" rx="5" fill="url(#steelLite)" stroke="#5c636d" stroke-width="2"/>'
          '<circle cx="-32" cy="-12" r="5" fill="#3d434b"/><circle cx="-32" cy="14" r="5" fill="#3d434b"/>'
          '<circle cx="32" cy="-12" r="5" fill="#3d434b"/><circle cx="32" cy="14" r="5" fill="#3d434b"/>')
toolkit = ('<rect x="-64" y="-24" width="128" height="58" rx="8" fill="#1f5c39"/>'
           '<rect x="-64" y="-24" width="128" height="14" rx="7" fill="#2f7d4f"/>'
           '<rect x="-16" y="-38" width="32" height="16" rx="7" fill="#3d434b"/>'
           '<rect x="-44" y="-4" width="24" height="6" rx="3" fill="#c9ced6"/>'
           '<rect x="-8" y="-4" width="40" height="6" rx="3" fill="#c9ced6"/>')
push = ('<rect x="-10" y="-46" width="20" height="78" rx="6" fill="#f97316"/>'
        '<rect x="-34" y="26" width="68" height="18" rx="6" fill="#1f5c39"/>')
ppe = ('<path d="M-46 12 a46 40 0 0 1 92 0 z" fill="#f5b400"/><rect x="-52" y="12" width="104" height="12" rx="6" fill="#d19a00"/>'
       '<rect x="-40" y="-30" width="80" height="12" rx="6" fill="#22262c"/>')
manual = ('<rect x="-44" y="-52" width="88" height="106" rx="6" fill="#fff" stroke="#94a3b8" stroke-width="2"/>'
          '<rect x="-44" y="-52" width="88" height="26" rx="6" fill="#1f5c39"/>'
          + "".join(f'<rect x="-30" y="{-14+i*16}" width="{60-i*8}" height="6" rx="3" fill="#cbd5e1"/>' for i in range(4)))
lock = ('<path d="M-26 -6 v-16 a26 26 0 0 1 52 0 v16" fill="none" stroke="#6b7280" stroke-width="12"/>'
        '<rect x="-38" y="-8" width="76" height="58" rx="9" fill="#f97316"/>'
        '<circle cx="0" cy="20" r="8" fill="#7c2d12"/>')
grease = ('<rect x="-18" y="-44" width="36" height="76" rx="6" fill="#1f5c39"/>'
          '<rect x="-30" y="32" width="60" height="14" rx="6" fill="#3d434b"/>'
          '<path d="M0 -44 l40 -18" stroke="#6b7280" stroke-width="8" stroke-linecap="round"/>')
warranty = ('<rect x="-56" y="-40" width="112" height="80" rx="9" fill="#fff" stroke="#a3e635" stroke-width="3"/>'
            '<circle cx="0" cy="-6" r="20" fill="#a3e635"/>'
            '<path d="M-9 -6 l7 8 l13 -16" stroke="#14532d" stroke-width="5" fill="none" stroke-linecap="round"/>'
            '<rect x="-34" y="20" width="68" height="7" rx="3" fill="#cbd5e1"/>')

tiles = [("Cyclone 150 TD chipper", blades), ("Spare blade set ×2", blades), ("Tool & spanner roll", toolkit),
         ("Timber push paddle", push), ("Helmet, visor & ear kit", ppe), ("Printed UK manual", manual),
         ("Hitch lock & road pins", lock), ("1-year parts warranty", warranty)]
tiles[0] = ("Spare blade set ×2", blades)
tiles = [("Spare blade set ×2", blades), ("Tool & spanner roll", toolkit), ("Timber push paddle", push),
         ("Helmet, visor & ear kit", ppe), ("Printed UK manual", manual), ("Hitch lock & road pins", lock),
         ("Grease gun & cartridge", grease), ("1-year parts warranty", warranty)]
grid = "".join(kit_tile(56 + (i % 4) * 274, 200 + (i // 4) * 224, lbl, art) for i, (lbl, art) in enumerate(tiles))
S['08-included'] = doc(caption("In the crate", "Everything below ships with every Cyclone 150 TD", light=True)
                       + grid + wm(True), defs=PAINT, bg="flat")

for name, svg in S.items():
    open(f'{OUT}/{name}.svg','w').write(svg)
print("wrote", len(S), "->", OUT)
