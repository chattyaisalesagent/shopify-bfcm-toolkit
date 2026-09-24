#!/usr/bin/env python3
"""
Forecast daily support volume across the peak season, compare the agent-hours
it needs with the hours the named team can give each day, list the gap days
and the uncovered hours of the day, and estimate the helpdesk bill per
calendar month against the plan cap.

Deterministic and hand-checkable: same input, same output. No network access,
no dependencies beyond the standard library, no prompts. Reads a JSON file,
writes JSON (default) or Markdown tables to stdout. See
references/input-schema.md for the input shape.

Usage:
    python3 plan.py <input.json>
    python3 plan.py <input.json> --markdown
    python3 plan.py <input.json> --out <output.json>

Exit codes:
    0  computed successfully
    2  input file missing or invalid JSON
    3  input failed validation (see stderr for which field)
"""
import sys
import json
import math
import argparse
from datetime import date, timedelta

ALLOWED_SOURCES = ('merchant-stated', 'merchant-chosen estimate')
PHASES = ('pre_sale', 'bfcm_week', 'december', 'returns')
WEEKDAY_NAMES = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')


class InputError(Exception):
    pass


def round_half_up(x, ndigits=0):
    """Round half away from zero, the way people round by hand."""
    m = 10 ** ndigits
    return math.floor(x * m + 0.5) / m if ndigits else int(math.floor(x + 0.5))


def parse_date(s, field):
    try:
        y, m, d = (int(x) for x in str(s).split('-'))
        return date(y, m, d)
    except Exception as e:
        raise InputError(f'{field}: "{s}" is not a valid YYYY-MM-DD date') from e


def parse_hhmm(s, field):
    try:
        h, m = (int(x) for x in s.split(':'))
    except Exception as e:
        raise InputError(f'{field}: "{s}" is not HH:MM') from e
    if not (0 <= h <= 24 and 0 <= m < 60) or (h == 24 and m != 0):
        raise InputError(f'{field}: "{s}" is out of range')
    return h * 60 + m


def parse_shift(s, field):
    """'09:00-17:00' -> list of (start_min, end_min) segments within one day.
    An overnight shift such as '22:00-06:00' is counted as two segments on the
    same calendar day (22:00-24:00 and 00:00-06:00)."""
    if s is None:
        return []
    if not isinstance(s, str) or '-' not in s:
        raise InputError(f'{field}: "{s}" must look like "09:00-17:00" or be null')
    a, b = s.split('-', 1)
    start, end = parse_hhmm(a.strip(), field), parse_hhmm(b.strip(), field)
    if start == end:
        raise InputError(f'{field}: shift "{s}" has zero length')
    if end > start:
        return [(start, end)]
    return [(start, 1440), (0, end)]


def labelled(data, key, required=True):
    """Read an assumption stored as {"value": ..., "source": ...}."""
    if key not in data:
        if required:
            raise InputError(f'missing required field "{key}"')
        return None, None
    item = data[key]
    if not isinstance(item, dict) or 'value' not in item or 'source' not in item:
        raise InputError(f'"{key}" must be an object with "value" and "source"')
    if item['source'] not in ALLOWED_SOURCES:
        raise InputError(
            f'"{key}.source" must be one of {ALLOWED_SOURCES}, got "{item["source"]}"')
    return item['value'], item['source']


def number(v, field, minimum=0.0):
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise InputError(f'{field} must be a number')
    if v < minimum:
        raise InputError(f'{field} must be >= {minimum}')
    return float(v)


def fmt_ranges(minutes_covered):
    """Turn a 1440-length coverage list into uncovered 'HH:MM-HH:MM' ranges."""
    out, start = [], None
    for m in range(1441):
        uncovered = m < 1440 and not minutes_covered[m]
        if uncovered and start is None:
            start = m
        elif not uncovered and start is not None:
            out.append(f'{start // 60:02d}:{start % 60:02d}-{m // 60:02d}:{m % 60:02d}')
            start = None
    return out


