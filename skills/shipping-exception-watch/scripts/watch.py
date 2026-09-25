#!/usr/bin/env python3
"""
Find fulfilled orders that are likely to turn into "where is my order?"
contacts before the shopper asks, sort them into exception groups, and rank
them by urgency. Deterministic: same CSV and config always produce the same
output, and every classification is checkable by hand against the CSV row.

No network access, no dependencies beyond the standard library, no prompts.
Reads a CSV (a Shopify order export with a Delivery Status column added, or a
tracking app / carrier export) and a JSON config, writes JSON to stdout.
See references/input-schema.md for the config shape and expected columns,
and references/exception-types.md for the exact rule behind each group.

On Shopify-only data (route A) customs holds and stalled tracking cannot be
confirmed, so the script lists candidates instead, in `check_tracking`: orders
the merchant should open in Shopify admin and check before messaging anyone.
Those rules run only with numbers the merchant gave (normal transit days per
country, days without a first scan, ship-from country); a rule without its
number is skipped and the output says why.

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

# Canonical field -> header names seen in Shopify order exports and common
# tracking/carrier exports. Matched case-insensitively, first hit wins.
# config["columns"] overrides any of these with an exact header name.
#
# There is deliberately no customer-name field: drafts use a [first name]
# placeholder the merchant's email or helpdesk tool fills in.
#
# `tracking_detail` has NO aliases on purpose. Shopify's order export has a
# `Notes` column, but it holds the order note (shopper or staff text such as
# "will I pay customs fees?"), not carrier events. Auto-matching it put normal
# orders in customs_hold. The carrier's status detail / last event column must
# be named explicitly in config["columns"]["tracking_detail"].
COLUMN_ALIASES = {
    'order_number': ['Name', 'Order', 'Order Number', 'Order Name', 'Order #', 'Order ID'],
    'ship_date': ['Fulfilled at', 'Fulfilled At', 'Fulfillment Date', 'Shipped At', 'Ship Date', 'Shipped Date'],
    'promised_date': ['Promised Delivery Date', 'Promised Date', 'Delivery Promise'],
    'delivery_status': ['Delivery Status', 'Shipment Status', 'Tracking Status', 'Carrier Status', 'Shipping Status'],
    'last_update': ['Last Tracking Update', 'Last Tracking Event Date', 'Last Update', 'Last Scan Date', 'Tracking Updated At', 'Last Event Date'],
    'carrier': ['Tracking Company', 'Carrier', 'Shipping Carrier', 'Courier'],
    'tracking_number': ['Tracking Number', 'Tracking Numbers', 'Tracking No'],
    'zone': ['Shipping Country', 'Shipping Zone', 'Zone', 'Shipping Country Code', 'Destination Country'],
    'tracking_detail': [],
}

# The values of the "Delivery status" filter on the Shopify admin Orders page
# (help.shopify.com, Filtering orders). A file whose statuses are all from
# this list and that has no tracking-detail column is Shopify-only data: it
# cannot show customs holds, and the script says so instead of guessing.
SHOPIFY_DELIVERY_STATUS_VALUES = {
    'in transit', 'out for delivery', 'attempted delivery', 'delayed',
    'failed delivery', 'delivered', 'tracking added', 'no status',
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

# Words that mean the carrier tried and failed, or flagged the parcel as
# delayed. Covers Shopify's "Attempted delivery", "Failed delivery" and
# "Delayed" and common tracking-app wording. Matched as substrings of the
# status and the tracking detail.
DEFAULT_PROBLEM_KEYWORDS = [
    'attempted',
    'attempt fail',
    'attemptfail',
    'failed',
    'failure',
    'delayed',
    'delay',
    'exception',
    'return to sender',
    'returned to sender',
    'undeliverable',
]

GROUP_ORDER = ['past_promised_date', 'customs_hold', 'delivery_problem', 'tracking_stalled',
               'check_tracking', 'delivered_but_contacted']

# Route A candidates. Shopify statuses that may hide a stall (the parcel is
# not reported as delivered, out for delivery or failed), the ones that mean
# the carrier may never have scanned it, and the ones that may hide a customs
# hold on an international order.
STALL_CANDIDATE_STATUSES = {'in transit', 'tracking added', 'no status'}
NO_SCAN_STATUSES = {'tracking added', 'no status'}
CUSTOMS_CANDIDATE_STATUSES = {'in transit', 'delayed'}

# What the merchant does once the tracking page confirms something. There is
# no draft for a check_tracking order until then.
CHECK_TRACKING_NEXT = {
    'customs': 'tracking says customs, clearance, duties or documents: use the Held at customs message',
    'no_movement': 'tracking has not moved for several days: use the Tracking stalled message, with the last scan date from the tracking page',
    'failed': 'tracking says failed, attempted or exception: use the Delivery problem message',
    'moving': 'tracking shows recent scans: no message needed',
}

PRIVACY_NOTE = (
    'Only order number, carrier, tracking number, zone, status as written and '
    'dates are read into the output. Names, emails, phone numbers and address '
    'columns are never read, even when present in the CSV.'
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


def matched_keywords(keywords, text):
    """Keywords found in text, dropping any that is only part of a longer
    match (so "Delayed" reports "delayed", not "delayed" and "delay")."""
    hits = [k for k in keywords if k in text]
    return [k for k in hits if not any(k != other and k in other for other in hits)]


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
    for field in overrides:
        if field not in COLUMN_ALIASES:
            bad_overrides.append(f'config columns.{field} is not a field this script reads (fields: {", ".join(COLUMN_ALIASES)})')
    return mapping, bad_overrides


def load_orders(rows, mapping):
    """Shopify writes one row per line item; order-level fields sit on the
    first row only. Merge rows by order number, keeping the first non-empty
    value of each field. Different non-empty delivery statuses for the same
    order (it appears in two filtered exports, or has two shipments) are
    kept so the order can go to needs_review instead of picking one."""
    orders = {}
    sequence = []
    col = mapping['order_number']
    for row in rows:
        num = (row.get(col) or '').strip()
        if not num:
            continue
        key = norm_order(num)
        if key not in orders:
            orders[key] = {'order_number': num, '_statuses': []}
            sequence.append(key)
        rec = orders[key]
        for field, header in mapping.items():
            if header is None or field == 'order_number':
                continue
            val = (row.get(header) or '').strip()
            if field == 'delivery_status' and val and val.lower() not in [s.lower() for s in rec['_statuses']]:
                rec['_statuses'].append(val)
            if val and not rec.get(field):
                rec[field] = val
    return [orders[k] for k in sequence]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('csv_path', help='Order or tracking export CSV')
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
            tried = (cfg.get('columns', {}) or {}).get(field) or ' / '.join(COLUMN_ALIASES[field])
            missing.append(f'{field} ({why}); looked for: {tried}')

    need('order_number', 'identifies each order')
    need('delivery_status', (
        'needed to tell delivered from not delivered. Shopify\'s order export has no delivery status: '
        'filter the Orders page by Delivery status, export each view and add a "Delivery Status" column '
        'holding the filter value, or use a tracking app or carrier export'))
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
        cfg_problems.append('config "stall_days" is required (ask the merchant how many days without a tracking update counts as stalled; set it to null to skip that check on purpose, or when the file has no last-update date)')
    elif cfg['stall_days'] is not None and (not isinstance(cfg['stall_days'], int) or cfg['stall_days'] < 1):
        cfg_problems.append('config "stall_days" must be a whole number of days, 1 or more, or null')
    nt = cfg.get('normal_transit_days')
    if nt is not None:
        ok = isinstance(nt, dict) and ('default' in nt or nt.get('by_zone'))
        vals = ([nt.get('default')] if isinstance(nt, dict) and 'default' in nt else []) + \
               (list((nt.get('by_zone') or {}).values()) if isinstance(nt, dict) else [])
        if not ok or any(not isinstance(v, int) or v < 1 for v in vals):
            cfg_problems.append('config "normal_transit_days" must be {"default": N} and/or {"by_zone": {"US": N}}, whole calendar days 1 or more, or null (ask the merchant how many days orders to each country normally take)')
    ns = cfg.get('no_scan_days')
    if ns is not None and (not isinstance(ns, int) or ns < 1):
        cfg_problems.append('config "no_scan_days" must be a whole number of days, 1 or more, or null')
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
    problem_keywords = [k.lower() for k in cfg.get('problem_keywords', DEFAULT_PROBLEM_KEYWORDS)]
    ship_from = (cfg.get('ship_from_country') or '').strip().upper() or None
    normal_days = cfg.get('normal_transit_days')
    no_scan_days = cfg.get('no_scan_days')
    contacted_raw = cfg.get('contacted_orders', []) or []
    contacted = {norm_order(c) for c in contacted_raw}

    orders = load_orders(rows, mapping)

    # ---- what this file can and cannot show ------------------------------
    statuses_seen = {s.lower() for o in orders for s in o['_statuses']}
    shopify_only = (
        mapping['tracking_detail'] is None
        and mapping['last_update'] is None
        and bool(statuses_seen)
        and statuses_seen <= SHOPIFY_DELIVERY_STATUS_VALUES
    )
    data_source = 'shopify_delivery_status' if shopify_only else 'tracking_export'

    skipped = {}
    limits = []
    if shopify_only:
        skipped['customs_hold'] = (
            'the file only has Shopify delivery statuses (In transit, Delayed, Failed delivery and so on), '
            'which never say customs; a customs hold can only be found from a tracking app or carrier '
            'export with the status detail column mapped as tracking_detail. Group skipped rather than guessed; '
            'international orders that might be held are listed in check_tracking instead, to confirm on the tracking page'
        )
    elif mapping['tracking_detail'] is None:
        limits.append(
            'no tracking-detail column is mapped (config columns.tracking_detail), so customs holds and '
            'delivery problems are found only where the status column itself says so'
        )
    if stall_days is None:
        skipped['tracking_stalled'] = 'merchant chose not to check stalled tracking, or the file has no last-update date (stall_days is null)'
    elif mapping['last_update'] is None:
        skipped['tracking_stalled'] = (
            'the file has no last-tracking-update date (Shopify\'s order export never has one), so stalled '
            'tracking cannot be detected; group skipped rather than guessed from the ship date'
            + ('; orders shipped longer ago than the merchant\'s normal delivery time are listed in check_tracking instead'
               if shopify_only else '')
        )
    # Route A candidate rules. Each needs a number only the merchant can give.
    check_rules_skipped = {}
    if shopify_only:
        if normal_days is None:
            check_rules_skipped['possible_stall'] = (
                'no "normally delivered within N days" per country was given, so orders still In transit, '
                'Tracking added or No status are not compared with a normal delivery time; ask the merchant '
                'rather than assume one')
        if no_scan_days is None:
            check_rules_skipped['possible_not_scanned'] = (
                'no number of days was given after which Tracking added or No status looks like the carrier '
                'never scanned the parcel; ask the merchant rather than assume one')
        if ship_from is None:
            check_rules_skipped['possible_customs_hold'] = (
                'no ship-from country was given, so international orders cannot be told apart from domestic ones')
        elif normal_days is None:
            check_rules_skipped['possible_customs_hold'] = (
                'In transit orders are only customs candidates once past the normal delivery time, and none '
                'was given; Delayed international orders are still flagged')
    zones_without_normal = set()

    if not contacted:
        skipped['delivered_but_contacted'] = 'no contacted order list supplied; delivered orders are counted as on track'

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
        detail = o.get('tracking_detail', '')
        detail_l = detail.lower()
        ship = parse_date(o.get('ship_date'), date_fmt)
        last = parse_date(o.get('last_update'), date_fmt)
        zone = o.get('zone')

        entry = {
            'order_number': o['order_number'],
            'carrier': o.get('carrier') or None,
            'tracking_number': o.get('tracking_number') or None,
            'zone': zone or None,
            'status_in_file': status or None,
            'tracking_detail_in_file': detail or None,
            'ship_date': ship.isoformat() if ship else None,
            'last_update': last.isoformat() if last else None,
        }

        if len(o['_statuses']) > 1:
            needs_review.append({'order_number': o['order_number'], 'reason': (
                'the file gives this order more than one delivery status (' + ', '.join(o['_statuses']) +
                '); it may have more than one shipment, or appear in two filtered exports. Check it in Shopify admin')})
            continue
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
        text = status_l + ' | ' + detail_l
        customs_text = text
        for phrase in customs_released:
            customs_text = customs_text.replace(phrase, ' ')
        customs_matched = [] if 'customs_hold' in skipped else matched_keywords(customs_keywords, customs_text)
        problem_matched = matched_keywords(problem_keywords, text)
        days_stalled = (today - last).days if (last and 'tracking_stalled' not in skipped) else None
        is_late = days_late > 0
        is_customs = bool(customs_matched)
        is_problem = bool(problem_matched)
        is_stalled = days_stalled is not None and days_stalled > stall_days

        # Route A candidates: never asserted, only listed for a tracking check.
        check_reasons = []
        if shopify_only:
            days_since_ship = (today - ship).days if ship else None
            window = None
            if normal_days is not None:
                bz = normal_days.get('by_zone') or {}
                window = bz.get(zone) if zone in bz else normal_days.get('default')
                if window is None and status_l in STALL_CANDIDATE_STATUSES and not is_late:
                    zones_without_normal.add(zone or '(blank)')
            beyond = days_since_ship is not None and window is not None and days_since_ship > window
            international = bool(ship_from and zone and zone.strip().upper() != ship_from)
            if status_l in STALL_CANDIDATE_STATUSES and beyond:
                check_reasons.append({'rule': 'possible_stall', 'why': (
                    f'status {status}, fulfilled {days_since_ship} days ago; you said orders to {zone} are '
                    f'normally delivered within {window} days')})
            if (status_l in NO_SCAN_STATUSES and no_scan_days is not None and days_since_ship is not None
                    and days_since_ship > no_scan_days):
                check_reasons.append({'rule': 'possible_not_scanned', 'why': (
                    f'status {status} {days_since_ship} days after Fulfilled at (your limit is {no_scan_days}); '
                    f'the carrier may never have scanned it')})
            if international and status_l in CUSTOMS_CANDIDATE_STATUSES and (
                    status_l == 'delayed' or beyond or is_late):
                check_reasons.append({'rule': 'possible_customs_hold', 'why': (
                    f'international ({ship_from} to {zone}) and {status}'
                    + ('' if status_l == 'delayed' else ' past the normal delivery time')
                    + '; Shopify statuses never say customs, so check the carrier tracking')})
            if days_since_ship is not None:
                entry['days_since_ship'] = days_since_ship

        flags = []
        if key in contacted:
            flags.append('shopper_already_contacted')
        if is_late:
            entry['days_late'] = days_late
        if is_customs:
            entry['customs_keywords_matched'] = customs_matched
        if is_problem:
            entry['problem_keywords_matched'] = problem_matched
        if is_stalled:
            entry['days_stalled'] = days_stalled

        if is_late:
            group = 'past_promised_date'
        elif is_customs:
            group = 'customs_hold'
        elif is_problem:
            group = 'delivery_problem'
        elif is_stalled:
            group = 'tracking_stalled'
        elif check_reasons:
            group = 'check_tracking'
            entry['check_reasons'] = check_reasons
        else:
            on_track += 1
            if key in contacted:
                contacted_on_track.append(o['order_number'])
            continue
        flags += [g for g, hit in (('customs_hold', is_customs), ('delivery_problem', is_problem),
                                   ('tracking_stalled', is_stalled)) if hit and g != group]
        if group != 'check_tracking':
            # A late or delivery-problem order that also meets a route A
            # candidate rule keeps its group; the rules show as flags.
            flags += [r['rule'] for r in check_reasons]
        entry['flags'] = flags
        groups[group].append(entry)

    # ---- rank ------------------------------------------------------------
    groups['past_promised_date'].sort(key=lambda e: (-e['days_late'], norm_order(e['order_number'])))
    groups['customs_hold'].sort(key=lambda e: (e['ship_date'] or '9999', norm_order(e['order_number'])))
    groups['delivery_problem'].sort(key=lambda e: (e['promised_date'], norm_order(e['order_number'])))
    groups['tracking_stalled'].sort(key=lambda e: (-e['days_stalled'], norm_order(e['order_number'])))
    groups['check_tracking'].sort(key=lambda e: (-(e.get('days_since_ship') or 0), norm_order(e['order_number'])))
    groups['delivered_but_contacted'].sort(key=lambda e: norm_order(e['order_number']))

    urgency = []
    for g in GROUP_ORDER:
        for e in groups[g]:
            urgency.append({'rank': len(urgency) + 1, 'order_number': e['order_number'], 'group': g})

    output = {
        'today': today.isoformat(),
        'rows_read': len(rows),
        'orders_read': len(orders),
        'data_source': data_source,
        'column_mapping': mapping,
        'settings': {
            'stall_days': stall_days,
            'promise': promise,
            'delivered_values': delivered_values,
            'customs_keywords': customs_keywords,
            'customs_released_phrases': customs_released,
            'problem_keywords': problem_keywords,
            'contacted_orders_supplied': len(contacted),
            'ship_from_country': ship_from,
            'normal_transit_days': normal_days,
            'no_scan_days': no_scan_days,
        },
        'counts': {**{g: len(groups[g]) for g in GROUP_ORDER}, 'on_track': on_track, 'needs_review': len(needs_review)},
        'skipped_groups': skipped,
        'limits': limits + ([
            'no normal delivery time for zone(s) ' + ', '.join(sorted(zones_without_normal)) +
            ', so their In transit, Tracking added and No status orders were not checked for a possible stall'
        ] if zones_without_normal else []),
        'check_tracking_rules_skipped': check_rules_skipped,
        'check_tracking_next_step': (
            'These are candidates, not confirmed problems. Open each order in Shopify admin and click its tracking '
            'number to see the carrier\'s tracking page before messaging the shopper. Then: '
            + '; '.join(CHECK_TRACKING_NEXT.values()) + '.') if shopify_only else None,
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
