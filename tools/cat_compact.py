# -*- coding: utf-8 -*-
"""The compact-plant catalogue: mini excavator, mini dumper, log splitter and
   ATV flail mower. Brand-neutral -- %BRAND% is substituted per store."""

EX10 = dict(
    slug="ex10-mini-excavator", url="ex10-mini-excavator.html", dir="assets/img/ex10-excavator",
    sku="XX-EX10", name="EX10 1 Tonne Mini Excavator", short="EX10",
    short_desc="1 tonne rubber-tracked mini digger with a variable-width undercarriage and a "
               "blade — through a side gate, then straight into the trench.",
    lede="A 1050 kg diesel mini excavator on rubber tracks, with an undercarriage that retracts to "
         "930 mm to clear a side gate and expands to 1200 mm for stability once it is in. Digs to "
         "1.75 m, slews through 360° and runs a breaker off the auxiliary circuit.",
    tag="930 mm access", price=4999, was=6199, finance=117,
    stockline="In stock — ships crated from our UK warehouse",
    meta_desc="%BRAND% EX10 1 tonne mini excavator: 14 hp diesel, rubber tracks, variable-width "
              "undercarriage 930–1200 mm, 1.75 m dig depth. Free UK mainland delivery.",
    images=[("01-hero.svg", "EX10 1 tonne mini excavator, full machine on a studio background"),
            ("02-side.svg", "EX10 side profile with the arm folded for transport"),
            ("03-dig.svg", "Boom, dipper and bucket extended, showing dig depth and reach"),
            ("04-cab.svg", "Operator station: canopy, seat, joysticks and instrument panel"),
            ("05-undercarriage.svg", "Rubber tracks, variable-width undercarriage and dozer blade"),
            ("06-dimensions.svg", "Dimensioned drawing: 930 mm retracted width, 1.75 m dig depth"),
            ("07-in-use.svg", "EX10 digging a drainage trench on a domestic site"),
            ("08-included.svg", "Everything supplied in the crate with the EX10")],
    bullets=["Retracts to 930 mm — through a standard side gate, then widens to 1200 mm to dig",
             "Digs to 1.75 m and loads over the side of a 1-tonne dumper",
             "360° slew with boom offset, so you can dig alongside a wall",
             "Rear dozer blade for backfilling and levelling without a second machine",
             "Auxiliary hydraulic circuit — runs a breaker, auger or grab",
             "1050 kg: legal on a 2000 kg plant trailer behind a 4x4",
             "Two-year parts warranty and UK-held spares"],
    spec_hi=[("Operating weight", "1050 kg"), ("Dig depth", "1.75 m"),
             ("Width", "930–1200 mm"), ("Engine", "14 hp diesel")],
    specs=[("Model", "%BRAND% EX10"), ("Operating weight", "1050 kg"),
           ("Engine", "3-cylinder liquid-cooled diesel"), ("Rated power", "14 hp (10.3 kW)"),
           ("Starting", "Electric, 12 V with key isolator"), ("Fuel capacity", "18 litres"),
           ("Maximum dig depth", "1750 mm"), ("Maximum reach at ground level", "3200 mm"),
           ("Maximum dump height", "2300 mm"), ("Slew", "360° continuous, with boom offset"),
           ("Undercarriage width", "930 mm retracted / 1200 mm expanded"),
           ("Track width", "180 mm rubber"), ("Dozer blade width", "930 mm"),
           ("Standard bucket", "300 mm digging bucket, bolt-on teeth"),
           ("Auxiliary hydraulics", "Single circuit, 32 L/min, breaker-ready"),
           ("Travel speed", "0–2.5 km/h"), ("Maximum gradient", "30 degrees"),
           ("Overall length (arm folded)", "3.10 m"), ("Overall height to canopy", "2.28 m"),
           ("Noise level", "96 dB(A) at operator position"),
           ("Warranty", "2 years parts, 1 year engine (manufacturer-backed)")],
    features_h2="Why a 1 tonne digger is the one that earns its keep",
    features=[("930 mm retracted", "The number that decides most domestic jobs. Tracks in retracted, "
               "widen once you are through, and dig with a stable footprint instead of a nervous one."),
              ("Rear dozer blade", "Backfill the trench and level the spoil with the same machine. "
               "A digger without a blade means a second pass with a shovel."),
              ("Boom offset", "Swings the boom sideways so the arm digs parallel to a wall or fence "
               "while the tracks stay square. Footings next to a boundary stop being a hand-dig."),
              ("Breaker-ready", "The auxiliary circuit is plumbed and fitted with couplers from new. "
               "Hire a breaker for the morning it is needed instead of hiring the whole machine."),
              ("Diesel, not petrol", "Torque at low revs is what holds the bucket through clay. "
               "A diesel also idles all day on a fraction of the fuel a petrol equivalent burns."),
              ("Trailerable at 1050 kg", "A 2000 kg plant trailer and a 4x4 move it legally. No plant "
               "lorry, no transport booking, no waiting for a slot to start.")],
    faq=[("Will it fit through a side gate?",
          "<p>Retracted, the undercarriage is 930 mm across and the canopy is the widest point at "
          "930 mm. A standard UK side gate opening is 780–900 mm, so it clears a wide gate and a "
          "double gate but not a narrow one. Measure the narrowest point — usually the gate post.</p>"),
         ("Do I need a licence or a card to operate it?",
          "<p>There is no legal licence to own or use one on private land. For paid work on a "
          "commercial site most principal contractors want a CPCS or NPORS card for 360° excavators "
          "below 10 tonnes. That is a site-access requirement, not a legal one, and we do not "
          "provide certification.</p>"),
         ("What can I tow it with?",
          "<p>1050 kg operating weight plus the trailer. A 2000 kg braked plant trailer and a vehicle "
          "rated to tow it — most 4x4s and larger vans — is the usual combination. Check your V5C "
          "towing capacity, your nose weight and your licence entitlement before you load it.</p>"),
         ("Can it run a breaker?",
          "<p>Yes. The auxiliary circuit gives 32 L/min at the couplers, which suits the 60–70 kg "
          "class of hydraulic breaker normally paired with a 1 tonne machine. The breaker itself is "
          "not supplied.</p>"),
         ("How long do the rubber tracks last?",
          "<p>Typically 800–1200 hours on mixed ground, considerably less on hardcore and kerbs. "
          "Replacements are held in the UK and dispatched within 48 hours.</p>")],
)

