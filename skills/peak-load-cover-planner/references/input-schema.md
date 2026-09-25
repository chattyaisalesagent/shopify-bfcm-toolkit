# Input schema for `scripts/plan.py`

Build this JSON from the merchant's answers. Never invent a value. Every assumption is an object with a `value` and a `source`, and `source` must be exactly `merchant-stated` or `merchant-chosen estimate`. The script refuses anything else, which is the point: a number with no owner cannot enter the plan.

Pick one `baseline.method`, in this order of preference:

1. `daily_series`: the merchant has last year's daily counts. Best, because every spike keeps its own day.
2. `messages` or `orders`: the merchant has only last year's BFCM-week average. Phase mode.
3. `new_store`: no last year at all. Normal weeks now, times the uplift the merchant expects.

## Example: daily series

```json
{
  "dates": {"black_friday": "2026-11-27", "cyber_monday": "2026-11-30",
            "holiday": "2026-12-25", "end_date": "2027-01-15"},
  "baseline": {
    "method": "daily_series",
    "last_year_black_friday": "2025-11-28",
    "last_year_daily": {"value": {"2025-11-21": 60, "2025-11-22": 45, "...": 0}, "source": "merchant-stated"}
  },
  "growth_pct": {"value": 10, "source": "merchant-chosen estimate"},
  "minutes_per_conversation": {"value": 6, "source": "merchant-stated"},
  "share_of_shift_answering_pct": {"value": 75, "source": "merchant-chosen estimate"},
  "team": [
    {"name": "Mai", "weekday_shift": "09:00-17:00", "weekend_shift": null,
     "can_add_days": ["Sat"], "extra_shift": "10:00-16:00", "max_hours_per_week": 46},
    {"name": "Lan", "weekday_shift": "13:00-21:00", "weekend_shift": "10:00-14:00",
     "days_off": ["2026-12-25"]}
  ],
  "helpdesk": {"billing_unit": "tickets", "plan_price_per_month": 300, "included_per_month": 2000,
               "overage_block_size": 100, "overage_price_per_block": 36, "source": "merchant-stated"}
}
```

## Example: new store

```json
{
  "dates": {"black_friday": "2026-11-27", "cyber_monday": "2026-11-30",
            "holiday": "2026-12-25", "end_date": "2027-01-15"},
  "baseline": {"method": "new_store",
               "normal_messages_per_week": {"value": 126, "source": "merchant-stated"}},
  "phase_uplift": {"value": {"pre_sale": 1.0, "bfcm_week": 3.0, "december": 1.5, "returns": 1.2},
                   "source": "merchant-chosen estimate"},
  "weekend_factor": {"value": 1.0, "source": "merchant-stated"},
  "scenarios": {"value": [1.5, 2], "source": "merchant-chosen estimate"},
  "minutes_per_conversation": {"value": 6, "source": "merchant-chosen estimate"},
  "share_of_shift_answering_pct": {"value": 60, "source": "merchant-chosen estimate"},
  "team": [{"name": "Owner", "weekday_shift": "09:00-17:00", "weekend_shift": "10:00-12:00"}]
}
```

## Fields

**`dates`** (required). `black_friday`, `cyber_monday`, `holiday` (the main gift-giving date) and `end_date` (usually mid-January). Optional `start_date`; the default is seven days before Black Friday. In 2026: Black Friday 27 November, Cyber Monday 30 November, Christmas Friday 25 December.

**`baseline`** (required), one of:

- `"method": "daily_series"`: `last_year_daily` (labelled; an object of `"YYYY-MM-DD": count` covering every day the window maps to), `last_year_black_friday` (2025-11-28 for a US store), optional `last_year_holiday` (default: the holiday date one year earlier). Needs `growth_pct`. `phase_factors` and `weekend_factor` are not used, because the daily counts already hold both.
  Mapping: before the day before the holiday, each day takes last year's day at the same distance from Black Friday, which is also the same weekday (27 Nov 2026 takes 28 Nov 2025; 21 Dec 2026 takes 22 Dec 2025). From the day before the holiday on, each day takes the same calendar date one year earlier, because Christmas Eve, Christmas and the returns peak follow the date, not the weekday. Forecast = last year's count x (1 + growth / 100) x any day override, rounded half up. If a needed day is missing, the script stops and names it.
- `"method": "messages"`: `conversations_per_day`, last year's BFCM-week average over all seven days (week total / 7). Needs `growth_pct`, `phase_factors`, `weekend_factor`.
- `"method": "orders"`: `orders_per_day` and `tickets_per_100_orders`. Same extra fields as `messages`.
- `"method": "new_store"`: either `normal_messages_per_week`, or `normal_orders_per_week` with `messages_per_100_orders`, all measured from the merchant's last four normal weeks. Needs `phase_uplift` and `weekend_factor`. Does not use `growth_pct` or `phase_factors`.

