# The four exception groups

Each order goes into exactly one group. Conditions it also meets are listed in its `flags`, so nothing is hidden, but the message it gets follows the group. The rules below are the whole logic of `scripts/watch.py`; the manual fallback uses the same rules, in the same order.

## Order of checks

1. Status is empty: `needs_review`.
2. Status is delivered (a value in `delivered_values`):
   - on the contacted list: **`delivered_but_contacted`**
   - otherwise: on track.
3. Not delivered. Work out the promised date (the column, or ship date plus N business days for the zone). If it cannot be worked out: `needs_review`, with the reason.
4. Today is after the promised date: **`past_promised_date`**.
5. Else a customs keyword matches: **`customs_hold`**.
6. Else the last tracking update is more than `stall_days` days ago: **`tracking_stalled`**.
7. Else on track (counted, not listed).

## Urgency rank

1. `past_promised_date`, most days late first. The promise is already broken, and every day adds to the chance the shopper writes in, disputes the charge, or both.
2. `customs_hold`, oldest ship date first. Usually needs the merchant or the shopper to act (documents, duties) before anything moves.
3. `tracking_stalled`, longest silence first. Not late yet, but the shopper watching the tracking page sees nothing happening.
4. `delivered_but_contacted`. The shopper has already asked, so this is a reply rather than a proactive notice; it is ranked last only because it is already in the inbox, not because it matters less.

## 1. `past_promised_date`

Today is strictly after the promised delivery date and the status is not delivered. `days_late` is calendar days from the promised date to today. On the promised date itself the order is not late.

The promised date comes from the merchant, never from the skill: either a column in the file or the merchant's rule (ship date plus N business days per zone, skipping weekends and named closures, ship date not counted).

## 2. `customs_hold`

The status or notes column contains one of these, case-insensitively:

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

Before matching, these phrases are removed, because they mean customs is finished: `customs cleared`, `cleared customs`, `clearance complete`, `clearance completed`, `released by customs`, `released from customs`. The matched keywords are listed in the output so the merchant can see why an order landed here.

Keyword matching is blunt. A note like "no customs issues expected" still matches. That is why the matched words are shown: the merchant confirms each one before a message goes out. Add or remove keywords in the config to fit the carrier's wording.

## 3. `tracking_stalled`

The last tracking update is more than `stall_days` days before today (strictly more: with `stall_days` 4, an update exactly 4 days ago is not stalled). `days_stalled` is calendar days.

This group needs a last-update date column. If the export has none, the group is skipped and the output says so. It is never inferred from the ship date: an order shipped ten days ago may have been scanned yesterday.

## 4. `delivered_but_contacted`

The carrier says delivered, and the order number is on the list the merchant pasted of shoppers who said it did not arrive. Common causes: left at the wrong door or with a neighbour, a safe place, a parcel locker, scanned delivered early, or theft. The file cannot say which.

## Not a group, but reported

- **`needs_review`**: orders the rules cannot classify (no status, no ship date, unreadable date, a zone with no promise rule). Each carries its reason.
- **`contacted_but_on_track`**: the shopper asked, but the file shows nothing wrong yet. They still need an answer.
- **`contacted_orders_not_in_file`**: numbers on the contacted list that are not in this export, often because the export's date range or filter left them out.
