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

The skills themselves (`SKILL.md` plus `scripts/` and `references/`) follow the open, cross-vendor [Agent Skills](https://agentskills.io/specification) format. The repo ships two packagings on top of that, one per plugin ecosystem, so they coexist without conflict:

- `.claude-plugin/` — Claude Code's own manifest and marketplace format
- `plugin.json` at the repo root, plus `.agents/plugins/marketplace.json` — the [Agent Plugins 1.0.0](https://agent-plugins.org/specification) format used by Codex, ChatGPT and other clients built on that standard (Amazon, Cursor, Microsoft, OpenAI, Vercel back it; Anthropic does not, which is why Claude Code needs its own manifest above)

### Claude Code

Verified end-to-end: cloned, installed and run through `claude plugin marketplace add` / `claude plugin install` on this machine.

**Try it for one session, no install:**

```bash
claude --plugin-dir /path/to/shopify-peak-season-toolkit
```

**Install once, keep it:**

```bash
claude plugin marketplace add thulmservice/shopify-peak-season-toolkit
claude plugin install shopify-peak-season-toolkit
```

### Codex / ChatGPT / other Agent Plugins 1.0.0 clients

Packaged to the published spec (root `plugin.json`, `.agents/plugins/marketplace.json`, `skills/` at the plugin root) but **not yet verified against a real Codex or ChatGPT install** — this machine has no Codex CLI to test with. If you try it and it doesn't pick up, open an issue with what the client did instead.

```bash
codex plugin marketplace add https://github.com/thulmservice/shopify-peak-season-toolkit
codex plugin install shopify-peak-season-toolkit
```

(Command names above are the documented pattern; confirm against your client's actual CLI, which may differ.)

### Any other agent that reads SKILL.md directly

Point it at `skills/campaign-rules-policy-qa/` or `skills/delivery-cutoff-planner/` — each is a self-contained, spec-compliant skill folder that doesn't depend on the plugin wrapper at all.

Then just describe what you need — "check this sale terms draft before we publish it", "when's the last day to order for Christmas delivery to the EU" — and the relevant skill fires on its own.

## Status

Early. Two skills, a fixed field list each, no integrations. Evaluated against a no-skill baseline with a small eval suite; see `evals/` for the method, the results, and a retraction of an earlier measurement that turned out to be a tooling artifact — kept in place rather than deleted, as a record of what happened.

## License

MIT, see [`LICENSE`](LICENSE).
