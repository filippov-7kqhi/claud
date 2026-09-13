# -*- coding: utf-8 -*-
"""The four machines AgriMaxx and GroundMaxx sell, brand-neutral.

Both stores have photography of the identical range, each decalled in that
store's own name -- the same pattern as CREX6M/DP5000/TW1375G/SW360 in
cat_photo.py for RootVexx and LawnStride, just for the US market. Figures not
confirmed by the manufacturer are left out rather than guessed; the FAQ says
to ask. %BRAND% is substituted per store. Prices are draft placeholders set
by the owner pending real supplier cost and margin -- see tools/products.py
and the AgriMaxx/GroundMaxx launch notes.
"""

VHF71 = dict(
    slug="vhf71-ditch-bank-mower", url="vhf71-ditch-bank-mower.html", dir="assets/img/vhf71",
    sku="XX-VHF71", name="VHF71 71″ Heavy-Duty Hydraulic Offset Flail Ditch Bank Mower",
    short="VHF71",
    short_desc="71-inch hydraulic offset flail mower for verges, ditch banks and road shoulders -- "
               "swings out on a hydraulic arm while the tractor stays on flat ground.",
    lede="A 3-point, PTO-driven flail mower built for verges, ditch banks and road shoulders. A "
         "hydraulic arm swings the 71-inch cutting head out to the side -- and tilts it -- so the "
         "tractor runs along flat ground while the head does the work on the bank or slope beside it.",
    tag="Hydraulic side-offset", price=7499, was=8999, finance=170,
    stockline="In stock -- ships freight from our US warehouse",
    meta_desc="%BRAND% VHF71 71-inch hydraulic offset flail ditch bank mower: PTO driven, hydraulic "
              "side-offset arm, 3-point mounted, for 60-100 HP tractors. Nationwide freight shipping.",
    images=[], bullets=[
        "71-inch cutting width -- flail (hammer-blade) head for verges, banks and rough growth",
        "Hydraulic side-offset arm swings the head out to mow ditch banks and shoulders while the "
        "tractor stays on flat, stable ground",
        "Head also tilts on the arm, so you angle the cut to the slope instead of fighting it",
        "3-point rear mounted, PTO driven -- built for 60-100 HP tractors",
        "Category-appropriate 3-point hitch",
        "VHF71 model designation is stamped on the machine itself",
        "PTO driveline shaft included"],
    spec_hi=[("Cutting width", "71 in"), ("Mounting", "3-point, rear"),
             ("Offset", "Hydraulic side-offset"), ("Tractor size", "60-100 HP")],
    specs=[("Model", "%BRAND% VHF71"), ("Cutting width", "71 in"),
           ("Cutting system", "PTO-driven flail (hammer-blade) rotor"),
           ("Mounting", "3-point, rear-mounted"),
           ("Offset arm", "Hydraulic side-offset, with head tilt"),
           ("Recommended tractor", "60-100 HP"),
           ("Hitch category", "Category-appropriate 3-point hitch -- confirm Cat. I/II with us "
            "before ordering"),
           ("Driveline", "PTO shaft included")],
    features_h2="What makes an offset mower different from a standard flail",
    features=[("Hydraulic side-offset arm", "The cutting head swings out to the side on a hydraulic "
               "arm, so you mow the verge, ditch bank or shoulder while the tractor itself stays on "
               "flat, stable ground instead of leaning down the slope.",
               ("07-side-profile-full.jpg", "Full-length side profile showing the offset arm and "
                "hydraulic cylinder")),
              ("Head tilt", "The head angles on the arm as well as swinging out, so the cut follows "
               "the bank's slope rather than sitting flat against it.",
               ("05-rear-three-quarter.jpg", "Rear three-quarter view of the cutting head housing "
                "with the offset arm extending back to the 3-point hitch")),
              ("71-inch flail head", "A hammer-blade (flail) rotor mulches rough growth, brambles "
               "and small saplings without throwing debris the way a rotary blade does.",
               ("06-gearbox-detail.jpg", "Close view of the gearbox, cutting head housing and skid "
                "shoe")),
              ("3-point, PTO driven", "Mounts on a standard rear 3-point hitch and runs off the "
               "tractor's PTO -- no separate engine to fuel or service.",
               ("04-hitch-and-offset-arm-detail.jpg", "Close view of the 3-point hitch pins, "
                "hydraulic hoses and offset-arm pivot")),
              ("Built for 60-100 HP tractors", "Sized for the kind of tractor that already does "
               "road-shoulder, ditch and right-of-way work.",
               ("03-side-profile.jpg", "Full side profile with the hydraulic offset arm folded in "
                "for transport")),
              ("VHF71 on the machine", "The model number is stamped on the machine itself, so parts "
               "and service enquiries are easy to identify.",
               ("01-hero.jpg", "Three-quarter studio view showing the VHF71 model stamp"))],
    faq=[("What does “offset” mean on this mower?",
          "<p>The cutting head is mounted on a hydraulic arm that swings out to the side of the "
          "tractor, and tilts, so you can mow a ditch bank, verge or road shoulder while the tractor "
          "itself stays on flat ground. It is not a straight rear-mounted mower.</p>"),
         ("What size tractor do I need?",
          "<p>The VHF71 is built for tractors in the 60-100 HP range. Check your tractor's rear "
          "hydraulic remotes (the offset arm and head tilt are hydraulically actuated) and 3-point "
          "hitch category against the machine before you order, and ask us if you are not sure.</p>"),
         ("How far does the arm reach, and how many blades does it carry?",
          "<p>We are confirming the exact offset reach, blade count and gearbox ratio with the "
          "manufacturer and will publish them here rather than estimate them. Email us if you need a "
          "figure before you order and we will confirm it in writing.</p>"),
         ("What PTO speed does it run at?",
          "<p>We are confirming the rated PTO speed (540 or 1000 rpm) with the manufacturer before "
          "publishing it. Please ask us to confirm before ordering if this affects your tractor's PTO "
          "output.</p>"),
         ("Do I need a special hitch category?",
          "<p>The VHF71 uses a category-appropriate 3-point hitch. Confirm Category I or Category II "
          "with us against your tractor before you order.</p>"),
         ("Is the driveline shaft included?",
          "<p>Yes -- the PTO driveline shaft ships with the machine, as shown in the photographs.</p>")],
)

