#!/usr/bin/env python3
"""
Back-solve a per-zone last-order (cutoff) date from a target arrival date,
a carrier transit estimate, the store's own processing time, and non-working
days. Deterministic: same input always produces the same output, and the
arithmetic is checkable by hand.

No network access, no dependencies beyond the standard library, no prompts.
Reads a JSON file, writes JSON to stdout. See references/cutoff-input-schema.md
for the input shape and references/worked-example.md for a hand-checkable case.

Usage:
    python3 cutoff.py <input.json>
    python3 cutoff.py <input.json> --out <output.json>

Exit codes:
    0  computed successfully (see "zones" in the output; a zone can still be
       marked "feasible": false if the cutoff would already have passed)
    2  input file missing or invalid JSON
    3  input failed schema validation (see stderr for which field)
"""
import sys
import json
import argparse
from datetime import date, timedelta


def parse_date(s, field):
    try:
        y, m, d = (int(x) for x in s.split('-'))
        return date(y, m, d)
    except Exception as e:
        raise ValueError(f'{field}: "{s}" is not a valid YYYY-MM-DD date') from e


def subtract_working_days(start, n, non_working_weekdays, holidays):
    """
    Walk backward from `start` by `n` working days. A working day is one
    whose weekday is not in `non_working_weekdays` (0=Mon..6=Sun) and whose
    date is not in `holidays`. `start` itself is not counted as one of the
    n days moved; the walk begins the day before `start`.
    """
    d = start
    remaining = n
    while remaining > 0:
        d = d - timedelta(days=1)
        if d.weekday() in non_working_weekdays:
            continue
        if d.isoformat() in holidays:
            continue
        remaining -= 1
    return d


def compute_zone(zone, target_arrival, today, non_working_weekdays, holidays):
    name = zone['name']
    transit_days = zone['transit_days']
    processing_days = zone.get('processing_days', 0)
    buffer_days = zone.get('buffer_days', 0)

    total_days_before_arrival = transit_days + processing_days + buffer_days
    cutoff = subtract_working_days(
        target_arrival, total_days_before_arrival, non_working_weekdays, holidays
    )

    feasible = cutoff >= today
    days_remaining = (cutoff - today).days

    return {
        'zone': name,
        'target_arrival': target_arrival.isoformat(),
        'transit_days': transit_days,
        'processing_days': processing_days,
        'buffer_days': buffer_days,
        'total_working_days_before_arrival': total_days_before_arrival,
        'cutoff_date': cutoff.isoformat(),
        'feasible': feasible,
        'days_until_cutoff': days_remaining if feasible else None,
        'note': (
            None if feasible else
            f'Cutoff {cutoff.isoformat()} has already passed relative to today '
            f'({today.isoformat()}). This zone cannot meet the target arrival date '
            f'through standard processing; it needs an expedited or manual path, '
            f'or the target date needs to move.'
        ),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input', help='Path to input JSON')
    ap.add_argument('--out', help='Write JSON here instead of stdout')
    ap.add_argument('--today', help='Override "today" as YYYY-MM-DD, for testing')
    args = ap.parse_args()

    try:
        with open(args.input) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f'error: input file not found: {args.input}', file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as e:
        print(f'error: invalid JSON in {args.input}: {e}', file=sys.stderr)
        sys.exit(2)

    required_top = ['target_arrival', 'zones']
    for f in required_top:
        if f not in data:
            print(f'error: missing required field "{f}"', file=sys.stderr)
            sys.exit(3)

    try:
        target_arrival = parse_date(data['target_arrival'], 'target_arrival')
    except ValueError as e:
        print(f'error: {e}', file=sys.stderr)
        sys.exit(3)

    today = parse_date(args.today, 'today') if args.today else date.today()

    non_working_weekdays = set(data.get('non_working_weekdays', [5, 6]))  # default Sat/Sun
    holidays = set(data.get('holidays', []))

    zones = data['zones']
    if not isinstance(zones, list) or not zones:
        print('error: "zones" must be a non-empty list', file=sys.stderr)
        sys.exit(3)

    results = []
    for i, zone in enumerate(zones):
        for f in ['name', 'transit_days']:
            if f not in zone:
                print(f'error: zones[{i}] missing required field "{f}"', file=sys.stderr)
                sys.exit(3)
        results.append(compute_zone(zone, target_arrival, today, non_working_weekdays, holidays))

    output = {
        'target_arrival': target_arrival.isoformat(),
        'computed_on': today.isoformat(),
        'non_working_weekdays': sorted(non_working_weekdays),
        'holidays_excluded': sorted(holidays),
        'zones': results,
    }

    out_json = json.dumps(output, indent=2)
    if args.out:
        with open(args.out, 'w') as f:
            f.write(out_json + '\n')
    else:
        print(out_json)


if __name__ == '__main__':
    main()
