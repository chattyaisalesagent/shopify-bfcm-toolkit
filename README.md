# The BFCM Support Kit (Shopify Peak-Season Readiness Toolkit)

Six skills for the customer service work that happens outside a chat app: what a Shopify store promises shoppers, how the team covers the rush, and what happens to orders once they ship. Published by [Chatty](https://chatty.net/bfcm-2026/). Every skill drafts; nothing changes the store or messages a customer.

Each skill also ships as a copy-paste prompt in [`prompts/`](prompts/) for any AI chat (ChatGPT, Gemini, Claude, Copilot).

## What it does, in season order

| # | Skill | When | What you get |
|---|---|---|---|
| 1 | `peak-season-readiness-audit` | October | Reads your store (connected, or from admin exports), scores each readiness line, and gives the three fixes to make first and which skill handles each |
| 2 | `campaign-rules-policy-qa` | Every sale | Sale terms and holiday returns policy checked for gaps, and every place the same term reads differently |
| 3 | `delivery-cutoff-planner` | Early November | Per-zone "order by" dates (script), and on-track / late / won't-make-it messages |
| 4 | `peak-load-cover-planner` | Late October | Daily volume forecast to mid-January, a named roster, and the helpdesk bill if the cap is exceeded (script) |
| 5 | `peak-season-playbook` | Early November | A one-page staff brief, a who-decides-what table, and three contingency plans |
| 6 | `shipping-exception-watch` | Daily in season | Late, stalled, customs-held and reported-missing orders from your order export, ranked, with draft messages (script) |

`withdrawn/conversation-gap-analyzer` is kept for reference but is not part of the kit.

Rebuild the prompt copies and download zips for chatty.net with `scripts/package-kit.sh`.

## Why

Full reasoning, including which Shopify capabilities this does and does not duplicate, is in [`docs/`](docs/):

- [`docs/ebook-to-product-mapping.md`](docs/ebook-to-product-mapping.md) — the research behind this and what merchant work it points to
- [`docs/skill-opportunity-assessment.md`](docs/skill-opportunity-assessment.md) — why these two, and what was rejected or deferred
- [`docs/platform-compatibility.md`](docs/platform-compatibility.md) — how this packages across Claude Code and other agent platforms

Every skill carries one rule throughout: **never state a commercial rule you were not given.** A missing answer is marked and asked about; it is never guessed. See [`evals/RESULTS.md`](evals/RESULTS.md) for measured evidence that this matters — an unguided assistant asked to "write our sale terms" invents a stacking rule, a returns rule and an exclusion list in two of three tries.

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
claude plugin marketplace add chattyaisalesagent/shopify-bfcm-toolkit
claude plugin install shopify-peak-season-toolkit
```

### Codex

Verified: install via marketplace runs end to end with the Codex CLI and lands the correct files, skills included. Whether Codex actually *invokes* a skill on a natural request hasn't been checked yet — that needs a logged-in Codex session, which this install test didn't have.

```bash
codex plugin marketplace add chattyaisalesagent/shopify-bfcm-toolkit
codex plugin add shopify-peak-season-toolkit@shopify-peak-season
```

### ChatGPT / other Agent Plugins 1.0.0 clients

Packaged to the same spec Codex reads (root `plugin.json`, `.agents/plugins/marketplace.json`, `skills/` at the plugin root), but not separately verified against ChatGPT. If it behaves differently there, open an issue with what happened.

### Any other agent that reads SKILL.md directly

Point it at `skills/campaign-rules-policy-qa/` or `skills/delivery-cutoff-planner/` — each is a self-contained, spec-compliant skill folder that doesn't depend on the plugin wrapper at all.

**Let the readiness audit read your store.** It works best on your own data. In Claude Code, either authorise the Shopify CLI for your store once (read-only scopes, listed in [`store-data.md`](skills/peak-season-readiness-audit/references/store-data.md)):

```bash
shopify store auth --store your-store.myshopify.com --scopes read_legal_policies,read_discounts,read_orders,read_all_orders,read_content,read_shipping,read_reports
```

or drop your Shopify admin exports (orders CSV, discounts CSV, policy text) in the folder you run Claude Code from. In the Claude app, connect the Shopify connector for Claude, or upload the same exports.

Then just describe what you need — "check this sale terms draft before we publish it", "when's the last day to order for Christmas delivery to the EU" — and the relevant skill fires on its own.

## Status

Early. Two skills, a fixed field list each, no integrations. Evaluated against a no-skill baseline with a small eval suite; see `evals/` for the method, the results, and a retraction of an earlier measurement that turned out to be a tooling artifact — kept in place rather than deleted, as a record of what happened.

## License

MIT, see [`LICENSE`](LICENSE).
