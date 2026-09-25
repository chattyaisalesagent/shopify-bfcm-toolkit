# The six exception groups

Each order goes into exactly one group. Conditions it also meets are listed in its `flags`, so nothing is hidden, but the message it gets follows the group. The rules below are the whole logic of `scripts/watch.py`; the manual fallback uses the same rules, in the same order.

## Order of checks

1. The file gives the order two different statuses, or the status is empty: `needs_review`.
2. Status is delivered (a value in `delivered_values`):
   - on the contacted list: **`delivered_but_contacted`**
   - otherwise: on track.
3. Not delivered. Work out the promised date (the column, or ship date plus N business days for the zone). If it cannot be worked out: `needs_review`, with the reason.
4. Today is after the promised date: **`past_promised_date`**.
5. Else a customs keyword matches the status or tracking detail: **`customs_hold`** (skipped on route A data).
6. Else a delivery-problem keyword matches the status or tracking detail: **`delivery_problem`**.
7. Else the last scan is more than `stall_days` days ago: **`tracking_stalled`** (skipped when there is no scan date).
8. Else, on route A only, a candidate rule matches: **`check_tracking`** (see section 5).
9. Else on track (counted, not listed).

So the precedence is: needs review, delivered, past promised date, customs hold, delivery problem, tracking stalled, check tracking, on track. A route A order that is late or has a Failed, Attempted or Delayed status never lands in `check_tracking`; any candidate rule it also meets shows as a flag (`possible_customs_hold`, `possible_stall`, `possible_not_scanned`), so the merchant checks tracking before choosing between the late or delivery-problem message and the customs one.

## Which groups each input route can support

| Group | Route A: Shopify export + Delivery status filter | Route B: tracking app or carrier export |
|---|---|---|
| `past_promised_date` | yes, from `Fulfilled at` and the merchant's rule | yes |
| `customs_hold` | **no**: Shopify's status values never mention customs | yes, with `tracking_detail` mapped (or a status that says customs) |
| `delivery_problem` | yes: Failed delivery, Attempted delivery, Delayed | yes |
| `tracking_stalled` | **no**: the export has no scan dates | yes, with `last_update` |
| `check_tracking` | yes, candidates only, with the merchant's numbers | not used: customs and stalls are detected directly |
| `delivered_but_contacted` | yes, if Delivered orders are included | yes |

## Urgency rank

1. `past_promised_date`, most days late first. The promise is already broken, and every day adds to the chance the shopper writes in, disputes the charge, or both.
2. `customs_hold`, oldest ship date first. Usually needs the merchant or the shopper to act (documents, duties) before anything moves.
3. `delivery_problem`, earliest promised date first. The carrier tried and failed, or has flagged the parcel as delayed. The shopper often has to do something (rearrange delivery, collect it), and Shopify sends no notification for these statuses, so they turn into "where is my order?" messages fast.
4. `tracking_stalled`, longest silence first. Not late yet, but the shopper watching the tracking page sees nothing happening.
5. `check_tracking`, longest since `Fulfilled at` first. Nothing is confirmed yet: the merchant opens each one before deciding whether a message is needed.
6. `delivered_but_contacted`. The shopper has already asked, so this is a reply rather than a proactive notice; it is ranked last only because it is already in the inbox, not because it matters less.

## 1. `past_promised_date`

Today is strictly after the promised delivery date and the status is not delivered. `days_late` is calendar days from the promised date to today. On the promised date itself the order is not late.

The promised date comes from the merchant, never from the skill: either a column in the file or the merchant's rule (ship date plus N business days per zone, skipping weekends and named closures, ship date not counted). A carrier's estimated date from a tracking app is not the store's promise unless the merchant says it is.

## 2. `customs_hold`

The status or tracking detail contains one of these, case-insensitively:

- customs
- clearance
- held for documents
- awaiting documents
- documents required
- commercial invoice
- import duty
- import duties
- duties and taxes
- brokerage

Before matching, these phrases are removed, because they mean customs is finished: `customs cleared`, `cleared customs`, `clearance complete`, `clearance completed`, `released by customs`, `released from customs`.

Only carrier text is searched: the status and the column the merchant mapped as `tracking_detail`. Shopify's order `Notes` column is never read, because a shopper asking "will I pay customs fees?" is not a customs hold. On route A data (every status is a Shopify filter value, no tracking detail, no scan date) this group is skipped and the output says why.

