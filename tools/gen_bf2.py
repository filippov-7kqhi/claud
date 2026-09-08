import sys, os, math
sys.path.insert(0,'/home/user/claud/tools')
from svgkit import *
from bf_grinder import grinder, MODEL
from bf_chipper import PAINT, BRAND, LIME, ORANGE

OUT = sys.argv[1] if len(sys.argv)>1 else '/home/user/claud/branchforge/assets/img/grindmaster-380'
os.makedirs(OUT, exist_ok=True)
M = lambda **kw: f'<g transform="translate(58,10)">{grinder(**kw)}</g>'

def zoom(cx, cy, k, inner):
    return f'<g transform="translate({600-k*cx:.1f},{380-k*cy:.1f}) scale({k})">{inner}</g>'
def frame(light=False):
    c="#0f172a" if light else "#ffffff"
    return f'<rect x="26" y="26" width="{W-52}" height="{H-52}" rx="16" fill="none" stroke="{c}" stroke-width="1.5" opacity=".14"/>'
def wm(light=False):
    c="#0f172a" if light else "#ffffff"
    return (f'<text x="{W-56}" y="{H-42}" text-anchor="end" font-family="Arial,Helvetica,sans-serif" '
            f'font-weight="800" font-size="17" letter-spacing="3.5" fill="{c}" opacity=".38">BRANCHFORGE</text>')

def stump(x, y, r=64, h=52):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r*0.34}" fill="#c9a978"/>'
            f'<path d="M{x-r} {y} v{h} a{r} {r*0.34} 0 0 0 {2*r} 0 v-{h} z" fill="#8a6b45"/>'
            + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{r-i*11}" ry="{(r-i*11)*0.34}" fill="none" '
                      f'stroke="#a8895f" stroke-width="2"/>' for i in range(1,5)))

S={}
S['01-hero'] = doc(
    f'<ellipse cx="600" cy="320" rx="450" ry="240" fill="#a3e635" opacity=".05"/>' + M()
    + caption("Grindmaster 380 TX", "Tracked, self-propelled stump grinder")
    + badge(56, 148, "IN STOCK — UK WAREHOUSE", LIME)
    + badge(56, 198, "760 mm WIDE · FITS SIDE GATES", "#1f2937", "#e5e7eb")
    + frame() + wm(), defs=PAINT, bg="dark")

S['02-side'] = doc(M() + caption("Full side profile", "Low, narrow and gate-friendly", light=True)
                   + frame(True) + wm(True), defs=PAINT, bg="light")

S['03-cutter'] = doc(
    zoom(330, 500, 1.62, M(brand=False))
    + callout(430, 430, 600, 320, "16″ carbide cutter wheel")
    + callout(470, 560, 660, 620, "12 reversible teeth")
    + callout(240, 300, 340, 200, "Hinged debris shield")
    + caption("Cutting head", "Grinds 300 mm below grade in a single pass")
    + frame() + wm(), defs=PAINT, bg="dark")

S['04-engine'] = doc(
    zoom(700, 350, 1.28, M(brand=False))
    + f'<rect x="628" y="150" width="460" height="322" rx="16" fill="#0d1117" stroke="{LIME}" stroke-width="2.5"/>'
    + f'<text x="660" y="192" font-family="Arial,Helvetica,sans-serif" font-weight="800" font-size="20" fill="{LIME}">POWER UNIT</text>'
    + f'<g transform="translate(660,212)">' + engine_block(0,0,396,172) + '</g>'
    + f'<g transform="translate(660,212)"><circle cx="336" cy="86" r="32" fill="#2a2f38" stroke="#6b7280" stroke-width="3"/>'
      f'<circle cx="336" cy="86" r="12" fill="#9aa2ad"/><rect x="24" y="-14" width="110" height="14" rx="7" fill="#3d434b"/></g>'
    + f'<text x="660" y="424" font-family="Arial,Helvetica,sans-serif" font-size="17" fill="#cbd5e1">38 hp V-twin petrol · electric start</text>'
    + f'<text x="660" y="450" font-family="Arial,Helvetica,sans-serif" font-size="17" fill="#cbd5e1">Cyclonic pre-filter · 24 L tank</text>'
    + callout(330, 250, 220, 176, "Vented steel cowl")
    + callout(330, 500, 356, 608, "Hydrostatic drive")
    + caption("Power unit", "38 hp V-twin — full torque into the wheel")
    + frame() + wm(), defs=PAINT, bg="dark")