LFS53 = dict(
    slug="lfs53-flail-mower", url="lfs53-flail-mower.html", dir="assets/img/lfs53",
    sku="XX-LFS53", name="LFS53 53″ 3-Point Flail Mower", short="LFS53",
    short_desc="53-inch PTO flail mower for 15-35 HP tractors -- Category 1 3-point mount, "
               "hammer-blade cutting head.",
    lede="A 53-inch 3-point flail mower built for compact tractors: PTO driven, Category 1 hitch, "
         "with a hammer-blade cutting head that mulches rough grass, brambles and light brush "
         "instead of throwing it.",
    tag="53 in cutting width", price=2199, was=2699, finance=50,
    stockline="In stock -- ships freight from our US warehouse",
    meta_desc="%BRAND% LFS53 53-inch 3-point flail mower: PTO driven, Category 1 hitch, for 15-35 HP "
              "tractors. Nationwide freight shipping.",
    images=[], bullets=[
        "53-inch cutting width -- flail (hammer-blade) head",
        "PTO driven, Category 1 3-point mount",
        "Built for 15-35 HP compact tractors",
        "Hammer-blade rotor mulches rough grass and light brush rather than throwing it",
        "PTO driveline shaft included"],
    spec_hi=[("Cutting width", "53 in"), ("Mounting", "3-point, Category 1"),
             ("Cutting system", "PTO flail"), ("Tractor size", "15-35 HP")],
    specs=[("Model", "%BRAND% LFS53"), ("Cutting width", "53 in"),
           ("Cutting system", "PTO-driven flail (hammer-blade) rotor"),
           ("Mounting", "3-point, Category 1 hitch"), ("Recommended tractor", "15-35 HP"),
           ("Driveline", "PTO shaft included")],
    features_h2="A flail mower sized for a compact tractor",
    features=[("53-inch flail head", "Hammer blades swing on pivots and fold back off a stone or "
               "stump instead of transmitting the hit into the gearbox the way a fixed rotary blade "
               "does.",
               ("08-flail-blades-detail.jpg", "Close view of the flail rotor and hammer blades "
                "along the deck edge")),
              ("Category 1 hitch", "Mounts straight onto the 3-point hitch of a compact tractor -- "
               "no adapter needed on a Cat. 1 tractor.",
               ("05-hitch-and-gearbox.jpg", "Front three-quarter view of the Category 1 top link "
                "and lower-link A-frame with the gearbox")),
              ("Sized for 15-35 HP", "Matched to the tractors most likely to be running it, so you "
               "are not overpowering or underpowering the gearbox.",
               ("03-side-profile.jpg", "Full side profile of the LFS53 flail mower")),
              ("PTO driven", "Runs off the tractor's PTO -- no separate engine, fuel or service "
               "schedule.",
               ("02-driveline-detail.jpg", "Close view of the PTO driveline and gearbox area")),
              ("Mulches rather than throws", "Flail mowers cut and mulch in the housing, which is "
               "safer around fence lines, driveways and livestock than a discharge-style rotary "
               "cutter.",
               ("04-rotor-housing-detail.jpg", "Close view of the rotor housing and rear roller"))],
    faq=[("What size tractor do I need?",
          "<p>The LFS53 is built for 15-35 HP compact tractors with a Category 1 3-point hitch.</p>"),
         ("How many blades does it have, and how much does it weigh?",
          "<p>We are confirming the blade count, gearbox ratio and shipping weight with the "
          "manufacturer and will publish them here rather than estimate. Email us if you need a "
          "figure before ordering.</p>"),
         ("What PTO speed does it use?",
          "<p>We are confirming the rated PTO speed with the manufacturer before publishing it. Ask "
          "us to confirm before you order if this affects your tractor.</p>"),
         ("Is the driveline shaft included?",
          "<p>Yes -- the PTO driveline shaft ships with the machine, as shown in the photographs.</p>"),
         ("Will it cut brush as well as grass?",
          "<p>It is built for rough grass, brambles and light brush. For established woody growth or "
          "saplings above light-brush size, ask us whether this or a heavier machine is the right "
          "fit.</p>")],
)

