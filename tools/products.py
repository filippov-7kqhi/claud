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


def _images_on_disk(root, slug):
    """Read the gallery straight off disk so adding a photo needs no code change."""
    import os, json
    d = os.path.join(root, "assets", "img", slug)
    if not os.path.isdir(d):
        return []
    alts = {}
    alt_file = os.path.join(d, "alt.json")
    if os.path.exists(alt_file):
        alts = json.load(open(alt_file))
    names = os.listdir(d)
    svgs = {f[:-4] for f in names if f.lower().endswith(".svg")}
    # a .jpg that only exists as the raster twin of a .svg is for the feed, not the gallery
    files = sorted(f for f in names
                   if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
                   and os.path.splitext(f)[0] not in svgs)
    return [(f, alts.get(f, "")) for f in files]


def for_store(brand, prefix, store_key=None, root=None):
    """All four products, rebranded for one store, with feed fields filled in.
       Where the store has real photography of a real machine, that machine
       replaces the catalogue entry."""
    out = []
    overrides = OVERRIDES.get(store_key or "", {})
    for i, base in enumerate(BASE):
        if base["slug"] in overrides:
            real = copy.deepcopy(overrides[base["slug"]])
            real["order"] = i
            real["brand"] = brand
            real["name_full"] = f"{brand} {real['name']}"
            real["mpn"] = real["sku"]
            real.update({k: v for k, v in EXTRA[base["sku"]].items() if k in ("condition", "category", "gpc")})
            real.setdefault("weight_kg", "")
            real.setdefault("box", "")
            if root:
                real["images"] = _images_on_disk(root, real["dir"].split("/")[-1])
            out.append(real)
            continue
        p = _rebrand(copy.deepcopy(base), brand)
        p["order"] = i
        p["brand"] = brand
        p["name_full"] = f"{brand} {p['name']}"
        p["mpn"] = p["sku"].replace("BF-", prefix + "-").replace("HC-", prefix + "-")
        p.update(EXTRA[base["sku"]])
        p["sku"] = p["mpn"]
        out.append(p)
    return out


# ---------------------------------------------------------------------------
# Real machines. Where a store has genuine photography, the product on that
# store is the machine in the photographs -- model name, engine and capability
# taken from what is visible on it, not from the generic catalogue above.
# Figures that could not be read off the photographs are simply absent rather
# than guessed; ask the supplier and add them.
# ---------------------------------------------------------------------------

HC15H = dict(
    slug="hc15h-wood-chipper", url="hc15h-wood-chipper.html", dir="assets/img/hc15h",
    sku="BF-HC15H", name="HC15H Towable Wood Chipper", short="HC15H",
    short_desc="Road-towable 15 hp petrol chipper with hydraulic feed — tows behind a car, "
               "starts on a key.",
    lede="A single-axle towable chipper with a 15 hp petrol engine, electric key start and a "
         "hydraulic feed you control from the hopper. Built to be pulled to the job behind an "
         "ordinary vehicle and worked all day without a hire booking.",
    tag="Best seller", price=2899, was=3699, finance=68,
    stockline="In stock — ships crated from our UK warehouse",
    meta_desc="BranchForge HC15H towable wood chipper: 15 hp petrol, electric key start, "
              "hydraulic feed, road-towable single axle. Free UK mainland delivery.",
    images=[], bullets=[
        "15 hp petrol engine — no red-diesel paperwork, fills at any forecourt",
        "Electric key start with a recoil back-up when the battery is flat",
        "Hydraulic feed with a lever at the hopper, so you are not forcing timber in",
        "Belt drive to the cutting rotor, serviceable with ordinary spanners",
        "Single-axle road chassis with a ball hitch — tows behind a normal car",
        "Adjustable discharge chute puts the chip where you want it",
        "2-year parts warranty and UK-held spares"],
    spec_hi=[("Engine", "15 hp petrol"), ("Starting", "Electric key + recoil"),
             ("Feed", "Hydraulic, lever control"), ("Chassis", "Single-axle towable")],
    specs=[("Model", "BranchForge HC15H"), ("Engine", "Single-cylinder petrol"),
           ("Rated power", "15 hp"), ("Starting", "Electric key start with recoil back-up"),
           ("Feed system", "Hydraulic, operator lever at the hopper"),
           ("Cutting system", "Rotor with replaceable blades"),
           ("Drive", "Belt from engine to rotor"),
           ("Discharge", "Rotating chute with adjustable deflector"),
           ("Chassis", "Single-axle road chassis with ball hitch and support leg"),
           ("Warranty", "2 years parts, 1 year engine")],
    features_h2="What this chipper actually gives you",
    features=[("15 hp petrol", "Petrol keeps the machine light enough to tow behind a normal car "
               "and simple enough to service yourself. No red-diesel record-keeping, and you refuel "
               "anywhere."),
              ("Electric key start", "Turn a key and it runs. The recoil is there as a back-up for "
               "the morning the battery is flat, not as the normal way in."),
              ("Hydraulic feed", "A lever at the hopper drives the timber through, so you are "
               "guiding branches rather than shoving them. Safer, and far less tiring across a day."),
              ("Belt drive", "Engine to rotor through a belt — a wearing part you can inspect, "
               "tension and replace on site with ordinary tools."),
              ("Towable on a ball hitch", "Single axle and a standard coupling. It goes to the job "
               "behind the vehicle you already own."),
              ("Adjustable chute", "Rotate the chute and set the deflector to drop chip into a "
               "truck, a barrow or a pile without moving the machine.")],
    faq=[("What size timber will it take?",
          "<p>We are confirming the exact rated capacity with the manufacturer and will publish it "
          "here rather than estimate it. If you need the figure before you order, email us and we "
          "will confirm it in writing the same working day.</p>"),
         ("Can I tow it behind a car?",
          "<p>It is built on a single-axle road chassis with a standard ball hitch. Check your "
          "vehicle's towing capacity and nose weight on the V5C and the tow bar plate, and confirm "
          "the machine's gross weight with us before you set off.</p>"),
         ("Petrol or diesel?",
          "<p>Petrol. At this size petrol gives the best power-to-weight ratio, keeps the towed "
          "weight down and avoids red-diesel record-keeping for commercial use.</p>"),
         ("Do I need training to use it?",
          "<p>There is no legal licence to own or run one. For commercial work HSE expects operators "
          "to be trained and competent — City &amp; Guilds NPTC 0020 is the recognised UK unit. We "
          "supply the manual and PPE; we do not provide certification.</p>"),
         ("What does the warranty cover?",
          "<p>Two years on parts we supply and one year on the engine. Wear items — blades, belts, "
          "filters and the anvil — are excluded, as is damage from feeding stone, wire or metal "
          "into the hopper. Full terms are on our <a href='returns.html#warranty'>warranty page</a>.</p>")],
)

