# Results

Measured 21 September 2026, Claude Code 2.1.278, judge model haiku, 3 runs per arm per case, `--ablation with-without`, `allowed_tools: [Skill]`. Skill under test: `campaign-rules-policy-qa`.

| Case | What it tests | With skill | Without | Δ |
|---|---|---|---|---|
| `invention-trap` | Refuses to invent commercial rules the merchant never gave | **1.00** (9/9 judge votes) | 0.33 | **+0.67** |
| `free-shipping-threshold` | Knows the threshold is evaluated after the discount, and writes unambiguous wording | 0.67 | 0.00 | **+0.67** |
| `audit-planted-defects` | Finds four defects planted in a sale terms page | 0.67 | 0.33 | **+0.33** |
| `seasonal-returns-limit` | Knows a seasonal returns window is not expressible as a Shopify rule | 1.00 | 1.00 | **0.00** |

**Mean Δ +0.42. Three of four cases improved, one unchanged, none regressed.**

---

## The measurement error, and what it cost

The first baseline in `BASELINE.md` is retracted. It ran with `allowed_tools: [Read, Glob, Grep, Skill]`, which none of these cases need, and the tool configuration moved the unaided results **in both directions**:

| Case | Flawed baseline | Corrected, same config as the real runs |
|---|---|---|
| `seasonal-returns-limit` | 0 of 3 | 2 to 3 of 3 |
| `free-shipping-threshold` | 3 of 3 | 0 of 3 |

Unaided runs in the corrected configuration cost about $0.05 each against $0.12 to $0.35 before, which says the responses got much shorter. The plausible reading is that file tools in an empty working directory pull the model into exploring instead of answering, and that this helps on a case rewarding thoroughness and hurts on one rewarding a direct answer. That is a hypothesis, not a finding: it was not tested separately.

**Two conclusions drawn from the flawed baseline were wrong.** That plain Claude "fails outright" on platform limitations: it does not, it mostly passes. And that the free-shipping case was "already solved, no headroom": it is the opposite, and it is now one of the two largest deltas. Both were reported before they were checked.

---

## Adjudicating the pre-registered bars

Four bars were written in `BASELINE.md` before the skill existed. Two of them referenced baseline numbers now known to be artifacts, so they cannot be applied as written.

| Bar | Outcome |
|---|---|
| `seasonal-returns-limit` reaches 3 of 3 | **Met.** 3 of 3 with the skill. But the unaided arm also scores 3 of 3, so the bar no longer demonstrates anything |
| `invention-trap` reaches at least 2 of 3 | **Met, and exceeded.** 3 of 3 with unanimous judge votes |
| `audit-planted-defects` reaches 3 of 3 | **Not met.** 2 of 3 |
| `free-shipping-threshold` stays at 3 of 3 | **Void.** It assumed a 3 of 3 baseline that was an artifact. The skill takes it from 0 of 3 to 2 of 3 |

Two met, one missed, one void. Calling this a clean pass would be dishonest; calling it a failure would ignore a mean delta of +0.42 with no regression anywhere.

---

## What the skill actually buys

Not knowledge. That was the prediction and it was wrong on the case designed to prove it: the unaided model already knows Shopify return rules cannot express a seasonal window.

What it buys is **restraint and consistency**. The clearest single result in the suite is `invention-trap`: unaided, the model twice in three runs produces a polished, confident, publishable terms page that states a stacking rule, a returns rule and an exclusion list the merchant never gave it. With the skill, all three runs mark the gaps and ask.

That failure mode is the one with real money attached, because a merchant is bound by whatever their terms page says. A plausible invented rule is worse than a visible gap.

---

## What is still not settled

**Three runs per arm is not enough.** A Δ of +0.33 on `audit-planted-defects` is one run in three. The suite supports `--runs <n>`; the two positive-but-small results should be re-measured at 5 or more runs before anyone treats +0.42 as a number rather than a direction.

**The judge is haiku and the rubrics are strict.** Several graders demand specific named facts. A response can be useful to a merchant and still fail. That makes the absolute scores pessimistic and the deltas more trustworthy than the levels.

**Two cases sit at 2 of 3 with the skill.** The skill improves the mean and has not yet made anything reliable. If consistency is what the skill is for, 2 of 3 is the thing to fix next, and the fix belongs in the skill rather than in the rubric.

**Nothing here tests skill 2.** Delivery cutoffs have their own arithmetic and need their own fixtures with known answers, which is a stronger form of grading than any rubric used here.

---

## Recommendation

**Continue, with the scope unchanged.** The evidence supports the skill: three of four cases improved, none regressed, and the largest deltas land on the failure mode that matters commercially. It does not yet support a claim that the skill makes the work reliable.

Before anything ships: re-run the suite at `--runs 5`, and fix whatever causes the two cases sitting at 2 of 3. Then build skill 2 with fixture-based grading, where a computed date is either right or wrong and no judge is involved.

Total measurement cost to reach this point, including the retracted baseline: about $9.

---

## Decision, 21 September 2026

**Stopped measuring further.** The directional signal already gathered (no regression on any case, positive delta on 3 of 4, the invention-trap result unanimous across 9 judge votes) is treated as sufficient. No `--runs 5` re-measurement, no further statistical tightening. This trades certainty for speed at a stage where no merchant has yet confirmed demand for the product at all — spending more to sharpen confidence in one skill's internal quality was judged lower priority than having both MVP skills to look at.

