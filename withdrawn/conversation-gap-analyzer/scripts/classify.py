#!/usr/bin/env python3
"""
Rule-based first pass over an exported conversation/ticket CSV, from any
support platform. Classifies each row into one of five gap types where a
rule is confident, and leaves the rest "unclassified" for a human or a
model to read and decide.

Deterministic: the same input always produces the same rule-based labels,
so counts are comparable week over week. This script never uses an LLM
and never guesses a semantic category; it only catches the patterns
below. Everything it leaves unclassified is where a real reading of the
text is required, which this script does not attempt.

No network access, no dependencies beyond the standard library.

Gap types:
    needs_content   - a genuine question needing new or corrected content
    needs_action    - needs a workflow action (restock alert, cancellation,
                       address change), not a content page
    needs_context   - references an order number or account detail; needs
                       order-lookup / account data, not a content page
    needs_handoff   - explicit request for a human, or strong negative
                       sentiment language
    needs_nothing   - thank-yous, short acknowledgements, button-click
                       artifacts; no answer required
    unclassified    - the rules found no confident signal; read by hand
                       or by a model, one bucket only, no new buckets

Usage:
    python3 classify.py <input.csv> --text-column <column_name> [--out <output.csv>]

If --text-column is omitted, the script looks for a column named one of:
message, question, text, body, content, query (case-insensitive) and
reports an error naming the columns it found if none match.

Exit codes:
    0  classified successfully
    2  input file missing, unreadable, or no usable text column found
"""
import sys
import csv
import re
import argparse
from collections import Counter

TEXT_COLUMN_CANDIDATES = ['message', 'question', 'text', 'body', 'content', 'query']

# Order matters: more specific / higher-confidence patterns first.
# Every pattern here is deliberately narrow. A miss falls through to
# "unclassified" rather than being force-fit into the wrong bucket.

NEEDS_NOTHING_RE = re.compile(
    r'^\s*('
    r'thanks?( you)?!?|thank you( so much| very much)?!?|ty|tysm|'
    r'ok(ay)?!?|k\.?|got it!?|perfect!?|great!?|awesome!?|cool!?|'
    r'yes|yep|yeah|no|nope|nah|'
    r'sounds good!?|will do!?|understood!?|noted!?|👍+|❤️+|🙏+'
    r')\s*[.!]*\s*$',
    re.IGNORECASE
)

ORDER_REFERENCE_RE = re.compile(
    r'(#\s?\d{4,}|\border\s*(number|no\.?|#)?\s*:?\s*\d{4,}|\btracking\s*(number|#)?\s*:?\s*[a-z0-9]{6,})',
    re.IGNORECASE
)

NEEDS_ACTION_RE = re.compile(
    r'\b('
    r'notify me when|back in stock|restock|let me know when|'
    r'cancel (my )?order|change my (shipping )?address|'
    r'update my (email|phone|address)|add.{0,15}to.{0,15}cart|'
    r'unsubscribe'
    r')\b',
    re.IGNORECASE
)

NEEDS_HANDOFF_RE = re.compile(
    r'\b('
    r'talk to (a )?(human|person|agent|someone)|speak to (a )?(human|person|agent|manager)|'
    r'real person|actual human|human agent|'
    r'this is (unacceptable|ridiculous)|worst (service|experience)|'
    r'i want a (refund|manager)|escalate|file a complaint'
    r')\b',
    re.IGNORECASE
)


def find_text_column(fieldnames, override):
    if override:
        if override not in fieldnames:
            return None
        return override
    lower_map = {f.lower(): f for f in fieldnames}
    for candidate in TEXT_COLUMN_CANDIDATES:
        if candidate in lower_map:
            return lower_map[candidate]
    return None


def classify_row(text):
    if text is None or not text.strip():
        return 'needs_nothing', 'rule:empty'

    stripped = text.strip()

    if NEEDS_NOTHING_RE.match(stripped):
        return 'needs_nothing', 'rule:short_ack'

    if NEEDS_HANDOFF_RE.search(stripped):
        return 'needs_handoff', 'rule:handoff_language'

    if NEEDS_ACTION_RE.search(stripped):
        return 'needs_action', 'rule:action_keyword'

    if ORDER_REFERENCE_RE.search(stripped):
        return 'needs_context', 'rule:order_reference'

    return 'unclassified', 'rule:no_confident_match'


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('input', help='Path to the input CSV')
    ap.add_argument('--text-column', help='Name of the column holding message text')
    ap.add_argument('--out', help='Write the classified CSV here instead of alongside stdout summary')
    args = ap.parse_args()

    try:
        with open(args.input, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            if not fieldnames:
                print('error: input CSV has no header row', file=sys.stderr)
                sys.exit(2)

            text_col = find_text_column(fieldnames, args.text_column)
            if not text_col:
                print(
                    f'error: no usable text column found. Columns present: {fieldnames}. '
                    f'Pass --text-column <name> to specify one.',
                    file=sys.stderr
                )
                sys.exit(2)

            rows = list(reader)
    except FileNotFoundError:
        print(f'error: input file not found: {args.input}', file=sys.stderr)
        sys.exit(2)
    except UnicodeDecodeError as e:
        print(f'error: could not read {args.input} as UTF-8: {e}', file=sys.stderr)
        sys.exit(2)

    counts = Counter()
    for row in rows:
        gap_type, source = classify_row(row.get(text_col, ''))
        row['gap_type'] = gap_type
        row['gap_type_source'] = source
        counts[gap_type] += 1

    out_fieldnames = list(fieldnames) + ['gap_type', 'gap_type_source']
    out_path = args.out or (args.input.rsplit('.', 1)[0] + '.classified.csv')
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=out_fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    total = len(rows)
    print(f'Classified {total} rows from "{text_col}", written to {out_path}\n')
    print(f'{"Gap type":<16} {"Count":>7} {"Share":>8}')
    for gap_type in ['needs_content', 'needs_action', 'needs_context', 'needs_handoff', 'needs_nothing', 'unclassified']:
        c = counts.get(gap_type, 0)
        share = f'{100 * c / total:.1f}%' if total else '0.0%'
        print(f'{gap_type:<16} {c:>7} {share:>8}')
    print(
        f'\n{counts.get("unclassified", 0)} rows need a real read: open {out_path}, '
        f'read each row marked "unclassified", and assign exactly one of the five gap types. '
        f'Do not invent a sixth category.'
    )


if __name__ == '__main__':
    main()
