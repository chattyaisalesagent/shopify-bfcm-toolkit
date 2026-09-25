#!/usr/bin/env python3
"""
Run plan.py on each fixture and compare against the expected_*.json files,
whose numbers were worked out by hand (the working is in each file's
"_how_these_were_computed"). Standard library only. Exit 0 on pass, 1 on fail.

Cases:
    fixture.json                  phase mode from orders, weekend split, backlog, bill
    fixture_daily_case_a.json     last year's daily series mapped day by day (Case A)
    fixture_new_store_case_b.json new store, hourly share, scenarios, 57-day run flag (Case B)
    fixture_roster_fill.json      draft roster fill with day off, run limit and weekly hours

Usage:
    python3 tests/peak-load-cover-planner/run_test.py
"""
import copy
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
        ok = got is not None and abs(float(got) - float(want)) < 1e-9
    else:
        ok = got == want
    print(f"{'PASS' if ok else 'FAIL'}  {label}: got {got!r}, want {want!r}")
    if not ok:
        failures.append(label)


def load(name):
    with open(os.path.join(HERE, name)) as f:
        return json.load(f)


def run_data(data, tag):
    tmp = os.path.join(HERE, f'_{tag}.json')
    with open(tmp, 'w') as f:
        json.dump(data, f)
    try:
        p = subprocess.run([sys.executable, SCRIPT, tmp], capture_output=True, text=True)
    finally:
        os.remove(tmp)
    return p


def run(name):
    p = subprocess.run([sys.executable, SCRIPT, os.path.join(HERE, name)], capture_output=True, text=True)
    if p.returncode != 0:
        print(f'FAIL  {name}: plan.py exited {p.returncode}: {p.stderr}')
        failures.append(name)
        return None
    # the Markdown path must also run
    m = subprocess.run([sys.executable, SCRIPT, os.path.join(HERE, name), '--markdown'],
                       capture_output=True, text=True)
    check(f'{name} markdown renders', m.returncode, 0)
    return json.loads(p.stdout)


def by_date(res):
    return {r['date']: r for r in res['days']}


def case_phase():
    print('\n== phase mode (fixture.json)')
    res = run('fixture.json')
    if not res:
        return
    exp = load('expected.json')
    check('window', res['window'], exp['window'])
    days = by_date(res)
    for d, w in exp['days'].items():
        r = days[d]
        check(f'{d} forecast', r['forecast_conversations'], w['forecast'])
        check(f'{d} hours needed', r['required_agent_hours'], w['required'])
        check(f'{d} hours available', r['available_agent_hours'], w['available'])
        check(f'{d} gap', r['gap_hours'], w['gap'])
        if 'on_shift' in w:
            check(f'{d} on shift', r['on_shift'], w['on_shift'])
        if 'uncovered' in w:
            check(f'{d} uncovered hours', r['uncovered_hours_of_day'], w['uncovered'])
        if 'backlog_end' in w:
            check(f'{d} backlog at end of day', r['backlog_end_hours'], w['backlog_end'])
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
    check('gap_days matches GAP rows', [g['date'] for g in res['gap_days']],
          [r['date'] for r in res['days'] if r['status'] == 'GAP'])

    # Weekend is not reduced twice: a phase's total equals its average day x days.
    check('BFCM-week total = 220 x 7 within rounding', abs(totals['bfcm_week'] - 1540) <= 3, True)

    # Validation: an unlabelled assumption must be refused, not defaulted.
    bad = load('fixture.json')
    bad['growth_pct']['source'] = 'industry average'
    check('unlabelled assumption rejected (exit 3)', run_data(bad, 'bad').returncode, 3)


def case_daily():
    print('\n== daily series mode (Case A)')
    res = run('fixture_daily_case_a.json')
    if not res:
        return
    exp = load('expected_daily_case_a.json')
    check('Case A forecast, all 57 days', [r['forecast_conversations'] for r in res['days']], exp['forecast_all'])
    days = by_date(res)
    check('Case A Black Friday 2026 forecast', days['2026-11-27']['forecast_conversations'], 198)
    for d, src in exp['matched'].items():
        check(f'{d} matched to last year', days[d]['matched_last_year_date'], src)
    for d, w in exp['days'].items():
        r = days[d]
        if 'required' in w:
            check(f'{d} hours needed', r['required_agent_hours'], w['required'])
        if 'available' in w:
            check(f'{d} hours available', r['available_agent_hours'], w['available'])
        if 'gap' in w:
            check(f'{d} gap', r['gap_hours'], w['gap'])
        if 'backlog_end' in w:
            check(f'{d} backlog at end of day', r['backlog_end_hours'], w['backlog_end'])
    months = {m['month']: m for m in res['cost']['months']}
    for ym, w in exp['cost'].items():
        if ym == 'total_estimated_bill':
            continue
        for k, v in w.items():
            check(f'cost {ym} {k}', months[ym][k], v)
    check('total estimated bill', res['cost']['total_estimated_bill'], exp['cost']['total_estimated_bill'])

    # A missing last-year day must stop the plan, not be filled in.
    bad = load('fixture_daily_case_a.json')
    del bad['baseline']['last_year_daily']['value']['2025-12-26']
    p = run_data(bad, 'missing')
    check('missing last-year day rejected (exit 3)', p.returncode, 3)
    check('error names the missing day', '2025-12-26' in p.stderr, True)


