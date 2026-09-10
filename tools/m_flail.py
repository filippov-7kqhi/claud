# -*- coding: utf-8 -*-
"""15 hp ATV-towed flail mower, side view. Drawbar to the left, engine on the
   deck, flail rotor under it, height-setting roller at the back."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import *
import livery

MODEL = "FM150 ATV FLAIL MOWER"
GRAPH = "#2a2f38"


def _rotor(cy):
    """The flail rotor: a drum with swinging hammers, drawn at the given height."""
    return (f'<circle cx="540" cy="{cy}" r="44" fill="#20242a" stroke="#585f69" stroke-width="3"/>'
            + "".join(f'<rect x="580" y="{cy-4}" width="26" height="9" rx="4" fill="#c9ced6" '
                      f'stroke="#5c636d" stroke-width="1.5" transform="rotate({a} 540 {cy})"/>'
                      for a in range(0, 360, 45))
            + f'<circle cx="540" cy="{cy}" r="12" fill="#6f7883"/>')


def flail(brand=True, cut=False, deck=0, cutaway=False):
    """deck: pixels the cutting deck is raised on its roller adjustment."""
    L = livery.CUR
    g = []; A = g.append
    d = -deck

    # ---- drawbar and hitch --------------------------------------------------
    A(f'<path d="M312 {486+d} L146 {452+d}" stroke="url(#steel)" stroke-width="24" stroke-linecap="round"/>')
    A(f'<path d="M300 {524+d} L206 {462+d}" stroke="#4b5563" stroke-width="14" stroke-linecap="round"/>')
    A(f'<rect x="106" y="{436+d}" width="46" height="30" rx="9" fill="{GRAPH}" stroke="#171b21" stroke-width="2"/>')
    A(f'<circle cx="122" cy="{451+d}" r="9" fill="#12161b" stroke="#8c939d" stroke-width="3"/>')

    # ---- cutting deck -------------------------------------------------------
    A(_rotor(524 + d))                     # inside the housing, hidden unless cut away
    A(f'<path d="M300 {432+d} L822 {432+d} L822 {556+d} L300 {556+d} Z" fill="url(#paint)" '
      f'stroke="{L["edge"]}" stroke-width="3"/>')
    A(f'<path d="M300 {432+d} L822 {432+d} L796 {406+d} L274 {406+d} Z" fill="url(#paintTop)" '
      f'stroke="{L["edge"]}" stroke-width="3"/>')
    A(f'<rect x="300" y="{540+d}" width="522" height="18" rx="6" fill="{GRAPH}"/>')
    A(bolts([(322, 452 + d), (800, 452 + d), (322, 530 + d), (800, 530 + d)]))
    A(hazard_stripes(306, 512 + d, 120, 22))

    if cutaway:
        A(f'<rect x="452" y="{444+d}" width="180" height="{112}" fill="url(#paint)" opacity=".18"/>')
        A(_rotor(524 + d))
        A(f'<rect x="452" y="{444+d}" width="180" height="112" fill="none" stroke="{L["acc"]}" '
          f'stroke-width="2.5" stroke-dasharray="9 7"/>')

    # rear deflector flap
    A(f'<path d="M822 {450+d} L862 {446+d} L868 {556+d} L822 {556+d} Z" fill="{GRAPH}" '
      f'stroke="#171b21" stroke-width="2"/>')

    # ---- height roller and side skid ---------------------------------------
    A(f'<rect x="836" y="{560+d}" width="26" height="{max(6, 30+deck)}" rx="8" fill="url(#steel)"/>')
    A(f'<circle cx="848" cy="596" r="30" fill="url(#rubber)" stroke="#5c636d" stroke-width="3"/>')
    A(f'<circle cx="848" cy="596" r="11" fill="#6f7883"/>')
    A(f'<rect x="292" y="{560+d}" width="22" height="{max(6, 26+deck)}" rx="7" fill="url(#steel)"/>')
    A(f'<circle cx="303" cy="596" r="26" fill="url(#rubber)" stroke="#5c636d" stroke-width="3"/>')
    A(f'<circle cx="303" cy="596" r="9" fill="#6f7883"/>')

    # ---- engine on the deck -------------------------------------------------
    A(f'<rect x="470" y="{258+d}" width="228" height="152" rx="14" fill="url(#paint)" '
      f'stroke="{L["edge"]}" stroke-width="3"/>')
    A(f'<path d="M470 {258+d} L698 {258+d} L672 {232+d} L444 {232+d} Z" fill="url(#paintTop)" '
      f'stroke="{L["edge"]}" stroke-width="3"/>')
    A(louvres(626, 322 + d, 62, 74, n=5))
    A(f'<rect x="486" y="{322+d}" width="56" height="42" rx="7" fill="#12161b"/>')
    A(f'<circle cx="500" cy="{343+d}" r="7" fill="#dc2626"/><circle cx="521" cy="{343+d}" r="6" fill="#4ade80"/>')
    A(f'<circle cx="584" cy="{372+d}" r="23" fill="#2a2f38" stroke="#6b7280" stroke-width="4"/>')
    A(f'<circle cx="584" cy="{372+d}" r="9" fill="#9aa2ad"/>')
    A(f'<rect x="612" y="{204+d}" width="18" height="30" rx="6" fill="#31363d"/>')
    A(f'<rect x="604" y="{192+d}" width="34" height="15" rx="7" fill="#1b1f25"/>')
    A(f'<rect x="474" y="{212+d}" width="52" height="24" rx="9" fill="{GRAPH}"/>')      # air cleaner
    # belt cover down to the rotor
    A(f'<path d="M700 {300+d} L748 {300+d} L764 {440+d} L716 {440+d} Z" fill="{L["g3"]}" '
      f'stroke="{L["edge"]}" stroke-width="2.5"/>')

    if cut:
        A("".join(f'<path d="M{318+i*34} {602} q6 -26 14 -38" fill="none" stroke="#4b7a37" '
                  f'stroke-width="5" stroke-linecap="round"/>' for i in range(15)))

    # ---- decals -------------------------------------------------------------
    if brand:
        A(decal(560, 492 + d, L["brand"], size=30, col=L["ink"], sub=MODEL, subcol=L["sub"]))
        A(f'<text x="584" y="{292+d}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" '
          f'font-weight="800" font-size="17" letter-spacing="2" fill="{L["sub"]}">15 HP</text>')
    return "".join(g)
