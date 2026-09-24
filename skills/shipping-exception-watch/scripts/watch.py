#!/usr/bin/env python3
"""
Find fulfilled orders that are likely to turn into "where is my order?"
contacts before the shopper asks, sort them into exception groups, and rank
them by urgency. Deterministic: same CSV and config always produce the same
output, and every classification is checkable by hand against the CSV row.

No network access, no dependencies beyond the standard library, no prompts.
Reads a CSV order export and a JSON config, writes JSON to stdout.
See references/input-schema.md for the config shape and expected columns,
and references/exception-types.md for the exact rule behind each group.

Usage:
    python3 watch.py <orders.csv> <config.json>
    python3 watch.py <orders.csv> <config.json> --out <result.json>
    python3 watch.py <orders.csv> <config.json> --today 2026-12-08

Exit codes:
    0  classified successfully
    2  a file is missing, unreadable, or not valid CSV/JSON
    3  validation failed: required columns missing from the CSV, or a
       required config value missing (stderr lists every problem found)
"""
import argparse
import csv
import json
import sys
from datetime import date, datetime, timedelta

# Canonical field -> header names seen in Shopify exports and common
# tracking/report app exports. Matched case-insensitively, first hit wins.
# config["columns"] overrides any of these with an exact header name.
COLUMN_ALIASES = {
    'order_number': ['Name', 'Order', 'Order Number', 'Order Name', 'Order #', 'Order ID'],
    'customer_name': ['Shipping Name', 'Billing Name', 'Customer Name', 'Customer', 'First Name'],
    'ship_date': ['Fulfilled at', 'Fulfilled At', 'Fulfillment Date', 'Shipped At', 'Ship Date', 'Shipped Date'],
    'promised_date': ['Promised Delivery Date', 'Promised Date', 'Delivery Promise', 'Estimated Delivery Date', 'Expected Delivery Date'],
    'delivery_status': ['Shipment Status', 'Delivery Status', 'Tracking Status', 'Carrier Status', 'Shipping Status'],
    'last_update': ['Last Tracking Update', 'Last Tracking Event', 'Last Update', 'Last Scan Date', 'Tracking Updated At', 'Last Event Date'],
    'carrier': ['Tracking Company', 'Carrier', 'Shipping Carrier', 'Courier'],
    'tracking_number': ['Tracking Number', 'Tracking Numbers', 'Tracking', 'Tracking No'],
    'zone': ['Shipping Country', 'Shipping Zone', 'Zone', 'Shipping Country Code'],
    'notes': ['Notes', 'Tracking Status Detail', 'Status Detail', 'Tracking Detail', 'Last Event'],
}

DEFAULT_DELIVERED_VALUES = ['delivered']

DEFAULT_CUSTOMS_KEYWORDS = [
    'customs',
    'clearance',
    'held for documents',
    'awaiting documents',
    'documents required',
    'commercial invoice',
    'import duty',
    'import duties',
    'duties and taxes',
    'brokerage',
]

# Phrases that mean customs is already finished. Removed from the text
# before keyword matching, so "customs cleared" does not count as a hold.
DEFAULT_CUSTOMS_RELEASED = [
    'customs cleared',
    'cleared customs',
    'clearance complete',
    'clearance completed',
    'released by customs',
    'released from customs',
]

GROUP_ORDER = ['past_promised_date', 'customs_hold', 'tracking_stalled', 'delivered_but_contacted']

PRIVACY_NOTE = (
    'Only order number, customer first name, carrier, tracking number, zone and '
    'dates are read into the output. Email, phone and address columns are never '
    'read into the result, even when present in the CSV.'
)


def fail(code, messages):
    for m in messages:
        print(f'error: {m}', file=sys.stderr)
    sys.exit(code)


def norm_order(s):
    return (s or '').strip().lstrip('#').strip().lower()


def parse_date(s, fmt=None):
    """Return a date or None. Accepts YYYY-MM-DD with optional time and
    timezone suffix (Shopify's 'Fulfilled at' style), or a merchant-supplied
    strptime format. Never guesses between MM/DD and DD/MM."""
    s = (s or '').strip()
    if not s:
        return None
    if fmt:
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    try:
        y, m, d = (int(x) for x in s[:10].split('-'))
        return date(y, m, d)
    except Exception:
        return None