# remote control handset
remote = ('<rect x="-72" y="-104" width="144" height="208" rx="20" fill="#1b1f25" stroke="#3d434b" stroke-width="3"/>'
          '<rect x="-54" y="-84" width="108" height="52" rx="8" fill="#0b0e13"/>'
          f'<rect x="-46" y="-72" width="60" height="8" rx="4" fill="{LIME}"/>'
          '<rect x="-46" y="-58" width="86" height="6" rx="3" fill="#3d434b"/>'
          f'<circle cx="-34" cy="6" r="24" fill="#2a2f38" stroke="#5c636d" stroke-width="3"/>'
          f'<circle cx="-34" cy="6" r="10" fill="{ORANGE}"/>'
          f'<circle cx="34" cy="6" r="24" fill="#2a2f38" stroke="#5c636d" stroke-width="3"/>'
          f'<circle cx="34" cy="6" r="10" fill="{ORANGE}"/>'
          '<circle cx="-34" cy="70" r="15" fill="#dc2626"/><circle cx="34" cy="70" r="15" fill="#4b5563"/>'
          '<rect x="-16" y="-124" width="8" height="24" rx="4" fill="#6b7280"/>')

S['05-controls'] = doc(
    zoom(830, 330, 1.3, M(brand=False))
    + f'<rect x="612" y="128" width="470" height="500" rx="18" fill="#0d1117" stroke="{LIME}" stroke-width="2.5"/>'
    + f'<text x="646" y="172" font-family="Arial,Helvetica,sans-serif" font-weight="800" font-size="20" fill="{LIME}">WALK-BESIDE HANDSET</text>'
    + f'<g transform="translate(848,340)">{remote}</g>'
    + f'<text x="646" y="588" font-family="Arial,Helvetica,sans-serif" font-size="17" fill="#cbd5e1">'
      f'Proportional twin-joystick · 25 m range</text>'
    + callout(300, 300, 262, 206, "Twin control levers")
    + callout(340, 484, 372, 578, "Stand clear of the wheel")
    + caption("Controls", "Work from a safe distance — never over the wheel")
    + frame() + wm(), defs=PAINT, bg="dark")

S['06-dimensions'] = doc(
    f'<g opacity=".92">{M()}</g>'
    + dim_h(210, 1000, 676, "1.94 m")
    + dim_v(200, 622, 1112, "1.18 m")
    + dim_h(450, 874, 190, "760 mm width")
    + f'<text x="56" y="716" font-family="Arial,Helvetica,sans-serif" font-size="17" fill="#7fb7d8">'
      f'Operating weight 412 kg · 760 mm across the tracks — through a standard side gate</text>'
    + caption("Dimensions", "Narrow enough for back-garden access")
    + frame() + wm(), defs=PAINT, bg="blueprint")

S['07-in-use'] = doc(
    f'<rect width="{W}" height="{H}" fill="url(#skyG)"/>'
    + tree(96, 596, 400, 112, leaf="#33562f") + tree(1116, 598, 452, 120, leaf="#3a6135")
    + scene_ground()
    + f'<g transform="translate(196,132) scale(0.74)">{grinder()}</g>'
    + stump(392, 594, 58, 40)
    + f'<ellipse cx="402" cy="656" rx="150" ry="30" fill="#c2a173" opacity=".95"/>'
    + f'<ellipse cx="402" cy="646" rx="106" ry="21" fill="#d8bd8f"/>'
    + caption("Ten stumps a day, no hire fees", "Pays for itself inside a season", light=True)
    + wm(True), defs=PAINT, bg="scene")

