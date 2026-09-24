---
name: peak-season-readiness-audit
description: Score a Shopify store's peak-season readiness across nine checkable lines (discount rules, delivery cutoffs, order lookup, handoff, weekly review, plan cap, holiday returns, proactive late-delivery notices, contingency plan), starting from what broke last peak season, using live store data when a Shopify connector is available and merchant answers otherwise, then route each gap to the toolkit tool that fixes it or to the chat app setting where it is done. Use when someone asks "are we ready for BFCM", wants a readiness score, or wants to know what to fix first before peak season.
license: MIT
compatibility: Works from merchant answers alone. Optionally reads live data through an official Shopify connector (such as the Shopify plugin for ChatGPT) when the host session has one connected; degrades to questions when it does not. No connector is required.
metadata:
  version: "0.2"
---

# Peak-season readiness audit

Shopify already publishes a 25-step BFCM checklist. It tells a merchant to state discount terms clearly, extend the holiday returns window, prepare support for the volume, and update the FAQ page. It is undated prose, it produces nothing, and there is no official Shopify Admin score.

This skill is not another checklist. It is the thing that checks whether the store actually did what the checklist says, scores it, and sends the merchant to the tool that fixes each gap.

## The rule that governs everything here

**Check evidence, not answers.** "Do you have discount rules written down?" is a question a merchant can say yes to without it being true. Wherever possible, look at the actual thing: the text on the page, the live discount configuration, the actual published cutoff date, the actual late-delivery message. Where you cannot look, ask, and mark the line as self-reported rather than verified.

**Never invent a score.** Every line is Ready, Partial or Missing, decided from what the merchant showed you or told you. If you don't have enough to judge a line, say so and leave it unscored rather than guessing Partial.

## Two ways to gather evidence

**With a live Shopify connector.** If this session has access to an official Shopify connector, such as the actions listed in `references/live-data-with-shopify-connector.md` (`get-shop-info`, `search_products`, `list-orders`, `run-analytics-query`), use it to check what you can directly: whether a discount code exists and what it says, recent order volume, current inventory. Say plainly in the output which lines were checked this way.

**Without one.** Ask the merchant directly, one line at a time, and for the lines that involve a published page or a written message (discount terms, returns policy, delivery cutoffs, late-delivery notices, contingency plan), ask them to paste the actual text rather than describe it from memory.

Never assume a connector is present. Check what tools are actually available in this session before claiming to use one, and fall back silently to asking if none exist.

## The nine lines

Read `references/scorecard.md` for the full table, the three levels per line, and where each line's score comes from.

- **Lines 1 to 6** and their point bands come verbatim from the readiness scorecard in the research. They make up the 0 to 12 total.
- **Line 7, holiday returns policy; line 8, proactive late-delivery notices; line 9, contingency plan** are additions. They are scored the same way but reported separately, never blended into the 0 to 12 total, so the total stays comparable to the published bands.

**Three lines outrank the total, regardless of score elsewhere:** plan cap and overage, automated order lookup, and handoff to a person. A Missing on any of these is the first thing to raise, even if the total looks healthy. This mirrors the finding that a high aggregate score can hide one critical gap.

## How to work

1. **Ask what broke last peak season, before any scoring.** Ask the merchant to list, in their own words, what went wrong last BFCM through January: complaints that piled up, promises that failed, questions nobody could answer, bills that surprised them. Record the list as given. Do not turn it into scores. Use it two ways: to rank the fixes at the end (a gap that already cost them once goes first), and as a check on self-reports (if something broke last year on a line the merchant now calls Ready, ask what changed since, and score from the answer). If this is their first peak season, say so in the report and move on.
2. **Check for a live connector**, per the section above.
3. **Score all nine lines**, gathering evidence per line as described in `references/scorecard.md`. Mark each line verified (you saw the text, the setting or the live data) or self-reported.
4. **Compute the six-line total** (0 to 12) from lines 1 to 6 only. Report lines 7, 8 and 9 separately, one level each.
5. **Apply the critical-line override.** If any of the three critical lines is Missing, lead the report with that, not with the total.
6. **Route every non-Ready line** using `references/routing.md`. Most lines route to a tool in this kit. Three lines (order lookup, handoff mechanics, weekly review of unanswered chat questions) are work done inside the merchant's chat app, and route to that app's settings. Plan cap also gets the vendor question list, since no API exposes overage behaviour.
7. **Produce the report**, in this order:
   - Critical-line flag, if triggered.
   - The scored table: line, level, points (lines 1 to 6 only), evidence type (verified or self-reported), one-sentence reason.
   - The six-line total and band ("Ready" / "Foundations exist" / "Start here"), then lines 7, 8 and 9 on their own: "Returns policy: Partial. Late-delivery notices: Missing. Contingency plan: Partial."
   - What broke last season, as the merchant listed it, with the line each item maps to.
   - **Fix these three first**: the three highest-priority non-Ready lines, ranked by critical-line status first, then by whether it broke last season, then by which deadline in the season is nearest. Each with the tool or setting that fixes it.
   - Every remaining non-Ready line, one action each, with its route.

## What this skill does not do

It does not configure anything, write anything, or compute anything. It reads and scores. Every fix runs through `campaign-rules-policy-qa`, `delivery-cutoff-planner`, `peak-load-cover-planner`, `peak-season-playbook`, `shipping-exception-watch`, or a step in the merchant's own chat app or with their vendor, named plainly as such.

It does not claim a score is a guarantee. A "Ready" line based on merchant self-report is weaker evidence than one checked against a live page or a live connector, and the report should say which kind of evidence backed each line.
