#!/usr/bin/env python3
"""
Forecast daily support volume across the peak season, compare the agent-hours
it needs with the hours the named team can give each day, carry unanswered
work over to the next day, propose a draft roster from the people the
merchant says can take extra days, flag long runs of working days, list the
hours of the day nobody covers, and estimate the helpdesk bill per month.

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
PHASE_LABEL = {'pre_sale': 'pre-sale', 'bfcm_week': 'BFCM week',
               'december': 'December', 'returns': 'returns'}
WEEKDAY_NAMES = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
DEFAULT_MAX_RUN = 6  # the roster template flags more than six days in a row
EPS = 1e-9


class InputError(Exception):
    pass


def round_half_up(x, ndigits=0):
    """Round half away from zero, the way people round by hand."""
    if ndigits:
        m = 10 ** ndigits
        return math.floor(x * m + 0.5 + EPS) / m
    return int(math.floor(x + 0.5 + EPS))


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


def seg_hours(segs):
    return sum(b - a for a, b in segs) / 60.0


def labelled(data, key, required=True):
    """Read an assumption stored as {"value": ..., "source": ...}."""
    if key not in data or data[key] is None:
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


def fmt_min(m):
    return f'{m // 60:02d}:{m % 60:02d}'


def fmt_ranges(minutes_covered):
    """Turn a 1440-length coverage list into uncovered 'HH:MM-HH:MM' ranges."""
    out, start = [], None
    for m in range(1441):
        uncovered = m < 1440 and not minutes_covered[m]
        if uncovered and start is None:
            start = m
        elif not uncovered and start is not None:
            out.append(f'{fmt_min(start)}-{fmt_min(m)}')
            start = None
    return out


# ---------------------------------------------------------------- inputs

def read_dates(data):
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
    return start, bf, cm, bfcm_end, holiday, end


def phase_of(d, bf, bfcm_end, holiday):
    if d < bf:
        return 'pre_sale'
    if d <= bfcm_end:
        return 'bfcm_week'
    if d < holiday:
        return 'december'
    return 'returns'


def read_team(data):
    team = data.get('team')
    if not isinstance(team, list) or not team:
        raise InputError('"team" must be a non-empty list')
    members = []
    for i, t in enumerate(team):
        if 'name' not in t:
            raise InputError(f'team[{i}] missing "name"')
        can_add = t.get('can_add_days') or []
        for w in can_add:
            if w not in WEEKDAY_NAMES:
                raise InputError(f'team[{i}].can_add_days: "{w}" must be one of {WEEKDAY_NAMES}')
        extra = parse_shift(t.get('extra_shift'), f'team[{i}].extra_shift')
        if can_add and not extra:
            raise InputError(f'team[{i}] has can_add_days but no extra_shift '
                             '(the shift times they would work on an added day)')
        weekday = parse_shift(t.get('weekday_shift'), f'team[{i}].weekday_shift')
        weekend = parse_shift(t.get('weekend_shift'), f'team[{i}].weekend_shift')
        if not weekday and not weekend and not can_add:
            raise InputError(f'team[{i}] ({t["name"]}) has no shifts and no days they can add')
        mh = t.get('max_hours_per_week')
        members.append({
            'name': t['name'],
            'weekday': weekday, 'weekend': weekend,
            'weekday_str': t.get('weekday_shift'), 'weekend_str': t.get('weekend_shift'),
            'off': {parse_date(d, f'team[{i}].days_off').isoformat() for d in t.get('days_off', [])},
            'from': parse_date(t['start_date'], f'team[{i}].start_date') if t.get('start_date') else None,
            'to': parse_date(t['end_date'], f'team[{i}].end_date') if t.get('end_date') else None,
            'can_add': set(can_add), 'extra': extra, 'extra_str': t.get('extra_shift'),
            'max_hours_week': number(mh, f'team[{i}].max_hours_per_week') if mh is not None else None,
        })
    return members


def read_hourly(data, assumptions):
    hv, hs = labelled(data, 'hourly_share_pct', required=False)
    if hv is None:
        return None
    if isinstance(hv, dict):
        share = [0.0] * 24
        for k, v in hv.items():
            try:
                h = int(k)
            except ValueError as e:
                raise InputError(f'hourly_share_pct key "{k}" must be an hour 0 to 23') from e
            if not 0 <= h <= 23:
                raise InputError(f'hourly_share_pct key "{k}" must be an hour 0 to 23')
            share[h] = number(v, f'hourly_share_pct["{k}"]')
    elif isinstance(hv, list) and len(hv) == 24:
        share = [number(v, f'hourly_share_pct[{i}]') for i, v in enumerate(hv)]
    else:
        raise InputError('hourly_share_pct.value must be 24 numbers or an object keyed by hour')
    total = sum(share)
    if abs(total - 100) > 1:
        raise InputError(f'hourly_share_pct adds up to {total:g}, it must add up to 100 (plus or minus 1)')
    assumptions.append({'field': 'share of daily messages by hour of day (%)',
                        'value': {f'{h:02d}': share[h] for h in range(24) if share[h]}, 'source': hs})
    return share


# ------------------------------------------------------------ forecasting

def forecast_series(data, window, bf, bfcm_end, holiday, assumptions):
    """Return {date: raw forecast before rounding and overrides}, plus notes."""
    base = data.get('baseline')
    method = base.get('method') if isinstance(base, dict) else None
    if method not in ('daily_series', 'messages', 'orders', 'new_store'):
        raise InputError('"baseline.method" must be "daily_series", "messages", "orders" or "new_store"')
    info = {'method': method}

    if method == 'daily_series':
        series, ss = labelled(base, 'last_year_daily')
        if not isinstance(series, dict) or not series:
            raise InputError('baseline.last_year_daily.value must be an object of "YYYY-MM-DD": count')
        ly = {parse_date(k, 'baseline.last_year_daily key').isoformat():
              number(v, f'baseline.last_year_daily["{k}"]') for k, v in series.items()}
        if 'last_year_black_friday' not in base:
            raise InputError('missing "baseline.last_year_black_friday" (Black Friday 2025 was 2025-11-28)')
        ly_bf = parse_date(base['last_year_black_friday'], 'baseline.last_year_black_friday')
        ly_hol = parse_date(base['last_year_holiday'], 'baseline.last_year_holiday') \
            if base.get('last_year_holiday') else date(holiday.year - 1, holiday.month, holiday.day)
        g, gs = labelled(data, 'growth_pct')
        growth = number(g, 'growth_pct.value', minimum=-100)
        assumptions.append({'field': 'last year daily volume', 'value': f'{len(ly)} days',
                            'source': ss})
        assumptions.append({'field': 'growth this year (%)', 'value': g, 'source': gs})
        switch = holiday - timedelta(days=1)
        raw, matched, missing = {}, {}, []
        for d in window:
            src = ly_bf + (d - bf) if d < switch else ly_hol + (d - holiday)
            if src.isoformat() not in ly:
                missing.append(f'{d.isoformat()} needs {src.isoformat()}')
                continue
            raw[d] = ly[src.isoformat()] * (1 + growth / 100.0)
            matched[d] = src
        if missing:
            raise InputError('last_year_daily is missing days the plan needs: ' + '; '.join(missing[:10])
                             + (' ...' if len(missing) > 10 else ''))
        info.update({'last_year_black_friday': ly_bf.isoformat(), 'last_year_holiday': ly_hol.isoformat(),
                     'switch_to_date_matching': switch.isoformat(), 'growth_pct': growth,
                     'working': (f'each day = last year\'s matching day x {1 + growth / 100.0:g}. '
                                 f'Before {switch.isoformat()} days are matched by distance from Black Friday '
                                 f'({ly_bf.isoformat()} last year), which keeps the weekday. From '
                                 f'{switch.isoformat()} on they are matched by calendar date around the holiday.')})
        return raw, matched, info

    # ---- phase modes: an average-day level per phase, split into weekday and weekend
    if method in ('messages', 'orders'):
        if method == 'messages':
            v, s = labelled(base, 'conversations_per_day')
            base_daily = number(v, 'baseline.conversations_per_day')
            assumptions.append({'field': 'last year BFCM-week conversations per day (all 7 days averaged)',
                                'value': v, 'source': s})
            note = f'{v:g} per day last BFCM week'
        else:
            ov, os_ = labelled(base, 'orders_per_day')
            rv, rs = labelled(base, 'tickets_per_100_orders')
            base_daily = number(ov, 'baseline.orders_per_day') * number(rv, 'baseline.tickets_per_100_orders') / 100.0
            assumptions.append({'field': 'last year BFCM-week orders per day', 'value': ov, 'source': os_})
            assumptions.append({'field': 'tickets per 100 orders', 'value': rv, 'source': rs})
            note = f'{ov:g} orders per day x {rv:g} / 100 = {base_daily:g} per day'
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
        assumptions.append({'field': 'phase factors vs BFCM week (average day)', 'value': factors, 'source': pfs})
        phase_avg = {p: level * factors[p] for p in PHASES}
        note += f'; x {1 + growth / 100.0:g} growth = {round_half_up(level, 2):g} per average BFCM-week day'
    else:  # new_store
        if 'normal_messages_per_week' in base:
            v, s = labelled(base, 'normal_messages_per_week')
            normal_day = number(v, 'baseline.normal_messages_per_week') / 7.0
            assumptions.append({'field': 'normal messages per week (last 4 weeks)', 'value': v, 'source': s})
            note = f'{v:g} messages per normal week / 7 = {round_half_up(normal_day, 2):g} per normal day'
        else:
            ov, os_ = labelled(base, 'normal_orders_per_week')
            rv, rs = labelled(base, 'messages_per_100_orders')
            normal_day = number(ov, 'baseline.normal_orders_per_week') \
                * number(rv, 'baseline.messages_per_100_orders') / 100.0 / 7.0
            assumptions.append({'field': 'normal orders per week (last 4 weeks)', 'value': ov, 'source': os_})
            assumptions.append({'field': 'messages per 100 orders (last 4 weeks)', 'value': rv, 'source': rs})
            note = (f'{ov:g} orders per week x {rv:g} / 100 / 7 = '
                    f'{round_half_up(normal_day, 2):g} messages per normal day')
        uv, us = labelled(data, 'phase_uplift')
        if not isinstance(uv, dict):
            raise InputError('"phase_uplift.value" must be an object')
        up = {}
        for p in PHASES:
            if p not in uv:
                raise InputError(f'missing "phase_uplift.value.{p}" (volume vs a normal day, 1.0 = normal)')
            up[p] = number(uv[p], f'phase_uplift.value.{p}')
        assumptions.append({'field': 'expected volume vs a normal day, per phase', 'value': up, 'source': us})
        phase_avg = {p: normal_day * up[p] for p in PHASES}

    wf, wfs = labelled(data, 'weekend_factor')
    w = number(wf, 'weekend_factor.value')
    assumptions.append({'field': 'weekend day vs weekday (averages taken separately)', 'value': wf, 'source': wfs})
    # Split each phase's average day into weekday and weekend levels so that
    # the phase total is unchanged: weekday = avg x n / (weekdays + w x weekend days).
    counts = {p: [0, 0] for p in PHASES}
    for d in window:
        counts[phase_of(d, bf, bfcm_end, holiday)][1 if d.weekday() >= 5 else 0] += 1
    split = {}
    for p in PHASES:
        nwd, nwe = counts[p]
        if nwd + nwe == 0:
            continue
        wd = phase_avg[p] * (nwd + nwe) / (nwd + w * nwe) if (nwd + w * nwe) > 0 else 0.0
        split[p] = {'average_day': round_half_up(phase_avg[p], 2), 'weekdays': nwd, 'weekend_days': nwe,
                    'weekday_level': round_half_up(wd, 2), 'weekend_level': round_half_up(wd * w, 2),
                    '_wd': wd, '_we': wd * w}
    raw = {}
    for d in window:
        s = split[phase_of(d, bf, bfcm_end, holiday)]
        raw[d] = s['_we'] if d.weekday() >= 5 else s['_wd']
    info['working'] = note
    info['phase_levels'] = {p: {k: v for k, v in s.items() if not k.startswith('_')} for p, s in split.items()}
    return raw, None, info


# ---------------------------------------------------------------- roster

def working_segs(m, d):
    """Segments a person works on day d in the merchant's own roster."""
    if d.isoformat() in m['off']:
        return []
    if (m['from'] and d < m['from']) or (m['to'] and d > m['to']):
        return []
    return m['weekend'] if d.weekday() >= 5 else m['weekday']