def build(data):
    assumptions = []

    # --- dates (calendar facts) ---
    dates = data.get('dates')
    if not isinstance(dates, dict):
        raise InputError('missing required object "dates"')
    for k in ('black_friday', 'cyber_monday', 'holiday', 'end_date'):
        if k not in dates:
            raise InputError(f'missing required field "dates.{k}"')
    bf = parse_date(dates['black_friday'], 'dates.black_friday')
    cm = parse_date(dates['cyber_monday'], 'dates.cyber_monday')
    holiday = parse_date(dates['holiday'], 'dates.holiday')
    end = parse_date(dates['end_date'], 'dates.end_date')
    start = parse_date(dates['start_date'], 'dates.start_date') if 'start_date' in dates \
        else bf - timedelta(days=7)
    bfcm_end = cm + timedelta(days=3)
    if not (start < bf <= cm < bfcm_end < holiday <= end):
        raise InputError('dates must satisfy start_date < black_friday <= cyber_monday '
                         '< cyber_monday+3 < holiday <= end_date')

    # --- baseline ---
    base = data.get('baseline')
    if not isinstance(base, dict) or base.get('method') not in ('messages', 'orders'):
        raise InputError('"baseline.method" must be "messages" or "orders"')
    if base['method'] == 'messages':
        v, s = labelled(base, 'conversations_per_day')
        base_daily = number(v, 'baseline.conversations_per_day')
        assumptions.append({'field': 'last year BFCM-week conversations per day',
                            'value': v, 'source': s})
        base_note = f'{v} conversations per day last BFCM week'
    else:
        ov, os_ = labelled(base, 'orders_per_day')
        rv, rs = labelled(base, 'tickets_per_100_orders')
        orders = number(ov, 'baseline.orders_per_day')
        ratio = number(rv, 'baseline.tickets_per_100_orders')
        base_daily = orders * ratio / 100.0
        assumptions.append({'field': 'last year BFCM-week orders per day', 'value': ov, 'source': os_})
        assumptions.append({'field': 'tickets per 100 orders', 'value': rv, 'source': rs})
        base_note = f'{ov} orders per day x {rv} tickets per 100 orders = {base_daily:g} per day'

    g, gs = labelled(data, 'growth_pct')
    growth = number(g, 'growth_pct.value', minimum=-100)
    assumptions.append({'field': 'growth this year (%)', 'value': g, 'source': gs})
    level = base_daily * (1 + growth / 100.0)

    pf, pfs = labelled(data, 'phase_factors')
    if not isinstance(pf, dict):
        raise InputError('"phase_factors.value" must be an object')
    factors = {'bfcm_week': 1.0}
    for p in ('pre_sale', 'december', 'returns'):
        if p not in pf:
            raise InputError(f'missing "phase_factors.value.{p}"')
        factors[p] = number(pf[p], f'phase_factors.value.{p}')
    assumptions.append({'field': 'phase factors vs BFCM week', 'value': factors, 'source': pfs})

    wf, wfs = labelled(data, 'weekend_factor')
    weekend_factor = number(wf, 'weekend_factor.value')
    assumptions.append({'field': 'weekend factor', 'value': wf, 'source': wfs})

    overrides, ovs = labelled(data, 'day_overrides', required=False)
    overrides = overrides or {}
    for d, f in overrides.items():
        parse_date(d, f'day_overrides.value key "{d}"')
        number(f, f'day_overrides.value["{d}"]')
    if overrides:
        assumptions.append({'field': 'single-day multipliers', 'value': overrides, 'source': ovs})

    mpc, mpcs = labelled(data, 'minutes_per_conversation')
    minutes = number(mpc, 'minutes_per_conversation.value')
    if minutes <= 0:
        raise InputError('minutes_per_conversation must be > 0')
    assumptions.append({'field': 'minutes per conversation', 'value': mpc, 'source': mpcs})

    sh, shs = labelled(data, 'share_of_shift_answering_pct')
    share = number(sh, 'share_of_shift_answering_pct.value')
    if not 0 < share <= 100:
        raise InputError('share_of_shift_answering_pct must be between 0 and 100')
    assumptions.append({'field': 'share of each shift spent answering (%)', 'value': sh, 'source': shs})

    # --- team ---
    team = data.get('team')
    if not isinstance(team, list) or not team:
        raise InputError('"team" must be a non-empty list')
    members = []
    for i, t in enumerate(team):
        if 'name' not in t:
            raise InputError(f'team[{i}] missing "name"')
        members.append({
            'name': t['name'],
            'weekday': parse_shift(t.get('weekday_shift'), f'team[{i}].weekday_shift'),
            'weekend': parse_shift(t.get('weekend_shift'), f'team[{i}].weekend_shift'),
            'off': {parse_date(d, f'team[{i}].days_off').isoformat() for d in t.get('days_off', [])},
            'from': parse_date(t['start_date'], f'team[{i}].start_date') if t.get('start_date') else None,
            'to': parse_date(t['end_date'], f'team[{i}].end_date') if t.get('end_date') else None,
        })

    # --- daily walk ---
    days, d = [], start
    while d <= end:
        if d < bf:
            phase = 'pre_sale'
        elif d <= bfcm_end:
            phase = 'bfcm_week'
        elif d < holiday:
            phase = 'december'
        else:
            phase = 'returns'
        weekend = d.weekday() >= 5
        raw = level * factors[phase] * (weekend_factor if weekend else 1.0) \
            * float(overrides.get(d.isoformat(), 1.0))
        forecast = round_half_up(raw)
        required = round_half_up(forecast * minutes / 60.0, 1)

        covered = [False] * 1440
        on_shift, shift_hours = [], 0.0
        for m in members:
            if d.isoformat() in m['off']:
                continue
            if (m['from'] and d < m['from']) or (m['to'] and d > m['to']):
                continue
            segs = m['weekend'] if weekend else m['weekday']
            if not segs:
                continue
            on_shift.append(m['name'])
            for a, b in segs:
                shift_hours += (b - a) / 60.0
                for x in range(a, b):
                    covered[x] = True
        available = round_half_up(shift_hours * share / 100.0, 1)
        gap = round_half_up(required - available, 1)
        days.append({
            'date': d.isoformat(),
            'weekday': WEEKDAY_NAMES[d.weekday()],
            'phase': phase,
            'forecast_conversations': forecast,
            'required_agent_hours': required,
            'shift_hours': round_half_up(shift_hours, 1),
            'available_agent_hours': available,
            'gap_hours': gap if gap > 0 else 0.0,
            'status': 'GAP' if gap > 0 else 'covered',
            'on_shift': on_shift,
            'uncovered_hours_of_day': fmt_ranges(covered),
        })
        d += timedelta(days=1)

    phase_summary = []
    for p in PHASES:
        rows = [r for r in days if r['phase'] == p]
        if not rows:
            continue
        peak = max(rows, key=lambda r: r['forecast_conversations'])
        phase_summary.append({
            'phase': p,
            'from': rows[0]['date'], 'to': rows[-1]['date'], 'days': len(rows),
            'total_forecast': sum(r['forecast_conversations'] for r in rows),
            'peak_day': peak['date'], 'peak_forecast': peak['forecast_conversations'],
            'gap_days': sum(1 for r in rows if r['status'] == 'GAP'),
            'total_gap_hours': round_half_up(sum(r['gap_hours'] for r in rows), 1),
        })

    result = {
        'window': {'start': start.isoformat(), 'end': end.isoformat(), 'days': len(days)},
        'phases': {'pre_sale': [start.isoformat(), (bf - timedelta(days=1)).isoformat()],
                   'bfcm_week': [bf.isoformat(), bfcm_end.isoformat()],
                   'december': [(bfcm_end + timedelta(days=1)).isoformat(),
                                (holiday - timedelta(days=1)).isoformat()],
                   'returns': [holiday.isoformat(), end.isoformat()]},
        'baseline': {'method': base['method'], 'last_year_per_day': round_half_up(base_daily, 2),
                     'this_year_bfcm_level_per_day': round_half_up(level, 2), 'working': base_note},
        'assumptions': assumptions,
        'days': days,
        'phase_summary': phase_summary,
        'gap_days': [{k: r[k] for k in ('date', 'weekday', 'phase', 'forecast_conversations',
                                         'required_agent_hours', 'available_agent_hours', 'gap_hours')}
                     for r in days if r['status'] == 'GAP'],
        'cost': cost_estimate(data, days),
    }
    return result


