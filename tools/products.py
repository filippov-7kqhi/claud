# -*- coding: utf-8 -*-
"""The four machines, brand-neutral. Each store sells all four under its own brand."""
import copy
from cfg_branchforge import CYCLONE, GRIND
from cfg_haulcrest import TITAN, VANGUARD

BASE = [CYCLONE, GRIND, TITAN, VANGUARD]

# Store-neutral extras needed for a Google Merchant Center feed.
EXTRA = {
    "BF-CY150": dict(condition="new", category="Business & Industrial > Heavy Machinery",
                     gpc="5605", weight_kg=748, box="240 x 130 x 155 cm"),
    "BF-GM380": dict(condition="new", category="Business & Industrial > Heavy Machinery",
                     gpc="5605", weight_kg=412, box="205 x 90 x 130 cm"),
    "HC-TT1000": dict(condition="new", category="Business & Industrial > Heavy Machinery",
                      gpc="5605", weight_kg=385, box="240 x 80 x 135 cm"),
    "HC-VG850": dict(condition="new", category="Business & Industrial > Heavy Machinery",
                     gpc="5605", weight_kg=738, box="255 x 100 x 140 cm"),
}

_BRANDS = ("BranchForge", "HaulCrest")


def _rebrand(value, brand):
    if isinstance(value, str):
        for b in _BRANDS:
            value = value.replace(b, brand)
        return value
    if isinstance(value, list):
        return [_rebrand(v, brand) for v in value]
    if isinstance(value, tuple):
        return tuple(_rebrand(v, brand) for v in value)
    if isinstance(value, dict):
        return {k: _rebrand(v, brand) for k, v in value.items()}
    return value


def for_store(brand, prefix):
    """All four products, rebranded for one store, with feed fields filled in."""
    out = []
    for i, base in enumerate(BASE):
        p = _rebrand(copy.deepcopy(base), brand)
        p["order"] = i
        p["brand"] = brand
        p["name_full"] = f"{brand} {p['name']}"
        p["mpn"] = p["sku"].replace("BF-", prefix + "-").replace("HC-", prefix + "-")
        p.update(EXTRA[base["sku"]])
        p["sku"] = p["mpn"]
        out.append(p)
    return out
