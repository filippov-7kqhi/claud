# -*- coding: utf-8 -*-
"""1 tonne rubber-tracked mini excavator, side view facing left.

Drawn from scratch like every other machine here, so the only brand that
appears on it is the store livery passed in through livery.CUR.
"""
import sys
sys.path.insert(0, '/home/user/claud/tools')
from svgkit import *
import livery

MODEL = "EX10 MINI EXCAVATOR"
GRAPH = "#2a2f38"


def excavator(brand=True, boom=0, curl=0, blade=0):
    """boom: degrees the arm is raised. curl: degrees the bucket is curled in.
       blade: pixels the dozer blade is lifted off the ground."""
    L = livery.CUR
    g = []; A = g.append

    # ---- undercarriage ------------------------------------------------------
    A(track(322, 540, 486, 82))
    A(f'<rect x="352" y="492" width="430" height="50" rx="10" fill="url(#steel)" stroke="#171b21" stroke-width="2"/>')
    A(f'<rect x="392" y="470" width="350" height="26" rx="7" fill="{GRAPH}" stroke="#171b21" stroke-width="2"/>')

    # ---- dozer blade on the front -------------------------------------------
    A(f'<g transform="translate(0,{-blade})">')
    A(f'<path d="M300 556 L392 534" stroke="#4b5563" stroke-width="18" stroke-linecap="round"/>')
    A(f'<path d="M300 596 L386 568" stroke="#4b5563" stroke-width="12" stroke-linecap="round"/>')
    A(f'<path d="M226 534 L302 534 L302 610 L216 610 Z" fill="url(#paint)" stroke="{L["edge"]}" stroke-width="3"/>')
    A(f'<rect x="212" y="602" width="94" height="14" rx="5" fill="url(#steelLite)" stroke="#5c636d" stroke-width="2"/>')
    A(f'<path d="M232 546 L296 546" stroke="{L["g3"]}" stroke-width="6" opacity=".5"/>')
    A(f'</g>')

    # ---- slew ring and upper structure --------------------------------------
    A(f'<rect x="404" y="452" width="424" height="24" rx="8" fill="#3d434b" stroke="#171b21" stroke-width="2"/>')
    A(f'<path d="M416 452 L840 452 L860 366 L840 340 L470 340 Z" fill="url(#paint)" '
      f'stroke="{L["edge"]}" stroke-width="3"/>')
    A(f'<path d="M470 340 L840 340 L818 318 L494 318 Z" fill="url(#paintTop)" stroke="{L["edge"]}" stroke-width="3"/>')
    # counterweight, rear
    A(f'<path d="M796 452 L862 452 Q882 452 882 424 L882 356 Q882 336 858 336 L804 336 Z" '
      f'fill="{GRAPH}" stroke="#171b21" stroke-width="2.5"/>')
    A(bolts([(820, 360), (858, 360), (820, 428), (858, 428)]))
    # engine bay louvres and service door
    A(louvres(724, 356, 62, 86, n=6))
    A(f'<rect x="642" y="358" width="70" height="84" rx="8" fill="{L["g3"]}" opacity=".35" '
      f'stroke="{L["edge"]}" stroke-width="2"/>')
    A(f'<circle cx="700" cy="400" r="6" fill="#c9ced6"/>')

    # ---- canopy / operator station ------------------------------------------
    A(f'<rect x="470" y="212" width="248" height="22" rx="8" fill="url(#paintTop)" '
      f'stroke="{L["edge"]}" stroke-width="3"/>')
    A(f'<rect x="482" y="228" width="15" height="118" rx="6" fill="{GRAPH}"/>')
    A(f'<rect x="694" y="228" width="15" height="118" rx="6" fill="{GRAPH}"/>')
    A(f'<path d="M500 336 L690 336 L690 246 L500 246 Z" fill="url(#glassG)" opacity=".45"/>')
    # seat, levers and floor plate
    A(f'<path d="M556 336 L616 336 L616 286 L640 286 L640 270 L600 270 L600 300 L556 300 Z" fill="#23272d"/>')
    A(f'<rect x="546" y="330" width="86" height="12" rx="5" fill="#31363d"/>')
    A(f'<path d="M540 330 L528 288" stroke="#4b5563" stroke-width="8" stroke-linecap="round"/>')
    A(f'<path d="M648 330 L660 288" stroke="#4b5563" stroke-width="8" stroke-linecap="round"/>')
    A(f'<circle cx="527" cy="284" r="8" fill="#dc2626"/><circle cx="661" cy="284" r="8" fill="{L["hi"]}"/>')
    A(f'<rect x="486" y="288" width="34" height="52" rx="6" fill="#12161b"/>')
    A(f'<rect x="492" y="296" width="22" height="6" rx="3" fill="{L["hi"]}"/>')

    # ---- boom, dipper and bucket --------------------------------------------
    A(f'<g transform="rotate({-boom} 452 428)">')
    #   boom: a curved box section running up and forward
    A(f'<path d="M436 448 L470 408 L392 300 L338 246 L308 268 L360 336 Z" fill="url(#paint)" '
      f'stroke="{L["edge"]}" stroke-width="3"/>')
    A(f'<path d="M436 448 L470 408 L392 300 L360 336 Z" fill="{L["g3"]}" opacity=".3"/>')
    A(f'<circle cx="452" cy="428" r="14" fill="#31363d" stroke="#8c939d" stroke-width="3"/>')
    #   boom ram
    A(f'<path d="M498 452 L452 386" stroke="#4b5563" stroke-width="20" stroke-linecap="round"/>')
    A(f'<path d="M456 392 L410 328" stroke="#c9ced6" stroke-width="12" stroke-linecap="round"/>')
    #   dipper arm
    A(f'<g transform="rotate(14 324 258)">')
    A(f'<path d="M336 240 L306 264 L246 396 L280 414 Z" fill="url(#paint)" stroke="{L["edge"]}" stroke-width="3"/>')
    A(f'<circle cx="324" cy="258" r="12" fill="#31363d" stroke="#8c939d" stroke-width="3"/>')
    A(hose(348, 262, 300, 372, sag=26))
    #   dipper ram
    A(f'<path d="M368 288 L330 322" stroke="#4b5563" stroke-width="16" stroke-linecap="round"/>')
    A(f'<path d="M334 318 L298 350" stroke="#c9ced6" stroke-width="10" stroke-linecap="round"/>')
    #   bucket
    A(f'<g transform="rotate({curl} 264 404)">')
    A(f'<path d="M236 380 L296 402 L288 460 Q252 484 214 462 L206 404 Z" fill="url(#paint)" '
      f'stroke="{L["edge"]}" stroke-width="3"/>')
    A(f'<path d="M214 462 Q252 484 288 460" fill="none" stroke="#c9ced6" stroke-width="6"/>')
    A("".join(f'<path d="M{212+i*20} {470+i*2} l6 20 l10 -4 l-6 -20 z" fill="#c9ced6" '
              f'stroke="#5c636d" stroke-width="1.5"/>' for i in range(4)))
    A(f'<circle cx="264" cy="404" r="10" fill="#31363d" stroke="#8c939d" stroke-width="2.5"/>')
    A(f'</g>')
    A(f'<path d="M310 356 L282 386" stroke="#4b5563" stroke-width="13" stroke-linecap="round"/>')
    A(f'<path d="M286 382 L262 404" stroke="#c9ced6" stroke-width="8" stroke-linecap="round"/>')
    A(f'</g></g>')

    # ---- decals -------------------------------------------------------------
    if brand:
        A(decal(600, 400, L["brand"], size=30, col=L["ink"], sub=MODEL, subcol=L["sub"]))
    return "".join(g)
