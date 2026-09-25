# Input for `scripts/watch.py`

The script takes two files: a CSV of shipped orders with a delivery status per order, and a small JSON config built from what the merchant tells you. Every config value is either a merchant fact or a merchant decision. Never fill one in on the merchant's behalf.

```
python3 scripts/watch.py <orders.csv> <config.json>
```

## What Shopify's order export does and does not contain

Shopify's Orders CSV export (help.shopify.com, Exporting orders) has order-level and line-item columns such as `Name` (the order number), `Fulfillment Status`, `Fulfilled at`, `Shipping Country`, `Shipping Method` and `Notes`. **It has no tracking number, no carrier, no delivery status, no last scan date, and no estimated or delivered date.** `Fulfillment Status` says whether the order was fulfilled, not whether the parcel arrived. `Notes` is the order note written by the shopper or staff, not a tracking event.

So the export alone cannot be classified. Use one of two routes.

## Route A: Shopify only (Orders list Delivery status filter)

The admin Orders page has a **Delivery status** filter (help.shopify.com, Filtering orders) with these values: In transit, Out for delivery, Attempted delivery, Delayed, Failed delivery, Delivered, Tracking added, No status.

1. In Shopify admin, go to **Orders**. Filter **Delivery status** to one value, for example Failed delivery.
2. Click **Export** and export the orders the filter shows. Up to 50 orders or the current page download straight away; larger exports are emailed.
3. Open the CSV and add a column named `Delivery Status`, filled with the filter value (`Failed delivery`) on every row.
4. Repeat for Attempted delivery, Delayed, In transit, Tracking added and No status. Out for delivery can be left out: Shopify's own Out for delivery notification covers it. Export Delivered only for orders a shopper has reported missing.
5. Stack the files into one CSV. Rows for the same order are merged. If one order shows up under two different statuses (it has more than one shipment, or its status changed between exports), it goes to `needs_review`.

