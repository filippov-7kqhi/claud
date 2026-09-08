"""BranchForge Grindmaster 380 TX - tracked self-propelled stump grinder."""
import sys, math
sys.path.insert(0,'/home/user/claud/tools')
from svgkit import *
import livery

ORANGE = "#f97316"
MODEL = "GRINDMASTER 380 TX"


def grinder(brand=True, guard=True, arm_deg=0):
    L = livery.CUR; BRAND = L["brand"]
    g=[]; A=g.append
    # far-side depth plane
    A(f'<g opacity=".5"><rect x="470" y="330" width="330" height="230" rx="12" fill="{L["rec2"]}"/>'
      f'<path d="M500 356 L830 356 L800 328 L470 328 Z" fill="{L["rec2"]}"/></g>')

    # ---- undercarriage -----------------------------------------------------
    A(track(392, 540, 424, 80))
    A(f'<rect x="404" y="500" width="404" height="48" rx="10" fill="url(#steel)" stroke="#171b21" stroke-width="2"/>')

    # ---- main deck / body --------------------------------------------------
    A(f'<rect x="470" y="356" width="330" height="152" rx="12" fill="url(#paint)" stroke="{L["edge"]}" stroke-width="3"/>')
    A(f'<path d="M470 356 L800 356 L770 326 L452 328 Z" fill="url(#paintTop)" stroke="{L["edge"]}" stroke-width="3"/>')
    A(louvres(690, 384, 96, 96, n=6))
    A(f'<rect x="486" y="378" width="182" height="80" rx="8" fill="{L["rec"]}" opacity=".4"/>')
    A(bolts([(482,368),(788,368),(482,496),(788,496)]))

    # ---- engine cowl on top ------------------------------------------------
    A(f'<rect x="556" y="268" width="228" height="92" rx="12" fill="url(#paint)" stroke="{L["edge"]}" stroke-width="3"/>')
    A(f'<path d="M556 268 L784 268 L760 244 L532 244 Z" fill="url(#paintTop)" stroke="{L["edge"]}" stroke-width="3"/>')
    A(louvres(692, 286, 78, 60, n=5))
    A(f'<rect x="576" y="230" width="54" height="22" rx="7" fill="#2a2f38" stroke="#171b21" stroke-width="2"/>')  # air filter
    A(f'<rect x="640" y="212" width="20" height="42" rx="6" fill="#31363d"/>')  # exhaust
    A(f'<rect x="632" y="200" width="36" height="16" rx="7" fill="#1b1f25"/>')

    # ---- cutter arm --------------------------------------------------------
    A(f'<g transform="rotate({arm_deg} 476 452)">')
    A(f'<path d="M476 414 L476 492 L300 552 L268 512 Z" fill="url(#paint)" stroke="{L["edge"]}" stroke-width="3"/>')
    A(f'<path d="M462 408 L488 408 L488 500 L462 500 Z" fill="{L["mid"]}" stroke="{L["edge"]}" stroke-width="2"/>')
    # belt guard along arm
    A(f'<path d="M470 424 L306 480 L294 512 L470 470 Z" fill="{L["lite"]}" opacity=".8"/>')
    # cutter wheel
    cx, cy, r = 258, 528, 76
    A(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#steelLite)" stroke="#3d434b" stroke-width="4"/>')
    A(f'<circle cx="{cx}" cy="{cy}" r="{r*0.55}" fill="#6b7280" stroke="#3d434b" stroke-width="3"/>')
    A(f'<circle cx="{cx}" cy="{cy}" r="{r*0.18}" fill="#31363d"/>')
    for a in range(0, 360, 30):
        tx, ty = cx + r*0.86*math.cos(math.radians(a)), cy + r*0.86*math.sin(math.radians(a))
        A(f'<rect x="{tx-9}" y="{ty-9}" width="18" height="18" rx="4" fill="{ORANGE}" '
          f'stroke="#7c2d12" stroke-width="2" transform="rotate({a} {tx} {ty})"/>')
    A(f'<circle cx="{cx}" cy="{cy}" r="{r*0.34}" fill="#8b929c"/>')
    A(bolts([(cx+r*0.42*math.cos(math.radians(a)), cy+r*0.42*math.sin(math.radians(a))) for a in range(0,360,60)], r=4))
    # debris shield
    if guard:
        A(f'<path d="M154 528 A104 104 0 0 1 312 440 L296 462 A78 78 0 0 0 180 528 Z" '
          f'fill="#3d434b" stroke="#171b21" stroke-width="3"/>')
        A(hazard_stripes(150, 500, 26, 56))
    A(f'</g>')

    # hydraulic lift ram, deck -> arm
    A(f'<path d="M492 416 L446 444" stroke="#4b5563" stroke-width="21" stroke-linecap="round"/>')
    A(f'<path d="M448 443 L404 470" stroke="#c9ced6" stroke-width="11" stroke-linecap="round"/>')
    A(f'<circle cx="492" cy="416" r="9" fill="#31363d" stroke="#8c939d" stroke-width="2"/>')
    A(f'<circle cx="404" cy="470" r="8" fill="#31363d" stroke="#8c939d" stroke-width="2"/>')
    A(hose(486, 494, 404, 522, sag=18, w=6))

    # ---- operator station --------------------------------------------------
    A(f'<rect x="792" y="368" width="64" height="26" rx="8" fill="url(#steel)" stroke="#171b21" stroke-width="2"/>')
    A(f'<path d="M828 380 L860 372 L868 300 L840 300 Z" fill="url(#steel)" stroke="#171b21" stroke-width="2"/>')
    A(f'<rect x="808" y="286" width="112" height="66" rx="9" fill="#12161b" stroke="{L["edge"]}" stroke-width="2" transform="rotate(-8 808 286)"/>')
    A(f'<g transform="rotate(-8 808 286)"><circle cx="836" cy="308" r="10" fill="#dc2626"/>'
      f'<circle cx="864" cy="308" r="8" fill="#4ade80"/><rect x="822" y="326" width="86" height="9" rx="4" fill="#3d434b"/></g>')
    A(f'<path d="M862 300 L932 262" stroke="#4b5563" stroke-width="13" stroke-linecap="round"/>')
    A(f'<path d="M862 316 L928 288" stroke="#4b5563" stroke-width="13" stroke-linecap="round"/>')
    A(f'<circle cx="936" cy="258" r="13" fill="{ORANGE}"/><circle cx="932" cy="286" r="13" fill="{ORANGE}"/>')

    # ---- decals ------------------------------------------------------------
    if brand:
        A(decal(606, 420, BRAND, size=25, col=L["ink"], sub=MODEL, subcol=L["sub"]))
        A(decal(670, 316, "380", size=34, col=L["sub"]))
    return "".join(g)
