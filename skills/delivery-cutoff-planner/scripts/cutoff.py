#!/usr/bin/env python3
"""
Back-solve a per-zone last-order (cutoff) date from a target arrival date,
the carrier's transit time (or the carrier's published ship-by date), the
store's own processing time, a buffer, and two separate calendars: one for
the warehouse and one for the carrier.

Deterministic: same input always produces the same output, and every step
is printed in a countdown so it can be checked by hand. No network access,
no dependencies beyond the standard library, no prompts.

Input shape: references/cutoff-input-schema.md
Hand-checked cases: references/worked-example.md

THE RULE (identical in SKILL.md and in the copy-paste prompt)

  1. Delivery day. Start at the target date. If the carrier does not run
     that day (a carrier non-working weekday or a carrier closed date), step
     back to the latest carrier running day on or before the target. That
     day is the delivery day: the parcel must be delivered by it.
  2. Ship day. From the delivery day, step back one carrier running day at
     a time, `transit` times. Each step counts one transit day. Where you
     land is the latest ship day. If the warehouse is closed that day, step
     back to the latest day on or before it when the warehouse is open AND
     the carrier runs. With a published ship-by date instead of a transit
     time, the ship day is the latest such day on or before the ship-by date.
  3. Order day. From the ship day, step back one warehouse open day at a
     time, `processing` times. Processing N means the parcel is handed to
     the carrier on the Nth warehouse open day after the order day (0 = the
     same day, 1 = the next working day). The order day of an order placed
     on a warehouse open day before the order cutoff time is that day; after
     the cutoff time, or on a closed day, it is the next warehouse open day.
  4. Buffer. From the order day, step back one warehouse open day at a time,
     `buffer` times. Where you land is the published cutoff date. The cutoff
     moment is the order cutoff time on that date (the early-close time if
     that date is an early-close day).

  A transit range such as "5-8" always uses the upper bound (8).

Usage:
    python3 cutoff.py <input.json> [--today YYYY-MM-DD] [--out <output.json>]

Exit codes:
    0  computed (a zone can still be "feasible": false, or
       "status": "decision_needed" when it has no transit time or ship-by)
    2  input file missing or not valid JSON
    3  input failed validation (stderr says which field and why)
"""
import argparse
import json
import re
import sys
from datetime import date, timedelta

WEEKDAY_NAMES = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
MAX_WALK = 400  # calendar days; guards against a calendar with no open days


class InputError(Exception):
    pass


# ---------------------------------------------------------------- parsing

DATE_RE = re.compile(r'^(\d{4})-(\d{2})-(\d{2})$')
TIME_RE = re.compile(r'^(\d{1,2}):(\d{2})$')
RANGE_RE = re.compile(r'^\s*(\d+)\s*(?:-|to|–)\s*(\d+)\s*(?:working days|business days|days)?\s*$', re.I)
SINGLE_RE = re.compile(r'^\s*(\d+)\s*(?:working days|business days|days)?\s*$', re.I)


def parse_date(s, field):
    if not isinstance(s, str) or not DATE_RE.match(s):
        raise InputError(f'{field}: {json.dumps(s)} is not a date in YYYY-MM-DD form '
                         f'(two-digit month and day, for example 2026-12-05)')
    y, m, d = (int(x) for x in DATE_RE.match(s).groups())
    try:
        return date(y, m, d)
    except ValueError:
        raise InputError(f'{field}: {s} is not a real calendar date')


def parse_time(s, field):
    if not isinstance(s, str) or not TIME_RE.match(s):
        raise InputError(f'{field}: {json.dumps(s)} is not a 24-hour time like "14:00"')
    h, m = (int(x) for x in TIME_RE.match(s).groups())
    if h > 23 or m > 59:
        raise InputError(f'{field}: {s} is not a valid time of day')
    return (h, m)