PHD18 = dict(
    slug="phd18-post-hole-digger", url="phd18-post-hole-digger.html", dir="assets/img/phd18",
    sku="XX-PHD18", name="PHD18 3-Point Post Hole Digger", short="PHD18",
    short_desc="3-point post hole digger for 18 HP+ tractors -- gearbox and mast only; auger sold "
               "separately.",
    lede="A 3-point mounted, PTO-driven post hole digger gearbox and mast for tractors from 18 HP "
         "up. The auger shown in our photographs is for illustration -- it is sold separately and is "
         "not included.",
    tag="Auger sold separately", price=349, was=429, finance=8,
    stockline="In stock -- ships freight from our US warehouse",
    meta_desc="%BRAND% PHD18 3-point post hole digger: PTO driven, for 18 HP+ tractors. Auger sold "
              "separately. Nationwide freight shipping.",
    images=[], bullets=[
        "3-point mounted, PTO driven gearbox and mast",
        "Minimum 18 HP tractor required",
        "IMPORTANT: the auger is sold separately and is NOT included -- the auger shown in our "
        "photographs is for illustration only",
        "Stabilizer legs fold down for a steady, level bore"],
    spec_hi=[("Mounting", "3-point"), ("Drive", "PTO"), ("Min. tractor", "18 HP"),
             ("Auger", "Sold separately")],
    specs=[("Model", "%BRAND% PHD18"), ("Mounting", "3-point"), ("Drive", "PTO-driven gearbox"),
           ("Minimum tractor size", "18 HP"), ("Auger", "Not included -- sold separately")],
    features_h2="What you get, and what you need to add",
    features=[("3-point PTO gearbox", "Mounts on the tractor's 3-point hitch and runs off the PTO, "
               "with fold-down stabilizer legs to steady the bore.",
               ("03-mount-detail.jpg", "Close view of the gearbox and mast mounted on a tractor's "
                "3-point hitch")),
              ("Auger sold separately", "The digger unit ships without an auger. Choose the auger "
               "diameter that suits your posts and order it alongside the digger -- do not assume "
               "one is included.",
               ("04-auger-detail.jpg", "Auger bit turning into the ground -- auger sold separately, "
                "not included with the digger")),
              ("Minimum 18 HP", "Sized for a real compact-tractor PTO, not a garden tractor.",
               ("02-in-use-wide.jpg", "PHD18 mounted on the 3-point hitch of a compact tractor, "
                "boring a hole in an open field"))],
    faq=[("Does this come with an auger?",
          "<p><strong>No.</strong> The photographs on this page show the digger fitted with an auger "
          "for illustration, but the auger is sold separately and is not included with this listing. "
          "Choose an auger to suit your post size and order it alongside the digger.</p>"),
         ("What size tractor do I need?",
          "<p>A minimum of 18 HP with a 3-point hitch and PTO.</p>"),
         ("How deep will it dig, and what auger sizes fit?",
          "<p>We are confirming the maximum digging depth and the auger mounting size (hex or round, "
          "and shank diameter) with the manufacturer and will publish them here rather than estimate. "
          "Email us before you order an auger separately if you need this confirmed first.</p>"),
         ("What does the gearbox weigh?",
          "<p>We are confirming the shipping weight with the manufacturer and will publish it rather "
          "than estimate it.</p>")],
)

