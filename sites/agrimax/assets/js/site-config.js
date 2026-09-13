/* ---------------------------------------------------------------------------
   Runtime configuration for AgriMaxx. Edited through /admin.html, or by hand.

   THIS FILE IS PUBLIC. Everything in it ships to every visitor.
   Payment Link URLs, business details and the admin hash are all fine to publish.
   A Stripe SECRET key (sk_live_... / sk_test_...) is NOT. Never put one here.
--------------------------------------------------------------------------- */
window.SITE_CONFIG = {
  admin: { passHash: "5b9e9741342f4f8a87a03b52634853031e9478d49220cadd57e189392e0b7bb3" },

  business: {
    company:   "",
    companyNo: "",
    vatNo:     "",
    street:    "",
    city:      "",
    state:     "",
    postcode:  "",
    phone:     ""
  },

  analyticsEndpoint: "",

  checkoutEndpoint: "",

  paymentLinks: {
    "AM-VHF71": "",      // VHF71 71″ Heavy-Duty Hydraulic Offset Flail Ditch Bank Mower - USD 7,499
    "AM-LFS53": "",      // LFS53 53″ 3-Point Flail Mower - USD 2,199
    "AM-PHD18": "",      // PHD18 3-Point Post Hole Digger - USD 349
    "AM-RC72": "",       // RC72 6 ft. Round-Back Rotary Cutter - USD 1,449
  }
};