def can_be_added(m, d):
    if d.isoformat() in m['off']:
        return False
    if (m['from'] and d < m['from']) or (m['to'] and d > m['to']):
        return False
    return WEEKDAY_NAMES[d.weekday()] in m['can_add']


def run_through(work, i, idx, n):
    """Length of the working run that would include day idx if person i worked it."""
    a = idx - 1
    while a >= 0 and work[i][a]:
        a -= 1
    b = idx + 1
    while b < n and work[i][b]:
        b += 1
    return b - a - 1


def week_hours(hours, i, window, idx):
    wk = window[idx].isocalendar()[:2]
    return sum(hours[i][j] for j, d in enumerate(window) if d.isocalendar()[:2] == wk)


def simulate(members, window, forecasts, minutes, share, max_run, fill):
    """Walk the days: hours needed, hours available, backlog carried to the
    next day, and (if fill) extra shifts added from people who said they can
    take them."""
    n = len(window)
    segs = [[working_segs(m, d) for d in window] for m in members]
    work = [[bool(s) for s in row] for row in segs]
    hours = [[seg_hours(s) for s in row] for row in segs]
    added = [[False] * n for _ in members]
    backlog, rows = 0.0, []
    for idx, d in enumerate(window):
        need = round_half_up(forecasts[idx] * minutes / 60.0, 1)
        workload = round_half_up(need + backlog, 1)

        def avail():
            return round_half_up(sum(hours[i][idx] for i in range(len(members))) * share / 100.0, 1)

        if fill:
            while workload > avail() + EPS:
                pick = None
                for i, m in enumerate(members):
                    if work[i][idx] or not can_be_added(m, d):
                        continue
                    if run_through(work, i, idx, n) > max_run:
                        continue
                    extra_h = seg_hours(m['extra'])
                    if m['max_hours_week'] is not None and \
                            week_hours(hours, i, window, idx) + extra_h > m['max_hours_week'] + EPS:
                        continue
                    pick = i
                    break
                if pick is None:
                    break
                segs[pick][idx] = members[pick]['extra']
                work[pick][idx] = True
                hours[pick][idx] = seg_hours(members[pick]['extra'])
                added[pick][idx] = True
        available = avail()
        handled = min(workload, available)
        backlog_out = round_half_up(workload - handled, 1)
        rows.append({'need': need, 'backlog_in': round_half_up(backlog, 1), 'workload': workload,
                     'available': available, 'backlog_out': backlog_out,
                     'shift_hours': round_half_up(sum(hours[i][idx] for i in range(len(members))), 1)})
        backlog = backlog_out
    return rows, segs, work, hours, added


