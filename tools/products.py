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
            real = _rebrand(copy.deepcopy(overrides[base["slug"]]), brand)
            real["order"] = i
            real["brand"] = brand
            real["name_full"] = f"{brand} {real['name']}"
            # SKUs carry the store prefix, or both stores ship colliding feed IDs
            real["sku"] = f"{prefix}-{real['sku'].split('-', 1)[1]}"
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


CREX10K = dict(
    slug="crex10k-mini-excavator", url="crex10k-mini-excavator.html", dir="assets/img/crex10k",
    sku="BF-CREX10K", name="CREX10-K Mini Excavator", short="CREX10-K",
    short_desc="900 kg diesel mini excavator with a telescopic chassis that narrows to 800 mm "
               "for gated access.",
    lede="A 900 kg backhoe mini excavator on rubber tracks, with a dozer blade, boom swing and a "
         "telescopic undercarriage that closes to 800 mm to get down the side of a house and opens "
         "to 950 mm for stability once it is in.",
    tag="Most capable", price=3449, was=4299, finance=81,
    stockline="In stock — ships crated from our UK warehouse",
    meta_desc="BranchForge CREX10-K mini excavator: 900 kg, KOOP 192 diesel, 1580 mm digging depth, "
              "telescopic 800/950 mm chassis, rubber tracks. Free UK mainland delivery.",
    images=[], bullets=[
        "Telescopic chassis: 800 mm through a gate, 950 mm for working stability",
        "900 kg operating weight — moves on a braked car trailer, no plant lorry",
        "1580 mm digging depth and 3040 mm reach at ground level",
        "Boom swing 50° left and 55° right, so you dig alongside a wall",
        "Dozer blade for backfilling and levelling without a second machine",
        "Rubber tracks and 30% gradeability for soft or sloping ground",
        "Quick-hitch attachments: breaker, auger, grabber, rake, ripper and buckets"],
    spec_hi=[("Operating weight", "900 kg"), ("Digging depth", "1580 mm"),
             ("Chassis width", "800 / 950 mm"), ("Engine", "KOOP 192 diesel, 7 kW")],
    specs=[("Model", "BranchForge CREX10-K"), ("Operating weight", "900 kg"),
           ("Working device form", "Backhoe"), ("Standard bucket capacity", "0.02 m³"),
           ("Engine model", "KOOP 192 diesel"), ("Rated power", "7 kW"),
           ("Maximum torque", "25 N·m at 2860 rpm"),
           ("Maximum travel speed", "1.4 km/h"), ("Swing speed", "11 rpm"),
           ("Maximum gradeability", "30%"),
           ("Max. digging depth", "1580 mm"), ("Max. vertical digging depth", "1340 mm"),
           ("Max. digging radius on ground", "3040 mm"), ("Max. digging radius", "3135 mm"),
           ("Max. digging height", "2620 mm"), ("Max. dumping height", "2000 mm"),
           ("Min. swing radius", "1510 mm"),
           ("Boom swing", "50° left, 55° right"),
           ("Chassis width (telescopic)", "800 / 950 mm"),
           ("Track width", "180 mm"), ("Track length", "1235 mm"), ("Wheel tread", "910 mm"),
           ("Track material", "Rubber"), ("Track tension", "Screw adjustment"),
           ("Platform tail turning radius", "680 mm"),
           ("Transportation length", "2170 / 2850 mm"),
           ("Max. blade lifting height", "140 mm"), ("Max. blade lifting depth", "200 mm"),
           ("Hydraulic pump", "Gear oil pump"), ("Working pressure", "16 MPa"),
           ("Flow rate", "19 L/min"), ("Hydraulic oil tank", "16.5 L"), ("Fuel tank", "11 L"),
           ("Warranty", "2 years parts, 1 year engine")],
    features_h2="A real excavator that fits down the side of a house",
    features=[("Telescopic undercarriage", "Closed it is 800 mm across, which clears a standard "
               "side gate. Once through, it opens to 950 mm so it is stable enough to dig against "
               "rather than tipping toward the trench."),
              ("900 kg", "Light enough for a braked car trailer, so you are not hiring a plant "
               "lorry or waiting for a transport slot to start a job."),
              ("Boom swing", "50° left and 55° right lets you dig parallel to a wall or a fence "
               "without repositioning the tracks every metre."),
              ("Dozer blade", "Backfill and level with the same machine that dug the trench. "
               "It also stabilises the front while you are working."),
              ("Diesel", "A KOOP 192 diesel at 7 kW, with 16 MPa hydraulics and 19 L/min of flow "
               "— enough to run a breaker or an auger properly."),
              ("Quick-hitch attachments", "Breaker, auger, log grabber, rake, ripper and buckets "
               "from 200 mm to 800 mm all change over on the quick hitch.")],
    attachments=[("200 mm bucket", 249), ("800 mm bucket", 299), ("Quick hitch", 165),
                 ("Ripper", 159), ("Rake", 199), ("Log grabber", 339),
                 ("Auger", 799), ("Hydraulic breaker", 1299)],
    faq=[("Will it fit through a side gate?",
          "<p>The chassis is telescopic: 800 mm closed and 950 mm open. A standard UK side gate "
          "opening is 780–900 mm, so it fits the great majority with the tracks retracted. Measure "
          "the narrowest point on the route, which is usually a gate post rather than the gate.</p>"),
         ("How deep will it dig?",
          "<p>1580 mm maximum digging depth, 1340 mm vertical, with a reach of 3040 mm at ground "
          "level. That covers drainage, footings for a garden room, ponds and service trenches.</p>"),
         ("How do I get it to site?",
          "<p>900 kg operating weight, so a braked car trailer plated for a tonne or more will "
          "carry it. Check your trailer plate and your licence entitlement before loading.</p>"),
         ("Which attachments are included?",
          "<p>The machine ships with its standard bucket. The breaker, auger, grabber, rake, "
          "ripper, quick hitch and the wider buckets are separate — current prices are listed on "
          "this page. Ask us to add any of them to your order.</p>"),
         ("Do I need a licence or a card?",
          "<p>No legal licence to own or use one on private land. For paid work on a commercial "
          "site most principal contractors want a CPCS or NPORS card for 360° excavators under "
          "10 tonnes. That is a site-access requirement rather than a legal one, and we do not "
          "provide certification.</p>")],
)

