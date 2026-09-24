#!/usr/bin/env python3
"""
Answer-key test for skills/shipping-exception-watch/scripts/watch.py.
No AI grading: runs the script on orders.csv + config.json and compares every
order's group, the days late/stalled, the urgency order, and the privacy rule
against expected.json. Also checks the missing-column path exits with code 3.

Usage:  python3 tests/shipping-exception-watch/run_test.py
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, '..', '..', 'skills', 'shipping-exception-watch', 'scripts', 'watch.py')
CSV = os.path.join(HERE, 'orders.csv')
CONFIG = os.path.join(HERE, 'config.json')

failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)


with open(os.path.join(HERE, 'expected.json')) as f:
    expected = json.load(f)

proc = subprocess.run([sys.executable, SCRIPT, CSV, CONFIG], capture_output=True, text=True)
if proc.returncode != 0:
    print(proc.stderr)
    sys.exit(f'FAIL: watch.py exited {proc.returncode}')
out = json.loads(proc.stdout)

# 1. group membership for every order
actual = {}
for group, entries in out['groups'].items():
    for e in entries:
        check(e['order_number'] not in actual, f"{e['order_number']} appears in more than one group")
        actual[e['order_number']] = group
for item in out['needs_review']:
    actual[item['order_number']] = 'needs_review'
for num, group in expected['groups'].items():
    got = actual.get(num, 'on_track')
    check(got == group, f'{num}: expected {group}, got {got}')
check(out['counts']['on_track'] == sum(1 for g in expected['groups'].values() if g == 'on_track'),
      f"on_track count {out['counts']['on_track']} does not match expected")
check(out['orders_read'] == len(expected['groups']), f"orders_read {out['orders_read']} != {len(expected['groups'])}")

# 2. days late / stalled
by_num = {e['order_number']: e for entries in out['groups'].values() for e in entries}
for num, days in expected['days_late'].items():
    check(by_num.get(num, {}).get('days_late') == days, f'{num}: days_late expected {days}, got {by_num.get(num, {}).get("days_late")}')
for num, days in expected['days_stalled'].items():
    check(by_num.get(num, {}).get('days_stalled') == days, f'{num}: days_stalled expected {days}, got {by_num.get(num, {}).get("days_stalled")}')

# 3. urgency order
got_order = [r['order_number'] for r in out['urgency_rank']]
check(got_order == expected['urgency_order'], f'urgency order {got_order} != {expected["urgency_order"]}')
check(out['contacted_but_on_track'] == expected['contacted_but_on_track'], 'contacted_but_on_track mismatch')
check(out['contacted_orders_not_in_file'] == expected['contacted_orders_not_in_file'], 'contacted_orders_not_in_file mismatch')

# 4. privacy: no email, phone or street address anywhere in the output
for needle in ['@example.com', '+1-555', '+61-555', 'Sample Street', 'Sample Road', 'Sample Avenue', 'Testerson']:
    check(needle not in proc.stdout, f'privacy: output contains "{needle}"')

# 5. missing column -> exit 3 with the column named
with tempfile.TemporaryDirectory() as tmp:
    bad_csv = os.path.join(tmp, 'no_status.csv')
    with open(CSV) as src, open(bad_csv, 'w') as dst:
        for line in src:
            cols = line.rstrip('\n').split(',')
            dst.write(','.join(cols[:11] + cols[12:]) + '\n')  # drop Shipment Status
    p = subprocess.run([sys.executable, SCRIPT, bad_csv, CONFIG], capture_output=True, text=True)
    check(p.returncode == 3, f'missing-column run exited {p.returncode}, expected 3')
    check('delivery_status' in p.stderr, 'missing-column error does not name delivery_status')

    # 6. stall_days absent from config -> exit 3 (must be asked, never defaulted)
    cfg = json.load(open(CONFIG))
    del cfg['stall_days']
    cfg_path = os.path.join(tmp, 'no_stall.json')
    json.dump(cfg, open(cfg_path, 'w'))
    p = subprocess.run([sys.executable, SCRIPT, CSV, cfg_path], capture_output=True, text=True)
    check(p.returncode == 3 and 'stall_days' in p.stderr, 'missing stall_days did not exit 3')

    # 7. no last-update column -> tracking_stalled skipped, not guessed
    no_last = os.path.join(tmp, 'no_last.csv')
    with open(CSV) as src, open(no_last, 'w') as dst:
        for line in src:
            cols = line.rstrip('\n').split(',')
            dst.write(','.join(cols[:12] + cols[13:]) + '\n')  # drop Last Tracking Update
    p = subprocess.run([sys.executable, SCRIPT, no_last, CONFIG], capture_output=True, text=True)
    o = json.loads(p.stdout) if p.returncode == 0 else {}
    check('tracking_stalled' in o.get('skipped_groups', {}) and o.get('counts', {}).get('tracking_stalled') == 0,
          'without a last-update column the stalled group was not skipped')

total = len(expected['groups'])
if failures:
    print(f'FAIL: {len(failures)} problem(s)')
    for f_ in failures:
        print('  - ' + f_)
    sys.exit(1)
print(f'PASS: {total}/{total} orders in the expected group; urgency order, days late/stalled, '
      f'privacy, missing-column (exit 3), missing stall_days (exit 3) and no-tracking-data skip all correct')
