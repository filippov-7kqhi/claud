"""HaulCrest Titan 1000 HT - 1 tonne tracked hydraulic high-tip dumper."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import *
import livery


MODEL = "TITAN 1000 HT"
GRAPH = "#2a2f38"


def dumper(brand=True, tip_deg=0, load=False, lift=0):
    L = livery.CUR; BRAND = L["brand"]
    g=[]; A=g.append
    # ---- undercarriage -----------------------------------------------------
    A(track(300, 540, 570, 80))
    A(f'<rect x="312" y="492" width="556" height="52" rx="10" fill="url(#steel)" stroke="#171b21" stroke-width="2"/>')
    A(f'<rect x="330" y="470" width="520" height="26" rx="7" fill="{GRAPH}" stroke="#171b21" stroke-width="2"/>')

    # ---- lift frame (scissor post) ----------------------------------------
    A(f'<path d="M600 484 L640 484 L628 {372-lift*0.62:.0f} L590 {372-lift*0.62:.0f} Z" fill="url(#steel)" '
      f'stroke="#171b21" stroke-width="2"/>')
    A(f'<path d="M470 480 L560 400" stroke="#4b5563" stroke-width="22" stroke-linecap="round"/>')
    A(f'<path d="M556 404 L{612+lift*0.10:.0f} {366-lift*0.58:.0f}" stroke="#c9ced6" stroke-width="12" stroke-linecap="round"/>')

    # ---- skip / tub --------------------------------------------------------
    A(f'<g transform="translate({lift*0.16:.0f},{-lift}) rotate({-tip_deg} 700 300)">')
    A(f'<path d="M300 252 L706 252 L672 396 L340 396 Z" fill="url(#paint)" stroke="{L["edge"]}" stroke-width="3"/>')
    A(f'<path d="M300 252 L706 252 L678 228 L272 228 Z" fill="url(#paintTop)" stroke="{L["edge"]}" stroke-width="3"/>')
    A(f'<path d="M330 274 L676 274 L652 344 L354 344 Z" fill="{L["g3"]}" opacity=".28"/>')
    A(f'<rect x="292" y="244" width="420" height="14" rx="7" fill="{GRAPH}"/>')
    A(bolts([(320,268),(690,268),(352,384),(660,384)]))
    if load:
        A(f'<path d="M312 244 q86 -46 190 -26 q104 20 190 26 z" fill="#8a6b45"/>')
        A(f'<path d="M340 236 q70 -32 148 -18" fill="none" stroke="#a8895f" stroke-width="8" stroke-linecap="round"/>')
    if brand:
        A(decal(500, 314, BRAND, size=32, col=L["ink"], sub=MODEL, subcol=L["sub"]))
        A(f'<text x="500" y="374" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" '
          f'font-weight="800" font-size="19" letter-spacing="2.4" fill="{L["sub"]}">1000 kg PAYLOAD</text>')
    A(f'</g>')

    # ---- tipping ram -------------------------------------------------------
    A(f'<path d="M420 470 L508 418" stroke="#4b5563" stroke-width="20" stroke-linecap="round"/>')
    A(f'<path d="M504 420 L{556+lift*0.06:.0f} {392-lift*0.50:.0f}" stroke="#c9ced6" stroke-width="11" stroke-linecap="round"/>')
    A(f'<circle cx="420" cy="470" r="9" fill="#31363d" stroke="#8c939d" stroke-width="2"/>')

    # ---- power pack at the rear -------------------------------------------
    A(f'<rect x="700" y="372" width="170" height="122" rx="12" fill="url(#paint)" stroke="{L["edge"]}" stroke-width="3"/>')
    A(f'<path d="M700 372 L870 372 L844 346 L674 346 Z" fill="url(#paintTop)" stroke="{L["edge"]}" stroke-width="3"/>')
    A(louvres(776, 394, 82, 84, n=6))
    A(f'<rect x="716" y="392" width="46" height="36" rx="6" fill="#12161b"/>')
    A(f'<circle cx="731" cy="410" r="7" fill="#dc2626"/><circle cx="751" cy="410" r="6" fill="#4ade80"/>')
    A(f'<rect x="798" y="318" width="18" height="34" rx="6" fill="#31363d"/>')
    A(f'<rect x="790" y="306" width="34" height="15" rx="7" fill="#1b1f25"/>')
    

    # ---- operator handlebars ----------------------------------------------
    A(f'<path d="M858 388 L936 306" stroke="#4b5563" stroke-width="15" stroke-linecap="round"/>')
    A(f'<path d="M936 306 L1004 288 M936 306 L994 332" stroke="#4b5563" stroke-width="13" stroke-linecap="round"/>')
    A(f'<circle cx="1010" cy="286" r="14" fill="{GRAPH}"/><circle cx="1000" cy="334" r="14" fill="{GRAPH}"/>')
    A(f'<rect x="912" y="258" width="86" height="46" rx="9" fill="#12161b" stroke="#171b21" stroke-width="2" transform="rotate(-14 912 258)"/>')
    A(f'<g transform="rotate(-14 912 258)"><rect x="926" y="272" width="58" height="8" rx="4" fill="{L["hi"]}"/>'
      f'<circle cx="934" cy="290" r="6" fill="#dc2626"/></g>')

    # ---- decals ------------------------------------------------------------
    _ = brand
    return "".join(g)
