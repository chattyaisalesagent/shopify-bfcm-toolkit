#!/usr/bin/env python3
"""
Answer-key test for skills/shipping-exception-watch/scripts/watch.py.
No AI grading. Two fixtures, one per input route the skill tells merchants to use:

  route (a)  route_a_shopify_export.csv: a real 71-column Shopify order export
             (no tracking, carrier, scan date or delivery status columns) plus
             one added "Delivery Status" column holding the value of the admin
             Orders "Delivery status" filter. Customs and stalled tracking must
             be reported as skipped, the order Notes column must never trigger
             customs, and Failed / Attempted / Delayed must be caught.
  route (a+) route_a_check_tracking.csv: a trimmed Shopify export (US store
             shipping to US, CA, GB) with the merchant's normal delivery
             days, no-scan days and ship-from country. Stall and customs
             candidates land in check_tracking, never in customs_hold or
             tracking_stalled; each rule is skipped when its number is
             missing; precedence late > delivery_problem > check_tracking.
  route (b)  route_b_tracking_export.csv: a tracking-app style export with the
             status detail mapped explicitly as tracking_detail. Customs and
             stalled tracking fire here, and only here.

Also checks the exit-3 paths and that tracking_detail is never auto-mapped.

Usage:  python3 tests/shipping-exception-watch/run_test.py
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, '..', '..', 'skills', 'shipping-exception-watch', 'scripts', 'watch.py')

failures = []
passed = 0


def check(cond, msg):
    global passed
    if cond:
        passed += 1
    else:
        failures.append(msg)


def run(csv_path, cfg):
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
        json.dump(cfg, f)
        cfg_path = f.name
    try:
        return subprocess.run([sys.executable, SCRIPT, csv_path, cfg_path], capture_output=True, text=True)
    finally:
        os.unlink(cfg_path)


def load(name):
    with open(os.path.join(HERE, name)) as f:
        return json.load(f)


def check_answer_key(route, csv_name, cfg, expected):
    proc = run(os.path.join(HERE, csv_name), cfg)
    if proc.returncode != 0:
        failures.append(f'route {route}: watch.py exited {proc.returncode}: {proc.stderr.strip()}')
        return None
    out = json.loads(proc.stdout)
    tag = f'route {route}'

    check(out['data_source'] == expected['data_source'], f"{tag}: data_source {out['data_source']} != {expected['data_source']}")
    check(sorted(k for k in out['skipped_groups'] if k != 'delivered_but_contacted') == sorted(expected['skipped']),
          f"{tag}: skipped groups {sorted(out['skipped_groups'])} != {expected['skipped']}")

    actual = {}
    for group, entries in out['groups'].items():
        for e in entries:
            check(e['order_number'] not in actual, f"{tag}: {e['order_number']} appears in more than one group")
            actual[e['order_number']] = group
    for item in out['needs_review']:
        actual[item['order_number']] = 'needs_review'
    for num, group in expected['groups'].items():
        got = actual.get(num, 'on_track')
        check(got == group, f'{tag}: {num} expected {group}, got {got}')
    check(out['counts']['on_track'] == sum(1 for g in expected['groups'].values() if g == 'on_track'),
          f"{tag}: on_track count {out['counts']['on_track']} does not match expected")
    check(out['orders_read'] == len(expected['groups']), f"{tag}: orders_read {out['orders_read']} != {len(expected['groups'])}")

    by_num = {e['order_number']: e for entries in out['groups'].values() for e in entries}
    for num, days in expected['days_late'].items():
        check(by_num.get(num, {}).get('days_late') == days, f'{tag}: {num} days_late expected {days}, got {by_num.get(num, {}).get("days_late")}')
    for num, days in expected['days_stalled'].items():
        check(by_num.get(num, {}).get('days_stalled') == days, f'{tag}: {num} days_stalled expected {days}, got {by_num.get(num, {}).get("days_stalled")}')
    for num, flags in expected['flags'].items():
        check(by_num.get(num, {}).get('flags') == flags, f'{tag}: {num} flags expected {flags}, got {by_num.get(num, {}).get("flags")}')
    for num, rules in expected.get('check_reasons', {}).items():
        got = [r['rule'] for r in by_num.get(num, {}).get('check_reasons', [])]
        check(got == rules, f'{tag}: {num} check_reasons expected {rules}, got {got}')
        check(all(r.get('why') for r in by_num.get(num, {}).get('check_reasons', [])), f'{tag}: {num} a check reason has no why')

    got_order = [r['order_number'] for r in out['urgency_rank']]
    check(got_order == expected['urgency_order'], f'{tag}: urgency order {got_order} != {expected["urgency_order"]}')
    check(out['contacted_but_on_track'] == expected['contacted_but_on_track'], f'{tag}: contacted_but_on_track mismatch')
    check(out['contacted_orders_not_in_file'] == expected['contacted_orders_not_in_file'], f'{tag}: contacted_orders_not_in_file mismatch')

    for needle in expected['privacy_needles']:
        check(needle not in proc.stdout, f'{tag}: privacy: output contains "{needle}"')
    return out


# ---- route (a): Shopify export + Delivery Status column ------------------
cfg_a = load('config_route_a.json')
out_a = check_answer_key('a', 'route_a_shopify_export.csv', cfg_a, load('expected_route_a.json'))
if out_a:
    check(out_a['column_mapping']['tracking_detail'] is None, 'route a: Notes was auto-mapped as tracking detail')
    check(out_a['counts']['customs_hold'] == 0 and out_a['counts']['tracking_stalled'] == 0,
          'route a: customs or stalled fired on Shopify-only data')

# route (a) with a stall number given: still skipped, because there is no scan date
cfg = dict(cfg_a, stall_days=4)
p = run(os.path.join(HERE, 'route_a_shopify_export.csv'), cfg)
o = json.loads(p.stdout) if p.returncode == 0 else {}
check('tracking_stalled' in o.get('skipped_groups', {}) and 'last-tracking-update' in o['skipped_groups']['tracking_stalled'],
      'route a with stall_days 4: stalled group not skipped for lack of a scan date')

# route (a) where the merchant (wrongly) maps the order Notes as tracking detail:
# the file is no longer Shopify-only, so customs runs, and the note does match.
# This documents why the mapping must be explicit and checked by a person.
cfg = dict(cfg_a, columns={'tracking_detail': 'Notes'})
p = run(os.path.join(HERE, 'route_a_shopify_export.csv'), cfg)
o = json.loads(p.stdout) if p.returncode == 0 else {}
check(o.get('column_mapping', {}).get('tracking_detail') == 'Notes', 'explicit tracking_detail mapping was not honoured')

# route (a) with no candidate numbers given: nothing is invented, every
# candidate rule is reported as skipped with a reason.
check(out_a is not None and out_a['counts']['check_tracking'] == 0, 'route a without numbers: check_tracking not empty')
check(out_a is not None and sorted(out_a['check_tracking_rules_skipped']) ==
      ['possible_customs_hold', 'possible_not_scanned', 'possible_stall'],
      f"route a without numbers: skipped rules {sorted((out_a or {}).get('check_tracking_rules_skipped', {}))}")

# route (a) 71-column export with the candidate numbers on: Notes still never
# read, names still never printed, and the candidates are the expected ones.
cfg = dict(cfg_a, ship_from_country='US', normal_transit_days={'by_zone': {'US': 4, 'AU': 10}}, no_scan_days=3)
p = run(os.path.join(HERE, 'route_a_shopify_export.csv'), cfg)
o = json.loads(p.stdout) if p.returncode == 0 else {}
ct = {e['order_number']: [r['rule'] for r in e['check_reasons']] for e in o.get('groups', {}).get('check_tracking', [])}
check(ct == {'#2009': ['possible_stall'], '#2013': ['possible_stall'], '#2011': ['possible_not_scanned']},
      f'route a 71-col with numbers: check_tracking {ct}')
check(o.get('counts', {}).get('customs_hold') == 0, 'route a 71-col: customs_hold fired')
check(o.get('limits') == [], f"route a 71-col: late or Delayed orders reported as unchecked zones: {o.get('limits')}")
for needle in load('expected_route_a.json')['privacy_needles']:
    check(needle not in p.stdout, f'route a 71-col with numbers: privacy: output contains "{needle}"')

# ---- route (a+): check_tracking candidates ---------------------------------
cfg_c = load('config_route_a_check.json')
out_c = check_answer_key('a+', 'route_a_check_tracking.csv', cfg_c, load('expected_route_a_check.json'))
if out_c:
    check(out_c['counts']['customs_hold'] == 0 and out_c['counts']['tracking_stalled'] == 0,
          'route a+: candidates were asserted as customs_hold or tracking_stalled')
    check(out_c['check_tracking_rules_skipped'] == {}, 'route a+: a rule was skipped although every number was given')
    nxt = out_c.get('check_tracking_next_step') or ''
    check('tracking' in nxt and 'Held at customs' in nxt and 'Tracking stalled' in nxt and 'Delivery problem' in nxt,
          'route a+: check_tracking_next_step does not point to the tracking page and the existing templates')

def groups_of(o):
    g = {e['order_number']: k for k, es in o.get('groups', {}).items() for e in es}
    g.update({n['order_number']: 'needs_review' for n in o.get('needs_review', [])})
    return g

def reasons_of(o, num):
    return [r['rule'] for e in o.get('groups', {}).get('check_tracking', []) if e['order_number'] == num for r in e['check_reasons']]

def flags_of(o, num):
    return next((e['flags'] for es in o.get('groups', {}).values() for e in es if e['order_number'] == num), None)

csv_c = os.path.join(HERE, 'route_a_check_tracking.csv')

# No "normally delivered within N days" given: the stall rule is skipped and
# says why; nothing is inferred from the ship date. The no-scan rule still runs.
cfg = dict(cfg_c, normal_transit_days=None)
p = run(csv_c, cfg); o = json.loads(p.stdout) if p.returncode == 0 else {}
g = groups_of(o)
check('possible_stall' in o.get('check_tracking_rules_skipped', {}), 'no N: possible_stall not reported as skipped')
check('ask the merchant' in o.get('check_tracking_rules_skipped', {}).get('possible_stall', ''), 'no N: skip reason does not say to ask the merchant')
check(all(g.get(n) is None for n in ('#3105', '#3109', '#3110')), f'no N: stall candidates still listed: {[(n, g.get(n)) for n in ("#3105", "#3109", "#3110")]}')
check(all(g.get(n) == 'check_tracking' for n in ('#3107', '#3113', '#3119')), 'no N: no-scan candidates lost')
check(g.get('#3104') == 'delivery_problem' and flags_of(o, '#3104') == ['possible_customs_hold'],
      'no N: international Delayed lost its possible_customs_hold flag')
check('possible_customs_hold' in o.get('check_tracking_rules_skipped', {}), 'no N: In transit customs rule not reported as limited')

# No no-scan number given: that rule is skipped.
cfg = dict(cfg_c, no_scan_days=None)
p = run(csv_c, cfg); o = json.loads(p.stdout) if p.returncode == 0 else {}
g = groups_of(o)
check('possible_not_scanned' in o.get('check_tracking_rules_skipped', {}), 'no no-scan days: rule not reported as skipped')
check(all(g.get(n) is None for n in ('#3107', '#3113', '#3119')), 'no no-scan days: Tracking added / No status still listed')
check(g.get('#3105') == 'check_tracking' and g.get('#3110') == 'check_tracking', 'no no-scan days: stall candidates lost')

# No ship-from country: nothing is called international.
cfg = dict(cfg_c, ship_from_country=None)
p = run(csv_c, cfg); o = json.loads(p.stdout) if p.returncode == 0 else {}
check('possible_customs_hold' in o.get('check_tracking_rules_skipped', {}), 'no ship-from: customs rule not reported as skipped')
check(reasons_of(o, '#3109') == ['possible_stall'], f"no ship-from: #3109 reasons {reasons_of(o, '#3109')}")
check(flags_of(o, '#3104') == [] and 'possible_customs_hold' not in (flags_of(o, '#3112') or []), 'no ship-from: a customs flag was set anyway')

# A Delayed order shipped to the ship-from country is a delivery problem,
# never a customs candidate, even when the merchant ships from CA.
cfg = dict(cfg_c, ship_from_country='CA')
p = run(csv_c, cfg); o = json.loads(p.stdout) if p.returncode == 0 else {}
check(groups_of(o).get('#3104') == 'delivery_problem' and flags_of(o, '#3104') == [],
      f"ship-from CA: domestic Delayed #3104 got {groups_of(o).get('#3104')} {flags_of(o, '#3104')}")
check('possible_customs_hold' in reasons_of(o, '#3105'), 'ship-from CA: US In transit past window not a customs candidate')

# A zone with no normal delivery time and no default: not checked, reported.
cfg = dict(cfg_c, normal_transit_days={'by_zone': {'US': 5}})
p = run(csv_c, cfg); o = json.loads(p.stdout) if p.returncode == 0 else {}
check(groups_of(o).get('#3110') is None and any('CA' in l and 'GB' in l for l in o.get('limits', [])),
      'zone without a normal time: order checked anyway or not reported in limits')

# Bad candidate numbers stop the run.
p = run(csv_c, dict(cfg_c, no_scan_days=0))
check(p.returncode == 3 and 'no_scan_days' in p.stderr, 'no_scan_days 0 did not exit 3')
p = run(csv_c, dict(cfg_c, normal_transit_days=7))
check(p.returncode == 3 and 'normal_transit_days' in p.stderr, 'normal_transit_days as a bare number did not exit 3')

# ---- route (b): tracking-app export ---------------------------------------
cfg_b = load('config_route_b.json')
out_b = check_answer_key('b', 'route_b_tracking_export.csv', cfg_b, load('expected_route_b.json'))
if out_b:
    check(out_b['column_mapping']['tracking_detail'] == 'Last Checkpoint Message', 'route b: tracking_detail mapping wrong')
    check(out_b['counts']['check_tracking'] == 0 and out_b['check_tracking_next_step'] is None,
          'route b: check_tracking fired on tracking-app data')

# route (b) with the route (a) candidate numbers set: ignored, same result.
cfg = dict(cfg_b, ship_from_country='US', normal_transit_days={'default': 2}, no_scan_days=1)
p = run(os.path.join(HERE, 'route_b_tracking_export.csv'), cfg)
o = json.loads(p.stdout) if p.returncode == 0 else {}
check(out_b is not None and o.get('groups') == out_b['groups'] and o.get('urgency_rank') == out_b['urgency_rank'],
      'route b: setting the route (a) candidate numbers changed the route (b) result')

# route (b) without the explicit tracking_detail mapping: nothing is auto-read
# from Notes or from the detail column; customs is found from the status column
# only, and the output says so in `limits`.
cfg = json.loads(json.dumps(cfg_b))
del cfg['columns']['tracking_detail']
p = run(os.path.join(HERE, 'route_b_tracking_export.csv'), cfg)
o = json.loads(p.stdout) if p.returncode == 0 else {}
grp = {e['order_number']: g for g, es in o.get('groups', {}).items() for e in es}
check(o.get('column_mapping', {}).get('tracking_detail') is None, 'route b: tracking_detail was auto-mapped')
check(grp.get('#1011') is None, 'route b: #1011 (Notes asks about customs fees) left on track')
check(grp.get('#1004') == 'delivery_problem', f"route b unmapped: #1004 'Exception' expected delivery_problem, got {grp.get('#1004')}")
check(grp.get('#1010') is None, 'route b unmapped: #1010 should be on track when the detail column is not read')
check(bool(o.get('limits')), 'route b unmapped: no limits note about the missing tracking_detail column')

# ---- exit-3 paths ---------------------------------------------------------
with tempfile.TemporaryDirectory() as tmp:
    # A plain Shopify export with no Delivery Status column added: stop, name the fix.
    src = os.path.join(HERE, 'route_a_shopify_export.csv')
    plain = os.path.join(tmp, 'plain_shopify.csv')
    import csv
    with open(src, newline='') as f_in, open(plain, 'w', newline='') as f_out:
        r, w = csv.reader(f_in), csv.writer(f_out)
        for row in r:
            w.writerow(row[:-1])
    p = run(plain, cfg_a)
    check(p.returncode == 3, f'plain Shopify export exited {p.returncode}, expected 3')
    check('delivery_status' in p.stderr and 'Delivery status' in p.stderr,
          'plain Shopify export error does not name delivery_status and the admin filter fix')

    cfg = dict(cfg_b)
    cfg.pop('stall_days')
    p = run(os.path.join(HERE, 'route_b_tracking_export.csv'), cfg)
    check(p.returncode == 3 and 'stall_days' in p.stderr, 'missing stall_days did not exit 3')

    cfg = json.loads(json.dumps(cfg_b))
    cfg['columns']['tracking_detail'] = 'Tracking Detail'
    p = run(os.path.join(HERE, 'route_b_tracking_export.csv'), cfg)
    check(p.returncode == 3 and 'tracking_detail' in p.stderr, 'mapping to a header that does not exist did not exit 3')

if failures:
    print(f'FAIL: {len(failures)} problem(s), {passed} checks passed')
    for f_ in failures:
        print('  - ' + f_)
    sys.exit(1)
print(f'PASS: {passed}/{passed} checks. Route (a) Shopify export + Delivery Status: customs and stalled skipped, '
      f'order Notes ignored, Failed/Attempted/Delayed caught, stall and customs candidates in check_tracking only '
      f'with the merchant\'s numbers. Route (b) tracking export: customs, stalled, '
      f'delivery problems, urgency order and days correct. Privacy and exit-3 paths correct.')