def add_working_days(start, n, non_working_weekdays, holidays):
    """Walk forward from `start` by n working days. `start` itself is not
    counted; the walk begins the day after."""
    d = start
    remaining = n
    while remaining > 0:
        d = d + timedelta(days=1)
        if d.weekday() in non_working_weekdays or d.isoformat() in holidays:
            continue
        remaining -= 1
    return d


def resolve_columns(headers, overrides):
    lower = {h.strip().lower(): h for h in headers}
    mapping = {}
    bad_overrides = []
    for field, aliases in COLUMN_ALIASES.items():
        if field in overrides and overrides[field]:
            wanted = overrides[field]
            if wanted.strip().lower() in lower:
                mapping[field] = lower[wanted.strip().lower()]
            else:
                mapping[field] = None
                bad_overrides.append(f'config columns.{field} = "{wanted}" is not a header in the CSV')
            continue
        mapping[field] = next((lower[a.lower()] for a in aliases if a.lower() in lower), None)
    return mapping, bad_overrides


def load_orders(rows, mapping):
    """Shopify writes one row per line item; order-level fields sit on the
    first row only. Merge rows by order number, keeping the first non-empty
    value of each field."""
    orders = {}
    sequence = []
    col = mapping['order_number']
    for row in rows:
        num = (row.get(col) or '').strip()
        if not num:
            continue
        key = norm_order(num)
        if key not in orders:
            orders[key] = {'order_number': num}
            sequence.append(key)
        rec = orders[key]
        for field, header in mapping.items():
            if header is None or field == 'order_number':
                continue
            val = (row.get(header) or '').strip()
            if val and not rec.get(field):
                rec[field] = val
    return [orders[k] for k in sequence]


