#!/usr/bin/env python3
"""
Summarise a Shopify order export into the evidence the readiness audit needs.
Deterministic: same CSV always gives the same JSON, and every number can be
checked by hand against the rows. No network access, standard library only.

What it reads (Shopify admin, Orders, Export, "All orders" or a date range,
"CSV for Excel, Numbers, or other spreadsheet programs"):
  Name, Created at, Fulfilled at, Fulfillment Status, Cancelled at,
  Refunded Amount, Discount Code, Shipping Method, Shipping Country,
  Lineitem requires shipping.
Shopify writes one row per line item with order-level fields on the first
row only, so rows are merged by order Name.

What it cannot see, and says so in `limits`: tracking numbers, carriers and
delivery status are not in Shopify's order export, and neither are chats,
tickets or the text of any policy.

Output (JSON on stdout):
  range          first and last order date in the file
  seasons        per peak season found in the file (Nov 15 to Jan 15):
                 orders, busiest day, orders per day, busiest 7 days,
                 days from order to fulfilment (median, 90th percentile),
                 cancelled and refunded orders
  recent         the last 60 days of the file: orders, fulfilment days,
                 orders still unfulfilled more than 3 days after they were
                 placed (counted against the file's last order date)
  regions        orders per shipping country (line 2 needs an order-by date
                 for each country the store ships to)
  ships_goods    share of orders with at least one line that requires
                 shipping (line 3 is Not applicable only if this is 0)
  discount_codes orders per code, and orders that used more than one code
  shipping_methods orders per method
  limits         what this file cannot show

Usage:
    python3 orders_summary.py <orders_export.csv>
    python3 orders_summary.py <orders_export.csv> --out summary.json

Exit codes: 0 ok, 2 file missing or not CSV, 3 required columns missing.
"""
import argparse
import csv
import json
import sys
from collections import Counter
from datetime import date, timedelta

COLUMNS = {
    'name': ['Name', 'Order', 'Order Name'],
    'created': ['Created at', 'Created At'],
    'fulfilled': ['Fulfilled at', 'Fulfilled At'],
    'fulfillment_status': ['Fulfillment Status'],
    'cancelled': ['Cancelled at', 'Cancelled At'],
    'refunded': ['Refunded Amount'],
    'discount_code': ['Discount Code'],
    'shipping_method': ['Shipping Method'],
    'country': ['Shipping Country'],
    'requires_shipping': ['Lineitem requires shipping'],
}
REQUIRED = ['name', 'created']
UNFULFILLED_AFTER_DAYS = 3


def parse_day(s):
    """Date part of Shopify's '2025-11-28 10:15:00 -0500'. The export writes
    the store's own timezone, so the date part is the store's calendar day."""
    s = (s or '').strip()
    if len(s) < 10:
        return None
    try:
        y, m, d = (int(x) for x in s[:10].split('-'))
        return date(y, m, d)
    except ValueError:
        return None


def money(s):
    try:
        return float((s or '').replace(',', '').strip() or 0)
    except ValueError:
        return 0.0


def percentile(values, p):
    if not values:
        return None
    v = sorted(values)
    k = max(0, min(len(v) - 1, round(p / 100 * (len(v) - 1))))
    return v[k]


def median(values):
    if not values:
        return None
    v = sorted(values)
    n = len(v)
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2


