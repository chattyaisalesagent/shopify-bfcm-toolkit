---
name: delivery-cutoff-planner
description: Compute per-region last-order (cutoff) dates and times so a shipment arrives by a target date, from the store's own processing time, separate warehouse and carrier calendars, and the carrier's transit time or published ship-by date, and write the three delivery messages Shopify does not provide (on track, running late, will not arrive in time). Use when someone asks when customers have to order to get something by a holiday, wants a per-zone shipping deadline, or needs a message for a delayed or missed delivery.
license: MIT
compatibility: Runs the bundled Python script with the standard library only, no network access and no dependencies. Falls back to a guided manual countdown if scripts cannot run in the environment.
metadata:
  version: "0.2"
---

# Delivery cutoff planner

December, not sale week, is the longest exposure of the peak season, and delivery is the most-asked subject across every phase of it. Shopify shows each shopper a delivery date range for their own order at checkout, but it does not back-solve a holiday into a published per-zone "order by" date. For carrier shipments its notifications are Shipping confirmation, Shipping update, Out for delivery and Delivered, and none of them tells a shopper their parcel is late. (Local delivery has its own "Local order missed delivery" notification, which is about a failed local drop-off, not a late carrier parcel.) This skill produces the dates and the missing messages.

## The rule that governs everything here

**The transit time is a fact, not something to estimate.** The buffer is a judgment call, and it belongs to the merchant. Never blend the two, and never invent either. Never supply a carrier transit time or a carrier holiday ship-by date from memory.

Read `references/where-transit-times-come-from.md` before asking the merchant anything. If a zone has no transit time and no ship-by date, mark it `[DECISION NEEDED: confirm carrier transit time for <zone>]` and do not calculate it.

## If the message is a plain question, answer it first

Some requests are a yes-or-no question about Shopify, such as "can Shopify set a different cutoff per region natively". Answer it first, in one or two direct sentences, from the verified facts in `references/where-transit-times-come-from.md`:

- Shopify's manual delivery dates already use a transit time set per shipping rate, and rates live in zones, so checkout can show different date ranges per zone. Fulfillment time is a separate setting, not set per rate.
- But the order cutoff is fixed at 12 pm in the shipping origin's local time, business days are Monday to Friday, and Shopify does not publish an "order by <date>" per zone for a holiday. Automated delivery dates are a per-order estimate shown only within 5 days (US) or 4 days (Europe) inside one region.
- So a per-zone order-by date for a holiday has to be computed and published separately.

Do not claim Shopify has a native per-region holiday cutoff, and do not claim manual delivery dates cannot hold per-region numbers. Offer to run the workflow after the direct answer.

## How to work

Ask one question at a time.

1. **Zones.** Which zones need a cutoff: one per region with a different transit time.
2. **Target date.** The date the parcel should arrive by. Do not assume 24 or 25 December.
3. **Transit per zone, and where it comes from.** First ask for the transit time they already set on each shipping rate in Shopify (Settings, Shipping and delivery, the zone, the rate). Then ask whether their carrier has a current-year number, or a published ship-by date for this target. A range such as "5-8 days" always uses the upper bound. A ship-by date goes in as `ship_by`, not converted into transit.
4. **Processing.** How many warehouse working days after the order day the parcel is handed to the carrier during peak (0 = same day, 1 = next working day). And the order cutoff time of day with its timezone.
5. **Warehouse calendar.** Weekdays the warehouse does not work during peak, closed dates, and half days (an early order cutoff, for example 24 December).
6. **Carrier calendar, separately, per carrier.** Weekdays each carrier does not move or deliver, and its closed dates. Many carriers deliver on Saturday while the warehouse is closed; keep the two apart. A zone with a different carrier gets its own `carrier` calendar in the input.
7. **Buffer per zone.** Frame the trade-off: more buffer loses some late orders, less risks a promise the carrier does not keep. Never default it silently.
8. **Today's date**, and what the merchant will offer on late parcels and how shoppers reach a person.

Then build the JSON in `references/cutoff-input-schema.md` and run:

```
python3 scripts/cutoff.py <input.json>
```

## The counting rule

The script applies this rule, and a manual count must apply exactly the same one:

1. **Delivery day (day 0).** Start at the target date. If the carrier does not run that day, step back to the latest carrier running day on or before it. The parcel must be delivered by day 0.
2. **Ship day.** Step back one carrier running day at a time, transit times. If the warehouse is closed on the landing day, step back to the latest day when the warehouse is open and the carrier runs. With a ship-by date, the ship day is the latest such day on or before it.
3. **Order day.** Step back one warehouse open day at a time, processing times. Processing N means the parcel is handed over on the Nth warehouse open day after the order day. An order placed on an open day before the order cutoff time has that day as its order day; after the cutoff time or on a closed day, the next open day.
4. **Cutoff.** Step back one warehouse open day at a time, buffer times. The published cutoff is the order cutoff time (or the early-close time) on that date: "Order by 2 pm ET, Wed 16 Dec".

The start day of each step back is never counted in that step. `references/worked-example.md` has four hand-checked 2026 cases, including a Christmas Day target the carrier does not deliver on.

If the script cannot run, count by hand with this rule, first checking weekdays from a fixed anchor (1 November 2026 is a Sunday), and show a row per calendar day: date, weekday, warehouse open?, carrier running?, counted as. Tell the merchant it was counted by hand and to check each date against a calendar.

## Report

1. A cutoff table per zone: transit (and its source), processing, buffer, delivery day, ship day, order-by date and time, days left, feasible.
2. The countdown rows for each zone from the script output.
3. **Every zone, including infeasible ones.** An infeasible zone means standard processing cannot meet the target today. State the two ways out: expedite the remaining orders, or move the published target date for that zone.
4. The publishable line per zone, from `publishable_line`. Ask where it goes: banner, shipping policy page, product pages, or all three.
5. The three delivery messages from `references/delivery-templates.md`. Fill only what the merchant confirmed; an unconfirmed offer never appears in a message sent under the store's name.
6. Open decisions, blocking ones first (missing transit, cutoff time or timezone, buffer, offers, contact).

If the rate transit time in Shopify is faster than the carrier's current number, say the rate should be updated too, or checkout will promise more than the cutoff.

## Scope

This computes and publishes shipping deadlines and writes the messages for delivery problems. It does not change Shopify settings, does not touch discount or returns configuration (that is `campaign-rules-policy-qa`), does not track a shipment or call a carrier API, and does not convert timezones. If the merchant wants live tracking reflected in these messages, that needs an integration this skill does not have; say so rather than fabricating a tracking status.
