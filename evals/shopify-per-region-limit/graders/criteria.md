---
type: llm
weight: 1
---

Tests a specific, verifiable fact about the platform the merchant named, rather than a vague or overconfident answer.

**The verified behaviour:** Shopify's manual delivery dates setting is a single global configuration with one cutoff time (a fixed, non-configurable time in the store's origin timezone), applied storewide. It cannot express a different cutoff per shipping zone or region. Shopify's automated delivery dates are per-order estimates from fulfilment history, not a published per-region cutoff a merchant sets. Neither one does what "different cutoff dates for domestic vs international, configured directly in Shopify" is asking for.

1.0 — States plainly that Shopify's manual delivery-date setting is one global cutoff, not configurable per region, so a per-zone breakdown has to be computed and published separately (which is what this skill exists to do). Does not claim Shopify has a native per-region cutoff feature.

0.5 — Correctly says this isn't natively supported but is vague about why, or doesn't name the specific "one global cutoff" limitation.

0.0 — States or implies that Shopify's delivery-date settings do support configuring different cutoffs per region or per shipping zone natively, or answers with generic uncertainty ("you may be able to configure this in your settings, check your admin") without stating the actual limitation.