def first_name(full):
    full = (full or '').strip()
    return full.split()[0] if full else None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('csv_path', help='Order export CSV')
    ap.add_argument('config_path', help='Config JSON (see references/input-schema.md)')
    ap.add_argument('--out', help='Write JSON here instead of stdout')
    ap.add_argument('--today', help='Override "today" as YYYY-MM-DD')
    args = ap.parse_args()

    # ---- load config -----------------------------------------------------
    try:
        with open(args.config_path, encoding='utf-8') as f:
            cfg = json.load(f)
    except FileNotFoundError:
        fail(2, [f'config file not found: {args.config_path}'])
    except json.JSONDecodeError as e:
        fail(2, [f'invalid JSON in {args.config_path}: {e}'])

    # ---- load CSV --------------------------------------------------------
    try:
        with open(args.csv_path, encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            rows = list(reader)
    except FileNotFoundError:
        fail(2, [f'CSV file not found: {args.csv_path}'])
    except (csv.Error, UnicodeDecodeError) as e:
        fail(2, [f'could not read CSV {args.csv_path}: {e}'])
    if not headers:
        fail(2, [f'CSV {args.csv_path} has no header row'])

    mapping, problems = resolve_columns(headers, cfg.get('columns', {}) or {})

    # ---- validate: columns first, then config ----------------------------
    promise = cfg.get('promise') or {}
    source = promise.get('source')
    missing = []

    def need(field, why):
        if mapping.get(field) is None:
            tried = cfg.get('columns', {}).get(field) or ' / '.join(COLUMN_ALIASES[field])
            missing.append(f'{field} ({why}); looked for: {tried}')

    need('order_number', 'identifies each order')
    need('delivery_status', 'needed to tell delivered from not delivered')
    if source in ('column', 'column_or_rule'):
        if source == 'column':
            need('promised_date', 'promise.source is "column"')
    if source in ('rule', 'column_or_rule'):
        need('ship_date', f'promise.source is "{source}" and the rule counts from the ship date')
        by_zone = promise.get('business_days', {}).get('by_zone') if isinstance(promise.get('business_days'), dict) else None
        if by_zone:
            need('zone', 'promise.business_days.by_zone is set')

    if missing:
        problems = ['required columns missing from the CSV:'] + [f'  - {m}' for m in missing] + problems
        problems.append('headers found in the CSV: ' + ', '.join(headers))
        problems.append('fix: add the column to the export, or map an existing header in config "columns"')
        fail(3, problems)
    if problems:
        problems.append('headers found in the CSV: ' + ', '.join(headers))
        fail(3, problems)

    cfg_problems = []
    if source not in ('column', 'rule', 'column_or_rule'):
        cfg_problems.append('config "promise.source" must be "column", "rule" or "column_or_rule" (ask the merchant how delivery dates are promised)')
    bd = promise.get('business_days')
    if source in ('rule', 'column_or_rule'):
        if not isinstance(bd, dict) or ('default' not in bd and not bd.get('by_zone')):
            cfg_problems.append('config "promise.business_days" needs "default" and/or "by_zone" (ask the merchant: ship date + how many business days, per zone)')
    if 'stall_days' not in cfg:
        cfg_problems.append('config "stall_days" is required (ask the merchant how many days without a tracking update counts as stalled; set it to null to skip that check on purpose)')
    elif cfg['stall_days'] is not None and (not isinstance(cfg['stall_days'], int) or cfg['stall_days'] < 1):
        cfg_problems.append('config "stall_days" must be a whole number of days, 1 or more, or null')
    today_str = args.today or cfg.get('today')
    today = parse_date(today_str) if today_str else date.today()
    if today_str and today is None:
        cfg_problems.append(f'"today" = "{today_str}" is not a valid YYYY-MM-DD date')
    if cfg_problems:
        fail(3, cfg_problems)

    date_fmt = cfg.get('date_format')
    stall_days = cfg['stall_days']
    non_working = set(promise.get('non_working_weekdays', [5, 6]))
    holidays = set(promise.get('holidays', []))
    delivered_values = [v.strip().lower() for v in cfg.get('delivered_values', DEFAULT_DELIVERED_VALUES)]
    customs_keywords = [k.lower() for k in cfg.get('customs_keywords', DEFAULT_CUSTOMS_KEYWORDS)]
    customs_released = [k.lower() for k in cfg.get('customs_released_phrases', DEFAULT_CUSTOMS_RELEASED)]
    contacted_raw = cfg.get('contacted_orders', []) or []
    contacted = {norm_order(c) for c in contacted_raw}

    skipped = {}
    if stall_days is None:
        skipped['tracking_stalled'] = 'merchant chose not to check stalled tracking (stall_days is null)'
    elif mapping['last_update'] is None:
        skipped['tracking_stalled'] = (
            'the export has no last-tracking-update column, so stalled tracking cannot be '
            'detected from this file; group skipped rather than guessed'
        )
    if not contacted:
        skipped['delivered_but_contacted'] = 'no contacted order list supplied; delivered orders are counted as on track'

    orders = load_orders(rows, mapping)
    groups = {g: [] for g in GROUP_ORDER}
    on_track = 0
    needs_review = []
    contacted_on_track = []
    seen = set()

    for o in orders:
        key = norm_order(o['order_number'])
        seen.add(key)
        status = o.get('delivery_status', '')
        status_l = status.lower()
        notes_l = o.get('notes', '').lower()
        ship = parse_date(o.get('ship_date'), date_fmt)
        last = parse_date(o.get('last_update'), date_fmt)
        zone = o.get('zone')

        entry = {
            'order_number': o['order_number'],
            'first_name': first_name(o.get('customer_name')),
            'carrier': o.get('carrier') or None,
            'tracking_number': o.get('tracking_number') or None,
            'zone': zone or None,
            'status_in_file': status or None,
            'ship_date': ship.isoformat() if ship else None,
            'last_update': last.isoformat() if last else None,
        }

        if not status:
            needs_review.append({'order_number': o['order_number'], 'reason': 'delivery status is empty in the file'})
            continue

        if status_l in delivered_values:
            if key in contacted:
                entry['flags'] = []
                groups['delivered_but_contacted'].append(entry)
            else:
                on_track += 1
            continue

        # Not delivered: work out the promised date.
        promised, promised_from, reason = None, None, None
        col_val = o.get('promised_date')
        if source in ('column', 'column_or_rule') and col_val:
            promised = parse_date(col_val, date_fmt)
            promised_from = 'column'
            if promised is None:
                reason = f'promised date "{col_val}" is not a readable date'
        if promised is None and reason is None and source in ('rule', 'column_or_rule'):
            by_zone = bd.get('by_zone') or {}
            days = by_zone.get(zone) if zone in by_zone else bd.get('default')
            if ship is None:
                reason = 'no ship date in the file, so the promise rule cannot be applied'
            elif days is None:
                reason = f'no promise rule for zone "{zone}" (add it to promise.business_days.by_zone or set a default)'
            else:
                promised = add_working_days(ship, int(days), non_working, holidays)
                promised_from = f'rule: ship date + {days} business days'
        if promised is None and reason is None:
            reason = 'no promised date in the file'
        if promised is None:
            needs_review.append({'order_number': o['order_number'], 'reason': reason})
            continue

        entry['promised_date'] = promised.isoformat()
        entry['promised_from'] = promised_from

        days_late = (today - promised).days
        text = status_l + ' | ' + notes_l
        for phrase in customs_released:
            text = text.replace(phrase, ' ')
        matched = [k for k in customs_keywords if k in text]
        days_stalled = (today - last).days if (last and 'tracking_stalled' not in skipped) else None
        is_late = days_late > 0
        is_customs = bool(matched)
        is_stalled = days_stalled is not None and days_stalled > stall_days

        flags = []
        if key in contacted:
            flags.append('shopper_already_contacted')
        if is_late:
            entry['days_late'] = days_late
        if is_customs:
            entry['customs_keywords_matched'] = matched
        if is_stalled:
            entry['days_stalled'] = days_stalled

        if is_late:
            group = 'past_promised_date'
        elif is_customs:
            group = 'customs_hold'
        elif is_stalled:
            group = 'tracking_stalled'
        else:
            on_track += 1
            if key in contacted:
                contacted_on_track.append(o['order_number'])
            continue
        flags += [g for g, hit in (('customs_hold', is_customs), ('tracking_stalled', is_stalled)) if hit and g != group]
        entry['flags'] = flags
        groups[group].append(entry)

    # ---- rank ------------------------------------------------------------
    groups['past_promised_date'].sort(key=lambda e: (-e['days_late'], norm_order(e['order_number'])))
    groups['customs_hold'].sort(key=lambda e: (e['ship_date'] or '9999', norm_order(e['order_number'])))
    groups['tracking_stalled'].sort(key=lambda e: (-e['days_stalled'], norm_order(e['order_number'])))
    groups['delivered_but_contacted'].sort(key=lambda e: norm_order(e['order_number']))

    urgency = []
    for g in GROUP_ORDER:
        for e in groups[g]:
            urgency.append({'rank': len(urgency) + 1, 'order_number': e['order_number'], 'group': g})

    output = {
        'today': today.isoformat(),
        'rows_read': len(rows),
        'orders_read': len(orders),
        'column_mapping': mapping,
        'settings': {
            'stall_days': stall_days,
            'promise': promise,
            'delivered_values': delivered_values,
            'customs_keywords': customs_keywords,
            'customs_released_phrases': customs_released,
            'contacted_orders_supplied': len(contacted),
        },
        'counts': {**{g: len(groups[g]) for g in GROUP_ORDER}, 'on_track': on_track, 'needs_review': len(needs_review)},
        'skipped_groups': skipped,
        'urgency_rank': urgency,
        'groups': groups,
        'needs_review': needs_review,
        'contacted_but_on_track': contacted_on_track,
        'contacted_orders_not_in_file': sorted(c for c in contacted_raw if norm_order(c) not in seen),
        'privacy': PRIVACY_NOTE,
    }

    out_json = json.dumps(output, indent=2, ensure_ascii=False)
    if args.out:
        with open(args.out, 'w', encoding='utf-8') as f:
            f.write(out_json + '\n')
    else:
        print(out_json)


if __name__ == '__main__':
    main()
