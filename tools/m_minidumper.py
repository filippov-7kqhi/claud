# -*- coding: utf-8 -*-
"""500 kg rubber-tracked hydraulic mini dumper, side view facing left.

A walk-behind machine: hydraulic tipping skip over the tracks, petrol power
pack at the rear, handlebars behind that.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import *
import livery

MODEL = "TD500 MINI DUMPER"
GRAPH = "#2a2f38"


def minidumper(brand=True, tip_deg=0, load=False):
    L = livery.CUR
    g = []; A = g.append

    # ---- undercarriage ------------------------------------------------------
    A(track(268, 552, 452, 70))
    A(f'<rect x="292" y="512" width="404" height="44" rx="9" fill="url(#steel)" stroke="#171b21" stroke-width="2"/>')
    A(f'<rect x="322" y="494" width="344" height="22" rx="7" fill="{GRAPH}" stroke="#171b21" stroke-width="2"/>')

    # ---- skip subframe, so the tub sits on the chassis rather than above it --
    A(f'<rect x="304" y="466" width="352" height="32" rx="8" fill="{GRAPH}" stroke="#171b21" stroke-width="2"/>')
    # the skip pivots at the front, so tipping lifts the rear and the load runs out
    A(f'<rect x="288" y="452" width="48" height="46" rx="8" fill="url(#steel)" stroke="#171b21" stroke-width="2"/>')
    A(f'<circle cx="312" cy="472" r="9" fill="#31363d" stroke="#8c939d" stroke-width="2.5"/>')

    # ---- tipping skip -------------------------------------------------------
    A(f'<g transform="rotate({-tip_deg} 312 472)">')
    A(f'<path d="M262 330 L636 330 L606 474 L302 474 Z" fill="url(#paint)" stroke="{L["edge"]}" stroke-width="3"/>')
    A(f'<path d="M262 330 L636 330 L612 306 L238 306 Z" fill="url(#paintTop)" stroke="{L["edge"]}" stroke-width="3"/>')
    A(f'<path d="M292 352 L608 352 L584 420 L316 420 Z" fill="{L["g3"]}" opacity=".26"/>')
    A(f'<rect x="254" y="322" width="388" height="13" rx="6" fill="{GRAPH}"/>')
    A(bolts([(284, 346), (618, 346), (316, 462), (590, 462)]))
    if load:
        A(f'<path d="M276 322 q80 -44 176 -24 q96 20 176 24 z" fill="#8a6b45"/>')
        A(f'<path d="M304 314 q66 -30 138 -16" fill="none" stroke="#a8895f" stroke-width="8" stroke-linecap="round"/>')
    if brand:
        A(decal(444, 392, L["brand"], size=30, col=L["ink"], sub=MODEL, subcol=L["sub"]))
        A(f'<text x="444" y="446" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" '
          f'font-weight="800" font-size="18" letter-spacing="2.2" fill="{L["sub"]}">500 kg PAYLOAD</text>')
    A(f'</g>')

    # ---- tipping ram --------------------------------------------------------
    ram = tip_deg * 3.1
    A(f'<path d="M600 498 L578 {446-ram*0.28:.0f}" stroke="#4b5563" stroke-width="19" stroke-linecap="round"/>')
    A(f'<path d="M580 {452-ram*0.28:.0f} L556 {410-ram:.0f}" stroke="#c9ced6" stroke-width="11" stroke-linecap="round"/>')
    A(f'<circle cx="600" cy="498" r="9" fill="#31363d" stroke="#8c939d" stroke-width="2"/>')
    A(hose(612, 500, 700, 470, sag=32))

    # ---- power pack ---------------------------------------------------------
    A(f'<rect x="642" y="392" width="158" height="116" rx="12" fill="url(#paint)" stroke="{L["edge"]}" stroke-width="3"/>')
    A(f'<path d="M642 392 L800 392 L776 368 L618 368 Z" fill="url(#paintTop)" stroke="{L["edge"]}" stroke-width="3"/>')
    A(louvres(714, 412, 74, 78, n=6))
    A(f'<rect x="656" y="410" width="44" height="34" rx="6" fill="#12161b"/>')
    A(f'<circle cx="670" cy="427" r="7" fill="#dc2626"/><circle cx="689" cy="427" r="6" fill="#4ade80"/>')
    A(f'<rect x="732" y="342" width="17" height="30" rx="6" fill="#31363d"/>')
    A(f'<rect x="724" y="330" width="33" height="15" rx="7" fill="#1b1f25"/>')
    A(f'<rect x="656" y="456" width="60" height="14" rx="6" fill="{L["g3"]}" opacity=".5"/>')

    # ---- handlebars ---------------------------------------------------------
    A(f'<path d="M792 404 L880 330" stroke="#4b5563" stroke-width="15" stroke-linecap="round"/>')
    A(f'<path d="M880 330 L950 312 M880 330 L940 356" stroke="#4b5563" stroke-width="13" stroke-linecap="round"/>')
    A(f'<circle cx="956" cy="310" r="14" fill="{GRAPH}"/><circle cx="946" cy="358" r="14" fill="{GRAPH}"/>')
    A(f'<rect x="856" y="282" width="86" height="46" rx="9" fill="#12161b" stroke="#171b21" stroke-width="2" '
      f'transform="rotate(-14 856 282)"/>')
    A(f'<g transform="rotate(-14 856 282)"><rect x="870" y="296" width="58" height="8" rx="4" fill="{L["hi"]}"/>'
      f'<circle cx="878" cy="314" r="6" fill="#dc2626"/></g>')
    A(f'<path d="M862 344 L906 336" stroke="{L["acc"]}" stroke-width="9" stroke-linecap="round"/>')
    return "".join(g)
