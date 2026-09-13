"""HaulCrest Vanguard 850 SL - stand-on compact tracked loader."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import *
import livery

GRAPH = "#2a2f38"
MODEL = "VANGUARD 850 SL"


def loader(brand=True, arm_deg=0):
    L = livery.CUR; BRAND = L["brand"]
    g=[]; A=g.append
    A(f'<g opacity=".5"><rect x="452" y="382" width="330" height="132" rx="12" fill="{L["edge"]}"/>'
      f'<path d="M452 382 L782 382 L752 354 L422 354 Z" fill="{L["edge"]}"/></g>')

    # ---- undercarriage -----------------------------------------------------
    A(track(410, 538, 420, 82))
    A(f'<rect x="424" y="492" width="392" height="50" rx="10" fill="url(#steel)" stroke="#171b21" stroke-width="2"/>')

    # ---- main body ---------------------------------------------------------
    A(f'<rect x="452" y="382" width="330" height="132" rx="12" fill="url(#paint)" stroke="{L["edge"]}" stroke-width="3"/>')
    A(f'<path d="M452 382 L782 382 L752 354 L422 354 Z" fill="url(#paintTop)" stroke="{L["edge"]}" stroke-width="3"/>')
    A(louvres(694, 400, 74, 92, n=6))
    A(bolts([(464,394),(770,394),(464,502),(770,502)]))

    # ---- rear tower / operator station -------------------------------------
    A(f'<rect x="700" y="268" width="104" height="118" rx="12" fill="url(#paint)" stroke="{L["edge"]}" stroke-width="3"/>')
    A(f'<path d="M700 268 L804 268 L780 244 L676 244 Z" fill="url(#paintTop)" stroke="{L["edge"]}" stroke-width="3"/>')
    A(f'<rect x="714" y="282" width="76" height="50" rx="8" fill="#12161b" stroke="#171b21" stroke-width="2"/>')
    A(f'<rect x="724" y="292" width="54" height="8" rx="4" fill="{L["hi"]}"/>')
    A(f'<circle cx="732" cy="316" r="7" fill="#dc2626"/><circle cx="754" cy="316" r="6" fill="#4ade80"/>')
    A(f'<path d="M724 268 L712 230 M782 268 L794 230" stroke="#4b5563" stroke-width="11" stroke-linecap="round"/>')
    A(f'<circle cx="710" cy="224" r="12" fill="{GRAPH}"/><circle cx="796" cy="224" r="12" fill="{GRAPH}"/>')

    # ---- stand-on platform + backrest --------------------------------------
    A(f'<path d="M770 448 L830 448 L830 500 L770 512 Z" fill="url(#paint)" stroke="{L["edge"]}" stroke-width="3"/>')
    A(f'<rect x="804" y="484" width="122" height="22" rx="7" fill="{GRAPH}" stroke="#171b21" stroke-width="2"/>')
    A(hazard_stripes(808, 488, 114, 13))
    A(f'<path d="M916 484 L916 392 M846 484 L846 392" stroke="#4b5563" stroke-width="11" stroke-linecap="round"/>')
    A(f'<path d="M840 396 L922 396" stroke="#4b5563" stroke-width="13" stroke-linecap="round"/>')

    # ---- loader arm (arcs over the body) -----------------------------------
    A(f'<g transform="rotate({arm_deg} 736 420)">')
    A(f'<path d="M736 420 Q566 300 316 400" fill="none" stroke="{L["edge"]}" stroke-width="42" stroke-linecap="round"/>')
    A(f'<path d="M736 420 Q566 300 316 400" fill="none" stroke="url(#paint)" stroke-width="34" stroke-linecap="round"/>')
    A(f'<path d="M736 420 Q566 300 316 400" fill="none" stroke="{L["hi"]}" stroke-width="8" stroke-linecap="round" opacity=".35"/>')
    A(f'<circle cx="736" cy="420" r="18" fill="{GRAPH}" stroke="#8c939d" stroke-width="3"/>')
    A(f'<circle cx="736" cy="420" r="6" fill="#9aa2ad"/>')
    # lift ram, body front -> arm underside
    A(f'<path d="M466 510 L432 452" stroke="#4b5563" stroke-width="19" stroke-linecap="round"/>')
    A(f'<path d="M434 456 L398 402" stroke="#c9ced6" stroke-width="11" stroke-linecap="round"/>')
    A(f'<circle cx="466" cy="510" r="9" fill="#31363d" stroke="#8c939d" stroke-width="2"/>')

    # ---- bucket ------------------------------------------------------------
    A(f'<circle cx="316" cy="400" r="14" fill="{GRAPH}" stroke="#8c939d" stroke-width="3"/>')
    A(f'<rect x="304" y="372" width="20" height="118" rx="6" fill="{GRAPH}" stroke="#171b21" stroke-width="2"/>')
    A(f'<path d="M314 366 L206 374 L172 480 Q244 506 316 480 Z" fill="url(#paint)" stroke="{L["edge"]}" stroke-width="3"/>')
    A(f'<path d="M232 388 L300 384 L300 406 L224 412 Z" fill="{L["g3"]}" opacity=".32"/>')
    # leading cutting edge + teeth
    A(f'<path d="M206 374 L172 480" stroke="#c9ced6" stroke-width="10" stroke-linecap="round"/>')
    for i in range(5):
        t = i / 4.0
        tx = 206 - 34 * t; ty = 380 + 96 * t
        A(f'<path d="M{tx:.0f} {ty:.0f} l-22 4 l6 15 z" fill="#9aa2ad" stroke="#5c636d" stroke-width="1.5"/>')
    A(f'</g>')

    # ---- decals ------------------------------------------------------------
    if brand:
        A(decal(578, 446, BRAND, size=25, col=L["ink"], sub=MODEL, subcol=L["sub"]))
        A(decal(752, 370, "850", size=24, col=L["sub"]))
    return "".join(g)
