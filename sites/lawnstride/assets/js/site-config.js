/* ---------------------------------------------------------------------------
   Runtime configuration for LawnStride. Edited through /admin.html, or by hand.

   THIS FILE IS PUBLIC. Everything in it ships to every visitor.
   Payment Link URLs, business details and the admin hash are all fine to publish.
   A Stripe SECRET key (sk_live_... / sk_test_...) is NOT. Never put one here.
--------------------------------------------------------------------------- */
window.SITE_CONFIG = {
  // SHA-256 of the admin passphrase. This only hides the form from a casual
  // visitor -- anyone can read this file and bypass it. Nothing behind it is
  // secret; the real gate on changing the live site is your GitHub login.
  admin: { passHash: "5b9e9741342f4f8a87a03b52634853031e9478d49220cadd57e189392e0b7bb3" },

  // Shown in the footer of every page. Google and Stripe both verify these.
  business: {
    company:   "",
    companyNo: "",
    vatNo:     "",
    street:    "",
    city:      "",
    postcode:  "",
    phone:     ""
  },

  // Data collector that feeds the admin dashboard. Without it the dashboard
  // shows nothing rather than inventing figures. See stripe/README.md.
  analyticsEndpoint: "",

  // Optional: Checkout Sessions for baskets with more than one machine.
  checkoutEndpoint: "",

  // One Stripe Payment Link per machine. Blank = that machine routes to an
  // enquiry instead of pretending to take payment.
  paymentLinks: {
    "LS-EX10": "",       // EX10 1 Tonne Mini Excavator - GBP 4,999
    "LS-TD500": "",      // TD500 500 kg Tracked Mini Dumper - GBP 2,499
    "LS-LS22": "",       // LS22 22 Tonne Petrol Log Splitter - GBP 2,199
    "LS-FM150": "",      // FM150 15 hp ATV Flail Mower - GBP 2,599
  }
};
