---
name: shipping-exception-watch
description: Scan a Shopify merchant's shipped orders for the ones likely to turn into "where is my order?" messages before the shopper asks, sort them into five groups (past the promised delivery date, held at customs, failed or attempted or delayed delivery, tracking stalled, marked delivered but the shopper says it never arrived), rank them by urgency, and draft a proactive message for each group. Works from a Shopify order export plus the admin Delivery status filter, or from a tracking app or carrier export. With Shopify data only, it lists possible stalls and possible customs holds to check on the tracking page before messaging, using the merchant's own normal delivery times, and says plainly what that source cannot confirm. Use when a merchant wants to find late, failed or stuck shipments, get ahead of delivery complaints during the peak season, or write delay notices for orders that have already shipped.
license: MIT
compatibility: Runs the bundled Python script with the standard library only, no network access and no dependencies. Falls back to guided manual classification of pasted orders if scripts cannot run in the environment.
metadata:
  version: "0.3"
---

# Shipping exception watch

From Black Friday to mid-January, "where is my order?" is one of the questions a store gets most. Most of those messages are predictable: the parcel is past the date the store promised, a delivery attempt failed, it is stuck at customs, or its tracking has not moved in days. This skill finds those orders, puts the most urgent first, and drafts the message so the store writes to the shopper before the shopper writes in.

## The rule that governs everything here

**Never state a tracking status the data does not contain.** Every status, date and carrier in a draft comes from the merchant's file, quoted as written. If the file cannot show something (a customs hold, a stalled scan), say so and skip that group; do not infer it from the ship date or from order notes.

**Drafts only; the merchant sends.** This skill does not contact shoppers, change orders or call a carrier. Every offer in a message (refund, gift card, reship, paying duties) is `[DECISION NEEDED]` until the merchant confirms it.

The promised date and the stall threshold are the merchant's decisions. Ask for both. Do not pick defaults.

## What Shopify already tells the shopper

Shopify's customer notifications include Shipping confirmation, Shipping update, Out for delivery and Delivered. Out for delivery and Delivered go out when the carrier or fulfillment app sends that tracking event (Settings > Notifications > Customer notifications). There is no notification for a late, delayed, failed or held parcel. So this skill writes nothing for on-track orders; its drafts cover the cases Shopify is silent about. Tell the merchant this, so their messages do not repeat Shopify's.

## How to work

1. **Explain the two input routes and ask which one the merchant will use.** Shopify's order CSV export has no tracking number, carrier, delivery status, scan date or delivery date, so it cannot be used alone. `references/input-schema.md` has the exact steps and the columns the script reads.
   - **Route A, Shopify only:** filter the admin Orders page by **Delivery status** (values: In transit, Out for delivery, Attempted delivery, Delayed, Failed delivery, Delivered, Tracking added, No status), export each problem view, add a `Delivery Status` column holding the filter value, and combine. This finds late orders and failed, attempted or delayed deliveries. It **cannot confirm** customs holds or stalled tracking: Shopify's status values never mention customs and the export has no scan dates. Instead it lists candidates in `check_tracking` (possible stall, possible never scanned, possible customs hold) for the merchant to check on the tracking page. Say so before running, not after.
   - **Route B, tracking app or carrier export:** carries a last scan date and the status detail text, so all five groups can run. The status detail column must be mapped explicitly as `tracking_detail`.

2. **Ask how delivery was promised.** Either a promised-date column, or a rule: ship date plus how many business days, per country, and which days the carrier or warehouse is closed. The rule must match what shoppers were actually told (checkout estimate, shipping policy, or the cutoff table from `delivery-cutoff-planner`). Do not use a tracking app's carrier estimate as the promise. Do not assume a number.

3. **Ask for the stall threshold** if the file has a last scan date: how many days without an update counts as stalled for this store. Domestic express and international economy need very different numbers, so ask. With route A, set `stall_days` to `null` and say the group is skipped.

   **Route A only, ask three more things** (one at a time), for the `check_tracking` candidates: the country the store ships from; how many calendar days orders to each country normally take to arrive (not the promise); and after how many days a Tracking added or No status order looks like the carrier never scanned it. Never fill these in. If the merchant does not know one, leave it `null`: that rule is skipped and the output says why.

4. **Ask for the contacted list** (optional): order numbers where the shopper has already said the parcel did not arrive.

5. **Build the config and run the script.** Assemble the JSON described in `references/input-schema.md`, set `today` explicitly, and run:

   ```
   python3 scripts/watch.py <orders.csv> <config.json>
   ```

   Exit code 3 means a required column or config value is missing; the error lists each one and the headers the file has. Relay that plainly, fix the mapping in `columns` or ask for the missing column, and run again. Never map Shopify's `Notes` column as `tracking_detail`: it is the order note, written by shoppers and staff.

6. **Report by urgency.** Lead with the counts per group and `data_source`, then the orders in `urgency_rank` order: order number, group, status as written, carrier, tracking number, days late or days stalled, flags. State every `skipped_groups` entry, every `check_tracking_rules_skipped` entry and every `limits` note in plain words. Show `check_tracking` orders after the late and delivery-problem orders, each with its `check_reasons` in plain words, and tell the merchant to open the order in Shopify admin and click the tracking number before messaging. List every `needs_review` order with its reason, and every `contacted_but_on_track` order, since those shoppers still need a reply. `references/exception-types.md` explains each group.

7. **Draft the messages** from `references/message-templates.md`, one per group. `check_tracking` gets no draft: give the "if tracking shows X, use message Y" pointers from `check_tracking_next_step` instead. Quote the carrier status as written. Leave every offer as `[DECISION NEEDED]` and ask the merchant which options they are willing to offer. For customs and delivery-problem orders, show the matched keywords and ask the merchant to confirm before a message goes out.

8. **Keep it private.** Follow `references/privacy.md`. The script reads no names; drafts use `[first name]` for the merchant's sending tool to fill.

## If scripts cannot run here

Classify by hand with the same rules. Ask the merchant to paste up to about 50 orders with only these columns: order number, ship date, shipping country (if the promise differs by country), delivery status, promised date if they have one, and for route B carrier, tracking number, last scan date and status detail. Tell them to delete names, emails, phone numbers, addresses and the Notes column first. More than about 50 is too many to check reliably by hand; ask them to start with Failed delivery, Attempted delivery and Delayed, then the oldest shipments.

Apply the checks in `references/exception-types.md` in order, including the `check_tracking` rules on route A. For every order in a group, show the promised date and how it was computed (the business days skipped, for a rule), today's date, and the days late or stalled. Then report and draft as in steps 6 and 7, and say that hand classification is slower and worth a second look.

## Scope

This reads a file the merchant already has. It does not call a carrier API, fetch live tracking, or know anything that happened after the export was taken; the report should say what date the file is from. It does not send messages, edit orders or open carrier claims. Delivery cutoff dates and the pre-shipment delay templates are `delivery-cutoff-planner`; return and refund policy wording is `campaign-rules-policy-qa`.