MD500 = dict(
    slug="md-500hpro-mini-dumper", url="md-500hpro-mini-dumper.html", dir="assets/img/md-500hpro",
    sku="BF-MD500", name="MD-500HPRO Tracked Mini Dumper", short="MD-500HPRO",
    short_desc="Tracked petrol mini dumper with a hydraulic tipping skip — and a snow plough "
               "for the winter.",
    lede="A rubber-tracked walk-behind dumper with a hydraulic tipping skip, built to move a "
         "serious load across ground a wheelbarrow cannot cross and through gaps a lorry cannot "
         "reach. The plough blade bolts on for winter work.",
    tag="Most versatile", price=2699, was=3499, finance=63,
    stockline="In stock — ships crated from our UK warehouse",
    meta_desc="BranchForge MD-500HPRO tracked mini dumper: petrol, hydraulic tipping skip, rubber "
              "tracks, optional snow plough. Free UK mainland delivery.",
    images=[], bullets=[
        "Hydraulic tipping skip — raise and empty it from the handlebars",
        "Rubber tracks spread the load, so it crosses wet ground and finished lawns",
        "Petrol engine with hydraulic drive, controlled from a lever by the grips",
        "Walk-behind handlebar controls — no cab to climb into at every gate",
        "Snow plough blade available, so it earns through the winter too",
        "Ground-level engine access for fuel, oil and filters",
        "2-year parts warranty and UK-held spares"],
    spec_hi=[("Skip", "Hydraulic tipping"), ("Drive", "Rubber tracks"),
             ("Engine", "Petrol"), ("Controls", "Walk-behind handlebars")],
    specs=[("Model", "BranchForge MD-500HPRO"), ("Engine", "Single-cylinder petrol, air-cooled"),
           ("Tipping", "Hydraulic ram, forward discharge"),
           ("Undercarriage", "Rubber tracks"),
           ("Controls", "Walk-behind handlebars with hydraulic lever"),
           ("Attachments", "Snow plough blade (optional)"),
           ("Warranty", "2 years parts, 1 year engine")],
    features_h2="Why a tracked dumper beats a barrow and a plank",
    features=[("Hydraulic tipping", "Raise and empty the skip from the handlebars. No lifting, no "
               "tipping a barrow by hand, and no shovelling the same spoil twice."),
              ("Rubber tracks", "Weight spread across two tracks instead of one wheel. It crosses "
               "wet clay and a customer's finished lawn without cutting the ruts you then have to "
               "make good."),
              ("Walk-behind", "You are beside the machine, not in it. On a domestic job you are off "
               "and on every few minutes for a gate or a level check."),
              ("Petrol and hydraulics", "Petrol keeps it light; the hydraulics do the lifting. "
               "Everything you touch day to day is at standing height."),
              ("Snow plough attachment", "The blade bolts on for winter, so the machine keeps "
               "earning through the months when groundwork stops."),
              ("Serviceable in the open", "Fuel, oil and filters are reached without lifting the "
               "machine or booking it in anywhere.")],
    faq=[("What is the payload?",
          "<p>We are confirming the rated payload and the tipping height with the manufacturer and "
          "will publish both here rather than estimate them. Email us if you need the figures before "
          "you order and we will confirm them in writing the same working day.</p>"),
         ("Will it fit through a gateway?",
          "<p>It is built narrow deliberately, which is the whole point of a tracked dumper. Measure "
          "the narrowest point on your route — usually a gate post or a meter box rather than the "
          "gate itself — and we will confirm the exact track width against it before you order.</p>"),
         ("Can it climb a sloping garden?",
          "<p>Tracks give far better grip than wheels on a slope, and the low body keeps the centre "
          "of gravity down. Always drive up and down a slope rather than across it, and reduce the "
          "load rather than trusting a maximum figure.</p>"),
         ("Is the snow plough included?",
          "<p>The plough blade is an optional attachment, not part of the standard machine. Ask us "
          "for the current price and we will quote it with your order.</p>"),
         ("How do I get it on site?",
          "<p>It is designed to move on a braked car trailer rather than needing a plant lorry. "
          "Check your trailer's plated capacity and your licence entitlement, and confirm the "
          "machine weight with us first.</p>")],
)

# Which catalogue product each real machine replaces, per store.
OVERRIDES = {"branchforge": {"cyclone-150-td": HC15H, "titan-1000-ht": MD500}}
