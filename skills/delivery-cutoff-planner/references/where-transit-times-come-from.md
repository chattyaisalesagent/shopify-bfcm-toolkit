# Where `transit_days` comes from, and why the skill never supplies it

Verified against Shopify's own documentation, checked 21 September 2026.

## The platform does not give you a defensible number for free

**Automated delivery dates** predict from the store's own fulfilment history, but they render only when the prediction falls within 5 days (US) or 4 days (EU), and only when origin and destination sit in the same region. A merchant asking this skill for help is usually asking precisely because their situation falls outside that window: a longer-transit zone, a cross-region shipment, or a season where history from a quiet month does not represent December.

**Manual delivery dates** are a single global setting with a hard, non-configurable noon origin-local cutoff. It cannot express a per-zone number at all, which is the entire reason a merchant needs this skill instead of the built-in setting.

**Shop Promise** renders a real countdown, but it is US-domestic only, invite-assessed, and Shopify describes eligibility as the top 1% of shippers. Most merchants using this skill are not eligible.

**Shopify's own published carrier-deadline guidance goes stale.** The post at shopify.com/blog/holiday-shipping-deadlines was still the December 2025 edition when checked on 21 September 2026, nine months out of date. Never treat a cached copy of that post, or any other, as current-year truth. If the merchant points to it, ask them to confirm the dates against their actual carrier for this year.

**The API that carries real cutoff times and timezones, the Delivery Promise API, is restricted to approved delivery-promise partners.** It is not available to an ordinary merchant or to this skill.

## What this means for the skill

`transit_days` has to come from one of:

1. The merchant's own account rep or dashboard at their carrier, for this year.
2. A carrier's published current-year holiday shipping deadlines page, dated and named.
3. The merchant's own experience from last year, stated as their own estimate, with the buffer increased to cover the uncertainty.

**Never accept a number the skill itself recalls from training or from a general sense of "ground shipping takes about 5 days".** Carrier transit times change year to year and region to region, and an invented number here produces the single most damaging kind of wrong answer this skill can give: a published cutoff date that is wrong in the direction of promising too much time.

If the merchant does not have a transit time for a zone, say so plainly and mark it `[DECISION NEEDED: confirm carrier transit time for <zone>]` rather than filling in a plausible-sounding default. This is the same discipline as `campaign-rules-policy-qa`, applied to a fact rather than a commercial decision: an unverified number is not a small gap, it is the input the entire calculation depends on.
