# -*- coding: utf-8 -*-
"""AgriMaxx -- agrimax.shop. Products come from products.py (AgriMaxx sells the
   cat_us.py four, wired up via CATALOGUE["agrimax"]/OVERRIDES["agrimax"]); this
   file is the store's identity and copy only.

   country="US" switches build_site.py to USD pricing, US structured data and
   US-appropriate legal copy (see REGION/PHRASES in tools/build_site.py) -- the
   four UK stores are untouched by that switch, since they default to "GB".

   The sites/ directory this store builds into is "agrimax" (from the domain,
   agrimax.shop), one letter short of the brand name AgriMaxx -- deliberate,
   the owner's domain choice, not a typo. See tools/products.py for the
   matching "agrimax" keys in CATALOGUE/OVERRIDES.
"""

LOGO = ('<svg class="logo__mark" viewBox="0 0 32 32" fill="none" aria-hidden="true">'
        '<path d="M16 29V6" stroke="#2f5d34" stroke-width="2.3" stroke-linecap="round"/>'
        '<ellipse cx="12.3" cy="23" rx="2.6" ry="1.35" fill="#8a4b06" transform="rotate(-40 12.3 23)"/>'
        '<ellipse cx="19.7" cy="23" rx="2.6" ry="1.35" fill="#8a4b06" transform="rotate(40 19.7 23)"/>'
        '<ellipse cx="12.7" cy="17.4" rx="2.6" ry="1.35" fill="#a35d0a" transform="rotate(-32 12.7 17.4)"/>'
        '<ellipse cx="19.3" cy="17.4" rx="2.6" ry="1.35" fill="#a35d0a" transform="rotate(32 19.3 17.4)"/>'
        '<ellipse cx="13.3" cy="12" rx="2.4" ry="1.3" fill="#c9860f" transform="rotate(-24 13.3 12)"/>'
        '<ellipse cx="18.7" cy="12" rx="2.4" ry="1.3" fill="#c9860f" transform="rotate(24 18.7 12)"/>'
        '<ellipse cx="16" cy="7" rx="1.7" ry="2.8" fill="#c9860f"/></svg>')
# A wheat ear: a stem (deep crop-green) carrying three ascending pairs of
# grain kernels that ripen from a dark harvest gold at the base to a lighter
# gold at the tip -- reads as "harvest/agricultural" rather than the abstract
# sun-and-furrow mark this replaced. See tools/theme.py for the light-theme
# palette (warm wheat-cream ground, harvest-gold brand colour) this pairs with.

