#!/usr/bin/env python3
"""
Check that every copy-paste prompt fits in one chat message.

Counts characters (Unicode code points of the UTF-8 decoded text), not bytes,
so curly quotes and other non-ASCII count as one each.

Limit: 7,200 characters. The tightest mainstream chat box we could find is
about 8,000 characters (Microsoft 365 Copilot Chat without a Copilot licence,
user reports 2025; consumer Copilot reports 10,240; ChatGPT turns pastes over
10,000 into an attachment). 7,200 leaves a 10% margin for Windows line endings
and a line the merchant types above the prompt. See the kit notes for sources.

Usage:
    scripts/check-prompt-length.py                 # every prompts/*.md
    scripts/check-prompt-length.py slug [slug...]  # prompts/<slug>.md only
    PROMPT_MAX_CHARS=7000 scripts/check-prompt-length.py

Exit 0 if all fit, 1 if any is too long or missing.
"""
import glob
import os
import sys

MAX_CHARS = int(os.environ.get('PROMPT_MAX_CHARS', '7200'))
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PROMPTS = os.path.join(REPO, 'prompts')


def main(argv):
    if argv:
        paths = [os.path.join(PROMPTS, f'{slug}.md') for slug in argv]
    else:
        paths = sorted(glob.glob(os.path.join(PROMPTS, '*.md')))
    if not paths:
        print(f'no prompts found in {PROMPTS}', file=sys.stderr)
        return 1

    failed = False
    for path in paths:
        rel = os.path.relpath(path, REPO)
        if not os.path.isfile(path):
            print(f'MISSING   {rel}', file=sys.stderr)
            failed = True
            continue
        with open(path, encoding='utf-8') as f:
            n = len(f.read())
        if n > MAX_CHARS:
            print(f'TOO LONG  {rel}: {n:,} characters, limit {MAX_CHARS:,} '
                  f'(over by {n - MAX_CHARS:,})', file=sys.stderr)
            failed = True
        else:
            print(f'ok        {rel}: {n:,} characters')

    if failed:
        print(f'Prompt length check failed: every prompt must be at most '
              f'{MAX_CHARS:,} characters to paste into one chat message.',
              file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
