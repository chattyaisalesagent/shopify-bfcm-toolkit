# Input schema for `scripts/cutoff.py`

Build this JSON from the merchant's answers before calling the script. Never invent a value; every field here is either a merchant fact or a merchant decision.

```json
{
  "target_arrival": "2026-12-24",
  "non_working_weekdays": [5, 6],
  "holidays": ["2026-12-25"],
  "zones": [
    {
      "name": "Domestic",
      "transit_days": 2,
      "processing_days": 1,
      "buffer_days": 1
    }
  ]
}
```

## Fields

**`target_arrival`** (required). The date the merchant wants the order to arrive by, `YYYY-MM-DD`. Usually the holiday itself or the day before. Ask; do not assume the 24th or the 25th, some merchants target earlier for gift-wrapping time on the recipient's end.

**`non_working_weekdays`** (optional, default `[5, 6]`, Saturday and Sunday). Weekday integers, Monday is 0. Ask if the merchant's warehouse or carrier operates on weekends during peak season; several do specifically because of the season.

**`holidays`** (optional, default empty). Specific closed dates as `YYYY-MM-DD`, for the warehouse and for the carrier if the merchant knows a carrier blackout day. Every skipped day the merchant does not name will silently not be skipped, so ask directly: "any days your warehouse or your carrier is closed between now and the target date?"

**`zones`** (required, at least one). One entry per shipping zone or region the merchant wants a cutoff for. A merchant with one shipping profile for the whole country still gets one zone; a merchant with different transit times per region needs one zone per region, because a single global cutoff is understating the risk for the slower ones.

Each zone:

- **`name`** (required). Whatever the merchant calls the zone.
- **`transit_days`** (required). Carrier transit time in working days, from the merchant's own carrier data or agreement. This is the one figure the skill cannot supply and must not guess; see `references/where-transit-times-come-from.md`.
- **`processing_days`** (optional, default 0). The store's own time from order placed to order handed to the carrier. Ask, do not assume same-day.
- **`buffer_days`** (optional, default 0). Extra margin the merchant chooses to keep the promise defensible. This is a judgment call, not a fact; see the skill body for how to raise it.

## Output

The script prints one object per zone: the computed `cutoff_date`, whether it is still `feasible` relative to today, and `days_until_cutoff` when it is. An infeasible zone carries a `note` explaining that standard processing cannot meet the target and naming the two ways out: expedite, or move the target date. Never silently drop an infeasible zone from the output the merchant sees.

## Arithmetic

`cutoff_date` is `target_arrival` minus `(transit_days + processing_days + buffer_days)` **working days**, walking backward and skipping every weekday in `non_working_weekdays` and every date in `holidays`. The walk starts the day before `target_arrival`; `target_arrival` itself is never counted as one of the days subtracted.

This is ordinary date arithmetic with no ambiguity, which is why it is done in a script and not asserted in prose.
