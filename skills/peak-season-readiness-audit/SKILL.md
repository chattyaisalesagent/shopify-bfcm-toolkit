---
name: peak-season-readiness-audit
description: Score a Shopify store's peak-season readiness across seven checkable lines (discount rules, holiday returns policy, delivery cutoffs, order lookup, handoff, weekly review, plan cap), using live store data when a Shopify connector is available and merchant answers otherwise, then route each gap to the toolkit skill that fixes it. Use when someone asks "are we ready for BFCM", wants a readiness score, or wants to know what to fix first before peak season.
license: MIT
compatibility: Works from merchant answers alone. Optionally reads live data through an official Shopify connector (such as the Shopify plugin for ChatGPT) when the host session has one connected; degrades to questions when it does not. No connector is required.
metadata:
  version: "0.1"
---

# Peak-season readiness audit

Shopify already publishes a 25-step BFCM checklist. It tells a merchant to state discount terms clearly, extend the holiday returns window, prepare support for the volume, and update the FAQ page. It is undated prose, it produces nothing, and there is no official Shopify Admin score.

This skill is not another checklist. It is the thing that checks whether the store actually did what the checklist says, scores it, and sends the merchant to the toolkit skill that fixes each gap.

## The rule that governs everything here

**Check evidence, not answers.** "Do you have discount rules written down?" is a question a merchant can say yes to without it being true. Wherever possible, look at the actual thing: the text on the page, the live discount configuration, the actual published cutoff date. Where you cannot look, ask, and mark the line as self-reported rather than verified.

**Never invent a score.** Every line is Ready, Partial or Missing, decided from what the merchant showed you or told you. If you don't have enough to judge a line, say so and leave it unscored rather than guessing Partial.

## Two ways to gather evidence

**With a live Shopify connector.** If this session has access to an official Shopify connector, such as the actions listed in `references/live-data-with-shopify-connector.md` (`get-shop-info`, `search_products`, `list-orders`, `run-analytics-query`), use it to check what you can directly: whether a discount code exists and what it says, recent order volume, current inventory. Say plainly in the output which lines were checked this way.

**Without one.** Ask the merchant directly, one line at a time, and for the lines that involve a published page (discount terms, returns policy, delivery cutoffs), ask them to paste the actual text rather than describe it from memory.

Never assume a connector is present. Check what tools are actually available in this session before claiming to use one, and fall back silently to asking if none exist.

## The seven lines

Read `references/scorecard.md` for the full table, the three levels per line, and where each line's score comes from. Six lines and their point bands come verbatim from the ebook's own readiness scorecard; a seventh line, holiday returns and exchange policy, is added here because it maps to a real finding on data-gap pages in the same research and to half of what `campaign-rules-policy-qa` does, but it was not part of the original six-line score. Keep it as a separately reported line, not blended into the 0–12 total, so the total stays comparable to the published bands.

**Three lines outrank the total, regardless of score elsewhere:** plan cap and overage, automated order lookup, and handoff to a person. A Missing on any of these is the first thing to raise, even if the total looks healthy. This mirrors the finding that a high aggregate score can hide one critical gap.

## How to work

1. **Check for a live connector first**, per the section above.
2. **Score all seven lines**, gathering evidence per line as described in `references/scorecard.md`.
3. **Compute the six-line total** (0 to 12) using only the original six, report the returns line separately.
4. **Apply the critical-line override.** If any of the three critical lines is Missing, lead the report with that, not with the total.
5. **Route every non-Ready line** using `references/routing.md`. Three lines route to a skill in this toolkit that fixes them. Two lines are outside this toolkit's scope entirely (order lookup, handoff) and get a pointer to where the merchant checks them. One line (plan cap) gets the vendor-question approach, since no API exposes overage behaviour.
6. **Produce the report**: the scored table, the band ("Ready" / "Foundations exist" / "Start here"), the critical-line flag if triggered, and one ranked action for each non-Ready line with which skill or which external step fixes it.

## What this skill does not do

It does not configure anything, write anything, or compute anything. It reads and scores. Every fix runs through `campaign-rules-policy-qa`, `delivery-cutoff-planner`, `conversation-gap-analyzer`, or a step outside this toolkit named plainly as such.

It does not claim a score is a guarantee. A "Ready" line based on merchant self-report is weaker evidence than one checked against a live page or a live connector, and the report should say which kind of evidence backed each line.
