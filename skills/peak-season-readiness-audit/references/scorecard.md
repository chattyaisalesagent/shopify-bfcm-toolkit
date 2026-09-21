# The seven lines

The first six are verbatim from the readiness scorecard in the peak-season research (Chatty, "Before BFCM 2026", page 19). Each line scores Ready (2 points), Partial (1 point) or Missing (0 points). The seventh line is an addition, kept separate from the 0–12 total so that total stays comparable to the published bands.

## 1. Discount rules

- **Ready (2):** Written down and readable by the assistant handling shopper questions.
- **Partial (1):** Written but not loaded anywhere the assistant or staff can reach it.
- **Missing (0):** Only in the head of whoever runs the promotion.

**How to check.** Ask for the current or planned sale terms text. If a connector is available, `search_products` or a discount lookup can confirm a code exists, but existence of a code is not the same as the terms being written down; the terms text itself is what this line scores. Route a non-Ready result to `campaign-rules-policy-qa`.

## 2. Order-by dates per region

- **Ready (2):** Published for every region the store sells to.
- **Partial (1):** One general date only, not broken out by region.
- **Missing (0):** Not published anywhere.

**How to check.** Ask for the published cutoff text, or find it on the site. Route a non-Ready result to `delivery-cutoff-planner`.

## 3. Automated order lookup

- **Ready (2):** Shoppers can self-serve, tested on a real order.
- **Partial (1):** The feature exists but has not been tested end to end.
- **Missing (0):** Every lookup still needs a person.

**How to check.** Ask whether the store has order lookup enabled in Shopify Inbox or their helpdesk, and whether anyone has tested it on a real order recently. If a connector is available, `get-order` or `list-orders` confirm the underlying data is reachable, but do not confirm the shopper-facing self-serve path works; ask separately. **This line is outside the toolkit's scope to fix.** Route per `references/routing.md`.

## 4. Handoff to a person

- **Ready (2):** Rules, a summary, and someone with the authority to act.
- **Partial (1):** Handoff happens but the person receiving it has no context.
- **Missing (0):** No rules for when or how a handoff happens.

**How to check.** Ask who receives an escalated conversation, whether they get a summary or just a raw transcript, and whether that person can actually approve exceptions (refunds, address changes) or has to escalate again. **Outside the toolkit's scope to fix.** Route per `references/routing.md`.

## 5. Weekly review

- **Ready (2):** Run for at least two consecutive weeks already.
- **Partial (1):** Done occasionally, not on a cadence.
- **Missing (0):** The list of unanswered messages has never been opened.

**How to check.** Ask when the store last reviewed its unanswered or fallback message list, and whether it happens on a schedule. Route a non-Ready result to `conversation-gap-analyzer`.

## 6. Plan cap and overage

- **Ready (2):** Compared against last year's BFCM week volume.
- **Partial (1):** The cap is known but has not been compared against expected load.
- **Missing (0):** The overage price is not known at all.

**How to check.** Ask what plan or tier the store's support/AI system is on, what the included allowance is, and what happens at the cap. No API reliably exposes this across vendors; this is a question for the merchant to take to their own vendor. **Outside the toolkit's scope to fix**, but see `references/routing.md` for the question list to hand the merchant.

## 7. Holiday returns and exchange policy — added here, reported separately

Not part of the original six-line scorecard. Added because it traces to its own finding in the research (stock and returns questions peak after the holiday, and returns is the subject stores are least often ready to answer even outside the holiday), and because it is exactly the second half of what `campaign-rules-policy-qa` does. Scored the same way but kept out of the 0–12 total below.

- **Ready (2):** The holiday returns window, who pays return shipping, and the gift-without-receipt case are all written down.
- **Partial (1):** Some of these are decided but not all, or decided but not published anywhere a shopper or a staff member can see them.
- **Missing (0):** None of this has been decided.

**How to check.** Ask for the current returns policy text and whether it says anything specific about the holiday period. Route a non-Ready result to `campaign-rules-policy-qa`.

---

## Scoring

Sum lines 1–6 only, 0 to 12.

| Total | Band | Meaning |
|---|---|---|
| 10–12 | Ready | What remains is keeping the weekly review going |
| 6–9 | Foundations exist | Untested under load. Start with the lines scored Partial |
| Below 6 | Start here | Start with two lines scored Missing, prioritised by which deadline in the season is nearest |

Report line 7 (returns) alongside the total, not folded into it: "6-line score: 8/12 (Foundations exist). Returns policy: Partial."

## The critical-line override

Lines 3, 4 and 6 (order lookup, handoff, plan cap) outrank the total. If any of the three is Missing, say so first, before the total, regardless of what the total is. A store can score 10/12 and still be one plan-cap surprise away from the AI going silent in the busiest week.