def load(path):
    try:
        with open(path, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            rows = list(reader)
    except (OSError, csv.Error, UnicodeDecodeError) as e:
        print(f'error: cannot read {path}: {e}', file=sys.stderr)
        sys.exit(2)
    lower = {h.strip().lower(): h for h in headers}
    mapping = {k: next((lower[a.lower()] for a in al if a.lower() in lower), None) for k, al in COLUMNS.items()}
    missing = [COLUMNS[k][0] for k in REQUIRED if not mapping[k]]
    if missing:
        print(f'error: not a Shopify order export, missing column(s): {", ".join(missing)}', file=sys.stderr)
        sys.exit(3)
    orders, seq = {}, []
    for row in rows:
        name = (row.get(mapping['name']) or '').strip()
        if not name:
            continue
        if name not in orders:
            orders[name] = {'name': name, 'ships': False}
            seq.append(name)
        o = orders[name]
        for k, h in mapping.items():
            if not h or k in ('name', 'requires_shipping'):
                continue
            val = (row.get(h) or '').strip()
            if val and not o.get(k):
                o[k] = val
        if mapping['requires_shipping'] and (row.get(mapping['requires_shipping']) or '').strip().lower() == 'true':
            o['ships'] = True
    out = []
    for n in seq:
        o = orders[n]
        o['created_day'] = parse_day(o.get('created'))
        o['fulfilled_day'] = parse_day(o.get('fulfilled'))
        if o['created_day']:
            out.append(o)
    return out, mapping


def fulfil_days(orders):
    return [(o['fulfilled_day'] - o['created_day']).days for o in orders
            if o['fulfilled_day'] and not o.get('cancelled')]


def block(orders):
    fd = fulfil_days(orders)
    return {
        'orders': len(orders),
        'days_to_fulfil_median': median(fd),
        'days_to_fulfil_p90': percentile(fd, 90),
        'fulfilled_orders_measured': len(fd),
        'cancelled': sum(1 for o in orders if o.get('cancelled')),
        'refunded': sum(1 for o in orders if money(o.get('refunded')) > 0),
    }


def season_blocks(orders):
    years = sorted({o['created_day'].year for o in orders if o['created_day'].month in (11, 12)})
    result = []
    for y in years:
        start, end = date(y, 11, 15), date(y + 1, 1, 15)
        inside = [o for o in orders if start <= o['created_day'] <= end]
        if not inside:
            continue
        per_day = Counter(o['created_day'] for o in inside)
        days = [start + timedelta(d) for d in range((end - start).days + 1)]
        series = [per_day.get(d, 0) for d in days]
        best7 = max(range(len(series) - 6), key=lambda i: (sum(series[i:i + 7]), -i))
        busiest = max(days, key=lambda d: (per_day.get(d, 0), -d.toordinal()))
        b = block(inside)
        b.update({
            'season': f'{start.isoformat()} to {end.isoformat()}',
            'busiest_day': busiest.isoformat(),
            'busiest_day_orders': per_day.get(busiest, 0),
            'busiest_7_days': f'{days[best7].isoformat()} to {days[best7 + 6].isoformat()}',
            'busiest_7_days_orders': sum(series[best7:best7 + 7]),
            'orders_per_day': {d.isoformat(): per_day.get(d, 0) for d in days},
            # A date-range export starts at its first order, not at Nov 15, so
            # allow a week of slack at each end before calling the season partial.
            'covers_whole_season': min(o['created_day'] for o in orders) <= start + timedelta(7) and max(o['created_day'] for o in orders) >= end - timedelta(7),
        })
        result.append(b)
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    ap.add_argument('csv')
    ap.add_argument('--out')
    args = ap.parse_args()
    orders, mapping = load(args.csv)
    if not orders:
        print('error: no orders with a readable "Created at" date', file=sys.stderr)
        sys.exit(3)

    first = min(o['created_day'] for o in orders)
    last = max(o['created_day'] for o in orders)
    recent_from = last - timedelta(days=59)
    recent = [o for o in orders if o['created_day'] >= recent_from]
    rb = block(recent)
    rb['from'] = recent_from.isoformat()
    rb['to'] = last.isoformat()
    rb['unfulfilled_over_3_days'] = sorted(
        o['name'] for o in recent
        if o['ships'] and not o.get('cancelled') and not o['fulfilled_day']
        and (o.get('fulfillment_status') or '').lower() != 'fulfilled'
        and (last - o['created_day']).days > UNFULFILLED_AFTER_DAYS)

    codes, multi = Counter(), 0
    for o in orders:
        cs = [c.strip() for c in (o.get('discount_code') or '').split(',') if c.strip()]
        codes.update(set(cs))
        multi += len(set(cs)) > 1

    limits = [
        'No tracking numbers, carriers or delivery status: Shopify\'s order export does not include them. Line 3 and line 8 need the Order status page tested by hand, or a connected store.',
        'No chats, tickets or emails: what shoppers asked comes from the chat or helpdesk export, or from the merchant.',
        'No policy or sale terms text: read it from the connected store or ask the merchant to paste it.',
    ]
    for k in ('fulfilled', 'discount_code', 'country', 'requires_shipping'):
        if not mapping[k]:
            limits.append(f'Column "{COLUMNS[k][0]}" is missing, so the numbers that depend on it are left out.')
    seasons = season_blocks(orders)
    if not any(s['covers_whole_season'] for s in seasons):
        limits.append('No full peak season (Nov 15 to Jan 15) in this file. Export last year\'s November to January for a volume baseline.')

    summary = {
        'file': args.csv,
        'range': {'first_order': first.isoformat(), 'last_order': last.isoformat(), 'orders': len(orders)},
        'seasons': seasons,
        'recent': rb,
        'regions': dict(Counter(o.get('country') or 'unknown' for o in orders if o['ships']).most_common()),
        'ships_goods': round(sum(o['ships'] for o in orders) / len(orders), 3) if mapping['requires_shipping'] else None,
        'discount_codes': {'orders_per_code': dict(codes.most_common()), 'orders_with_more_than_one_code': multi},
        'shipping_methods': dict(Counter(o.get('shipping_method') or 'none' for o in orders).most_common()),
        'limits': limits,
    }
    text = json.dumps(summary, indent=2)
    if args.out:
        with open(args.out, 'w') as f:
            f.write(text + '\n')
    print(text)


if __name__ == '__main__':
    main()