SKIDSTEER = dict(
    slug="mini-skid-steer-loader", url="mini-skid-steer-loader.html", dir="assets/img/mini-skid-steer",
    sku="BF-MSS739", name="Mini Skid Steer Loader", short="Mini Skid Steer",
    short_desc="739 cc petrol tracked loader with auxiliary hydraulics — the machine that "
               "replaces the gang.",
    lede="A tracked stand-on loader with a 739 cc petrol engine, a quick-attach bucket and "
         "auxiliary hydraulic couplers on the arm, so it lifts, carries and runs powered "
         "attachments on ground a wheeled loader would tear up.",
    tag="Highest margin", price=3299, was=4199, finance=77,
    stockline="In stock — ships crated from our UK warehouse",
    meta_desc="BranchForge mini skid steer loader: 739 cc petrol, rubber tracks, quick-attach "
              "bucket, auxiliary hydraulics. Free UK mainland delivery.",
    images=[], bullets=[
        "739 cc petrol engine, key start, with an hour meter and oil temperature gauge",
        "Rubber tracks spread the weight — crosses wet ground and finished lawns",
        "Quick-attach plate, so the bucket comes off and other tools go on",
        "Auxiliary hydraulic couplers on the arm for powered attachments",
        "Loader arms lift clear above a trailer side or a skip wall",
        "CE marked, 95 dB(A) guaranteed sound power",
        "2-year parts warranty and UK-held spares"],
    spec_hi=[("Engine", "739 cc petrol"), ("Drive", "Rubber tracks"),
             ("Attachment", "Quick-attach plate"), ("Hydraulics", "Auxiliary couplers")],
    specs=[("Model", "BranchForge Mini Skid Steer Loader"),
           ("Engine", "739 cc petrol, air-cooled"),
           ("Starting", "Electric key start"),
           ("Instrumentation", "Hour meter and oil temperature gauge"),
           ("Undercarriage", "Rubber tracks"),
           ("Attachment interface", "Quick-attach plate, bucket supplied"),
           ("Auxiliary hydraulics", "Quick couplers on the loader arm"),
           ("Sound power", "95 dB(A) guaranteed (Lwa)"),
           ("Conformity", "CE marked"),
           ("Warranty", "2 years parts, 1 year engine")],
    features_h2="One machine, the whole muck-away job",
    features=[("739 cc petrol", "Enough engine to lift and drive attachments, while staying light "
               "enough to trailer and simple enough to service without a dealer."),
              ("Rubber tracks", "Weight spread across two tracks rather than four wheels, so it "
               "works on wet clay and crosses a customer's lawn without cutting ruts."),
              ("Quick-attach plate", "The bucket comes off in a minute. Forks, grapples and "
               "augers go on in its place without tools."),
              ("Auxiliary hydraulics", "Quick couplers are already plumbed to the arm, so a "
               "powered attachment connects and works rather than needing a conversion."),
              ("Hour meter and oil temperature", "You can see what the machine has done and how "
               "hard it is working — the two things that decide when to service it."),
              ("Stand-on and compact", "Step off at every gate without shutting down, and turn "
               "within the machine's own length in a back garden.")],
    faq=[("What can it lift?",
          "<p>We are confirming the rated operating capacity with the manufacturer and will publish "
          "it here rather than estimate it. Rated capacity is conventionally half the static "
          "tipping load — be wary of any seller quoting the tipping load as the lift. Email us if "
          "you need the figure before ordering.</p>"),
         ("Will other attachments fit?",
          "<p>It uses a quick-attach plate with auxiliary hydraulics already run to the arm. Check "
          "the plate standard and the flow requirement of any attachment against the machine before "
          "buying it, and we will confirm compatibility in writing.</p>"),
         ("How wide is it?",
          "<p>We are confirming the exact track width and overall width with the manufacturer. "
          "Measure the narrowest point on your access route and we will check it against the real "
          "figure before you order.</p>"),
         ("Petrol rather than diesel?",
          "<p>Petrol keeps the weight down so the machine trailers easily and stays manoeuvrable "
          "in a garden. It also avoids red-diesel record-keeping for commercial use.</p>"),
         ("Is the bucket included?",
          "<p>Yes — the machine ships with the bucket shown in the photographs. Other attachments "
          "are separate; ask us for prices and we will quote them with your order.</p>")],
)

OVERRIDES["branchforge"]["grindmaster-380-tx"] = CREX10K
OVERRIDES["branchforge"]["vanguard-850-sl"] = SKIDSTEER

# HaulCrest sells the same four machines under its own brand; the photographs
# show identical models, so the same definitions apply once rebranded.
OVERRIDES["haulcrest"] = {
    "cyclone-150-td": HC15H,
    "grindmaster-380-tx": CREX10K,
    "titan-1000-ht": MD500,
    "vanguard-850-sl": SKIDSTEER,
}