def runs_over(work_row, window, limit):
    out, start = [], None
    for j in range(len(window) + 1):
        on = j < len(window) and work_row[j]
        if on and start is None:
            start = j
        elif not on and start is not None:
            length = j - start
            if length > limit:
                out.append({'from': window[start].isoformat(), 'to': window[j - 1].isoformat(), 'days': length})
            start = None
    return out


def longest_run(work_row):
    best = cur = 0
    for x in work_row:
        cur = cur + 1 if x else 0
        best = max(best, cur)
    return best


# ------------------------------------------------------------------ build

def build(data, multiplier=1.0):
    assumptions = []
    start, bf, cm, bfcm_end, holiday, end = read_dates(data)
    window = [start + timedelta(days=i) for i in range((end - start).days + 1)]

    raw, matched, info = forecast_series(data, window, bf, bfcm_end, holiday, assumptions)

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

    rules = data.get('roster_rules') or {}
    mr, mrs = labelled(rules, 'max_consecutive_days', required=False)
    if mr is None:
        max_run = DEFAULT_MAX_RUN
        assumptions.append({'field': 'longest run of working days before a flag', 'value': max_run,
                            'source': 'kit check (change it if your own rule differs)'})
    else:
        max_run = int(number(mr, 'roster_rules.max_consecutive_days.value', minimum=1))
        assumptions.append({'field': 'longest run of working days allowed', 'value': mr, 'source': mrs})

    hourly = read_hourly(data, assumptions)
    members = read_team(data)
    fill = any(m['can_add'] for m in members)

    forecasts = [round_half_up(raw[d] * multiplier * float(overrides.get(d.isoformat(), 1.0)))
                 for d in window]

    base_rows, _, base_work, _, _ = simulate(members, window, forecasts, minutes, share, max_run, False)
    if fill:
        rows, segs, work, hours, added = simulate(members, window, forecasts, minutes, share, max_run, True)
    else:
        rows, segs, work, hours, added = simulate(members, window, forecasts, minutes, share, max_run, False)

    days = []
    for idx, d in enumerate(window):
        r = rows[idx]
        covered = [False] * 1440
        on_shift = []
        for i, m in enumerate(members):
            if not work[i][idx]:
                continue
            times = ', '.join(f'{fmt_min(a)}-{fmt_min(b)}' for a, b in segs[i][idx])
            on_shift.append({'name': m['name'], 'times': times, 'added_in_draft': added[i][idx]})
            for a, b in segs[i][idx]:
                for x in range(a, b):
                    covered[x] = True
        gap = round_half_up(r['need'] - r['available'], 1)
        row = {
            'date': d.isoformat(),
            'weekday': WEEKDAY_NAMES[d.weekday()],
            'phase': phase_of(d, bf, bfcm_end, holiday),
            'forecast_conversations': forecasts[idx],
            'required_agent_hours': r['need'],
            'shift_hours': r['shift_hours'],
            'available_agent_hours': r['available'],
            'gap_hours': gap if gap > 0 else 0.0,
            'backlog_in_hours': r['backlog_in'],
            'backlog_end_hours': r['backlog_out'],
            'status': 'GAP' if gap > 0 else ('BACKLOG' if r['backlog_out'] > 0 else 'covered'),
            'on_shift': [p['name'] for p in on_shift],
            'on_shift_detail': on_shift,
            'uncovered_hours_of_day': fmt_ranges(covered),
        }
        if matched:
            row['matched_last_year_date'] = matched[d].isoformat()
            row['matched_last_year_weekday'] = WEEKDAY_NAMES[matched[d].weekday()]
        if hourly:
            empty = [h for h in range(24) if hourly[h] > 0 and not any(covered[h * 60:(h + 1) * 60])]
            ranges = []
            for h in empty:
                if ranges and ranges[-1][1] == h:
                    ranges[-1][1] = h + 1
                else:
                    ranges.append([h, h + 1])
            row['hours_with_messages_and_nobody_on'] = [f'{a:02d}:00-{b:02d}:00' for a, b in ranges]
            row['messages_in_those_hours'] = round_half_up(forecasts[idx] * sum(hourly[h] for h in empty) / 100.0)
        days.append(row)

    phase_summary = []
    for p in PHASES:
        prow = [r for r in days if r['phase'] == p]
        if not prow:
            continue
        peak = max(prow, key=lambda r: r['forecast_conversations'])
        phase_summary.append({
            'phase': p, 'from': prow[0]['date'], 'to': prow[-1]['date'], 'days': len(prow),
            'total_forecast': sum(r['forecast_conversations'] for r in prow),
            'peak_day': peak['date'], 'peak_forecast': peak['forecast_conversations'],
            'gap_days': sum(1 for r in prow if r['status'] == 'GAP'),
            'total_gap_hours': round_half_up(sum(r['gap_hours'] for r in prow), 1),
            'backlog_days': sum(1 for r in prow if r['backlog_end_hours'] > 0),
        })

    people = []
    for i, m in enumerate(members):
        worked = [window[j].isoformat() for j in range(len(window)) if work[i][j]]
        flags = runs_over(work[i], window, max_run)
        people.append({
            'name': m['name'], 'days_worked': len(worked),
            'total_shift_hours': round_half_up(sum(hours[i]), 1),
            'added_days': [window[j].isoformat() for j in range(len(window)) if added[i][j]],
            'longest_run_days': longest_run(work[i]),
            'runs_over_limit': flags,
            'decisions': [f'[DECISION NEEDED: {m["name"]} works {f["days"]} days in a row from '
                          f'{f["from"]} to {f["to"]}, confirm or change]' for f in flags],
        })

    need_help = [{'date': r['date'], 'weekday': r['weekday'],
                  'hours_short_end_of_day': r['backlog_end_hours']}
                 for r in days if r['backlog_end_hours'] > 0]

    base_backlog_days = sum(1 for r in base_rows if r['backlog_out'] > 0)
    result = {
        'window': {'start': start.isoformat(), 'end': end.isoformat(), 'days': len(days)},
        'phases': {'pre_sale': [start.isoformat(), (bf - timedelta(days=1)).isoformat()],
                   'bfcm_week': [bf.isoformat(), bfcm_end.isoformat()],
                   'december': [(bfcm_end + timedelta(days=1)).isoformat(),
                                (holiday - timedelta(days=1)).isoformat()],
                   'returns': [holiday.isoformat(), end.isoformat()]},
        'baseline': info,
        'scenario_multiplier': multiplier,
        'assumptions': assumptions,
        'backlog_rule': ('Hours of work not done on a day are added to the next day. The inbox is '
                         'assumed empty on the first day. Nothing is dropped.'),
        'days': days,
        'phase_summary': phase_summary,
        'gap_days': [{k: r[k] for k in ('date', 'weekday', 'phase', 'forecast_conversations',
                                         'required_agent_hours', 'available_agent_hours', 'gap_hours')}
                     for r in days if r['status'] == 'GAP'],
        'backlog_days': [{'date': r['date'], 'weekday': r['weekday'], 'backlog_end_hours': r['backlog_end_hours']}
                         for r in days if r['backlog_end_hours'] > 0],
        'final_backlog_hours': days[-1]['backlog_end_hours'],
        'roster_draft': {
            'filled': fill,
            'rule': ('Walk the days in order. When the day\'s work plus carried-over work is more than '
                     'the hours on shift, add the first person in team order who is free that day, lists '
                     'that weekday in can_add_days, is not on a day off or outside their dates, would not '
                     f'go over {max_run} days in a row, and would stay within their weekly hours. Repeat '
                     'until the day is covered or nobody is left.') if fill else
                    'No one listed extra days they can take, so the roster is the merchant\'s own shifts.',
            'before_draft': {'backlog_days': base_backlog_days,
                             'final_backlog_hours': base_rows[-1]['backlog_out'],
                             'longest_runs': {m['name']: longest_run(base_work[i]) for i, m in enumerate(members)}},
        },
        'people': people,
        'need_extra_help': need_help,
        'cost': cost_estimate(data, days),
    }
    if not hourly:
        result['hourly_note'] = ('No hourly share given, so the plan lists the hours nobody is on shift '
                                 'but cannot say how many messages arrive in them.')
    return result


