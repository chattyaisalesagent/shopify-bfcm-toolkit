# Baseline, measured before any skill was written

> **RETRACTED IN PART, 21 September 2026.** The numbers in the table below were measured with `allowed_tools: [Read, Glob, Grep, Skill]`. Removing those three tools, which none of these cases need, changes the result substantially: `seasonal-returns-limit` goes from 0 of 3 to 2 of 3 with no skill present. The unaided model appears to spend turns exploring an empty working directory instead of answering. **The original baseline was an artifact of the tool configuration and overstated the headroom.** The corrected measurements are in `RESULTS.md`. This file is kept unedited below as a record of the mistake.

**Run 21 September 2026**, Claude Code 2.1.278, judge model haiku, 3 runs per case, `--ablation none` against a plugin containing a manifest and no skills. Every number below is therefore what the model does **unaided**. Total cost $2.69.

The `skill-fired` grader fails in every run by construction, because there is no skill to fire. Only the `criteria` grader is meaningful here, so it is reported separately.

| Case | What it tests | Criteria runs passed | Headroom |
|---|---|---|---|
| `audit-planted-defects` | Finds four defects planted in a sale terms page | **1 of 3** | High, and it is a consistency problem |
| `invention-trap` | Refuses to invent commercial rules the merchant never gave | **1 of 3** | High, same shape |
| `seasonal-returns-limit` | Knows Shopify return rules cannot express a purchase-date-range window, and that rule changes are not retroactive | **0 of 3** | **Highest. Unaided, this fails outright** |
| `free-shipping-threshold` | Knows a free-shipping threshold is evaluated against the discounted cart value | **3 of 3** | **None. Already solved** |

## What this changes

**1. One case is already solved and must not be used to justify the skill.** `free-shipping-threshold` passes every run without help. The model knows the platform behaviour and writes unambiguous terms wording for it. The case stays in the suite as a regression guard, but it contributes nothing to the argument that a skill is needed. Counting it toward a headline score would be self-deception.

**2. The strongest justification is platform limitation knowledge.** `seasonal-returns-limit` fails all three runs. Unaided, the model writes a holiday returns policy and describes configuring it in Shopify as though a seasonal window were supported. It is not: return rules offer only a number of days from delivery, and changes apply to future orders only. This is the clearest case where a skill carries knowledge the model does not have, and it maps directly to the finding in the research that returns is the second-worst subject for having no answer ready.

**3. The other two cases are consistency failures, not capability failures.** Both pass once in three runs. The model can do the work and does not do it reliably. That is precisely what a fixed field list and an explicit refusal rule are for, and it is the least glamorous but most defensible reason to package this as a skill rather than a prompt.

## The bar the skill has to clear

Ablation flips to `with-without` once a skill exists, and the delta is what decides whether this ships.

- `seasonal-returns-limit`: must reach 3 of 3. Anything less means the skill is not carrying the knowledge it exists to carry.
- `audit-planted-defects` and `invention-trap`: must reach at least 3 of 3 and 2 of 3 respectively. Going from one in three to two in three would be noise, not a result.
- `free-shipping-threshold`: must stay at 3 of 3. If adding the skill makes an already-solved case worse, the skill is interfering rather than helping, which is a known failure mode of over-specified instructions.

**If those bars are not met, the finding is that this should ship as documentation.** That conclusion was accepted in advance, which is the only reason measuring first was worth the wall-clock time.

## Method notes

- `--ablation none` was used because with no skill present the two arms would be identical, so running both would have doubled the cost for no information.
- `with-only: true` is not a valid grader key. A `tool_used: Skill` grader is treated as a plugin-fired indicator automatically under `with-without`.
- Judge votes are visible per run in `evals/results/<timestamp>/report.html`. Two of the failures show split votes, which is worth re-reading before trusting a marginal improvement later.
