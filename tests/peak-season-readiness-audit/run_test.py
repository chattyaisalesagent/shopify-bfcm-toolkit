#!/usr/bin/env python3
"""
Answer-key test for skills/peak-season-readiness-audit/scripts/orders_summary.py.
No AI grading. orders_export.csv uses Shopify's real order-export header, one
row per line item, and has every number below worked out by hand:

  2025 season (11 orders): Nov 28 x5, Nov 29 x3, Dec 1 x2, Dec 20 x1.
    Days to fulfil, cancelled #120 left out: 2,3,3,3,3,4,5,6,7,7
    -> median 3.5, 90th percentile 7. One cancelled, one refunded.
    Busiest 7 days: first window holding 10 orders, Nov 25 to Dec 1.
    The file starts Nov 28 and ends in September, so the season is partial.
  Last 60 days (Jul 31 to Sep 28 2026, 5 orders): #201 unfulfilled 6 days
    -> flagged; #202 only 2 days -> not; #203 digital -> not.
  Regions count shipping orders only: US 12, CA 2, GB 1.
  #104 used "BF20, WELCOME10" -> one order with more than one code.

Usage:  python3 tests/peak-season-readiness-audit/run_test.py
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, '..', '..', 'skills', 'peak-season-readiness-audit', 'scripts', 'orders_summary.py')
failures, passed = [], 0


def check(cond, msg):
    global passed
    if cond:
        passed += 1
    else:
        failures.append(msg)


def run(path):
    return subprocess.run([sys.executable, SCRIPT, path], capture_output=True, text=True)


r = run(os.path.join(HERE, 'orders_export.csv'))
check(r.returncode == 0, f'exit {r.returncode}: {r.stderr}')
d = json.loads(r.stdout)
s = d['seasons'][0]
check(len(d['seasons']) == 1, 'one season')
check(s['orders'] == 11, f"season orders {s['orders']}")
check(s['days_to_fulfil_median'] == 3.5, f"median {s['days_to_fulfil_median']}")
check(s['days_to_fulfil_p90'] == 7, f"p90 {s['days_to_fulfil_p90']}")
check(s['cancelled'] == 1 and s['refunded'] == 1, 'cancelled/refunded')
check(s['busiest_day'] == '2025-11-28' and s['busiest_day_orders'] == 5, 'busiest day')
check(s['busiest_7_days'] == '2025-11-25 to 2025-12-01' and s['busiest_7_days_orders'] == 10, 'busiest 7 days')
check(s['covers_whole_season'] is False, 'partial season flagged')
check(any('No full peak season' in l for l in d['limits']), 'partial season named in limits')
check(d['recent']['orders'] == 5, f"recent orders {d['recent']['orders']}")
check(d['recent']['unfulfilled_over_3_days'] == ['#201'], f"unfulfilled {d['recent']['unfulfilled_over_3_days']}")
check(d['regions'] == {'US': 12, 'CA': 2, 'GB': 1}, f"regions {d['regions']}")
check(d['ships_goods'] == 0.938, f"ships_goods {d['ships_goods']}")
check(d['discount_codes']['orders_per_code'] == {'BF20': 8, 'WELCOME10': 2}, 'codes')
check(d['discount_codes']['orders_with_more_than_one_code'] == 1, 'multi-code')
check(any('tracking' in l for l in d['limits']), 'tracking limit stated')

bad = os.path.join(HERE, '_not_orders.csv')
with open(bad, 'w') as f:
    f.write('foo,bar\n1,2\n')
r = run(bad)
os.remove(bad)
check(r.returncode == 3 and 'Created at' in r.stderr, 'exit 3 on a file that is not an order export')

print(f'{passed} passed, {len(failures)} failed')
for m in failures:
    print('FAIL', m)
sys.exit(1 if failures else 0)