def build_with_scenarios(data):
    res = build(data)
    sv, ss = labelled(data, 'scenarios', required=False)
    if sv:
        if not isinstance(sv, list):
            raise InputError('scenarios.value must be a list of multipliers, for example [1.5, 2]')
        out = []
        for x in sv:
            mult = number(x, 'scenarios.value item')
            r = build(data, multiplier=mult)
            out.append({
                'label': f'scenario: every day x {mult:g}',
                'multiplier': mult, 'source': ss,
                'total_forecast': sum(p['total_forecast'] for p in r['phase_summary']),
                'peak_day': max(r['days'], key=lambda d: d['forecast_conversations'])['date'],
                'peak_forecast': max(d['forecast_conversations'] for d in r['days']),
                'gap_days': len(r['gap_days']),
                'total_gap_hours': round_half_up(sum(d['gap_hours'] for d in r['days']), 1),
                'backlog_days': len(r['backlog_days']),
                'final_backlog_hours': r['final_backlog_hours'],
                'total_estimated_bill': r['cost']['total_estimated_bill'] if r['cost'] else None,
            })
        res['scenarios'] = out
    return res


# ------------------------------------------------------------------- cost

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

    ai = hd.get('ai_meter')
    if ai is not None:
        for k in ('share_resolved_by_ai_pct', 'price_per_month', 'included_per_month',
                  'overage_price_per_resolution', 'ai_resolutions_also_count_as_tickets', 'source'):
            if k not in ai:
                raise InputError(f'missing "helpdesk.ai_meter.{k}"')
        if ai['source'] not in ALLOWED_SOURCES:
            raise InputError(f'"helpdesk.ai_meter.source" must be one of {ALLOWED_SOURCES}')
        ai_share = number(ai['share_resolved_by_ai_pct'], 'helpdesk.ai_meter.share_resolved_by_ai_pct')
        if ai_share > 100:
            raise InputError('helpdesk.ai_meter.share_resolved_by_ai_pct must be at most 100')
        ai_price = number(ai['price_per_month'], 'helpdesk.ai_meter.price_per_month')
        ai_cap = number(ai['included_per_month'], 'helpdesk.ai_meter.included_per_month')
        ai_over = number(ai['overage_price_per_resolution'], 'helpdesk.ai_meter.overage_price_per_resolution')
        also_ticket = bool(ai['ai_resolutions_also_count_as_tickets'])

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
        row = {'month': ym, 'forecast_in_window': in_window, 'rest_of_month_volume': outside,
               'total_volume': round_half_up(volume), 'lower_bound_only': (not full) and outside is None}
        ticket_volume = volume
        ai_cost = 0.0
        if ai is not None:
            ai_res = round_half_up(volume * ai_share / 100.0)
            ai_over_units = max(0.0, ai_res - ai_cap)
            ai_cost = ai_price + ai_over_units * ai_over
            if not also_ticket:
                ticket_volume = volume - ai_res
            row.update({'ai_resolutions': ai_res, 'ai_included': ai_cap,
                        'ai_over_cap': round_half_up(ai_over_units),
                        'ai_meter_cost': round_half_up(ai_cost, 2)})
        over_units = max(0.0, ticket_volume - cap)
        blocks = math.ceil(over_units / block - EPS) if over_units > 0 else 0
        over_cost = blocks * block_price
        bill = price + over_cost + ai_cost
        total += bill
        row.update({'ticket_meter_volume': round_half_up(ticket_volume), 'included': cap,
                    'over_cap_units': round_half_up(over_units), 'overage_blocks': blocks,
                    'overage_cost': round_half_up(over_cost, 2), 'estimated_bill': round_half_up(bill, 2)})
        rows.append(row)
    return {'billing_unit': hd['billing_unit'], 'source': hd['source'],
            'ai_meter': ai is not None, 'months': rows, 'total_estimated_bill': round_half_up(total, 2)}


