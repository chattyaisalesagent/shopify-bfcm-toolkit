# Input schema for `scripts/plan.py`

Build this JSON from the merchant's answers. Never invent a value. Every assumption is an object with a `value` and a `source`, and `source` must be exactly `merchant-stated` or `merchant-chosen estimate`. The script refuses anything else, which is the point: a number with no owner cannot enter the plan.

```json
{
  "store_timezone": "America/New_York",
  "dates": {
    "black_friday": "2026-11-27",
    "cyber_monday": "2026-11-30",
    "holiday": "2026-12-25",
    "end_date": "2027-01-15"
  },
  "baseline": {
    "method": "orders",
    "orders_per_day": {"value": 800, "source": "merchant-stated"},
    "tickets_per_100_orders": {"value": 25, "source": "merchant-chosen estimate"}
  },
  "growth_pct": {"value": 10, "source": "merchant-chosen estimate"},
  "phase_factors": {
    "value": {"pre_sale": 0.5, "december": 0.6, "returns": 0.4},
    "source": "merchant-chosen estimate"
  },
  "weekend_factor": {"value": 0.9, "source": "merchant-chosen estimate"},
  "day_overrides": {"value": {"2026-12-26": 1.5}, "source": "merchant-chosen estimate"},
  "minutes_per_conversation": {"value": 6, "source": "merchant-stated"},
  "share_of_shift_answering_pct": {"value": 75, "source": "merchant-chosen estimate"},
  "team": [
    {"name": "Anna", "weekday_shift": "09:00-17:00", "weekend_shift": "10:00-14:00"},
    {"name": "Ben", "weekday_shift": "12:00-20:00", "weekend_shift": null,
     "days_off": ["2026-11-26", "2026-12-25"]},
    {"name": "Cara (seasonal)", "weekday_shift": "09:00-13:00", "weekend_shift": "09:00-13:00",
     "start_date": "2026-11-23", "end_date": "2026-12-31"}
  ],
  "helpdesk": {
    "billing_unit": "tickets",
    "plan_price_per_month": 300,
    "included_per_month": 3000,
    "overage_block_size": 100,
    "overage_price_per_block": 40,
    "source": "merchant-stated",
    "rest_of_month_volume": {"2026-11": 1500}
  }
}
```

## Fields

**`dates`** (required). Calendar facts. `black_friday`, `cyber_monday`, `holiday` (the main gift-giving date the merchant plans around) and `end_date` (usually mid-January). Optional `start_date`; the default is seven days before Black Friday. All times of day are in `store_timezone`, which is informational only.

**`baseline`** (required). Either:
- `"method": "messages"` with `conversations_per_day`: last year's average per day across BFCM week, or
- `"method": "orders"` with `orders_per_day` and `tickets_per_100_orders`. If the merchant has no ratio, they choose one after seeing the published range in the skill body; label it `merchant-chosen estimate`.

**`growth_pct`** (required). Expected change on last year, percent. Can be negative.

**`phase_factors`** (required). Volume on an average day of each phase as a fraction of a BFCM-week day, which is fixed at 1.0. Keys `pre_sale`, `december`, `returns`. See `phase-calendar.md`.

**`weekend_factor`** (required). Multiplier on every Saturday and Sunday, in every phase. Use 1.0 if weekends are as busy as weekdays.

**`day_overrides`** (optional). Extra multiplier for named dates, such as the returns peak or a second launch day.

**`minutes_per_conversation`** (required). Average handle time, in minutes.

**`share_of_shift_answering_pct`** (required). Percent of a shift actually spent answering customers.

**`team`** (required, at least one person). Per person: `name`; `weekday_shift` and `weekend_shift` as `"HH:MM-HH:MM"` or `null` for not working; optional `days_off` list; optional `start_date` and `end_date` for seasonal hires. An overnight shift such as `"22:00-06:00"` is counted on the same calendar day as two pieces.

**`helpdesk`** (optional; omit to skip the bill). `billing_unit` (what the plan counts: tickets, conversations, resolutions; must match what the forecast counts), `plan_price_per_month`, `included_per_month`, `overage_block_size` (1 if charged per unit), `overage_price_per_block`, `source`, and optional `rest_of_month_volume` keyed `YYYY-MM` for days in a month that fall outside the window.

## Output

- `assumptions`: every input with its label.
- `days`: one row per day with `forecast_conversations`, `required_agent_hours`, `available_agent_hours`, `gap_hours`, `status` (`GAP` or `covered`), `on_shift`, `uncovered_hours_of_day`.
- `phase_summary`: totals, peak day, gap days and gap hours per phase.
- `gap_days`: the GAP rows only.
- `cost`: per calendar month, volume, over-cap units, overage blocks and cost, estimated bill, and `lower_bound_only` when part of the month is missing.

## Arithmetic

Forecast = level x phase factor x weekend factor (Sat, Sun) x day override, rounded half up. Level = baseline per day x (1 + growth / 100). Hours needed = forecast x minutes / 60, to one decimal. Hours available = total shift hours of people on shift x share / 100, to one decimal. Overage blocks = ceiling((month volume minus included) / block size).