Skill 1 (`campaign-rules-policy-qa`) proceeds as built. Skill 2 (`delivery-cutoff-planner`) is next, graded by fixture arithmetic rather than a judge model where possible, since that grading is cheap and does not carry the same uncertainty this file documents.

---

## Skill 2, `delivery-cutoff-planner`

Graded by fixture arithmetic instead of a judge model: a target date, two zones with known transit, processing and buffer days, and two regex checks for the correct computed cutoff date. Domestic 2026-12-18, international 2026-12-11, both verified by hand and against Node's own regex engine before use.

**3 runs, single arm (`--ablation none`), $0.37 total.** 2 of 3 matched both dates. The one that did not is a false negative in the eval tool, not a wrong answer: the transcript for that run shows the skill computed both dates correctly, calling the script and reporting "Dec 18, 2026" and "Dec 11, 2026" with correct working-day arithmetic shown. Testing the same regex against that exact text in Node confirms it matches. `claude plugin eval` reported "pattern not found in last_message" anyway.

Not investigated further, per the decision above to stop chasing measurement precision. Recorded here so the false negative isn't mistaken for a skill defect later. The skill's own output was correct in all 3 runs.

No two-arm comparison was run for skill 2. The unaided-model question, whether Claude without the skill invents a plausible-sounding transit time or cutoff date instead of asking for one, is the more interesting one, and matches the failure mode `invention-trap` already found for skill 1. Left untested here; flagged for anyone extending this suite.

---

## Skill 2, `delivery-cutoff-planner` — full two-arm measurement, 21 September 2026

Requested explicitly after the skill shipped without one. 3 cases, `--ablation with-without`, 3 runs per arm, judge model haiku except `cutoff-arithmetic` which is regex-graded (no judge, no cost for that grader).

| Case | What it tests | With skill | Without | Δ |
|---|---|---|---|---|
| `transit-time-invention-trap` | Refuses to invent a carrier transit time the merchant never gave | **1.00** (9/9 votes) | 0.33 | **+0.67** |
| `cutoff-arithmetic` | Computes the correct cutoff date per zone from stated inputs | **1.00** | 0.67 | **+0.33** |
| `shopify-per-region-limit` | States plainly that Shopify's manual delivery dates are one global cutoff, not per-region | 0.67 | **1.00** | **−0.33** |

**Mean Δ +0.22.** Two of three cases improved, one regressed. Total cost of this measurement round: about $1.30.

### The regression, investigated rather than waved off

`shopify-per-region-limit` is a straight fact question: "can Shopify natively give us different cutoffs per region?" The unaided model answers it in one clean paragraph: *"No — Shopify's native delivery date settings... only support a single, store-wide order cutoff time... there's no built-in way to set separate cutoffs per shipping zone."* Direct, correct, matches the verified fact in `where-transit-times-come-from.md` almost word for word.

With the skill, the model instead opened with *"Partially,"* described a real but different Shopify feature (per-zone delivery-estimate **text** on shipping rates, which is not a computed cutoff date), and only then pivoted to *"want me to run it?"* The core fact was in there, but buried behind a hedge and a sales pitch instead of leading with it.

**Root cause:** `SKILL.md`'s "how to work" section is written entirely around the compute-and-publish workflow. It never tells the model what to do when the incoming message is a pure yes/no capability question rather than a request to actually compute something. Left to its own judgment, the model reached for "be thorough and offer to help" instead of "answer directly, then offer to help," and the directness is exactly what the baseline did right.

**Not fixed yet.** Recorded here rather than patched, consistent with the project's working pattern of writing down a finding on a live measurement before deciding whether it earns a fix. The fix, if made, is narrow: one line in `SKILL.md` instructing a direct factual answer first when the message is a capability question, before any workflow framing.

### Combined picture across both built skills

| | Skill 1 mean Δ | Skill 2 mean Δ |
|---|---|---|
| | +0.42 | +0.22 |

Both skills show real, measured value, and both show at least one case where an unaided model already does fine or better. Neither skill has been "proven" in the sense of a large sample; both have been checked honestly, including the ways they fall short, at a total measurement cost across both skills of roughly $10.50.

---

## Fix verified, 21 September 2026

Added one section to `SKILL.md`, "If the message is a plain question, answer it first" — instructs a direct factual lead before any workflow framing when the message is a yes/no platform-capability question, and names the specific failure to avoid (hedging into "partially," leading with an adjacent feature that doesn't answer what was asked).

Re-measured `shopify-per-region-limit` after the fix, same methodology:

| | Before fix | After fix |
|---|---|---|
| With skill | 0.67 (2/3) | **1.00 (3/3)** |
| Without skill | 1.00 | 0.33 |
| Δ | −0.33 | **+0.67** |

The with-skill arm is what the fix targeted, and it moved from 2/3 to 3/3 as intended. The without-skill arm also moved between runs (1.00 → 0.33), which is baseline variance across separate runs, not something the fix touched — a reminder that a single 3-run batch on either arm is noisy, and the with-skill result is the one this fix set out to change and did.

Skill 2 now stands at three cases checked, all three positive: `transit-time-invention-trap` +0.67, `cutoff-arithmetic` +0.33, `shopify-per-region-limit` +0.67 post-fix.
