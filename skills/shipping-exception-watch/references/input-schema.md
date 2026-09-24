# Input for `scripts/watch.py`

The script takes two files: the merchant's order export as CSV, and a small JSON config built from the merchant's answers. Every config value is either a merchant fact or a merchant decision. Never fill one in on the merchant's behalf.

```
python3 scripts/watch.py <orders.csv> <config.json>
```

## Getting the export out of Shopify

In Shopify admin: **Orders**, filter to the orders that matter (for example Fulfillment status = Fulfilled, and a date range covering the last few weeks of shipments), then **Export**, choose "Orders matching your search" or "Current page", and a CSV format. Shopify emails the file or downloads it directly, depending on size.

**Be honest with the merchant about what that file contains.** Shopify's standard order export carries order-level fields such as `Name` (the order number), `Fulfillment Status`, `Fulfilled at`, `Shipping Name` and `Shipping Country`. It is not a carrier tracking report. Before relying on it, check the actual file for:

- **a delivery status per shipment** (Delivered, In transit, Exception). `Fulfillment Status` is not this: it says whether the order was fulfilled, not whether the parcel arrived.
- **a last tracking update date**, the date of the carrier's most recent scan.
- **carrier and tracking number.**

We could not confirm that the standard export includes carrier scan events, and the merchant should assume it does not until they see the columns in their own file. Those columns usually come from somewhere else: an export from the tracking or order-status app the store already uses, the carrier's own shipment report from the merchant's carrier account, or a column the merchant adds by hand for the orders they are worried about. Merge them into one CSV with one row per order (or one row per line item; the script merges rows that share an order number).

If the file has no delivery status at all, the script stops (exit code 3) because it cannot tell a delivered order from one still moving. If the file has no last-update date, the script skips the stalled-tracking group and says so; it never guesses a tracking status.

## Columns

The script auto-detects common header names, case-insensitively. Anything it does not recognise can be mapped in `columns` in the config.

| Field | Required | Headers it looks for | Used for |
|---|---|---|---|
| `order_number` | always | Name, Order, Order Number, Order Name, Order #, Order ID | identifying the order |
| `delivery_status` | always | Shipment Status, Delivery Status, Tracking Status, Carrier Status, Shipping Status | delivered vs not; customs keywords |
| `ship_date` | when the promise is a rule | Fulfilled at, Fulfillment Date, Shipped At, Ship Date, Shipped Date | counting the promise from ship date |
| `promised_date` | when `promise.source` is `column` | Promised Delivery Date, Promised Date, Delivery Promise, Estimated Delivery Date, Expected Delivery Date | the promise itself |
| `zone` | when the rule differs by zone | Shipping Country, Shipping Zone, Zone, Shipping Country Code | picking the business days per zone |
| `last_update` | optional | Last Tracking Update, Last Tracking Event, Last Update, Last Scan Date, Tracking Updated At, Last Event Date | stalled-tracking check |
| `notes` | optional | Notes, Tracking Status Detail, Status Detail, Tracking Detail, Last Event | customs keywords |
| `carrier` | optional | Tracking Company, Carrier, Shipping Carrier, Courier | shown in the output |
| `tracking_number` | optional | Tracking Number, Tracking Numbers, Tracking, Tracking No | shown in the output |
| `customer_name` | optional | Shipping Name, Billing Name, Customer Name, Customer, First Name | first name only, for the greeting |

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
  "columns": { "delivery_status": "Carrier Status" },
  "delivered_values": ["delivered"],
  "customs_keywords": ["customs", "clearance"],
  "date_format": null
}
```

**`today`** (optional, defaults to the machine's date). Set it explicitly so the result is reproducible and the merchant can check the arithmetic. `--today` on the command line overrides it.

**`stall_days`** (required key). How many days without a tracking update the merchant counts as stalled. A merchant shipping domestic express and one shipping international economy will answer very differently, so ask; the script refuses to run without the key. Set it to `null` only when the merchant explicitly does not want this check.

**`promise`** (required). How the merchant decides the delivery date a shopper was promised:

- `source`: `"column"` (the file has a promised date for every order), `"rule"` (ship date plus N business days), or `"column_or_rule"` (use the column where it is filled, the rule where it is empty).
- `business_days.default`: business days after the ship date, for any zone not listed in `by_zone`. Leave it out if every zone must be named; orders from an unnamed zone then go to `needs_review` rather than getting a guessed promise.
- `business_days.by_zone`: business days per zone, keyed by the exact value in the zone column (Shopify's `Shipping Country` holds codes such as `US`, `CA`).
- `non_working_weekdays`: default `[5, 6]` (Saturday, Sunday; Monday is 0).
- `holidays`: carrier or warehouse closed dates, `YYYY-MM-DD`. The ship date itself is not counted; the count starts the day after.

The rule should match what the store actually told shoppers (checkout delivery estimate, shipping policy, or the cutoff table from `delivery-cutoff-planner`), not what the merchant hopes the carrier achieves.

**`contacted_orders`** (optional). Order numbers where the shopper has already said the parcel did not arrive, pasted by the merchant from their inbox. With or without `#`. Without this list the `delivered_but_contacted` group is skipped and reported as skipped.

**`columns`** (optional). Map any field above to an exact header name in the file. Overrides auto-detection.

**`delivered_values`** (optional, default `["delivered"]`). Status values, compared whole and case-insensitively, that mean the carrier marked the parcel delivered. Add the merchant's own wording if their file uses something like `"Delivered to mailbox"`.

**`customs_keywords`** and **`customs_released_phrases`** (optional). Override the lists in `exception-types.md`.

## Output

JSON on stdout: `counts` per group, `skipped_groups` with the reason, `urgency_rank` (one line per exception order), `groups` with the order details, `needs_review` (orders the rules could not classify, each with a reason), `contacted_but_on_track` (shoppers who asked about an order that shows no problem in the file), and `contacted_orders_not_in_file`. `column_mapping` shows which header was used for each field, so the merchant can check the script read the right column.