# --------------------------------------------------------------- markdown

def to_markdown(res):
    L = []
    w = res['window']
    L.append(f"Window {w['start']} to {w['end']} ({w['days']} days). Method: {res['baseline']['method']}.")
    L.append(f"Working: {res['baseline']['working']}\n")
    if 'phase_levels' in res['baseline']:
        L.append('| Phase | Average day | Weekdays | Weekend days | Weekday level | Weekend level |')
        L.append('|---|---|---|---|---|---|')
        for p, s in res['baseline']['phase_levels'].items():
            L.append(f"| {PHASE_LABEL[p]} | {s['average_day']:g} | {s['weekdays']} | {s['weekend_days']} | "
                     f"{s['weekday_level']:g} | {s['weekend_level']:g} |")
        L.append('')
    L.append('| Assumption | Value | Source |\n|---|---|---|')
    order = sorted(res['assumptions'], key=lambda a: a['source'] != 'merchant-chosen estimate')
    for a in order:
        L.append(f"| {a['field']} | {json.dumps(a['value'])} | {a['source']} |")

    daily = 'matched_last_year_date' in res['days'][0]
    hourly = 'hours_with_messages_and_nobody_on' in res['days'][0]
    head = ['Date', 'Day', 'Phase']
    if daily:
        head.append('Last year day')
    head += ['Forecast', 'Hours needed', 'On shift (shift times)', 'Hours available', 'Gap',
             'Carried in', 'Left at end of day', 'Uncovered hours']
    if hourly:
        head.append('Messages while nobody is on')
    L.append('\n| ' + ' | '.join(head) + ' |')
    L.append('|' + '---|' * len(head))
    for r in res['days']:
        shift = ', '.join(f"{p['name']} {p['times']}" + (' (added)' if p['added_in_draft'] else '')
                          for p in r['on_shift_detail']) or 'nobody'
        cells = [r['date'], r['weekday'], PHASE_LABEL[r['phase']]]
        if daily:
            cells.append(f"{r['matched_last_year_date']} {r['matched_last_year_weekday']}")
        cells += [str(r['forecast_conversations']), f"{r['required_agent_hours']:.1f}", shift,
                  f"{r['available_agent_hours']:.1f}", f"{r['gap_hours']:.1f}" if r['gap_hours'] else '-',
                  f"{r['backlog_in_hours']:.1f}" if r['backlog_in_hours'] else '-',
                  f"{r['backlog_end_hours']:.1f}" if r['backlog_end_hours'] else '-',
                  ', '.join(r['uncovered_hours_of_day']) or 'none']
        if hourly:
            cells.append(f"{r['messages_in_those_hours']} ({', '.join(r['hours_with_messages_and_nobody_on']) or 'none'})")
        L.append('| ' + ' | '.join(cells) + ' |')
    L.append(f"\nBacklog rule: {res['backlog_rule']}")

    L.append('\n| Phase | From | To | Total forecast | Peak day | Gap days | Gap hours | Days ending with backlog |')
    L.append('|---|---|---|---|---|---|---|---|')
    for p in res['phase_summary']:
        L.append(f"| {PHASE_LABEL[p['phase']]} | {p['from']} | {p['to']} | {p['total_forecast']} | "
                 f"{p['peak_day']} ({p['peak_forecast']}) | {p['gap_days']} | {p['total_gap_hours']:g} | "
                 f"{p['backlog_days']} |")

    rd = res['roster_draft']
    L.append(f"\nRoster draft: {rd['rule']}")
    b = rd['before_draft']
    L.append(f"Before the draft: {b['backlog_days']} days end with backlog, {b['final_backlog_hours']:g} hours "
             f"left on the last day. After: {len(res['backlog_days'])} days, {res['final_backlog_hours']:g} hours.")
    L.append('\n| Person | Days worked | Shift hours | Days added in draft | Longest run of days |')
    L.append('|---|---|---|---|---|')
    for p in res['people']:
        L.append(f"| {p['name']} | {p['days_worked']} | {p['total_shift_hours']:g} | "
                 f"{', '.join(p['added_days']) or 'none'} | {p['longest_run_days']} |")
    for p in res['people']:
        for dcn in p['decisions']:
            L.append(dcn)

    if res['need_extra_help']:
        L.append('\nNeed extra help (hours of work still waiting at the end of the day):')
        for n in res['need_extra_help']:
            L.append(f"- {n['date']} {n['weekday']}: {n['hours_short_end_of_day']:.1f} hours")
    if res.get('hourly_note'):
        L.append('\n' + res['hourly_note'])

    c = res['cost']
    if c:
        L.append(f"\nHelpdesk bill, billed per {c['billing_unit']} ({c['source']})\n")
        head = ['Month', 'Volume', 'Ticket meter', 'Included', 'Over cap', 'Overage cost']
        if c['ai_meter']:
            head += ['AI resolutions', 'AI over cap', 'AI meter cost']
        head += ['Estimated bill', 'Note']
        L.append('| ' + ' | '.join(head) + ' |')
        L.append('|' + '---|' * len(head))
        for m in c['months']:
            note = 'lower bound: days outside the window not counted' if m['lower_bound_only'] else ''
            cells = [m['month'], str(m['total_volume']), str(m['ticket_meter_volume']), f"{m['included']:g}",
                     str(m['over_cap_units']), f"{m['overage_cost']:g}"]
            if c['ai_meter']:
                cells += [str(m['ai_resolutions']), str(m['ai_over_cap']), f"{m['ai_meter_cost']:g}"]
            cells += [f"{m['estimated_bill']:g}", note]
            L.append('| ' + ' | '.join(cells) + ' |')
        L.append(f"\nTotal estimated bill across these months: {c['total_estimated_bill']:g}")

    if res.get('scenarios'):
        L.append('\nScenarios. These are what-ifs on the merchant\'s own number, not forecasts.\n')
        L.append('| Scenario | Total forecast | Peak day | Gap days | Gap hours | Days ending with backlog | '
                 'Backlog on last day | Bill |')
        L.append('|---|---|---|---|---|---|---|---|')
        L.append(f"| your number | {sum(p['total_forecast'] for p in res['phase_summary'])} | "
                 f"{max(res['days'], key=lambda d: d['forecast_conversations'])['date']} "
                 f"({max(d['forecast_conversations'] for d in res['days'])}) | {len(res['gap_days'])} | "
                 f"{round_half_up(sum(d['gap_hours'] for d in res['days']), 1):g} | {len(res['backlog_days'])} | "
                 f"{res['final_backlog_hours']:g} | {c['total_estimated_bill'] if c else '-'} |")
        for s in res['scenarios']:
            L.append(f"| {s['label']} | {s['total_forecast']} | {s['peak_day']} ({s['peak_forecast']}) | "
                     f"{s['gap_days']} | {s['total_gap_hours']:g} | {s['backlog_days']} | "
                     f"{s['final_backlog_hours']:g} | {s['total_estimated_bill'] if s['total_estimated_bill'] is not None else '-'} |")
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
        res = build_with_scenarios(data)
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