def cost_estimate(data, days):
    hd = data.get('helpdesk')
    if hd is None:
        return None
    for k in ('plan_price_per_month', 'included_per_month', 'overage_price_per_block',
              'overage_block_size', 'billing_unit', 'source'):
        if k not in hd:
            raise InputError(f'missing "helpdesk.{k}"')
    if hd['source'] not in ALLOWED_SOURCES:
        raise InputError(f'"helpdesk.source" must be one of {ALLOWED_SOURCES}')
    price = number(hd['plan_price_per_month'], 'helpdesk.plan_price_per_month')
    cap = number(hd['included_per_month'], 'helpdesk.included_per_month')
    block_price = number(hd['overage_price_per_block'], 'helpdesk.overage_price_per_block')
    block = number(hd['overage_block_size'], 'helpdesk.overage_block_size')
    if block <= 0:
        raise InputError('helpdesk.overage_block_size must be > 0')
    rest = hd.get('rest_of_month_volume', {}) or {}

    months = {}
    for r in days:
        months.setdefault(r['date'][:7], []).append(r)
    rows, total = [], 0.0
    for ym in sorted(months):
        in_window = sum(r['forecast_conversations'] for r in months[ym])
        y, m = int(ym[:4]), int(ym[5:])
        nxt = date(y + (m == 12), m % 12 + 1, 1)
        month_days = (nxt - date(y, m, 1)).days
        full = len(months[ym]) == month_days
        outside = rest.get(ym)
        volume = in_window + (number(outside, f'helpdesk.rest_of_month_volume["{ym}"]') if outside is not None else 0)
        over_units = max(0.0, volume - cap)
        blocks = math.ceil(over_units / block) if over_units > 0 else 0
        over_cost = blocks * block_price
        bill = price + over_cost
        total += bill
        rows.append({
            'month': ym,
            'forecast_in_window': in_window,
            'rest_of_month_volume': outside,
            'total_volume': round_half_up(volume),
            'included': cap,
            'over_cap_units': round_half_up(over_units),
            'overage_blocks': blocks,
            'overage_cost': round_half_up(over_cost, 2),
            'estimated_bill': round_half_up(bill, 2),
            'lower_bound_only': (not full) and outside is None,
        })
    return {'billing_unit': hd['billing_unit'], 'source': hd['source'],
            'months': rows, 'total_estimated_bill': round_half_up(total, 2)}