def parse_whole(v, field, minimum):
    """A whole number >= minimum. Rejects booleans, decimals, negatives, text."""
    if isinstance(v, bool) or not isinstance(v, int):
        if isinstance(v, str) and SINGLE_RE.match(v):
            v = int(SINGLE_RE.match(v).group(1))
        else:
            raise InputError(f'{field}: {json.dumps(v)} must be a whole number of days '
                             f'(no decimals, no negatives)')
    if v < minimum:
        raise InputError(f'{field}: {v} must be a whole number of days, {minimum} or more (no negatives)')
    return v


def parse_transit(v, field):
    """Whole number of carrier days, or a range "5-8" which uses the upper bound.
    Returns (days_used, original_text, used_upper_bound)."""
    if isinstance(v, str) and RANGE_RE.match(v):
        lo, hi = (int(x) for x in RANGE_RE.match(v).groups())
        if lo > hi:
            raise InputError(f'{field}: range "{v}" has the larger number first; write it as "{hi}-{lo}"')
        if lo < 1:
            raise InputError(f'{field}: range "{v}" must start at 1 day or more')
        return hi, v, lo != hi
    days = parse_whole(v, field, 1)
    return days, v, False


def parse_weekdays(v, field):
    if not isinstance(v, list):
        raise InputError(f'{field}: must be a list of weekdays, for example ["Sat", "Sun"] or [5, 6]')
    out = set()
    for item in v:
        if isinstance(item, bool):
            raise InputError(f'{field}: {json.dumps(item)} is not a weekday')
        if isinstance(item, int) and 0 <= item <= 6:
            out.add(item)
        elif isinstance(item, str) and item.strip()[:3].title() in WEEKDAY_NAMES:
            out.add(WEEKDAY_NAMES.index(item.strip()[:3].title()))
        else:
            raise InputError(f'{field}: {json.dumps(item)} is not a weekday (use Mon..Sun or 0..6, Monday is 0)')
    if len(out) == 7:
        raise InputError(f'{field}: every weekday is closed, so nothing can ever be counted')
    return out


def parse_dates(v, field):
    if not isinstance(v, list):
        raise InputError(f'{field}: must be a list of YYYY-MM-DD dates')
    return {parse_date(x, f'{field}[{i}]') for i, x in enumerate(v)}


def parse_calendar(raw, name):
    if not isinstance(raw, dict):
        raise InputError(f'"{name}" is required and must be an object')
    if 'closed_weekdays' not in raw:
        raise InputError(f'{name}.closed_weekdays is required: ask which weekdays the {name} '
                         f'does not work during peak (use [] if it works every day)')
    cal = {
        'closed_weekdays': parse_weekdays(raw['closed_weekdays'], f'{name}.closed_weekdays'),
        'closed_dates': parse_dates(raw.get('closed_dates', []), f'{name}.closed_dates'),
    }
    return cal


def fmt_date(d):
    return f'{WEEKDAY_NAMES[d.weekday()]} {d.day} {MONTHS[d.month - 1]}'


def fmt_time(hm):
    h, m = hm
    suffix = 'am' if h < 12 else 'pm'
    h12 = h % 12 or 12
    return f'{h12} {suffix}' if m == 0 else f'{h12}:{m:02d} {suffix}'


# ------------------------------------------------------------ calendars

def warehouse_open(d, wh):
    return d.weekday() not in wh['closed_weekdays'] and d not in wh['closed_dates']


def carrier_runs(d, ca):
    return d.weekday() not in ca['closed_weekdays'] and d not in ca['closed_dates']


def closed_reason(d, cal, who):
    if d in cal['closed_dates']:
        return f'{who} closed date'
    return f'{who} does not work {WEEKDAY_NAMES[d.weekday()]}'