**`growth_pct`**. Expected change on last year, percent. Can be negative.

**`phase_factors`** (phase mode only). An average day of each phase, all days included, as a fraction of an average BFCM-week day (fixed at 1.0). Keys `pre_sale`, `december`, `returns`. See `phase-calendar.md`.

**`phase_uplift`** (new store only). An average day of each phase as a multiple of a normal day now. Keys `pre_sale`, `bfcm_week`, `december`, `returns`. The merchant's own expectation of their sales lift. If they have none, do not supply one: ask, and use `scenarios` to show what a bigger lift would do.

**`weekend_factor`** (phase and new store modes). A weekend day's average divided by a weekday's average, each averaged separately. The script uses it to split each phase average into a weekday level and a weekend level that keep the phase total unchanged: weekday level = phase average x days / (weekdays + factor x weekend days), weekend level = weekday level x factor. Weekends are therefore never reduced twice.

**`scenarios`** (optional). A list of multipliers, such as `[1.5, 2]`, applied to every day's forecast. Output is a summary table labelled as scenarios, not forecasts. Offer it whenever the volume level is a merchant-chosen estimate.

**`day_overrides`** (optional). Extra multiplier for named dates. In daily-series mode, use it only for something new this year, such as a second launch.

**`minutes_per_conversation`**, **`share_of_shift_answering_pct`** (required).

**`hourly_share_pct`** (optional). The share of a day's messages that arrives in each hour, from the merchant's helpdesk report: 24 numbers, or an object keyed by hour (`"9": 10`). Must add up to 100. With it, each day lists the hours that have messages and nobody on shift, and how many messages arrive in them. Without it, the plan lists only the hours nobody is on. Never make up an hourly curve.

**`roster_rules.max_consecutive_days`** (optional, labelled). The longest run of working days allowed. If absent, the script uses six, the roster template's check, and says so in the assumptions.

**`team`** (required, at least one person). Per person: `name`; `weekday_shift` and `weekend_shift` as `"HH:MM-HH:MM"` or `null`; optional `days_off`; optional `start_date` and `end_date`. For the draft roster, optional `can_add_days` (weekday names `Mon` to `Sun` on which they could take an extra shift), `extra_shift` (the times they would work on an added day, the merchant's usual shift) and `max_hours_per_week`. A person may have no regular shifts if they have `can_add_days` (an on-call helper). An overnight shift such as `"22:00-06:00"` is counted on the same calendar day as two pieces.

**`helpdesk`** (optional). `billing_unit`, `plan_price_per_month`, `included_per_month`, `overage_block_size` (1 if charged per unit), `overage_price_per_block`, `source`, optional `rest_of_month_volume` keyed `YYYY-MM`. Optional `ai_meter` for a vendor that bills AI-resolved conversations on a separate meter: `share_resolved_by_ai_pct` (the merchant's own resolution rate), `price_per_month` (0 if none), `included_per_month`, `overage_price_per_resolution`, `ai_resolutions_also_count_as_tickets` (true when the vendor charges the ticket fee as well, as Gorgias does), `source`. All prices come from the merchant's own plan page or invoice.

## Output

- `assumptions`: every input with its label.
- `days`: per day `forecast_conversations`, `required_agent_hours`, `available_agent_hours`, `gap_hours` (that day's work minus that day's hours), `backlog_in_hours`, `backlog_end_hours`, `status` (`GAP`, `BACKLOG` or `covered`), `on_shift` and `on_shift_detail` (times, and whether the shift was added by the draft), `uncovered_hours_of_day`, in daily mode `matched_last_year_date`, and with an hourly share `hours_with_messages_and_nobody_on` and `messages_in_those_hours`.
- `phase_summary`, `gap_days`, `backlog_days`, `final_backlog_hours`.
- `roster_draft`: the fill rule and the backlog before the draft.
- `people`: days worked, hours, days added, longest run, runs over the limit with a `[DECISION NEEDED]` line.
- `need_extra_help`: days that still end with work waiting after the draft.
- `cost`: per month, ticket meter, overage, AI meter if given, bill, `lower_bound_only`.
- `scenarios`: one summary row per multiplier.

## Backlog rule

Hours of work not done on a day are added to the next day's work. The inbox is assumed empty on the first day. Nothing is dropped, so a weekend shortfall shows up on Monday.