def case_new_store():
    print('\n== new store (Case B)')
    res = run('fixture_new_store_case_b.json')
    if not res:
        return
    exp = load('expected_new_store_case_b.json')
    days = by_date(res)
    for d, v in exp['forecast'].items():
        check(f'{d} forecast', days[d]['forecast_conversations'], v)
    totals = {p['phase']: p['total_forecast'] for p in res['phase_summary']}
    for p, t in exp['phase_totals'].items():
        check(f'phase total {p}', totals.get(p), t)
    for d, v in exp['backlog_end'].items():
        check(f'{d} backlog at end of day', days[d]['backlog_end_hours'], v)
    owner = res['people'][0]
    check('owner longest run', owner['longest_run_days'], exp['owner_longest_run'])
    check('owner 57-day run flagged', owner['runs_over_limit'], [exp['owner_flag']])
    check('owner flag is a DECISION NEEDED line', owner['decisions'][0].startswith('[DECISION NEEDED: Owner works 57 days'), True)
    for d, w in exp['hourly'].items():
        if 'hours' in w:
            check(f'{d} hours with messages and nobody on', days[d]['hours_with_messages_and_nobody_on'], w['hours'])
        check(f'{d} messages in those hours', days[d]['messages_in_those_hours'], w['messages'])
    sc = {f"{s['multiplier']:g}": s for s in res['scenarios']}
    for k, v in exp['scenario_totals'].items():
        check(f'scenario x{k} total', sc[k]['total_forecast'], v)
        check(f'scenario x{k} labelled as scenario', sc[k]['label'].startswith('scenario'), True)
    months = {m['month']: m for m in res['cost']['months']}
    for ym, w in exp['cost'].items():
        if ym == 'total_estimated_bill':
            continue
        for k, v in w.items():
            check(f'cost {ym} {k}', months[ym][k], v)
    check('total estimated bill', res['cost']['total_estimated_bill'], exp['cost']['total_estimated_bill'])

    # Same store described by orders x messages per order gives the same plan.
    alt = load('fixture_new_store_case_b.json')
    alt['baseline'] = {'method': 'new_store',
                       'normal_orders_per_week': {'value': 630, 'source': 'merchant-stated'},
                       'messages_per_100_orders': {'value': 20, 'source': 'merchant-stated'}}
    p = run_data(alt, 'orders')
    r2 = json.loads(p.stdout) if p.returncode == 0 else None
    check('orders route gives the same totals', r2 and [x['total_forecast'] for x in r2['phase_summary']],
          [126, 378, 567, 484])

    # No uplift from the merchant: refuse, do not assume one.
    nou = load('fixture_new_store_case_b.json')
    del nou['phase_uplift']
    check('missing uplift rejected (exit 3)', run_data(nou, 'nouplift').returncode, 3)

    # AI resolution meter billed on top of the ticket meter.
    ai = load('fixture_new_store_case_b.json')
    ai['helpdesk']['ai_meter'] = {'share_resolved_by_ai_pct': 20, 'price_per_month': 0, 'included_per_month': 50,
                                  'overage_price_per_resolution': 0.9,
                                  'ai_resolutions_also_count_as_tickets': True, 'source': 'merchant-stated'}
    p = run_data(ai, 'ai')
    r3 = json.loads(p.stdout)
    w = exp['ai_meter_case']
    months = {m['month']: m for m in r3['cost']['months']}
    for ym, v in w['bills'].items():
        check(f'AI meter bill {ym}', months[ym]['estimated_bill'], v)
    check('AI meter total', r3['cost']['total_estimated_bill'], w['total'])
    ai['helpdesk']['ai_meter']['ai_resolutions_also_count_as_tickets'] = False
    r4 = json.loads(run_data(ai, 'ai2').stdout)
    check('ticket meter without AI resolutions (Dec)',
          {m['month']: m for m in r4['cost']['months']}['2026-12']['ticket_meter_volume'],
          w['dec_ticket_meter_if_not_tickets'])


def case_fill():
    print('\n== roster fill')
    res = run('fixture_roster_fill.json')
    if not res:
        return
    exp = load('expected_roster_fill.json')
    days = by_date(res)
    for d, v in exp['backlog_end'].items():
        check(f'{d} backlog at end of day', days[d]['backlog_end_hours'], v)
    people = {p['name']: p for p in res['people']}
    check('Bo days added', people['Bo']['added_days'], exp['bo_added'])
    check('Ann days added', people['Ann']['added_days'], exp['ann_added'])
    check('Bo not on his day off', 'Bo' in days['2026-11-28']['on_shift'], False)
    check('Ann run over limit flagged', people['Ann']['runs_over_limit'], exp['ann_flag'])
    check('Bo stays within run limit', people['Bo']['runs_over_limit'], exp['bo_flag'])
    check('before draft backlog days', res['roster_draft']['before_draft']['backlog_days'],
          exp['before_draft']['backlog_days'])
    check('before draft final backlog', res['roster_draft']['before_draft']['final_backlog_hours'],
          exp['before_draft']['final_backlog_hours'])
    check('need extra help dates', [n['date'] for n in res['need_extra_help']], exp['need_extra_help_dates'])
    check('added shift marked in detail',
          [p['added_in_draft'] for p in days['2026-11-25']['on_shift_detail']], [False, True])


def main():
    case_phase()
    case_daily()
    case_new_store()
    case_fill()
    print()
    if failures:
        print(f'{len(failures)} check(s) failed')
        sys.exit(1)
    print('all checks passed')


if __name__ == '__main__':
    main()
