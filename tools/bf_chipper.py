"""BranchForge Cyclone 150 TD - 6in road-towable diesel wood chipper."""
import sys, math
sys.path.insert(0, '/home/user/claud/tools')
from svgkit import *
import livery


MODEL = "CYCLONE 150 TD"
ORANGE = "#f97316"


def chipper(scale=1.0, dx=0, dy=0, chute_deg=0, feed_open=True, brand=True):
    L = livery.CUR; BRAND = L["brand"]
    g = []
    A = g.append
    # ---- depth / far-side plane -------------------------------------------
    A(f'<g opacity=".55">')
    A(f'<path d="M400 292 L744 292 L716 262 L372 262 Z" fill="{L["rec2"]}"/>')
    A(f'<rect x="372" y="262" width="344" height="252" rx="10" fill="{L["rec2"]}"/>')
    A(f'</g>')

    # ---- trailer chassis ---------------------------------------------------
    A(f'<path d="M306 520 H906 V552 H306 Z" fill="url(#steel)" stroke="#171b21" stroke-width="2"/>')
    A(f'<path d="M306 520 L246 542 L246 566 L306 552 Z" fill="url(#steel)" stroke="#171b21" stroke-width="2"/>')
    # drawbar
    A(f'<path d="M246 546 L120 566 L120 584 L246 566 Z" fill="url(#steel)" stroke="#171b21" stroke-width="2"/>')
    A(f'<rect x="78" y="556" width="52" height="34" rx="8" fill="#3d434b" stroke="#171b21" stroke-width="2"/>')
    A(f'<circle cx="104" cy="573" r="9" fill="#1b1f25"/>')
    A(hazard_stripes(84, 594, 60, 16))
    # jockey wheel
    A(f'<rect x="196" y="560" width="16" height="44" rx="4" fill="#4b5563" stroke="#171b21" stroke-width="2"/>')
    A(wheel(204, 612, 20, hub="#9aa2ad"))
    # safety chain
    A(hose(150, 578, 236, 566, sag=26, col="#6b7280", w=4))
    # stabiliser leg
    A(f'<rect x="876" y="548" width="18" height="62" rx="4" fill="#4b5563" stroke="#171b21" stroke-width="2"/>')
    A(f'<rect x="862" y="606" width="46" height="14" rx="4" fill="#31363d"/>')

    # ---- road wheels -------------------------------------------------------
    A(f'<rect x="560" y="500" width="152" height="34" rx="8" fill="#2a2f38"/>')  # mudguard mount
    A(f'<path d="M556 536 q80 -78 160 0 z" fill="#15181d" opacity=".9"/>')
    A(wheel(636, 558, 64))

    # ---- main body ---------------------------------------------------------
    A(f'<rect x="400" y="292" width="344" height="230" rx="12" fill="url(#paint)" stroke="{L["edge"]}" stroke-width="3"/>')
    A(f'<path d="M400 292 L744 292 L716 262 L372 262 Z" fill="url(#paintTop)" stroke="{L["edge"]}" stroke-width="3"/>')
    # recessed rotor housing (subtle, behind decals)
    A(f'<circle cx="482" cy="444" r="64" fill="{L["mid"]}" stroke="{L["edge"]}" stroke-width="2.5" opacity=".85"/>')
    A(f'<circle cx="482" cy="444" r="44" fill="{L["rec"]}" opacity=".6"/>')
    A(f'<g opacity=".8">' + bolts([(482+52*math.cos(a*math.pi/180), 444+52*math.sin(a*math.pi/180))
                                   for a in range(0,360,60)], r=3.4) + '</g>')
    # engine bay door
    A(f'<rect x="624" y="300" width="112" height="210" rx="9" fill="{L["lite"]}" stroke="{L["edge"]}" stroke-width="2.5"/>')
    A(louvres(636, 390, 88, 108, n=7))
    A(f'<rect x="614" y="392" width="14" height="28" rx="4" fill="#c9ced6"/>')
    # control panel, top-right of body
    A(f'<rect x="636" y="312" width="88" height="62" rx="7" fill="#12161b" stroke="{L["edge"]}" stroke-width="2"/>')
    A(f'<circle cx="660" cy="334" r="10" fill="#dc2626"/>')
    A(f'<circle cx="686" cy="334" r="8" fill="#4ade80"/>')
    A(f'<circle cx="708" cy="334" r="8" fill="{ORANGE}"/>')
    A(f'<rect x="648" y="352" width="66" height="8" rx="4" fill="#3d434b"/>')
    A(bolts([(412,304),(732,304),(412,510),(732,510)]))

    # ---- discharge chute ---------------------------------------------------
    A(f'<g transform="rotate({chute_deg} 476 292)">')
    A(f'<path d="M418 298 L534 298 L556 168 L474 168 Z" fill="url(#paint)" stroke="{L["edge"]}" stroke-width="3"/>')
    A(f'<path d="M438 288 L524 288 L540 186 L478 186 Z" fill="{L["rec"]}" opacity=".35"/>')
    A(f'<rect x="410" y="276" width="132" height="24" rx="7" fill="#31363d" stroke="#171b21" stroke-width="2"/>')
    A(f'<circle cx="428" cy="288" r="7" fill="#9aa2ad"/><circle cx="524" cy="288" r="7" fill="#9aa2ad"/>')
    # deflector flap
    A(f'<path d="M470 170 L560 170 L586 116 L502 108 Z" fill="#2a2f38" stroke="#171b21" stroke-width="3"/>')
    A(f'<rect x="466" y="160" width="98" height="15" rx="6" fill="{ORANGE}"/>')
    A(f'<circle cx="470" cy="170" r="8" fill="#9aa2ad" stroke="#171b21" stroke-width="2"/>')
    A(f'</g>')

    # ---- infeed hopper -----------------------------------------------------
    if feed_open:
        A(f'<path d="M744 316 L1062 236 L1062 508 L744 480 Z" fill="url(#paint)" stroke="{L["edge"]}" stroke-width="3"/>')
        A(f'<path d="M744 316 L1062 236 L1030 214 L722 292 Z" fill="url(#paintTop)" stroke="{L["edge"]}" stroke-width="3"/>')
        A(f'<path d="M772 332 L1038 264 L1038 302 L772 364 Z" fill="{L["rec2"]}" opacity=".5"/>')
        A(hazard_stripes(1036, 236, 26, 272))
        A(f'<rect x="750" y="358" width="26" height="100" rx="10" fill="#31363d" stroke="#171b21" stroke-width="2"/>')
    # red emergency stop bar across the hopper mouth
    A(f'<rect x="736" y="272" width="330" height="18" rx="9" fill="#dc2626" stroke="#7f1d1d" stroke-width="2" transform="rotate(-13 736 272)"/>')
    # hydraulic hose to feed rollers
    A(hose(742, 470, 660, 512, sag=26, w=6))

    # ---- decals ------------------------------------------------------------
    if brand:
        A(decal(510, 338, BRAND, size=27, col=L["ink"], sub=MODEL, subcol=L["sub"]))
        A(decal(898, 418, "150", size=52, col=L["sub"], weight="800"))
        A(f'<text x="898" y="450" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" '
          f'font-weight="700" font-size="16" letter-spacing="3" fill="{L["ink"]}" opacity=".9">6&#8221; CAPACITY</text>')
    out = "".join(g)
    if scale != 1.0 or dx or dy:
        out = f'<g transform="translate({dx},{dy}) scale({scale})">{out}</g>'
    return out