class Walker:
    """Records every calendar day visited so the countdown can be printed."""

    def __init__(self, wh, ca):
        self.wh, self.ca, self.rows = wh, ca, []

    def row(self, d, counted_as):
        self.rows.append({
            'date': d.isoformat(),
            'weekday': WEEKDAY_NAMES[d.weekday()],
            'warehouse_open': warehouse_open(d, self.wh),
            'carrier_running': carrier_runs(d, self.ca),
            'counted_as': counted_as,
        })

    def step_back(self, start, n, is_ok, label, skip_who):
        """Step back from `start` n times onto days where is_ok(d) is true.
        `start` itself is never counted. Returns the landing day."""
        d, done, guard = start, 0, 0
        while done < n:
            d -= timedelta(days=1)
            guard += 1
            if guard > MAX_WALK:
                raise InputError('the calendars leave no working days in the last 400 days; check closed dates')
            if is_ok(d):
                done += 1
                self.row(d, f'{label} {done}')
            else:
                cal = self.wh if skip_who == 'warehouse' else self.ca
                self.row(d, f'skipped: {closed_reason(d, cal, skip_who)}')
        return d

    def roll_to(self, start, is_ok, first_label, skip_label):
        """Latest day on or before `start` where is_ok(d). Records the days passed."""
        d, guard = start, 0
        while not is_ok(d):
            self.row(d, skip_label(d))
            d -= timedelta(days=1)
            guard += 1
            if guard > MAX_WALK:
                raise InputError('the calendars leave no working days in the last 400 days; check closed dates')
        self.row(d, first_label)
        return d


# ------------------------------------------------------------ compute

