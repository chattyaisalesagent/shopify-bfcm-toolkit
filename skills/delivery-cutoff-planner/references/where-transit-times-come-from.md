# Where `transit_days` comes from, and why the skill never supplies it

Shopify facts below checked against help.shopify.com on 24 September 2026.

## What Shopify already holds, and what it does not do

**Manual delivery dates.** Shopify builds a delivery date range at checkout from two inputs: the fulfillment time you set, and the transit time on each shipping rate. Transit time is set per shipping rate ("When you add transit time to a shipping rate, the transit time is displayed underneath the shipping rate name", help.shopify.com/en/manual/fulfillment/setup/shipping-rates/transit-time), and rates live inside shipping zones, so different zones can already carry different transit numbers. Transit time can be set only on flat rates; carrier-calculated rates include it automatically. Fulfillment time is a separate setting, not set per rate, with options from "Same business day" to custom business days. Shopify counts business days as Monday to Friday, and "The business day cutoff time is 12 pm in the local timezone of the shipping origin" (help.shopify.com/en/manual/fulfillment/setup/delivery-expectations/manual-delivery-dates).

What it does not do: it shows each shopper a date range for their own order at checkout. It does not back-solve a holiday into a published "order by" date per zone, it does not let you choose your own cutoff time or your own warehouse and carrier working days, and it does not work with rates from third-party apps. So a per-zone order-by date still has to be computed and published, which is what this skill does.

**Automated delivery dates** predict from the store's own fulfilment history, but only show when "The delivery date prediction is within 5 days for US orders, or 4 days for European orders" and origin and destination are in the same region (help.shopify.com/en/manual/fulfillment/setup/delivery-expectations/automated-delivery-dates). A per-order estimate, not a published per-zone cutoff.

**Shop Promise** needs a fulfillment location in the United States and passing shipping-performance thresholds, reassessed every 30 days; Shopify describes it as the top 1% of shippers (help.shopify.com/en/manual/fulfillment/setup/shop-promise/eligibility). Most merchants using this skill are not eligible.

**Shopify's own published carrier-deadline guidance goes stale.** The post at shopify.com/blog/holiday-shipping-deadlines was still the December 2025 edition when checked on 21 September 2026. Never treat a cached copy of that post, or any other, as current-year truth.

## Where the number comes from, in order of preference

1. **The transit time the merchant already entered on each shipping rate in Shopify** (Settings, Shipping and delivery, the zone, the rate). Ask for it first: it is the promise the shopper already sees at checkout, so the cutoff should not promise faster than that. If the rate shows a range such as "3 to 5 business days", use the upper bound.
2. **The carrier's current-year number**: the merchant's account rep or dashboard, or the carrier's published holiday page for this year, named and dated. A published page usually gives a **ship-by date** rather than a transit time. Take the ship-by date as it is (`ship_by` in the input) instead of converting it into a transit time.
3. **The merchant's own experience from last year**, stated as their estimate, with a larger buffer to cover the uncertainty.

If the rate's transit time and the carrier's current number disagree, use the slower one and tell the merchant the rate may need updating.

**Never supply a number from memory or from a general sense of "ground shipping takes about 5 days", and never supply a carrier's holiday ship-by date from memory.** They change every year and by region, and an invented number produces the most damaging wrong answer this skill can give: a published cutoff that promises too much time.

If the merchant does not have a number for a zone, mark it `[DECISION NEEDED: confirm carrier transit time for <zone>]` and do not calculate that zone.