TD500 = dict(
    slug="td500-mini-dumper", url="td500-mini-dumper.html", dir="assets/img/td500-dumper",
    sku="XX-TD500", name="TD500 500 kg Tracked Mini Dumper", short="TD500",
    short_desc="500 kg tracked dumper with a hydraulic tip — fits a doorway, empties itself.",
    lede="A 780 mm wide rubber-tracked barrow that carries half a tonne and tips it hydraulically "
         "at the touch of a lever. It goes where a wheelbarrow goes, and does the work of twelve "
         "of them without a plank or a second pair of hands.",
    tag="780 mm access", price=2499, was=3099, finance=59,
    stockline="In stock — ships crated from our UK warehouse",
    meta_desc="%BRAND% TD500 tracked mini dumper: 500 kg payload, hydraulic tip, 9 hp petrol, "
              "780 mm wide. Free UK mainland delivery.",
    images=[("01-hero.svg", "TD500 tracked mini dumper, full machine on a studio background"),
            ("02-side.svg", "TD500 side profile showing the low loading height"),
            ("03-tip.svg", "Skip tipped forward, discharging a load of spoil"),
            ("04-engine.svg", "Power pack detail: 9 hp petrol engine and hydraulic pump"),
            ("05-controls.svg", "Walk-behind handlebars, tip lever and dead-man bar"),
            ("06-dimensions.svg", "Dimensioned drawing: 780 mm wide, 1.95 m long"),
            ("07-in-use.svg", "TD500 carrying spoil down a narrow garden path"),
            ("08-included.svg", "Everything supplied in the crate with the TD500")],
    bullets=["500 kg payload — twelve barrow loads in one trip",
             "780 mm across: through a standard doorway and down a terrace alley",
             "Hydraulic tip on a lever; you never shovel the same spoil twice",
             "Rubber tracks spread the load and stay off a finished lawn",
             "9 hp petrol with recoil start — fills at any forecourt",
             "265 kg unladen: two people and a ramp get it onto a van",
             "Two-year parts warranty and UK-held spares"],
    spec_hi=[("Payload", "500 kg"), ("Width", "780 mm"),
             ("Tip", "Hydraulic"), ("Engine", "9 hp petrol")],
    specs=[("Model", "%BRAND% TD500"), ("Payload", "500 kg"),
           ("Skip capacity", "250 litres (0.25 m³) heaped"),
           ("Tipping", "Hydraulic, single lever"), ("Engine", "Single-cylinder OHV petrol"),
           ("Rated power", "9 hp (6.6 kW)"), ("Starting", "Recoil"),
           ("Fuel capacity", "6.5 litres"), ("Drive", "Hydrostatic, independent track control"),
           ("Travel speed", "0–4 km/h"), ("Maximum gradient", "25 degrees"),
           ("Track width", "180 mm rubber"), ("Overall width", "780 mm"),
           ("Overall length", "1.95 m"), ("Overall height to handlebars", "1.05 m"),
           ("Loading height", "0.72 m"), ("Unladen weight", "265 kg"),
           ("Noise level", "94 dB(A) at operator position"),
           ("Warranty", "2 years parts, 1 year engine (manufacturer-backed)")],
    features_h2="Why this replaces a gang with barrows",
    features=[("780 mm across", "Through a standard 838 mm doorway and down the side of a terrace. "
               "The access is the job; everything else follows from it."),
              ("Hydraulic tip", "Pull the lever and the skip empties itself. Shovelling a load out "
               "of a tipper by hand is where a day actually goes."),
              ("Rubber tracks", "Low ground pressure keeps it off a customer's lawn and gets it up "
               "a slope a barrow cannot be pushed up."),
              ("Low loading height", "The skip lip sits at 720 mm, so you are dropping spoil in, "
               "not lifting it over your head."),
              ("Recoil start", "No battery to go flat over a wet winter. It starts on the pull "
               "whether it has run this month or not."),
              ("265 kg unladen", "Light enough for two people and a ramp to load into a Transit. "
               "No trailer needed to get to the job.")],
    faq=[("Will it really fit through a doorway?",
          "<p>780 mm across the widest point. A standard UK internal door opening is 838 mm and a "
          "back door is usually 813 mm, so yes — but measure the frame, not the door, and watch for "
          "a threshold strip that eats the height.</p>"),
         ("How much is 500 kg in barrow loads?",
          "<p>A builder's barrow holds roughly 40 kg of wet spoil before it becomes unmanageable, so "
          "one load here is about twelve barrow runs. On a 20 metre path that is the difference "
          "between an afternoon and a morning.</p>"),
         ("Petrol or diesel?",
          "<p>Petrol, deliberately. At this size a diesel adds around 25 kg and roughly £400 to the "
          "price for capability you cannot use. Petrol also starts on a recoil after a month "
          "standing, which a small diesel often will not.</p>"),
         ("Can it climb a slope with a full load?",
          "<p>Rated to 25 degrees laden. That is a steep garden, not a bank. Take slopes straight up "
          "or straight down and never across — a tracked machine tips sideways with very little "
          "warning once the load shifts.</p>"),
         ("What does a replacement track cost?",
          "<p>£185 a track from our UK stock, dispatched within 48 hours. A spare is not supplied "
          "with this machine; most owners buy one after the first season.</p>")],
)

