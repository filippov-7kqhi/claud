# -*- coding: utf-8 -*-
"""RootVexx — rootvexx.shop. Products come from products.BASE; this file is the
   store's identity and copy only."""

LOGO = ('<svg class="logo__mark" viewBox="0 0 32 32" fill="none" aria-hidden="true">'
        '<path d="M4 7h24v6a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z" fill="#991b1b" stroke="#ef4444" stroke-width="1.6"/>'
        '<path d="M16 18v10M16 22l-5 5M16 22l5 5M11 12h10" stroke="#ef4444" stroke-width="1.8" '
        'stroke-linecap="round"/></svg>')

CFG = dict(
    brand="RootVexx", brand_a="Root", brand_b="Vexx", domain="rootvexx.shop",
    theme="#0f0b0c", logomark=LOGO,
    favicon="%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%23991b1b'/%3E%3Cpath d='M16 5v22M16 15l-6 7M16 15l6 7M9 9h14' stroke='%23ef4444' stroke-width='2.4' stroke-linecap='round'/%3E%3C/svg%3E",
    title="RootVexx — Stump Grinders, Chippers & Compact Plant, Free UK Delivery",
    desc="Stump grinders, wood chippers, tracked dumpers and compact loaders for UK tree surgeons, "
         "landscapers and groundworkers. Free mainland delivery, 30-day returns, 2-year warranty.",
    hero_eyebrow="Clearance machinery for UK ground crews",
    hero_h1="Take the stump out.<br>Not the <span style='color:var(--brand)'>whole day</span>.",
    hero_lead="Four machines picked for clearance work: a tracked stump grinder that fits a side gate, "
              "a road-towable 6″ diesel chipper, a 1-tonne high-tip dumper that fits a doorway and a "
              "stand-on loader that runs standard skid-steer attachments. All four in UK stock, all "
              "four delivered free to the mainland, all four movable on a car trailer.",
    hero_pills=["&#10003; In UK stock now", "&#10003; Free mainland delivery",
                "&#10003; 2-year parts warranty", "&#10003; Finance from £68/mo"],
    range_h2="Four machines. Nothing that sits idle.",
    range_lead="Grind it out, chip what is left, barrow the spoil off and load the muck away. Four "
               "machines that cover the whole clearance job instead of one stage of it.",
    why_h2="A grinder is £160 a day to hire. This one stops that.",
    why_lead="Straightforward buying: UK stock, UK spares, honest weights and no dealer forecourt margin.",
    why=[("&#128230;", "Shipped from UK stock", "Crated in our UK warehouse, not on a boat. Order by "
          "2pm and it leaves within two working days."),
         ("&#9878;", "Honest weights", "Every weight on this site is the gross figure that matters for "
          "towing law — not a dry weight that leaves out fuel and the chassis."),
         ("&#128736;", "Spares held here", "Teeth, blades, belts, tracks and filters ship from our own "
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
         ("Can I see one before I buy?", "<p>We are a warehouse operation, not a showroom, so there is "
          "no forecourt to walk around. That is part of why the price is what it is. The 30-day return "
          "window is there so the machine can prove itself on your own site instead.</p>"),
         ("What happens if it arrives damaged?",
          "<p>Inspect before you sign and note any damage on the carrier's paperwork — that note is "
          "what makes a claim straightforward. Photograph it, email us the same day and we arrange "
          "collection and a replacement at our cost.</p>"),
         ("Do you take trade accounts?", "<p>Yes. Email sales with your company details and we will "
          "set up 30-day terms subject to a credit check.</p>")],
    cta_h2="Stop hiring. Start owning.",
    cta_lead="All four machines are in stock and shipping this week. Reserve one now, or talk the "
             "access through with someone who has ground a stump out of a back garden before.",
    about_h1="Four machines for clearance work, and we know all of them properly",
    about_desc="RootVexx is a UK equipment supplier stocking clearance and groundcare machinery.",
    about_paras=[
        "RootVexx started because buying clearance plant in the UK was needlessly hard. The choice was "
        "a main dealer charging showroom prices, or an import listing with a photograph, no weights "
        "that meant anything, and no answer when a belt failed.",
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
                 ("Parts on the shelf", "Teeth, blades, belts, filters and rollers held in the UK and "
                  "dispatched within 48 hours of your call.")],
    footer_blurb="UK supplier of stump grinders, wood chippers, tracked dumpers and compact loaders. "
                 "Machines held in stock, spares held in stock, and weights quoted honestly.",

    fonts="https://fonts.googleapis.com/css2?family=Archivo+Narrow:wght@600;700&family=Inter:wght@400;600;700;800&display=swap",
    email="sales@rootvexx.shop", support_email="support@rootvexx.shop",
    phone="+44 7858 117670", phone_link="+447858117670", ref_prefix="RV",
    company="RootVexx Ltd",
    company_no="", vat_no="",
    street="7TE, Conway Rd", city="Conwy, Colwyn Bay", postcode="",
    return_fee=150,
    topbar=["&#128666; Free UK mainland delivery", "&#8634; 30-day returns",
            "&#128737; 2-year warranty", "&#9993; sales@rootvexx.shop"],
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
