# Input schema for `scripts/cutoff.py`

Build this JSON from the merchant's answers before calling the script. Never invent a value; every field here is either a merchant fact or a merchant decision.

```json
{
  "target_arrival": "2026-12-24",
  "warehouse": {
    "closed_weekdays": ["Sat", "Sun"],
    "closed_dates": ["2026-11-26", "2026-12-25"],
    "order_cutoff_time": "14:00",
    "timezone": "ET",
    "early_close": {"2026-12-24": "10:00"}
  },
  "carrier": {
    "closed_weekdays": ["Sun"],
    "closed_dates": ["2026-11-26", "2026-12-25"]
  },
  "zones": [
    {"name": "US", "transit_days": 3, "processing_days": 2, "buffer_days": 1,
     "transit_source": "Transit time on our Standard rate in Shopify, US zone"},
    {"name": "EU", "transit_days": "5-8", "processing_days": 2, "buffer_days": 2,
     "transit_source": "DHL account rep, email of 2 Oct 2026"},
    {"name": "UK", "ship_by": "2026-12-15", "processing_days": 2, "buffer_days": 1,
     "transit_source": "Royal Mail 2026 last posting dates page"}
  ]
}
```

## Top level

**`target_arrival`** (required). The date the parcel should arrive by, `YYYY-MM-DD` with two-digit month and day. Ask; do not assume the 24th or the 25th.

**`warehouse`** (required). The calendar for processing and the buffer.
- `closed_weekdays` (required, `[]` allowed). Days the warehouse does not pick, pack or hand over during peak. `"Mon"`..`"Sun"` or `0`..`6` (Monday is 0).
- `closed_dates` (optional). Specific dates the warehouse is closed.
- `order_cutoff_time` (optional, `"HH:MM"` 24-hour). Orders placed before this time on an open day start processing that day. Without it the publishable line has no time and the output flags `[DECISION NEEDED: order cutoff time of day and timezone]`.
- `timezone` (optional text, such as `"ET"` or `"Europe/Berlin"`). Printed next to the time. It is a label only; the script does no timezone conversion.
- `early_close` (optional, `{"YYYY-MM-DD": "HH:MM"}`). Half days. The day still counts as a warehouse open day, but orders placed on it must come in before the earlier time. If a half day cannot process a normal day's orders, put it in `closed_dates` instead.

**`carrier`** (required unless every zone has its own). The calendar for transit and the delivery day. A zone shipped by a different carrier gets its own `carrier` object with the same shape, which overrides this one for that zone. `closed_weekdays` (required, `[]` allowed) and `closed_dates` (optional). Use the days the carrier counts in its transit estimate. A carrier that delivers on Saturday but quotes transit in Monday to Friday business days should get `["Sat", "Sun"]` here, with a note to the merchant.

**`processing_days`** (optional). A default for every zone; a zone value wins.

The old keys `non_working_weekdays` and `holidays` are refused, because they merged the two calendars.

## Zones

One entry per shipping zone with its own transit time.

- **`name`** (required).
- **`transit_days`**. Carrier days, a whole number of 1 or more, or a range like `"5-8"`, which always uses the upper bound (8). Decimals, negatives and text such as `"about 5"` are refused.
- **`ship_by`**. Instead of `transit_days`: the carrier's published last ship date for delivery by the target, `YYYY-MM-DD`. Give one or the other, never both.
- A zone with neither is returned with `status: "decision_needed"` and no date.
- **`processing_days`** (required here or at top level). Whole number, 0 or more. 0 means the parcel is handed over the same day as the order (Shopify's "Same business day"), 1 the next warehouse open day.
- **`buffer_days`** (required, 0 allowed). The merchant's decision. The script refuses to default it.
- **`carrier`** (optional). This zone's own carrier calendar, same shape as the top-level one.
- **`transit_source`** (optional text). Where the number came from. Echoed back so the report can cite it.

## The rule the script applies

1. **Delivery day (day 0).** The target date, or if the carrier does not run that day, the latest carrier running day before it.
2. **Ship day.** Step back one carrier running day at a time, `transit_days` times. If the warehouse is closed on the landing day, step back to the latest day when the warehouse is open and the carrier runs. In ship-by mode, the ship day is the latest such day on or before `ship_by`.
3. **Order day.** Step back one warehouse open day at a time, `processing_days` times. An order placed on an open day before the cutoff time has that day as its order day; after the cutoff time or on a closed day, the next open day.
4. **Cutoff date.** Step back one warehouse open day at a time, `buffer_days` times. The cutoff moment is the order cutoff time (or the early-close time) on that date.

The start day of each step back is never counted in that step.

## Output

Per zone: `delivery_day`, `ship_day`, `order_day_before_buffer`, `cutoff_date`, `order_cutoff_time`, `feasible` (cutoff date on or after today), `days_until_cutoff`, `publishable_line` (for example `Order by 2 pm ET, Wed 16 Dec for delivery to US by Thu 24 Dec.`), `note` (open decisions, range used, early close, infeasibility and the two ways out), and `countdown`: one row per calendar day walked, with `date`, `weekday`, `warehouse_open`, `carrier_running` and `counted_as`. Show the countdown to the merchant.

Exit codes: 0 computed, 2 file missing or not JSON, 3 input refused (the message on stderr names the field and the reason).
