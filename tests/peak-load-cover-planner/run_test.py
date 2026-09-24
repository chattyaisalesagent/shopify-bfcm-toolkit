#!/usr/bin/env python3
"""
Run plan.py on fixture.json and compare against expected.json, whose numbers
were worked out by hand. Standard library only. Exit 0 on pass, 1 on fail.

Usage:
    python3 tests/peak-load-cover-planner/run_test.py
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
SCRIPT = os.path.join(ROOT, 'skills', 'peak-load-cover-planner', 'scripts', 'plan.py')

failures = []


def check(label, got, want):
    if isinstance(want, float) or isinstance(got, float):
        ok = abs(float(got) - float(want)) < 1e-9
    else:
        ok = got == want
    print(f"{'PASS' if ok else 'FAIL'}  {label}: got {got!r}, want {want!r}")
    if not ok:
        failures.append(label)


def main():
    proc = subprocess.run([sys.executable, SCRIPT, os.path.join(HERE, 'fixture.json')],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        print(f'FAIL  plan.py exited {proc.returncode}: {proc.stderr}')
        sys.exit(1)
    res = json.loads(proc.stdout)
    with open(os.path.join(HERE, 'expected.json')) as f:
        exp = json.load(f)

    check('window', res['window'], exp['window'])
    check('BFCM-week level', res['baseline']['this_year_bfcm_level_per_day'],
          exp['this_year_bfcm_level_per_day'])

    by_date = {r['date']: r for r in res['days']}
    for d, w in exp['days'].items():
        r = by_date[d]
        check(f'{d} forecast', r['forecast_conversations'], w['forecast'])
        check(f'{d} hours needed', r['required_agent_hours'], w['required'])
        check(f'{d} hours available', r['available_agent_hours'], w['available'])
        check(f'{d} gap', r['gap_hours'], w['gap'])
        if 'on_shift' in w:
            check(f'{d} on shift', r['on_shift'], w['on_shift'])
        if 'uncovered' in w:
            check(f'{d} uncovered hours', r['uncovered_hours_of_day'], w['uncovered'])

    totals = {p['phase']: p['total_forecast'] for p in res['phase_summary']}
    for p, t in exp['phase_totals'].items():
        check(f'phase total {p}', totals.get(p), t)

    months = {m['month']: m for m in res['cost']['months']}
    for ym, w in exp['cost'].items():
        if ym == 'total_estimated_bill':
            continue
        for k, v in w.items():
            check(f'cost {ym} {k}', months[ym][k], v)
    check('total estimated bill', res['cost']['total_estimated_bill'], exp['cost']['total_estimated_bill'])

    # Every gap day listed must be a GAP day, and vice versa.
    gap_dates = [g['date'] for g in res['gap_days']]
    check('gap_days matches GAP rows', gap_dates,
          [r['date'] for r in res['days'] if r['status'] == 'GAP'])

    # Validation: an unlabelled assumption must be refused, not defaulted.
    bad = json.load(open(os.path.join(HERE, 'fixture.json')))
    bad['growth_pct']['source'] = 'industry average'
    tmp = os.path.join(HERE, '_bad.json')
    with open(tmp, 'w') as f:
        json.dump(bad, f)
    p2 = subprocess.run([sys.executable, SCRIPT, tmp], capture_output=True, text=True)
    os.remove(tmp)
    check('unlabelled assumption rejected (exit 3)', p2.returncode, 3)

    print()
    if failures:
        print(f'{len(failures)} check(s) failed')
        sys.exit(1)
    print('all checks passed')


if __name__ == '__main__':
    main()