RC72 = dict(
    slug="rc72-rotary-cutter", url="rc72-rotary-cutter.html", dir="assets/img/rc72",
    sku="XX-RC72", name="RC72 6 ft. Round-Back Rotary Cutter", short="RC72",
    short_desc="6-foot round-back rotary cutter -- 3-point mounted, PTO driven brush-hog style "
               "cutter.",
    lede="A 6-foot round-back rotary cutter for 3-point mounting on a PTO tractor -- the round-back, "
         "brush-hog style deck that clears pasture, fence lines and overgrown ground.",
    tag="6 ft cutting width", price=1449, was=1799, finance=33,
    stockline="In stock -- ships freight from our US warehouse",
    meta_desc="%BRAND% RC72 6 ft. round-back rotary cutter: 3-point mounted, PTO driven. Nationwide "
              "freight shipping.",
    images=[], bullets=[
        "6-foot cutting width",
        "Round-back deck -- the classic brush-hog style rotary cutter",
        "3-point mounted, PTO driven",
        "Tail wheel for a consistent cutting height",
        "PTO driveline shaft included"],
    spec_hi=[("Cutting width", "6 ft"), ("Deck", "Round-back"), ("Mounting", "3-point"),
             ("Drive", "PTO")],
    specs=[("Model", "%BRAND% RC72"), ("Cutting width", "6 ft"), ("Deck style", "Round-back"),
           ("Mounting", "3-point"), ("Drive", "PTO-driven"), ("Driveline", "PTO shaft included")],
    features_h2="A brush-hog style cutter built to be mounted and forgotten",
    features=[("6-foot round-back deck", "Wide enough to make real progress on pasture and rough "
               "ground, in the round-back shape most operators already recognize as a brush hog.",
               ("02-in-use-tall-grass.jpg", "RC72 mounted on a tractor, cutting through tall "
                "dormant grass and brush")),
              ("3-point, PTO driven", "Mounts on the tractor's rear 3-point hitch and runs off the "
               "PTO.",
               ("04-driveline-detail.jpg", "Close view of the PTO driveline shaft and yoke "
                "connecting to the tractor")),
              ("Tail wheel", "Holds a consistent cutting height across uneven ground instead of "
               "scalping high spots.",
               ("01-hero.jpg", "Side profile studio view with tail wheel and PTO driveline shaft"))],
    faq=[("What HP tractor do I need?",
          "<p>We are confirming the recommended tractor HP range with the manufacturer and will "
          "publish it here rather than estimate it. Email us if you need this confirmed before you "
          "order.</p>"),
         ("How many blades does it have, and what gauge is the deck?",
          "<p>We are confirming blade count and deck gauge with the manufacturer and will publish "
          "them rather than estimate.</p>"),
         ("How much does it weigh?",
          "<p>We are confirming the shipping weight with the manufacturer and will publish it here "
          "rather than estimate it.</p>"),
         ("Is the driveline shaft included?",
          "<p>Yes -- the PTO driveline shaft ships with the machine, as shown in the photographs.</p>")],
)

US_FOUR = [VHF71, LFS53, PHD18, RC72]