def compute_zone(i, zone, ctx):
    field = f'zones[{i}]'
    if not isinstance(zone, dict):
        raise InputError(f'{field} must be an object')
    name = zone.get('name')
    if not isinstance(name, str) or not name.strip():
        raise InputError(f'{field}.name is required')
    has_transit = zone.get('transit_days') not in (None, '')
    has_ship_by = zone.get('ship_by') not in (None, '')
    if has_transit and has_ship_by:
        raise InputError(f'{field} ("{name}"): give transit_days OR ship_by, not both. '
                         f'Ask the merchant which one comes from the carrier for this year.')

    raw_processing = zone.get('processing_days', ctx['processing_days'])
    if raw_processing is None:
        raise InputError(f'{field}.processing_days is required (or set top-level processing_days)')
    processing = parse_whole(raw_processing, f'{field}.processing_days', 0)
    if 'buffer_days' not in zone:
        raise InputError(f'{field}.buffer_days is required: the buffer is the merchant\'s decision, '
                         f'ask for it (0 is allowed if they choose it)')
    buffer_days = parse_whole(zone['buffer_days'], f'{field}.buffer_days', 0)

    target, wh = ctx['target'], ctx['warehouse']
    if zone.get('carrier') is not None:
        ca = parse_calendar(zone['carrier'], f'{field}.carrier')
    elif ctx['carrier'] is not None:
        ca = ctx['carrier']
    else:
        raise InputError(f'{field}.carrier is required when there is no top-level "carrier" calendar')
    base = {
        'zone': name,
        'target_arrival': target.isoformat(),
        'carrier_calendar': {
            'closed_weekdays': [WEEKDAY_NAMES[i] for i in sorted(ca['closed_weekdays'])],
            'closed_dates': sorted(d.isoformat() for d in ca['closed_dates']),
        },
        'processing_days': processing,
        'buffer_days': buffer_days,
        'transit_source': zone.get('transit_source'),
    }

    if not has_transit and not has_ship_by:
        base.update({
            'status': 'decision_needed',
            'cutoff_date': None,
            'feasible': None,
            'publishable_line': None,
            'note': f'[DECISION NEEDED: confirm carrier transit time for {name}]',
        })
        return base

    w = Walker(wh, ca)
    both_ok = lambda d: warehouse_open(d, wh) and carrier_runs(d, ca)

    def ship_skip(d):
        if not warehouse_open(d, wh):
            return f'skipped: {closed_reason(d, wh, "warehouse")}'
        return f'skipped: {closed_reason(d, ca, "carrier")}'

    if has_transit:
        transit, transit_text, upper = parse_transit(zone['transit_days'], f'{field}.transit_days')
        base.update({'mode': 'transit', 'transit_days_used': transit,
                     'transit_as_given': transit_text, 'used_upper_bound_of_range': upper})
        delivery = w.roll_to(target, lambda d: carrier_runs(d, ca), 'delivery day (day 0)',
                             lambda d: f'skipped: {closed_reason(d, ca, "carrier")}, no delivery')
        latest_ship = w.step_back(delivery, transit, lambda d: carrier_runs(d, ca), 'transit', 'carrier')
        if both_ok(latest_ship):
            ship = latest_ship
            w.rows[-1]['counted_as'] += ', ship day'
        else:
            w.rows[-1]['counted_as'] += ', warehouse closed so cannot ship'
            ship = w.roll_to(latest_ship - timedelta(days=1), both_ok, 'ship day', ship_skip)
    else:
        ship_by = parse_date(zone['ship_by'], f'{field}.ship_by')
        if ship_by > target:
            raise InputError(f'{field}.ship_by {ship_by.isoformat()} is after the target date')
        base.update({'mode': 'ship_by', 'carrier_ship_by': ship_by.isoformat()})
        delivery = None
        ship = w.roll_to(ship_by, both_ok, 'ship day (carrier ship-by)', ship_skip)

    if processing == 0:
        order_day = ship
        w.rows[-1]['counted_as'] += ', order day (processing 0: ships the same day)'
    else:
        order_day = w.step_back(ship, processing, lambda d: warehouse_open(d, wh), 'processing', 'warehouse')
        w.rows[-1]['counted_as'] += ', order day'
    cutoff = w.step_back(order_day, buffer_days, lambda d: warehouse_open(d, wh), 'buffer', 'warehouse') \
        if buffer_days else order_day
    w.rows[-1]['counted_as'] += ', cutoff date'

    # cutoff moment
    time_hm = ctx['early_close'].get(cutoff, ctx['order_cutoff_time'])
    early = cutoff in ctx['early_close']
    tz = ctx['timezone']
    if time_hm is not None:
        when = f'{fmt_time(time_hm)}{" " + tz if tz else ""}, {fmt_date(cutoff)}'
    else:
        when = fmt_date(cutoff)
    line = f'Order by {when} for delivery to {name} by {fmt_date(target)}.'

    today = ctx['today']
    feasible = cutoff >= today
    notes = []
    if time_hm is None:
        notes.append('[DECISION NEEDED: order cutoff time of day and timezone]')
    elif not tz:
        notes.append('[DECISION NEEDED: timezone for the order cutoff time]')
    if has_transit and base['used_upper_bound_of_range']:
        notes.append(f'Transit given as a range ("{transit_text}"); the upper bound {transit} was used.')
    if has_ship_by:
        notes.append('Ship-by mode: confirm the carrier ship-by date is for delivery by the same target date.')
    if early:
        notes.append(f'The cutoff date is an early-close day, so the earlier order cutoff time applies.')
    if feasible and cutoff == today:
        notes.append('The cutoff is today; it is still open only until the cutoff time.')
    if not feasible:
        notes.append(f'Cutoff {cutoff.isoformat()} has already passed relative to today '
                     f'({today.isoformat()}). Standard processing cannot meet the target for this zone. '
                     f'Two ways out: expedite the remaining orders, or move the published target date.')

    base.update({
        'status': 'computed',
        'delivery_day': delivery.isoformat() if delivery else None,
        'ship_day': ship.isoformat(),
        'order_day_before_buffer': order_day.isoformat(),
        'cutoff_date': cutoff.isoformat(),
        'cutoff_weekday': WEEKDAY_NAMES[cutoff.weekday()],
        'order_cutoff_time': f'{time_hm[0]:02d}:{time_hm[1]:02d}' if time_hm else None,
        'timezone': tz,
        'early_close_applies': early,
        'feasible': feasible,
        'days_until_cutoff': (cutoff - today).days if feasible else None,
        'publishable_line': line,
        'countdown': w.rows,
        'note': ' '.join(notes) or None,
    })
    return base