What route A can find: past promised date (from `Fulfilled at` plus the merchant's rule, or a promised date the merchant adds), delivery problems (Failed delivery, Attempted delivery, Delayed), delivered but not received, and a `check_tracking` list of possible stalls and possible customs holds to confirm on the tracking page (see below).

What it **cannot confirm**, and the script says so in `skipped_groups`:

- **Held at customs.** None of Shopify's delivery status values mentions customs, and the export has no carrier event text. When every status in the file is one of Shopify's filter values and no `tracking_detail` or `last_update` column is present, `data_source` is `shopify_delivery_status` and the customs group is skipped.
- **Tracking stalled.** The export has no scan dates. The group is skipped; it is never guessed from `Fulfilled at`.

Without scan dates the script cannot tell whether an order has moved. What it can do is compare the time since `Fulfilled at` with numbers the merchant gives, and list the orders worth checking by hand. Ask for these three; never fill them in:

- **`ship_from_country`**: the country the store ships from, as the code Shopify's `Shipping Country` uses (`US`). Orders to any other country are international.
- **`normal_transit_days`**: how many calendar days orders to each country normally take to arrive, `{"by_zone": {"US": 5, "CA": 8}}` and/or `{"default": N}`. This is how long parcels usually take, not the promise.
- **`no_scan_days`**: how many days after `Fulfilled at` a Tracking added or No status order starts to look like the carrier never scanned it.

Leave any of them out (or `null`) and its rule is skipped, with the reason in `check_tracking_rules_skipped`. Candidate orders go to `check_tracking` with `check_reasons`; nothing there is a confirmed problem, and none gets a draft.

## Route B: tracking app or carrier export

An export from the store's tracking app or the carrier's shipment report usually has a status per shipment, the text of the last event, and its date. Column names differ by app, so check the merchant's file and map them in `columns`. Keep the order number column so the merchant can match rows to orders.

The status detail column (the last event text, such as "Held by customs - awaiting commercial invoice") **must be mapped explicitly** as `columns.tracking_detail`. It has no automatic match, because the obvious candidate in a Shopify file, `Notes`, is the order note: a shopper asking "will I pay customs fees?" would otherwise put a normal order in the customs group. Never map `Notes` as `tracking_detail`.

Without a `tracking_detail` mapping on route B, customs holds and delivery problems are found only where the status column itself says so, and `limits` in the output says this.

## Columns the script reads

Only these fields are read. Everything else in the file (names, emails, phones, addresses, notes, line items, prices) is ignored.

| Field | Required | Headers it looks for automatically | Used for |
|---|---|---|---|
| `order_number` | always | Name, Order, Order Number, Order Name, Order #, Order ID | identifying the order |
| `delivery_status` | always | Delivery Status, Shipment Status, Tracking Status, Carrier Status, Shipping Status | delivered or not; delivery-problem and customs words |
| `ship_date` | when the promise is a rule | Fulfilled at, Fulfillment Date, Shipped At, Ship Date, Shipped Date | counting the promise from ship date |
| `promised_date` | when `promise.source` is `column` | Promised Delivery Date, Promised Date, Delivery Promise | the promise itself |
| `zone` | when the rule differs by country | Shipping Country, Shipping Zone, Zone, Shipping Country Code, Destination Country | picking the business days per zone |
| `last_update` | route B, optional | Last Tracking Update, Last Tracking Event Date, Last Update, Last Scan Date, Tracking Updated At, Last Event Date | stalled-tracking check |
| `tracking_detail` | route B, optional | none: map it in `columns` | customs and delivery-problem words |
| `carrier` | optional | Tracking Company, Carrier, Shipping Carrier, Courier | shown in the output |
| `tracking_number` | optional | Tracking Number, Tracking Numbers, Tracking No | shown in the output |

A tracking app's "estimated delivery" column is the carrier's forecast, not what the store promised, so it is not picked up as `promised_date` automatically. Map it only if the merchant confirms that date is what shoppers were told.

The script validates columns first and exits with code 3, listing every missing column, the headers it tried and the headers it found. Fix the export or add a `columns` mapping, then run again.

Dates must be `YYYY-MM-DD`, optionally followed by a time and timezone (Shopify's `2026-11-24 10:15:00 -0500` works). For any other format, set `date_format` to a Python `strptime` pattern such as `"%d/%m/%Y"`. The script never guesses between month-first and day-first; an unreadable date puts the order in `needs_review`.

## Config

```json
{
  "today": "2026-12-08",
  "stall_days": 4,
  "promise": {
    "source": "column_or_rule",
    "business_days": { "default": 5, "by_zone": { "US": 5, "CA": 8 } },
    "non_working_weekdays": [5, 6],
    "holidays": ["2026-11-26"]
  },
  "contacted_orders": ["#1005", "#1015"],
  "ship_from_country": null,
  "normal_transit_days": null,
  "no_scan_days": null,
  "columns": {
    "delivery_status": "Status",
    "tracking_detail": "Last Checkpoint Message",
    "last_update": "Last Checkpoint Date"
  },
  "delivered_values": ["delivered"],
  "date_format": null
}
```

**`today`** (optional, defaults to the machine's date). Set it explicitly so the result is reproducible. `--today` on the command line overrides it.

**`stall_days`** (required key). How many days without a tracking update the merchant counts as stalled. The script refuses to run without the key. Set it to `null` when the merchant does not want this check or the file has no scan date (route A).

**`promise`** (required). How the merchant decides the delivery date a shopper was promised:

- `source`: `"column"` (the file has a promised date for every order), `"rule"` (ship date plus N business days), or `"column_or_rule"` (column where filled, rule where empty).
- `business_days.default`: business days after the ship date for any zone not in `by_zone`. Leave it out if every zone must be named; orders from an unnamed zone then go to `needs_review`.
- `business_days.by_zone`: business days per zone, keyed by the exact value in the zone column (Shopify's `Shipping Country` holds codes such as `US`, `CA`).
- `non_working_weekdays`: default `[5, 6]` (Saturday, Sunday; Monday is 0).
- `holidays`: carrier or warehouse closed dates, `YYYY-MM-DD`. The ship date itself is not counted; the count starts the day after.

**`ship_from_country`**, **`normal_transit_days`**, **`no_scan_days`** (optional, route A only). The merchant's numbers for the `check_tracking` candidates, described under route A. Ignored on route B. `normal_transit_days` must be whole calendar days, 1 or more; `no_scan_days` likewise. A route A config for a US store might carry `"ship_from_country": "US", "normal_transit_days": {"by_zone": {"US": 5, "CA": 8, "GB": 10}}, "no_scan_days": 3`.

**`contacted_orders`** (optional). Order numbers where the shopper has already said the parcel did not arrive, with or without `#`. Without it the `delivered_but_contacted` group is skipped.

**`columns`** (optional). Map any field above to an exact header. Required for `tracking_detail`.

**`delivered_values`** (optional, default `["delivered"]`). Status values, compared whole and case-insensitively, that mean delivered. Add the file's own wording, such as `"Delivered to mailbox"`.

**`customs_keywords`**, **`customs_released_phrases`**, **`problem_keywords`** (optional). Override the lists in `exception-types.md`.

## Output

JSON on stdout: `data_source` (`shopify_delivery_status` or `tracking_export`), `counts` per group, `skipped_groups` with the reason, `limits` (checks that ran with less data than they need), `check_tracking_rules_skipped` and `check_tracking_next_step` (route A), `urgency_rank`, `groups` with the order details and matched keywords, `needs_review` with reasons, `contacted_but_on_track`, and `contacted_orders_not_in_file`. `column_mapping` shows which header was used for each field, so the merchant can check the script read the right column.
