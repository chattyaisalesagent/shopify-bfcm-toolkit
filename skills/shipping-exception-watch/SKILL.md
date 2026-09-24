---
name: shipping-exception-watch
description: Scan a Shopify export of fulfilled orders for the ones likely to turn into "where is my order?" messages before the shopper asks, sort them into four groups (past the promised delivery date, held at customs, tracking stalled, marked delivered but the shopper says it never arrived), rank them by urgency, and draft a proactive message for each group. Use when a merchant wants to find late or stuck shipments in their order list, get ahead of delivery complaints during the peak season, or write delay notices for orders that have already shipped.
license: MIT
compatibility: Runs the bundled Python script with the standard library only, no network access and no dependencies. Falls back to guided manual classification of pasted orders if scripts cannot run in the environment.
metadata:
  version: "0.1"
---

# Shipping exception watch

From Black Friday to mid-January, "where is my order?" is the question a store answers most. Most of those messages are predictable: the parcel is past the date the store promised, stuck at customs, or its tracking has not moved in days. The order list already shows which orders these are. This skill finds them, puts the most urgent first, and drafts the message so the store writes to the shopper before the shopper writes in.

## The rule that governs everything here

**Never state a tracking status the file does not contain.** Every status, date and carrier in a draft comes from the merchant's file, quoted as written. If the file has no tracking-event data, say so and skip what depends on it; do not infer it from the ship date.

**Drafts only; the merchant sends.** This skill does not contact shoppers, change orders or call a carrier. Every offer in a message (refund, gift card, reship, paying duties) is `[DECISION NEEDED]` until the merchant confirms it.

The promised date and the stall threshold are the merchant's decisions. Ask for both. Do not pick defaults.

## How to work

1. **Ask for the export.** Explain how to get it: Shopify admin, **Orders**, filter to fulfilled orders from the last few weeks, **Export** as CSV. Then be straight about its limits: the standard order export is not a carrier tracking report. Ask whether the file has a delivery status per shipment, a last tracking update date, carrier and tracking number, and if not, whether they can add them from their tracking app's export or their carrier account's shipment report. `references/input-schema.md` has the details and the column names the script recognises.

2. **Ask how delivery was promised.** Either a promised-date column in the file, or a rule: ship date plus how many business days, per zone, and which days the carrier or warehouse is closed. The rule must match what shoppers were actually told (checkout estimate, shipping policy, or the cutoff table from `delivery-cutoff-planner`). Do not assume a number.

3. **Ask for the stall threshold,** if the file has a last-update column: how many days without a tracking update counts as stalled for this store. Domestic express and international economy need very different answers, so put it as a question, not a suggestion. If the file has no last-update column, tell the merchant this group will be skipped.

4. **Ask for the contacted list** (optional): order numbers where the shopper has already said the parcel did not arrive. Without it, the "delivered but contacted" group is skipped.

5. **Build the config and run the script.** Assemble the JSON described in `references/input-schema.md`, set `today` explicitly, and run:

   ```
   python3 scripts/watch.py <orders.csv> <config.json>
   ```

   Exit code 3 means a required column or config value is missing; the error lists each one and the headers the file actually has. Relay that to the merchant plainly, fix the mapping in `columns` or ask for the missing column, and run again. Do not work around a missing column by guessing.

6. **Report by urgency.** Lead with the counts per group, then the orders in `urgency_rank` order: order number, first name, carrier, tracking number, days late or days stalled, and any flags. State which groups were skipped and why. List every `needs_review` order with its reason, and every `contacted_but_on_track` order, since those shoppers still need a reply. `references/exception-types.md` explains each group and why it ranks where it does.

7. **Draft the messages** from `references/message-templates.md`, one per group, filled from the script output. Quote the carrier status as written in the file. Leave every offer as `[DECISION NEEDED]` and ask the merchant, while there is still time, which options they are willing to offer. For customs orders, show the matched keywords and ask the merchant to confirm the order is really held before a message goes out.

8. **Keep it private.** Follow `references/privacy.md`: no emails, phone numbers or addresses in the report or the drafts.

## If scripts cannot run here

If script execution is unavailable or disabled, classify by hand with the same rules. Ask the merchant to paste up to about 50 orders as rows with only these columns: order number, first name, carrier, tracking number, ship date, promised date (or zone, if the promise is a rule), delivery status, last update date, notes. More than about 50 is too many to check reliably by hand; ask them to filter to the oldest shipments first, or run the script elsewhere.

For each order, apply the checks in `references/exception-types.md` in order: delivered (and contacted or not), then promised date passed, then customs keyword, then stalled. For every order you place in a group, show the working: the promised date and how it was computed (the business days skipped, for a rule), today's date, and the days late or days stalled, so the merchant can check it. Then report and draft exactly as in steps 6 and 7. Tell the merchant that hand classification is slower and more error-prone than the script, and that the dates are worth a second look.

## Scope

This reads a file the merchant already has. It does not call a carrier API, fetch live tracking, or know anything that happened after the export was taken; a status in the file may already be out of date, and the report should say what date the file is from. It does not send messages, edit orders or open carrier claims. Delivery cutoff dates and the pre-shipment delay templates are `delivery-cutoff-planner`; return and refund policy wording is `campaign-rules-policy-qa`.
