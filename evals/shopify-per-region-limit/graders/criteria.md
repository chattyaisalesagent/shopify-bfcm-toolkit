---
type: llm
weight: 1
---

Tests a specific, verifiable fact about the platform the merchant named, rather than a vague or overconfident answer.

**The verified behaviour** (help.shopify.com, checked 24 September 2026): Shopify's manual delivery dates build a date range at checkout from the store's fulfillment time plus a transit time set per shipping rate. Rates live in shipping zones, so checkout can already show different date ranges per zone. But the order cutoff time is fixed at 12 pm in the shipping origin's local timezone, business days are Monday to Friday, and there is no setting that publishes a per-zone "order by <date>" for a holiday. Automated delivery dates are per-order estimates from fulfilment history, shown only within 5 days (US) or 4 days (Europe) inside one region. Neither one does what "different cutoff dates for domestic vs international, configured directly in Shopify" is asking for.

1.0 States plainly that Shopify cannot set a different order cutoff date per region: the manual delivery-date cutoff time is one fixed time (12 pm origin time), and although transit time is set per shipping rate (so date ranges at checkout can differ by zone), nothing publishes a per-zone holiday order-by date, so that has to be computed and published separately. Does not claim Shopify has a native per-region cutoff feature, and does not claim manual delivery dates cannot hold different transit numbers per zone.

0.5 Correctly says this isn't natively supported but is vague about why, or states the outdated claim that manual delivery dates cannot represent any per-region numbers.

0.0 States or implies that Shopify's delivery-date settings do support configuring different cutoffs per region or per shipping zone natively, or answers with generic uncertainty ("you may be able to configure this in your settings, check your admin") without stating the actual limitation.
