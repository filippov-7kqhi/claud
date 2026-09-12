# -*- coding: utf-8 -*-
"""GroundMaxx -- groundmax.shop. Products come from products.py (GroundMaxx
   sells the cat_us.py four, wired up via CATALOGUE["groundmax"]/
   OVERRIDES["groundmax"]); this file is the store's identity and copy only.

   country="US" switches build_site.py to USD pricing, US structured data and
   US-appropriate legal copy (see REGION/PHRASES in tools/build_site.py) -- the
   four UK stores are untouched by that switch, since they default to "GB".

   The sites/ directory this store builds into is "groundmax" (from the
   domain, groundmax.shop), one letter short of the brand name GroundMaxx --
   deliberate, the owner's domain choice, not a typo. See tools/products.py
   for the matching "groundmax" keys in CATALOGUE/OVERRIDES.
"""

LOGO = ('<svg class="logo__mark" viewBox="0 0 32 32" fill="none" aria-hidden="true">'
        '<path d="M3 16h9" stroke="#eab308" stroke-width="2.8" stroke-linecap="round"/>'
        '<circle cx="20" cy="16" r="7.5" stroke="#e7e9ec" stroke-width="2.4"/>'
        '<path d="M20 6.5v3M20 22.5v3M9.5 16h3M27.5 16h3" stroke="#eab308" stroke-width="2.4" '
        'stroke-linecap="round"/></svg>')

CFG = dict(
    brand="GroundMaxx", brand_a="Ground", brand_b="Maxx", domain="groundmax.shop",
    country="US",
    theme="#101114", logomark=LOGO,
    favicon="%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%23101114'/%3E%3Ccircle cx='18' cy='16' r='7' stroke='%23eab308' stroke-width='2.6'/%3E%3Cpath d='M4 16h8M18 7v2M18 23v2M9 16h2M27 16h2' stroke='%23eab308' stroke-width='2.4' stroke-linecap='round'/%3E%3C/svg%3E",
    title="GroundMaxx — 3-Point Tractor Implements: Ditch Bank Mower, Flail Mower, Post Hole "
          "Digger & Rotary Cutter",
    desc="Heavy-duty 3-point PTO implements for tractors: a hydraulic offset ditch bank flail "
         "mower, a 53-inch flail mower, a post hole digger and a 6 ft. rotary cutter. Nationwide "
         "freight shipping.",
    hero_eyebrow="Ground-engaging implements, built to run",
    hero_h1="Clear it. Bore it.<br>Knock it back &mdash; with "
             "<span style='color:var(--brand)'>PTO power you already have</span>.",
    hero_lead="Four 3-point implements sized for real ground work: a hydraulic offset flail mower "
              "that swings out for ditch banks and shoulders, a 53-inch flail mower, a post hole "
              "digger and a 6-foot round-back rotary cutter. All PTO driven, all shipped freight "
              "nationwide.",
    hero_pills=["&#10003; In US stock now", "&#10003; Nationwide freight shipping",
                "&#10003; 2-year parts warranty", "&#10003; Financing available"],
    range_h2="Four implements. One tractor. No dealer lot.",
    range_lead="Knock back the brush, bore the post holes, mow the acreage and clear the ditch "
               "line -- one 3-point hitch, four jobs done.",
    why_h2="Skip the dealer markup on a bolt-on implement.",
    why_lead="Plain buying: US stock, confirmed specs, and a warranty you can read before you "
             "order -- not after.",
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
    about_h1="Four implements for ground work, and we know exactly what's confirmed",
    about_desc="GroundMaxx is a US supplier of heavy-duty 3-point tractor implements.",
    about_paras=[
        "GroundMaxx started because buying a 3-point implement online too often means a stock "
        "photo, a vague spec sheet, and no straight answer when something does not fit your "
        "tractor.",
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
    footer_blurb="US supplier of heavy-duty 3-point tractor implements: a hydraulic offset flail "
                 "ditch bank mower, a 53-inch flail mower, a post hole digger and a 6 ft. rotary "
                 "cutter. Specs quoted only where we can stand behind them.",

    fonts="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;600;700;800&display=swap",
    email="contact@groundmax.shop", support_email="contact@groundmax.shop",
    phone="", phone_link="", ref_prefix="GM",
    # Real trading address supplied by the owner; the legal entity name has not
    # been registered/decided yet, so that field is left as an explicit TODO
    # rather than inventing a company name. Phone is likewise left blank until
    # the owner has one to publish.
    company="[Legal entity name — TBD]",
    company_no="",
    street="5602 S Hermitage Ave", city="Chicago", state="IL", postcode="60636",
    return_fee=250,
    topbar=["&#128666; Free nationwide freight shipping", "&#8634; 30-day returns",
            "&#128737; 2-year warranty", "&#9993; contact@groundmax.shop"],
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
