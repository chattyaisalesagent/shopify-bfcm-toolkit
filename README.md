# Shopify Peak-Season Readiness Toolkit

Two Claude Code skills that turn peak-season decisions into publishable artifacts for a Shopify store: sale terms and holiday policy QA, and per-region delivery cutoff dates.

No Shopify account, export, API key or integration required. Everything runs from what you tell it.

## What it does

**`campaign-rules-policy-qa`** — Check a sale terms page you already have for contradictions, missing rules and ambiguity, or write one from scratch by answering a fixed set of questions. Covers discount stacking, sale-item returnability, free-shipping thresholds, exclusions, and holiday returns and exchanges. Flags what Shopify's platform cannot actually enforce, so you are not publishing a promise the store will break.

**`delivery-cutoff-planner`** — Compute the last day a customer can order and still get their package by a target date, per shipping zone, from your own processing time and carrier transit estimates. Also writes the three delivery messages Shopify does not provide out of the box: on track, running late, and won't arrive in time.

## Why

Full reasoning, including which Shopify capabilities this does and does not duplicate, is in [`docs/`](docs/):

- [`docs/ebook-to-product-mapping.md`](docs/ebook-to-product-mapping.md) — the research behind this and what merchant work it points to
- [`docs/skill-opportunity-assessment.md`](docs/skill-opportunity-assessment.md) — why these two, and what was rejected or deferred
- [`docs/platform-compatibility.md`](docs/platform-compatibility.md) — how this packages across Claude Code and other agent platforms

Both skills carry one rule throughout: **never state a commercial rule you were not given.** A missing answer is marked and asked about; it is never guessed. See [`evals/RESULTS.md`](evals/RESULTS.md) for measured evidence that this matters — an unguided assistant asked to "write our sale terms" invents a stacking rule, a returns rule and an exclusion list in two of three tries.

## Install

**Try it for one session, no install:**

```bash
claude --plugin-dir /path/to/shopify-peak-season-toolkit
```

**Install once, keep it:**

```bash
claude plugin marketplace add thulmservice/shopify-peak-season-toolkit
claude plugin install shopify-peak-season-toolkit
```

Then just describe what you need — "check this sale terms draft before we publish it", "when's the last day to order for Christmas delivery to the EU" — and the relevant skill fires on its own.

## Status

Early. Two skills, a fixed field list each, no integrations. Evaluated against a no-skill baseline with a small eval suite; see `evals/` for the method, the results, and a retraction of an earlier measurement that turned out to be a tooling artifact — kept in place rather than deleted, as a record of what happened.

## License

MIT, see [`LICENSE`](LICENSE).
