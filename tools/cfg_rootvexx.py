# -*- coding: utf-8 -*-
"""RootVexx — rootvexx.shop. Products come from products.BASE; this file is the
   store's identity and copy only."""

LOGO = ('<svg class="logo__mark" viewBox="0 0 32 32" fill="none" aria-hidden="true">'
        '<path d="M4 9h24" stroke="#c2410c" stroke-width="2.8" stroke-linecap="round"/>'
        '<path d="M16 9v18" stroke="#c2410c" stroke-width="2.8" stroke-linecap="round"/>'
        '<path d="M16 15c-4 0-6 3-6 7M16 15c4 0 6 3 6 7" stroke="#ea580c" stroke-width="2.3" '
        'stroke-linecap="round"/>'
        '<path d="M16 3v6" stroke="#7c2d12" stroke-width="2.8" stroke-linecap="round"/></svg>')

CFG = dict(
    brand="RootVexx", brand_a="Root", brand_b="Vexx", domain="rootvexx.shop",
    theme="#f5f3f0", logomark=LOGO,
    favicon="%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%23c2410c'/%3E%3Cpath d='M6 11h20M16 11v15M16 16c-4 0-5 3-5 6M16 16c4 0 5 3 5 6' stroke='%23ffffff' stroke-width='2.4' stroke-linecap='round'/%3E%3C/svg%3E",
    title="RootVexx — Mini Excavators, Dumpers, Splitters & Flails, Free UK Delivery",
    desc="Mini excavators, tracked mini dumpers, petrol log splitters and ATV flail mowers for UK "
         "groundworkers, landscapers and smallholders. Free mainland delivery, 30-day returns, "
         "2-year warranty.",
    hero_eyebrow="Compact plant for UK ground crews",
    hero_h1="Dig it. Move it.<br>Without the <span style='color:var(--brand)'>hire desk</span>.",
    hero_lead="Four machines picked because they finish a groundwork job on their own: a 1 tonne mini "
              "excavator that retracts to 930 mm, a 500 kg tracked dumper that fits a doorway, a "
              "22 tonne towable log splitter and a 1200 mm ATV flail mower with its own engine. All "
              "four in UK stock, all four delivered free to the mainland, all four trailerable.",
    hero_pills=["&#10003; In UK stock now", "&#10003; Free mainland delivery",
                "&#10003; 2-year parts warranty", "&#10003; Finance from £52/mo"],
    range_h2="Four machines. Nothing that sits idle.",
    range_lead="Dig the trench, barrow the spoil out, split what came off the site and cut back what "
               "grew over it. Four machines that cover a whole job instead of one stage of it.",
    why_h2="A digger is £140 a day to hire. This one stops that.",
    why_lead="Straightforward buying: UK stock, UK spares, honest weights and no dealer forecourt margin.",
    why=[("&#128230;", "Shipped from UK stock", "Crated in our UK warehouse, not on a boat. Order by "
          "2pm and it leaves within two working days."),
         ("&#9878;", "Honest weights", "Every weight on this site is the operating figure that matters "
          "for trailer law — not a dry weight that leaves out fuel, bucket and tracks."),
         ("&#128736;", "Spares held here", "Tracks, flails, belts, filters and hoses ship from our own "
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
             "access through with someone who has walked a digger down a terrace path before.",
    about_h1="Four machines for groundwork, and we know all of them properly",
    about_desc="RootVexx is a UK equipment supplier stocking compact excavators and groundcare plant.",
    about_paras=[
        "RootVexx started because buying compact plant in the UK was needlessly hard. The choice was "
        "a main dealer charging showroom prices, or an import listing with a photograph, no weights "
        "that meant anything, and no answer when a hose failed.",
        "So we do the opposite. We stock four machines — a 1 tonne excavator, a 500 kg tracked dumper, "
        "a 22 tonne log splitter and an ATV flail mower — hold them in one warehouse, and keep the "
        "wear parts for all four on our own shelves. A short range means we can tell you the real "
        "operating weight, the real retracted width and the real cost of a set of flails, without "
        "checking a catalogue.",
        "We are not a manufacturer and we do not pretend to be. We specify the machines, inspect every "
        "one before it ships, and stand behind them for two years. If a fifth machine ever earns a "
        "place here, it will be because it pays for itself as clearly as these four do."],
    about_tiles=[("Stock, not drop-ship", "Machines sit in our own UK warehouse. When the site says in "
                  "stock, there is one on the floor with a serial number."),
                 ("Inspected before it ships", "Fluids, fasteners, track tension and a running test on "
                  "every unit. The signed sheet travels in the crate with the machine."),
                 ("Parts on the shelf", "Rubber tracks, flails, belts, filters and hoses held in the "
                  "UK and dispatched within 48 hours of your call.")],
    footer_blurb="UK supplier of mini excavators, tracked mini dumpers, log splitters and ATV flail "
                 "mowers. Machines held in stock, spares held in stock, weights quoted honestly.",

    fonts="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;700;800&family=Inter:wght@400;600;700;800&display=swap",
    email="sales@rootvexx.shop", support_email="support@rootvexx.shop",
    phone="+44 7858 117670", phone_link="+447858117670", ref_prefix="RV",
    company="RootVexx Ltd",
    company_no="", vat_no="",
    street="Conway Rd", city="Conwy", postcode="LL32 7TE",
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