LS22 = dict(
    slug="ls22-log-splitter", url="ls22-log-splitter.html", dir="assets/img/ls22-splitter",
    sku="XX-LS22", name="LS22 22 Tonne Petrol Log Splitter", short="LS22",
    short_desc="22 tonne towable petrol splitter with a 14 second cycle — a winter of firewood "
               "in a weekend.",
    lede="A horizontal-beam splitter with 22 tonnes of force, a 15 hp petrol engine and its own "
         "road chassis. Takes a 650 mm round up to 400 mm across, resets in fourteen seconds, and "
         "tows to the woodpile behind a vehicle instead of waiting for one to be brought to it.",
    tag="22 tonne force", price=2199, was=2749, finance=52,
    stockline="In stock — ships crated from our UK warehouse",
    meta_desc="%BRAND% LS22 22 tonne petrol log splitter: 15 hp petrol, 14 second cycle, "
              "650 mm log length, towable chassis. Free UK mainland delivery.",
    images=[("01-hero.svg", "LS22 log splitter, full machine on a studio background"),
            ("02-side.svg", "LS22 side profile showing the beam and towing chassis"),
            ("03-wedge.svg", "Splitting wedge, log cradle and push plate at the working end"),
            ("04-engine.svg", "Engine and hydraulic pack: 15 hp petrol driving a two-stage pump"),
            ("05-controls.svg", "Valve lever, cradle wings and the towing hitch"),
            ("06-dimensions.svg", "Dimensioned drawing: 650 mm log length, 2.45 m towing length"),
            ("07-in-use.svg", "LS22 splitting seasoned rounds beside a log store"),
            ("08-included.svg", "Everything supplied in the crate with the LS22")],
    bullets=["22 tonnes of force — knotted elm and wet oak, not just clean softwood",
             "14 second cycle: split, return, reload, without waiting on the ram",
             "Takes a 650 mm log up to 400 mm across",
             "15 hp petrol with a two-stage pump — fast approach, slow power stroke",
             "Horizontal beam at working height; you roll the round on, not lift it",
             "Road chassis with a hitch, so it tows to the woodpile",
             "Two-year parts warranty and UK-held spares"],
    spec_hi=[("Splitting force", "22 tonnes"), ("Cycle time", "14 seconds"),
             ("Log length", "650 mm"), ("Engine", "15 hp petrol")],
    specs=[("Model", "%BRAND% LS22"), ("Splitting force", "22 tonnes"),
           ("Cycle time (out and back)", "14 seconds"),
           ("Maximum log length", "650 mm"), ("Maximum log diameter", "400 mm"),
           ("Engine", "Single-cylinder OHV petrol"), ("Rated power", "15 hp (11 kW)"),
           ("Starting", "Recoil"), ("Fuel capacity", "6.5 litres"),
           ("Pump", "Two-stage gear pump"), ("Hydraulic reservoir", "26 litres"),
           ("Beam", "Horizontal, welded box section"),
           ("Wedge", "Hardened two-way wedge, 4-way head available separately"),
           ("Control", "Two-hand lever with automatic return"),
           ("Chassis", "Single-axle towable with 50 mm ball hitch and jockey leg"),
           ("Working height", "0.80 m"), ("Overall length (towing)", "2.45 m"),
           ("Overall width", "0.95 m"), ("Weight", "285 kg"),
           ("Noise level", "102 dB(A) at operator position"),
           ("Warranty", "2 years parts, 1 year engine (manufacturer-backed)")],
    features_h2="Why 22 tonnes is the size that finishes the job",
    features=[("22 tonnes, not 8", "A domestic 8 tonne electric splitter handles clean, straight, "
               "dry softwood. Twenty-two tonnes takes what is actually in a UK log pile: knotted "
               "elm, forked ash and wet oak."),
              ("Two-stage pump", "The ram runs out fast on no load and drops into low gear only when "
               "it meets the wood. That is where the 14 second cycle comes from."),
              ("Horizontal beam", "You roll a heavy round onto the beam instead of lifting it to "
               "a vertical wedge. Over a day, that is the difference your back notices."),
              ("Cradle wings", "Hold the halves on the beam instead of dropping them on the ground, "
               "so a re-split is one lever pull rather than a bend and a lift."),
              ("Towable", "Its own road chassis and a ball hitch. The splitter goes to the timber, "
               "which is the only sensible direction for a tonne of wood to not travel."),
              ("Two-hand control", "Both hands are on levers while the wedge moves, which is the only "
               "reliable way to keep them out of the way of it.")],
    faq=[("Is it legal to tow on the road?",
          "<p>The chassis is fitted with a 50 mm ball coupling and a jockey wheel for site and yard "
          "movement. For use on a public road a trailer must also carry lighting, indicators and a "
          "number plate board — a lighting board is not supplied. Most owners move it on a trailer "
          "or within private ground.</p>"),
         ("What size timber will 22 tonnes actually split?",
          "<p>650 mm long by 400 mm across is the physical capacity of the beam. Force is rarely the "
          "limit below that; a round that stalls the ram is usually forked or frozen rather than "
          "simply large. Ring it shorter and it will go.</p>"),
         ("Can I fit a four-way wedge?",
          "<p>Yes. A bolt-on four-way head is available separately. It quarters clean straight rounds "
          "in one stroke, but it needs more force per pass, so knotted timber is still better done "
          "two-way.</p>"),
         ("What maintenance does it need?",
          "<p>Check the hydraulic level before each session, change the oil and filter after the "
          "first 50 hours and annually after that, and keep the beam greased and clean. The wedge "
          "is hardened and does not need sharpening.</p>"),
         ("Is it safe to run on my own?",
          "<p>It is designed for single-operator use — that is what the two-hand control enforces. "
          "Never ask someone to steady a log while you operate the lever, and never override the "
          "control to run it one-handed.</p>")],
)