def build_context(data, today):
    for legacy in ('non_working_weekdays', 'holidays'):
        if legacy in data:
            raise InputError(f'"{legacy}" is no longer accepted: it merged the warehouse and carrier '
                             f'calendars. Use warehouse.closed_weekdays / warehouse.closed_dates and '
                             f'carrier.closed_weekdays / carrier.closed_dates instead.')
    if 'target_arrival' not in data:
        raise InputError('missing required field "target_arrival"')
    ctx = {
        'target': parse_date(data['target_arrival'], 'target_arrival'),
        'warehouse': parse_calendar(data.get('warehouse'), 'warehouse'),
        'carrier': parse_calendar(data['carrier'], 'carrier') if data.get('carrier') is not None else None,
        'today': today,
        'processing_days': data.get('processing_days'),
    }
    wh_raw = data['warehouse']
    ctx['order_cutoff_time'] = parse_time(wh_raw['order_cutoff_time'], 'warehouse.order_cutoff_time') \
        if wh_raw.get('order_cutoff_time') not in (None, '') else None
    tz = wh_raw.get('timezone')
    if tz is not None and (not isinstance(tz, str) or not tz.strip()):
        raise InputError('warehouse.timezone must be text such as "ET" or "Europe/Berlin"')
    ctx['timezone'] = tz.strip() if tz else None
    ec = wh_raw.get('early_close', {})
    if not isinstance(ec, dict):
        raise InputError('warehouse.early_close must be an object like {"2026-12-24": "10:00"}')
    ctx['early_close'] = {parse_date(k, f'warehouse.early_close key'): parse_time(v, f'warehouse.early_close["{k}"]')
                          for k, v in ec.items()}
    for d in ctx['early_close']:
        if d in ctx['warehouse']['closed_dates']:
            raise InputError(f'warehouse.early_close {d.isoformat()} is also a warehouse closed date; pick one')
    zones = data.get('zones')
    if not isinstance(zones, list) or not zones:
        raise InputError('"zones" must be a non-empty list')
    return ctx, zones


def run(data, today):
    if not isinstance(data, dict):
        raise InputError('input must be a JSON object')
    ctx, zones = build_context(data, today)
    results = [compute_zone(i, z, ctx) for i, z in enumerate(zones)]
    return {
        'target_arrival': ctx['target'].isoformat(),
        'computed_on': today.isoformat(),
        'warehouse': {
            'closed_weekdays': [WEEKDAY_NAMES[i] for i in sorted(ctx['warehouse']['closed_weekdays'])],
            'closed_dates': sorted(d.isoformat() for d in ctx['warehouse']['closed_dates']),
            'early_close': {d.isoformat(): fmt_time(t) for d, t in sorted(ctx['early_close'].items())},
        },
        'carrier': None if ctx['carrier'] is None else {
            'closed_weekdays': [WEEKDAY_NAMES[i] for i in sorted(ctx['carrier']['closed_weekdays'])],
            'closed_dates': sorted(d.isoformat() for d in ctx['carrier']['closed_dates']),
        },
        'zones': results,
    }


def main():
    ap = argparse.ArgumentParser(description='Per-zone delivery cutoff planner')
    ap.add_argument('input', help='Path to input JSON')
    ap.add_argument('--out', help='Write JSON here instead of stdout')
    ap.add_argument('--today', help='Override "today" as YYYY-MM-DD')
    args = ap.parse_args()

    try:
        with open(args.input) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f'error: input file not found: {args.input}', file=sys.stderr)
        sys.exit(2)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f'error: invalid JSON in {args.input}: {e}', file=sys.stderr)
        sys.exit(2)

    try:
        today = parse_date(args.today, '--today') if args.today else date.today()
        output = run(data, today)
    except InputError as e:
        print(f'error: {e}', file=sys.stderr)
        sys.exit(3)
    except Exception as e:  # never show a traceback to a merchant
        print(f'error: could not read the input ({type(e).__name__}: {e})', file=sys.stderr)
        sys.exit(3)

    out_json = json.dumps(output, indent=2)
    if args.out:
        with open(args.out, 'w') as f:
            f.write(out_json + '\n')
    else:
        print(out_json)


if __name__ == '__main__':
    main()