CFG = dict(
    brand="AgriMaxx", brand_a="Agri", brand_b="Maxx", domain="agrimax.shop",
    country="US",
    theme="#f8f3e6", logomark=LOGO,
    favicon="%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%2392400e'/%3E%3Cpath d='M16 27V8' stroke='%23fff8ec' stroke-width='2.4' stroke-linecap='round'/%3E%3Ccircle cx='12.6' cy='22' r='2.1' fill='%23fff8ec'/%3E%3Ccircle cx='19.4' cy='22' r='2.1' fill='%23fff8ec'/%3E%3Ccircle cx='13' cy='15.5' r='1.9' fill='%23fff8ec'/%3E%3Ccircle cx='19' cy='15.5' r='1.9' fill='%23fff8ec'/%3E%3Ccircle cx='16' cy='9' r='2.2' fill='%23fff8ec'/%3E%3C/svg%3E",
    title="AgriMaxx — 3-Point Tractor Implements: Ditch Bank Mower, Flail Mower, Post Hole Digger "
          "& Rotary Cutter",
    desc="3-point PTO implements for compact and mid-size tractors: a hydraulic offset ditch bank "
         "flail mower, a 53-inch flail mower, a post hole digger and a 6 ft. rotary cutter. "
         "Nationwide freight shipping.",
    hero_eyebrow="3-point implements for real acreage",
    hero_h1="Mow it. Bore it.<br>Cut it back &mdash; with the "
             "<span style='color:var(--brand)'>tractor you already own</span>.",
    hero_lead="Four PTO implements built to bolt onto a 3-point hitch and go to work: a hydraulic "
              "offset flail mower for ditch banks and road shoulders, a 53-inch flail mower for a "
              "compact tractor, a post hole digger and a 6-foot round-back rotary cutter. Shipped "
              "freight, nationwide.",
    hero_pills=["&#10003; In US stock now", "&#10003; Nationwide freight shipping",
                "&#10003; 2-year parts warranty", "&#10003; Financing available"],
    range_h2="Four implements. No hire yard, no dealer lot.",
    range_lead="Cut the bank, mow the pasture, bore the post holes and clear the fence line -- all "
               "with equipment that hooks straight to the tractor you already have.",
    why_h2="Buy the implement. Skip the dealer markup.",
    why_lead="Straightforward buying: US stock, confirmed specs, and a warranty you can read in "
             "full before you order.",
    why=[("&#128230;", "Shipped from US stock", "Freight shipped on a pallet, not backordered from "
          "overseas. We tell you the real ship date before you pay."),
         ("&#9878;", "Figures we can stand behind", "Every spec on this site came off the machine "
          "or the manufacturer's data sheet. Where we do not have a confirmed figure yet, we say so "
          "and get it rather than guess."),
         ("&#128736;", "Parts support", "Wear parts and driveline components are sourced through "
          "the manufacturer's US parts network."),
         ("&#128176;", "Financing available", "Spread the cost with an independent equipment "
          "finance provider. Subject to approval; we introduce, we do not lend.")],
    steps=[("Choose and reserve", "Pick the implement and reserve it. We confirm stock and freight "
            "timing in writing before you pay anything."),
           ("Pre-ship check", "Fasteners, welds and moving parts checked before the machine goes on "
            "the pallet."),
           ("Freight to your door", "Nationwide freight carrier. They call to schedule a delivery "
            "window before the truck arrives."),
           ("First job", "The manual and any starter hardware ship with the machine. Call us if "
            "anything is unclear before you hook it up.")],
    faq=[("Are these implements new?", "<p>Yes -- every implement ships new, with a pre-shipment "
          "check completed before it goes on the pallet.</p>"),
         ("Do you ship to Alaska, Hawaii or outside the contiguous US?",
          "<p>Free freight shipping covers the contiguous 48 states. Alaska, Hawaii and US "
          "territories are quoted individually -- ask before you order and we will price it "
          "exactly.</p>"),
         ("Can I see one before I buy?",
          "<p>We are a freight-ship operation, not a dealer lot, which is part of why the price is "
          "what it is. The 30-day return window is there so the implement can prove itself on your "
          "own ground instead.</p>"),
         ("What happens if it arrives damaged?",
          "<p>Inspect before you sign the delivery receipt and note any damage on the carrier's "
          "paperwork -- that note is what makes a claim straightforward. Photograph it, email us "
          "the same day and we arrange a replacement.</p>"),
         ("Do you sell to businesses and farms on account?",
          "<p>Yes. Email us with your details and we will discuss terms.</p>")],
    cta_h2="Stop paying dealer markup for a bolt-on implement.",
    cta_lead="All four implements are in US stock and ship this week. Reserve one now, or ask us "
             "about fit before you order.",
    about_h1="Four implements, and we know exactly what's confirmed and what isn't",
    about_desc="AgriMaxx is a US supplier of 3-point tractor implements.",
    about_paras=[
        "AgriMaxx started because buying a 3-point implement online too often means a stock photo, "
        "a vague spec sheet, and no straight answer when something does not fit your tractor.",
        "So we do the opposite: four implements, real photographs of the actual machine, and the "
        "confirmed specs printed plainly. Where a figure has not been confirmed by the manufacturer "
        "yet, we say so rather than guess, and we get it before it becomes your problem.",
        "We are not a manufacturer and we do not pretend to be. We specify the range, check every "
        "unit before it ships, and stand behind it for two years. If a fifth implement ever earns a "
        "place here, it will be because it pays for itself as clearly as these four do."],
    about_tiles=[("Freight, not backorder", "When the site says in stock, the implement is on the "
                  "floor ready to ship -- not on a boat."),
                 ("Checked before it ships", "Fasteners, welds and moving parts checked on every "
                  "unit before it goes on the pallet."),
                 ("A warranty you can read", "Two years on parts, spelled out in full on our "
                  "returns and warranty page -- no fine print you haven't seen.")],
    about_images=[
        ("assets/img/vhf71/01-hero.jpg", "AgriMaxx VHF71 hydraulic offset ditch bank flail mower"),
        ("assets/img/lfs53/01-hero.jpg", "AgriMaxx LFS53 53-inch 3-point flail mower"),
        ("assets/img/phd18/01-hero.jpg", "AgriMaxx PHD18 3-point post hole digger"),
        ("assets/img/rc72/01-hero.jpg", "AgriMaxx RC72 6 ft. round-back rotary cutter")],
    footer_blurb="US supplier of 3-point tractor implements: a hydraulic offset flail ditch bank "
                 "mower, a 53-inch flail mower, a post hole digger and a 6 ft. rotary cutter. Specs "
                 "quoted only where we can stand behind them.",

    # Fraunces (a warm display serif, weighted 600/700/900 for headline impact)
    # paired with Inter for body copy -- a deliberate contrast in style and
    # weight, and not used by any other store in this pipeline. The previous
    # choice, Oswald, collided verbatim with HaulCrest's display face.
    fonts="https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700;900&family=Inter:wght@400;600;700;800&display=swap",
    email="contact@agrimax.shop", support_email="contact@agrimax.shop",
    phone="", phone_link="", ref_prefix="AM",
    # Real trading address supplied by the owner; the legal entity name has not
    # been registered/decided yet, so that field is left as an explicit TODO
    # rather than inventing a company name. Phone is likewise left blank until
    # the owner has one to publish.
    company="[Legal entity name — TBD]",
    company_no="",
    street="5899-5809 S Claremont Ave", city="Chicago", state="IL", postcode="60636",
    return_fee=250,
    topbar=["&#128666; Free nationwide freight shipping", "&#8634; 30-day returns",
            "&#128737; 2-year warranty", "&#9993; contact@agrimax.shop"],
    assurance=[
      ("30 days to change your mind", "Return any implement within 30 days of delivery. Faulty or "
       "mis-described implements are picked up free with a full refund; a change-of-mind return is "
       "billed at the freight carrier's actual cost, confirmed with you before we book it. We "
       "charge no restocking fee, ever."),
      ("Two-year parts warranty", "Two years on parts we supply, starting on delivery and "
       "transferring with the implement if you sell it. As a written warranty it is also subject "
       "to the federal Magnuson-Moss Warranty Act."),
      ("No license required", "There is no license required to buy or operate this equipment on "
       "your own property. Read the operator's manual and follow standard PTO and "
       "tractor-attachment safety practice."),
    ],
)