FM150 = dict(
    slug="fm150-flail-mower", url="fm150-flail-mower.html", dir="assets/img/fm150-flail",
    sku="XX-FM150", name="FM150 15 hp ATV Flail Mower", short="FM150",
    short_desc="1200 mm towed flail with its own 15 hp engine — takes brambles and saplings, "
               "not just grass.",
    lede="A trailed flail mower with its own 15 hp petrol engine, so it cuts at full power behind "
         "any ATV, UTV or compact tractor regardless of what that machine can put out. Forty "
         "hammer flails take a paddock, a verge or two years of neglect down in one pass.",
    tag="1200 mm cut", price=2599, was=3199, finance=61,
    stockline="In stock — ships crated from our UK warehouse",
    meta_desc="%BRAND% FM150 ATV flail mower: 15 hp petrol, 1200 mm cut, 40 hammer flails, "
              "electric start, tows behind an ATV or UTV. Free UK mainland delivery.",
    images=[("01-hero.svg", "FM150 ATV flail mower, full machine on a studio background"),
            ("02-side.svg", "FM150 side profile showing the drawbar and deck"),
            ("03-rotor.svg", "Cutaway of the flail rotor and hammer blades inside the housing"),
            ("04-engine.svg", "Engine detail: 15 hp petrol with electric start"),
            ("05-hitch.svg", "Drawbar, pin hitch and the rear height-setting roller"),
            ("06-dimensions.svg", "Dimensioned drawing: 1200 mm cutting width"),
            ("07-in-use.svg", "FM150 cutting a neglected paddock behind an ATV"),
            ("08-included.svg", "Everything supplied in the crate with the FM150")],
    bullets=["1200 mm cut in one pass — a paddock in an afternoon, not a weekend",
             "Its own 15 hp engine: full rotor speed behind any ATV, UTV or compact tractor",
             "40 hammer flails take brambles, nettles and saplings up to 25 mm",
             "Cutting height 25–100 mm, set on the rear roller without tools",
             "Electric start with a key — no wrestling a recoil in a wet field",
             "Flails mulch and drop, so there is nothing left to rake or bale",
             "Two-year parts warranty and UK-held spares"],
    spec_hi=[("Cutting width", "1200 mm"), ("Engine", "15 hp petrol"),
             ("Flails", "40 hammer blades"), ("Cut height", "25–100 mm")],
    specs=[("Model", "%BRAND% FM150"), ("Cutting width", "1200 mm"),
           ("Cutting height", "25–100 mm, adjustable on the rear roller"),
           ("Rotor", "Balanced flail rotor, 40 swinging hammer blades"),
           ("Maximum material", "Grass, brambles, nettles and saplings to 25 mm"),
           ("Engine", "Single-cylinder OHV petrol"), ("Rated power", "15 hp (11 kW)"),
           ("Starting", "Electric, 12 V, with recoil back-up"),
           ("Fuel capacity", "6.5 litres"), ("Drive", "Belt to the rotor, guarded"),
           ("Hitch", "Pin hitch drawbar for ATV, UTV or compact tractor"),
           ("Wheels", "Two flotation wheels plus a full-width rear roller"),
           ("Discharge", "Rear, mulched under the deck"),
           ("Overall width", "1.42 m"), ("Overall length with drawbar", "1.98 m"),
           ("Weight", "245 kg"), ("Noise level", "100 dB(A) at operator position"),
           ("Warranty", "2 years parts, 1 year engine (manufacturer-backed)")],
    features_h2="Why a flail beats a topper on rough ground",
    features=[("Its own engine", "A towed flail with no engine of its own runs off the tow vehicle "
               "and is only ever as good as it. Fifteen horsepower on the deck means the rotor holds "
               "speed in heavy growth behind a quad that could not drive it."),
              ("Hammer flails, not blades", "A hammer swings back when it hits a stone or a post "
               "instead of bending a spindle. On rough ground that is the difference between a "
               "season and a repair bill."),
              ("Mulches as it cuts", "The material is cut repeatedly under the deck and dropped "
               "fine. Nothing to rake, nothing to bale, nothing to burn."),
              ("Roller height setting", "The rear roller carries the deck and sets the cut. Move a "
               "pin, not a spanner, and the height stays put over rough ground."),
              ("Cuts wider than the quad", "1200 mm covers the wheel tracks and more, so a paddock "
               "goes down in fewer passes and without a strip left standing between them."),
              ("Electric start", "A 15 hp single is unpleasant to start on a recoil in a wet field. "
               "The key start is the feature you will use twenty times a day.")],
    faq=[("What will actually tow it?",
          "<p>Anything with a pin hitch and enough grip: a 350cc-plus ATV, a UTV or a compact "
          "tractor. Because the mower has its own engine, the tow vehicle only has to pull 245 kg — "
          "it does not have to drive the rotor.</p>"),
         ("Will it cut brambles and saplings?",
          "<p>Brambles, nettles, docks and soft saplings to about 25 mm, yes. Beyond that you are "
          "into scrub-cutter territory, and hitting a 50 mm stem at rotor speed damages the machine "
          "rather than the tree.</p>"),
         ("How is it different from a topper?",
          "<p>A topper swings two or three long blades and leaves the material in rows. A flail cuts "
          "with forty small hammers and mulches it fine. The flail is slower per acre and far better "
          "on anything that is not a clean grass sward.</p>"),
         ("Can I use it on a lawn?",
          "<p>It will cut a lawn but it is not a finishing mower — expect a rough, mulched finish "
          "rather than stripes. It is built for paddocks, verges, orchards and land that has been "
          "left too long.</p>"),
         ("How often do the flails need replacing?",
          "<p>Hammers are reversible and typically last a season or two of paddock work. A full "
          "replacement set of forty is £148 from our UK stock. Always replace opposing pairs or the "
          "rotor goes out of balance.</p>")],
)

COMPACT = [EX10, TD500, LS22, FM150]