def to_markdown(res):
    L = []
    L.append(f"Window {res['window']['start']} to {res['window']['end']} ({res['window']['days']} days)")
    L.append(f"Baseline: {res['baseline']['working']}; this year's BFCM-week level "
             f"{res['baseline']['this_year_bfcm_level_per_day']} per day\n")
    L.append('| Assumption | Value | Source |\n|---|---|---|')
    for a in res['assumptions']:
        L.append(f"| {a['field']} | {json.dumps(a['value'])} | {a['source']} |")
    L.append('\n| Date | Day | Phase | Forecast | Hours needed | Hours available | Gap | On shift | Uncovered hours |')
    L.append('|---|---|---|---|---|---|---|---|---|')
    for r in res['days']:
        L.append(f"| {r['date']} | {r['weekday']} | {r['phase']} | {r['forecast_conversations']} | "
                 f"{r['required_agent_hours']} | {r['available_agent_hours']} | "
                 f"{r['gap_hours'] if r['status'] == 'GAP' else '-'} | {', '.join(r['on_shift']) or 'nobody'} | "
                 f"{', '.join(r['uncovered_hours_of_day']) or 'none'} |")
    L.append('\n| Phase | From | To | Total forecast | Peak day | Gap days | Gap hours |\n|---|---|---|---|---|---|---|')
    for p in res['phase_summary']:
        L.append(f"| {p['phase']} | {p['from']} | {p['to']} | {p['total_forecast']} | "
                 f"{p['peak_day']} ({p['peak_forecast']}) | {p['gap_days']} | {p['total_gap_hours']} |")
    c = res['cost']
    if c:
        L.append(f"\nHelpdesk bill, billed per {c['billing_unit']} ({c['source']})\n")
        L.append('| Month | Volume | Included | Over cap | Overage cost | Estimated bill | Note |\n|---|---|---|---|---|---|---|')
        for m in c['months']:
            note = 'lower bound: days outside the window not counted' if m['lower_bound_only'] else ''
            L.append(f"| {m['month']} | {m['total_volume']} | {m['included']:g} | {m['over_cap_units']} | "
                     f"{m['overage_cost']:g} | {m['estimated_bill']:g} | {note} |")
        L.append(f"\nTotal estimated bill across these months: {c['total_estimated_bill']:g}")
    return '\n'.join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('input', help='Path to input JSON')
    ap.add_argument('--out', help='Write output here instead of stdout')
    ap.add_argument('--markdown', action='store_true', help='Print Markdown tables instead of JSON')
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

    try:
        res = build(data)
    except InputError as e:
        print(f'error: {e}', file=sys.stderr)
        sys.exit(3)

    text = to_markdown(res) if args.markdown else json.dumps(res, indent=2)
    if args.out:
        with open(args.out, 'w') as f:
            f.write(text + '\n')
    else:
        print(text)


if __name__ == '__main__':
    main()
