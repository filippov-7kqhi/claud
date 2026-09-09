# -*- coding: utf-8 -*-
"""LawnStride — lawnstride.shop. Products come from products.BASE; this file is
   the store's identity and copy only."""

LOGO = ('<svg class="logo__mark" viewBox="0 0 32 32" fill="none" aria-hidden="true">'
        '<path d="M3 26h26" stroke="#2dd4bf" stroke-width="2.2" stroke-linecap="round"/>'
        '<path d="M9 26c0-8 3-13 7-16" stroke="#2dd4bf" stroke-width="2" stroke-linecap="round"/>'
        '<path d="M16 26c0-6 4-10 9-12" stroke="#2dd4bf" stroke-width="2" stroke-linecap="round"/>'
        '<path d="M23 26c0-4 2-7 5-8" stroke="#0f766e" stroke-width="2" stroke-linecap="round"/></svg>')

CFG = dict(
    brand="LawnStride", brand_a="Lawn", brand_b="Stride", domain="lawnstride.shop",
    theme="#081311", logomark=LOGO,
    favicon="%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%230f766e'/%3E%3Cpath d='M5 25h22' stroke='%232dd4bf' stroke-width='2.6' stroke-linecap='round'/%3E%3Cpath d='M10 25c0-7 3-11 7-14M17 25c0-5 4-9 8-11' stroke='%232dd4bf' stroke-width='2.4' stroke-linecap='round'/%3E%3C/svg%3E",
    title="LawnStride — Groundcare & Landscaping Machinery, Free UK Delivery",
    desc="Wood chippers, stump grinders, tracked dumpers and compact loaders for UK landscapers, "
         "grounds teams and garden contractors. Free mainland delivery, 30-day returns, 2-year warranty.",
    hero_eyebrow="Groundcare plant for UK landscapers",
    hero_h1="Finish the garden.<br>Without the <span style='color:var(--brand)'>hire van</span>.",
    hero_lead="Four machines chosen for landscaping work, where access is tight and the lawn has to "
              "survive: a tracked stump grinder that clears a side gate, a road-towable 6″ diesel "
              "chipper, a 1-tonne high-tip tracked dumper that fits a doorway and a stand-on loader "
              "that runs standard skid-steer attachments. All four in UK stock, all delivered free.",
    hero_pills=["&#10003; In UK stock now", "&#10003; Free mainland delivery",
                "&#10003; 2-year parts warranty", "&#10003; Finance from £68/mo"],
    range_h2="Four machines. One garden crew.",
    range_lead="Clear the stumps, chip the brash, move the topsoil and load the muck away. Four "
               "machines that cover a whole landscaping job instead of one stage of it.",
    why_h2="A week of hire is £600. These stop that.",
    why_lead="Plain buying: UK stock, UK spares, honest weights and no dealer forecourt margin.",
    why=[("&#128230;", "Shipped from UK stock", "Crated in our UK warehouse, not on a boat. Order by "
          "2pm and it leaves within two working days."),
         ("&#9878;", "Honest weights", "Every weight on this site is the gross figure that matters for "
          "towing law — not a dry weight that leaves out fuel and the chassis."),
         ("&#128736;", "Spares held here", "Tracks, teeth, blades, belts and filters ship from our own "
          "shelves in 48 hours. A machine you cannot get parts for is a liability."),
         ("&#128176;", "Finance available", "Spread it over 48 months with a UK asset-finance provider. "
          "Subject to status; we introduce, we do not lend.")],
    steps=[("Choose and reserve", "Pick the machine and reserve it. We confirm stock and delivery in "
            "writing before you pay anything."),
           ("Pre-delivery check", "Fluids, fasteners, track tension and a full running test on our "
            "floor. We record it and send you the sheet."),
           ("Booked in with you", "Tail-lift vehicle to UK mainland. The carrier calls you to agree a "
            "slot — no all-day waiting."),
           ("First job", "Manual, PPE and starter spares are in the crate. Call us if anything is "
            "unclear before you start.")],
    faq=[("Are these machines new?", "<p>Yes — every machine ships new and unregistered, with a full "
          "pre-delivery inspection and the inspection sheet in the crate.</p>"),
         ("Do you deliver to Scotland, Northern Ireland or the islands?",
          "<p>Free delivery covers the UK mainland including mainland Scotland. Northern Ireland, the "
          "Highlands and Islands, the Isle of Man and the Channel Islands are quoted individually — "
          "ask before you order and we will price it exactly.</p>"),
         ("Will these damage a finished lawn?",
          "<p>The grinder and the dumper both run on rubber tracks, which spread the load far better "
          "than wheels. On soft or newly laid ground you should still board out a route — low ground "
          "pressure reduces marking, it does not remove it.</p>"),
         ("What happens if it arrives damaged?",
          "<p>Inspect before you sign and note any damage on the carrier's paperwork — that note is "
          "what makes a claim straightforward. Photograph it, email us the same day and we arrange "
          "collection and a replacement at our cost.</p>"),
         ("Do you take trade accounts?", "<p>Yes. Email sales with your company details and we will "
          "set up 30-day terms subject to a credit check.</p>")],
    cta_h2="Stop hiring. Start owning.",
    cta_lead="All four machines are in stock and shipping this week. Reserve one now, or talk the "
             "access through with someone who has worked a machine down a terrace path before.",
    about_h1="Four machines for landscaping, and we know all of them properly",
    about_desc="LawnStride is a UK equipment supplier stocking groundcare and landscaping machinery.",
    about_paras=[
        "LawnStride started because buying groundcare plant in the UK was needlessly hard. The choice "
        "was a main dealer charging showroom prices, or an import listing with a photograph, no "
        "weights that meant anything, and no answer when a belt failed.",
        "So we do the opposite. We stock four machines — a stump grinder, a diesel chipper, a tracked "
        "dumper and a compact loader — hold them in one warehouse, and keep the wear parts for all "
        "four on our own shelves. A short range means we can tell you the real gross weight, the real "
        "gate clearance and the real cost of a set of teeth, without checking a catalogue.",
        "We are not a manufacturer and we do not pretend to be. We specify the machines, inspect every "
        "one before it ships, and stand behind them for two years. If a fifth machine ever earns a "
        "place here, it will be because it pays for itself as clearly as these four do."],
    about_tiles=[("Stock, not drop-ship", "Machines sit in our own UK warehouse. When the site says in "
                  "stock, there is one on the floor with a serial number."),
                 ("Inspected before it ships", "Fluids, fasteners, track tension and a running test on "
                  "every unit. The signed sheet travels in the crate with the machine."),
                 ("Parts on the shelf", "Tracks, teeth, blades, belts and filters held in the UK and "
                  "dispatched within 48 hours of your call.")],
    footer_blurb="UK supplier of wood chippers, stump grinders, tracked dumpers and compact loaders. "
                 "Machines held in stock, spares held in stock, and weights quoted honestly.",

    fonts="https://fonts.googleapis.com/css2?family=Saira+Condensed:wght@600;700&family=Inter:wght@400;600;700;800&display=swap",
    email="sales@lawnstride.shop", support_email="support@lawnstride.shop",
    phone="+44 7349 073003", phone_link="+447349073003", ref_prefix="LS",
    company="LawnStride Ltd",
    company_no="", vat_no="",
    street="50 Sea View Rd", city="Colwyn Bay", postcode="LL29 8DG",
    return_fee=150,
    topbar=["&#128666; Free UK mainland delivery", "&#8634; 30-day returns",
            "&#128737; 2-year warranty", "&#9993; sales@lawnstride.shop"],
    assurance=[
      ("30 days to change your mind", "Return any machine within 30 days of delivery. Faulty or "
       "mis-described machines are collected free with a full refund; a change of mind costs "
       "£150 for collection and nothing else. We charge no restocking fee, ever."),
      ("Two-year parts warranty", "Two years on parts we supply and one year on the engine through "
       "the manufacturer's UK network. The warranty starts on delivery and transfers with the machine "
       "if you sell it on."),
      ("Your statutory rights, in full", "Under the Consumer Rights Act 2015 you have a 30-day right "
       "to reject goods that are faulty or not as described. Everything we offer sits on top of that "
       "and takes nothing away from it."),
    ],
)