Keyword matching is still blunt: a carrier event like "no customs issues expected" matches. The matched words are in the output so the merchant confirms each order before a message goes out.

## 3. `delivery_problem`

Not late yet, but the status or tracking detail contains one of these: attempted, attempt fail, attemptfail, failed, failure, delayed, delay, exception, return to sender, returned to sender, undeliverable. This covers Shopify's Attempted delivery, Failed delivery and Delayed, and common tracking-app wording.

These parcels turn into "where is my order?" messages while still inside the promise, because the shopper got a card through the door, or the tracking page shows a problem. If the order is also past the promised date, it goes to `past_promised_date` with a `delivery_problem` flag.

## 4. `tracking_stalled`

The last scan is more than `stall_days` days before today (strictly more: with `stall_days` 4, a scan exactly 4 days ago is not stalled). `days_stalled` is calendar days.

This group needs a last scan date, which only route B has. Without one the group is skipped and the output says so. It is never inferred from the ship date: an order shipped ten days ago may have been scanned yesterday.

## 5. `check_tracking`: check tracking before you message (route A only)

Shopify's statuses never say customs and the export has no scan dates, so on route A a stall or customs hold can never be confirmed from the file. This group lists orders worth opening in Shopify admin (click the tracking number to reach the carrier's page) before anyone writes to the shopper. It never asserts a stall or a customs hold, and it gets **no draft**: the merchant checks, then uses an existing template if the tracking confirms a problem.

Only orders that are not delivered, not past the promised date, and not Failed, Attempted or Delayed reach this check. Each rule needs a number the merchant gave; a rule without its number is skipped and `check_tracking_rules_skipped` says why. Days are calendar days from `Fulfilled at` to today.

| Rule | Condition | Needs |
|---|---|---|
| `possible_stall` | status In transit, Tracking added or No status, and days since `Fulfilled at` are more than the merchant's "normally delivered within N days" for that country | `normal_transit_days` (per country, or a default) |
| `possible_not_scanned` | status Tracking added or No status, and days since `Fulfilled at` are more than `no_scan_days`: the carrier may never have scanned it | `no_scan_days` |
| `possible_customs_hold` | `Shipping Country` differs from `ship_from_country`, and the status is Delayed, or In transit past the normal window (or past the promised date) | `ship_from_country`, and `normal_transit_days` for the In transit case |

"More than" is strict: with a normal window of 5, an order shipped exactly 5 days ago is not flagged. A country with no normal window and no default is not checked, and `limits` names it. An order can meet several rules; they are all listed in `check_reasons`, each with a plain `why`, in one group. A Delayed order to the ship-from country is a `delivery_problem`, never a customs candidate. A Delayed international order is also a `delivery_problem` (the carrier did report a problem), with the flag `possible_customs_hold`.

What to do once the tracking page is open (also in `check_tracking_next_step`):

- it says customs, clearance, duties or documents: use the Held at customs message;
- it has not moved for several days: use the Tracking stalled message, with the last scan date from the tracking page;
- it says failed, attempted or exception: use the Delivery problem message;
- it shows recent scans: no message.

## 6. `delivered_but_contacted`

The carrier says delivered, and the order number is on the list the merchant pasted of shoppers who said it did not arrive. Common causes: left at the wrong door or with a neighbour, a safe place, a parcel locker, scanned delivered early, or theft. The file cannot say which.

## Not a group, but reported

- **`needs_review`**: orders the rules cannot classify (two different statuses, no status, no ship date, unreadable date, a zone with no promise rule). Each carries its reason.
- **`contacted_but_on_track`**: the shopper asked, but the file shows nothing wrong yet. They still need an answer.
- **`contacted_orders_not_in_file`**: numbers on the contacted list that are not in this file, often because a filter or date range left them out.
- **On route B, `check_tracking` is always empty**: customs and stalls are detected from the carrier data, and the route A numbers are ignored.
- **On track orders get no message.** Shopify's own shipping notifications (Shipping confirmation, Shipping update, Out for delivery, Delivered) can already reach them; Out for delivery and Delivered go out when the carrier or fulfillment app sends that event.
