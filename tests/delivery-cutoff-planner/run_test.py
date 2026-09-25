#!/usr/bin/env python3
"""
Run cutoff.py on every case in cases.json and compare against dates that were
counted by hand. Also feeds invalid inputs and checks each one is refused with
a clear message (exit 3, no traceback). Standard library only.
Exit 0 on pass, 1 on fail.

Usage:
    python3 tests/delivery-cutoff-planner/run_test.py
"""
import copy
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
SCRIPT = os.path.join(ROOT, 'skills', 'delivery-cutoff-planner', 'scripts', 'cutoff.py')

failures = []


def check(label, ok, detail=''):
    print(f"{'PASS' if ok else 'FAIL'}  {label}{'  ' + detail if detail else ''}")
    if not ok:
        failures.append(label)


def run(data, today, raw=None):
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
        f.write(raw if raw is not None else json.dumps(data))
        path = f.name
    try:
        return subprocess.run([sys.executable, SCRIPT, path, '--today', today],
                              capture_output=True, text=True)
    finally:
        os.unlink(path)


def main():
    with open(os.path.join(HERE, 'cases.json')) as f:
        cases = json.load(f)

    for case in cases['valid']:
        proc = run(case['input'], case['today'])
        if proc.returncode != 0:
            check(f"{case['id']} runs", False, proc.stderr.strip())
            continue
        zones = {z['zone']: z for z in json.loads(proc.stdout)['zones']}
        for exp in case['expect']:
            got = zones.get(exp['zone'])
            if got is None:
                check(f"{case['id']} {exp['zone']} present", False)
                continue
            for k, want in exp.items():
                if k == 'zone':
                    continue
                check(f"{case['id']} {exp['zone']} {k}", got.get(k) == want,
                      f"got {got.get(k)!r}, want {want!r}")
            if got.get('status') == 'computed':
                rows = got.get('countdown') or []
                check(f"{case['id']} {exp['zone']} countdown ends on cutoff",
                      bool(rows) and rows[-1]['date'] == got['cutoff_date'])

    base = cases['valid'][0]['input']
    for case in cases['invalid']:
        data = copy.deepcopy(base)
        zone = data['zones'][0]
        zone.update(case.get('patch', {}))
        if 'drop' in case:
            zone.pop(case['drop'])
        data.update(case.get('top', {}))
        data['warehouse'].update(case.get('top_warehouse', {}))
        if 'remove_top' in case:
            data.pop(case['remove_top'])
        proc = run(data, '2026-09-24')
        ok = (proc.returncode == 3 and case['error_contains'] in proc.stderr
              and 'Traceback' not in proc.stderr and not proc.stdout.strip())
        check(f"invalid {case['id']} refused", ok,
              f"exit {proc.returncode}: {proc.stderr.strip()}")

    proc = run(None, '2026-09-24', raw='{not json')
    check('invalid JSON file refused', proc.returncode == 2 and 'Traceback' not in proc.stderr,
          f"exit {proc.returncode}: {proc.stderr.strip()}")

    print(f"\n{'ALL PASS' if not failures else f'{len(failures)} FAILED'}")
    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main()