def kit_tile(x,y,label,inner):
    return (f'<rect x="{x}" y="{y}" width="250" height="196" rx="14" fill="#fff" stroke="#d8dee7" stroke-width="2"/>'
            f'<g transform="translate({x+125},{y+86})">{inner}</g>'
            f'<text x="{x+125}" y="{y+172}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" '
            f'font-weight="700" font-size="16" fill="#0f172a">{esc(label)}</text>')

teeth = ("".join(f'<rect x="{-60+i*30}" y="-18" width="24" height="24" rx="5" fill="{ORANGE}" stroke="#7c2d12" stroke-width="2"/>'
                 for i in range(5))
         + "".join(f'<rect x="{-60+i*30}" y="14" width="24" height="24" rx="5" fill="{ORANGE}" stroke="#7c2d12" stroke-width="2"/>'
                   for i in range(5)))
handset = f'<g transform="scale(0.44)">{remote}</g>'
toolroll = ('<rect x="-64" y="-24" width="128" height="58" rx="8" fill="#1f5c39"/>'
            '<rect x="-64" y="-24" width="128" height="14" rx="7" fill="#2f7d4f"/>'
            '<rect x="-16" y="-38" width="32" height="16" rx="7" fill="#3d434b"/>'
            '<rect x="-44" y="-4" width="24" height="6" rx="3" fill="#c9ced6"/>')
ppe = ('<path d="M-46 12 a46 40 0 0 1 92 0 z" fill="#f5b400"/><rect x="-52" y="12" width="104" height="12" rx="6" fill="#d19a00"/>'
       '<rect x="-40" y="-30" width="80" height="12" rx="6" fill="#22262c"/>')
manual = ('<rect x="-44" y="-52" width="88" height="106" rx="6" fill="#fff" stroke="#94a3b8" stroke-width="2"/>'
          '<rect x="-44" y="-52" width="88" height="26" rx="6" fill="#1f5c39"/>'
          + "".join(f'<rect x="-30" y="{-14+i*16}" width="{60-i*8}" height="6" rx="3" fill="#cbd5e1"/>' for i in range(4)))
ramps = ('<path d="M-70 30 L10 -34 L44 -34 L-36 30 Z" fill="url(#steelLite)" stroke="#5c636d" stroke-width="2"/>'
         '<path d="M-40 30 L40 -34 L74 -34 L-6 30 Z" fill="url(#steelLite)" stroke="#5c636d" stroke-width="2"/>')
grease = ('<rect x="-18" y="-44" width="36" height="76" rx="6" fill="#1f5c39"/>'
          '<rect x="-30" y="32" width="60" height="14" rx="6" fill="#3d434b"/>'
          '<path d="M0 -44 l40 -18" stroke="#6b7280" stroke-width="8" stroke-linecap="round"/>')
warranty = ('<rect x="-56" y="-40" width="112" height="80" rx="9" fill="#fff" stroke="#a3e635" stroke-width="3"/>'
            '<circle cx="0" cy="-6" r="20" fill="#a3e635"/>'
            '<path d="M-9 -6 l7 8 l13 -16" stroke="#14532d" stroke-width="5" fill="none" stroke-linecap="round"/>'
            '<rect x="-34" y="20" width="68" height="7" rx="3" fill="#cbd5e1"/>')

tiles=[("Spare carbide teeth ×10",teeth),("Radio handset + charger",handset),("Tool & spanner roll",toolroll),
       ("Helmet, visor & ear kit",ppe),("Printed UK manual",manual),("Folding loading ramps",ramps),
       ("Grease gun & cartridge",grease),("1-year parts warranty",warranty)]
grid="".join(kit_tile(56+(i%4)*274, 200+(i//4)*224, l, a) for i,(l,a) in enumerate(tiles))
S['08-included'] = doc(caption("In the crate","Everything below ships with every Grindmaster 380 TX",light=True)
                       + grid + wm(True), defs=PAINT, bg="flat")

for n,s in S.items(): open(f'{OUT}/{n}.svg','w').write(s)
print("wrote", len(S))
