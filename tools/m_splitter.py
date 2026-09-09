# -*- coding: utf-8 -*-
"""22 tonne petrol log splitter, horizontal beam on a towable road chassis.
   Side view, wedge to the left, engine and pump over the axle to the right."""
import sys
sys.path.insert(0, '/home/user/claud/tools')
from svgkit import *
import livery

MODEL = "LS22 LOG SPLITTER"
GRAPH = "#2a2f38"


def splitter(brand=True, stroke=0, log=False):
    """stroke: pixels the push plate has travelled toward the wedge."""
    L = livery.CUR
    g = []; A = g.append

    # ---- tow bar and hitch --------------------------------------------------
    A(f'<path d="M232 462 L118 486" stroke="url(#steel)" stroke-width="26" stroke-linecap="round"/>')
    A(f'<path d="M132 484 L96 492" stroke="#4b5563" stroke-width="18" stroke-linecap="round"/>')
    A(f'<circle cx="92" cy="493" r="19" fill="none" stroke="#c9ced6" stroke-width="9"/>')
    A(f'<rect x="176" y="474" width="16" height="72" rx="6" fill="{GRAPH}"/>')      # jockey leg
    A(f'<rect x="162" y="540" width="44" height="13" rx="6" fill="url(#steelLite)" stroke="#5c636d" stroke-width="2"/>')

    # ---- main beam ----------------------------------------------------------
    A(f'<rect x="212" y="428" width="768" height="46" rx="7" fill="url(#steel)" stroke="#171b21" stroke-width="2.5"/>')
    A(f'<rect x="222" y="434" width="748" height="10" rx="5" fill="#6e767f" opacity=".4"/>')
    A(f'<rect x="212" y="474" width="768" height="16" rx="6" fill="{GRAPH}"/>')

    # ---- splitting wedge and log cradle -------------------------------------
    A(f'<path d="M300 300 L336 300 L336 424 L318 396 L300 424 Z" fill="url(#steelLite)" '
      f'stroke="#5c636d" stroke-width="2.5"/>')
    A(f'<rect x="292" y="288" width="52" height="20" rx="6" fill="{GRAPH}"/>')
    A(f'<path d="M264 428 L264 372 M372 428 L372 372" stroke="{L["g2"]}" stroke-width="12" stroke-linecap="round"/>')
    A(f'<path d="M258 372 L280 356 M366 372 L388 356" stroke="{L["g2"]}" stroke-width="10" stroke-linecap="round"/>')
    # ---- push plate and cylinder -------------------------------------------
    px = 636 - stroke
    if log:
        # the round stays against the wedge; the plate closes the gap onto it
        A(f'<rect x="386" y="352" width="{max(40, px - 390)}" height="74" rx="12" fill="#a8895f" '
          f'stroke="#7c6242" stroke-width="3"/>')
        A(f'<ellipse cx="390" cy="389" rx="13" ry="37" fill="#c9a978" stroke="#7c6242" stroke-width="3"/>')
        A(f'<ellipse cx="390" cy="389" rx="7" ry="20" fill="none" stroke="#a8895f" stroke-width="2"/>')
    A(f'<rect x="{px}" y="336" width="30" height="94" rx="6" fill="url(#paint)" stroke="{L["edge"]}" stroke-width="3"/>')
    A(f'<rect x="{px+30}" y="366" width="{max(6, 118 + stroke)}" height="26" rx="13" fill="#c9ced6" '
      f'stroke="#8c939d" stroke-width="2"/>')
    A(f'<rect x="754" y="344" width="150" height="70" rx="16" fill="url(#steel)" stroke="#171b21" stroke-width="2.5"/>')
    A(f'<rect x="742" y="352" width="20" height="54" rx="7" fill="{GRAPH}"/>')
    A(hose(770, 414, 856, 452, sag=30))
    A(hose(806, 414, 880, 452, sag=26))

    # ---- valve lever --------------------------------------------------------
    A(f'<path d="M712 428 L700 340" stroke="#4b5563" stroke-width="11" stroke-linecap="round"/>')
    A(f'<circle cx="699" cy="332" r="12" fill="{L["acc"]}"/>')

    # ---- engine and hydraulic pack over the axle ----------------------------
    A(f'<rect x="828" y="486" width="150" height="72" rx="10" fill="{GRAPH}" stroke="#171b21" stroke-width="2"/>')
    A(f'<rect x="838" y="498" width="60" height="12" rx="6" fill="#4b5563"/>')      # reservoir
    A(f'<rect x="826" y="286" width="176" height="146" rx="14" fill="url(#paint)" stroke="{L["edge"]}" stroke-width="3"/>')
    A(f'<path d="M826 286 L1002 286 L978 262 L802 262 Z" fill="url(#paintTop)" stroke="{L["edge"]}" stroke-width="3"/>')
    A(louvres(942, 352, 58, 70, n=5))
    A(f'<rect x="838" y="352" width="54" height="40" rx="7" fill="#12161b"/>')
    A(f'<circle cx="852" cy="372" r="7" fill="#dc2626"/><circle cx="872" cy="372" r="6" fill="#4ade80"/>')
    A(f'<rect x="932" y="236" width="18" height="28" rx="6" fill="#31363d"/>')      # exhaust
    A(f'<rect x="924" y="224" width="34" height="15" rx="7" fill="#1b1f25"/>')
    A(f'<circle cx="908" cy="404" r="22" fill="#2a2f38" stroke="#6b7280" stroke-width="4"/>')  # recoil start
    A(f'<circle cx="908" cy="404" r="9" fill="#9aa2ad"/>')

    # ---- road wheels --------------------------------------------------------
    A(f'<path d="M886 486 L902 552 M940 486 L916 552" stroke="{GRAPH}" stroke-width="16" stroke-linecap="round"/>')
    A(wheel(902, 564, 58))
    A(f'<rect x="862" y="544" width="84" height="14" rx="6" fill="{GRAPH}"/>')

    # ---- decals -------------------------------------------------------------
    if brand:
        A(decal(914, 318, L["brand"], size=21, col=L["ink"], sub=MODEL, subcol=L["sub"]))
        A(f'<text x="470" y="461" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" '
          f'font-weight="800" font-size="19" letter-spacing="2.4" fill="{L["hi"]}">22 TONNE SPLITTING FORCE</text>')
    return "".join(g)
