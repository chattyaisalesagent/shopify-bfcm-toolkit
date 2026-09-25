---
name: peak-season-readiness-audit
description: Score a Shopify store's customer service for BFCM through January across nine checkable lines (discount rules, order-by dates, self-serve order status, handoff to a person, weekly review of what the assistant could not answer, plan cap, holiday returns, late-delivery notices, contingency plan), starting from what broke last peak season, marking lines that do not apply to the store (no AI assistant, no usage-capped tool, nothing shipped) as Not applicable, using live store data when a Shopify connector is available and merchant answers otherwise, then giving a first step for each line that is not Ready (in Shopify admin, the store's chat or helpdesk app, or a toolkit tool). Use when someone asks "are we ready for BFCM", wants a peak-season score, or wants to know what to fix first before peak season.
license: MIT
compatibility: Works from merchant answers alone. Optionally reads live data through an official Shopify connector (the Shopify plugin for ChatGPT or the Shopify connector for Claude) when the host session has one connected; falls back to questions when it does not. No connector is required.
metadata:
  version: "0.3"
---

# Peak-season readiness audit

Shopify already publishes a BFCM checklist. It tells a merchant to state discount terms clearly, extend the holiday returns window, prepare support for the volume, and update the FAQ page. It is undated prose, it produces nothing, and there is no official Shopify Admin score.

This skill checks whether the store actually did those things, scores it, and gives the merchant a first step for each line that is not Ready.

## The rules that govern everything here

**Check evidence, not descriptions.** "Do you have discount rules written down?" is a question a merchant can say yes to without it being true. Wherever possible, look at the actual thing: the text on the page, the live discount setup, the published cutoff date, the late-delivery message. Where you cannot look, ask, and mark the line self-reported rather than verified.

**Never invent a score.** Every line is Ready, Partial or Missing, decided from what the merchant showed or told you. If you cannot judge a line, leave it "Not scored: <what is missing>" rather than guessing Partial.

**Do not punish a store for a tool it does not have.** Lines 3, 5 and 6 can be "Not applicable: <reason>" when the condition in `references/scorecard.md` is true. A store with no AI assistant has no list of unanswered assistant questions to review; a store on Shopify Inbox or plain email has no usage cap. Not applicable is left out of the score and never triggers the critical-line warning. Never use it to hide a line that applies but is hard to judge.

**No sales copy.** Do not recommend, compare or praise any software, including Chatty, which publishes this kit. Where a fix lives in the merchant's chat app or helpdesk, describe what to set up in tool-neutral terms and name the app's setting only when the merchant has named the app and you know the setting from its own help pages.

## Two ways to gather evidence

**With a live Shopify connector.** If this session has an official Shopify connector (see `references/live-data-with-shopify-connector.md` for the exact action names), use it to check what it can: whether a discount exists and how it is set up (through `graphql_query`, since no dedicated action reads discounts), recent order volume, fulfilment and tracking on a real order, inventory. Say plainly in the output which lines were checked this way.

**Without one.** Ask the merchant, one question at a time, and for anything written (discount terms, returns policy, delivery cutoffs, late-delivery messages, contingency plan) ask them to paste the text rather than describe it.

Never assume a connector is present. Check the tools actually available before claiming to use one, and fall back to asking if none exist.

## How to work

1. **Ask what broke last peak season, before any scoring.** Complaints that piled up, promises that failed, questions nobody could answer, bills that surprised them. Record it as given; do not turn it into scores. Use it to rank fixes, and as a check on self-reports: if something broke on a line the merchant now calls Ready, ask what changed. If this is their first peak season, say so.
2. **Ask about the setup.** How shoppers reach the store (Shopify Inbox, another chat app, a helpdesk, email only), whether an AI assistant or bot replies on its own, whether any support tool has a usage cap or per-ticket, per-conversation or per-message charge, and whether the store ships physical goods. These answers decide which lines are Not applicable.
3. **Check for a live connector**, per the section above.
4. **Score the nine lines** using `references/scorecard.md`. Mark each verified or self-reported.
5. **Compute the score** from lines 1 to 6 that apply (see Scoring below). Report lines 7, 8 and 9 separately.
6. **Apply the critical-line override.** If line 3, 4 or 6 is Missing, lead with that.
7. **Give a first step for every line not Ready** using `references/routing.md`: something the merchant can do in under 30 minutes in Shopify admin or their chat or helpdesk app, then the kit tool if one exists. Lines 3, 4 and 5 are set up in Shopify or the merchant's chat or helpdesk app. No tool in this kit does them, and the report says so.
8. **Produce the report**, in this order:
   - Critical lines, if triggered.
   - The scorecard: line, level, points ("none" if Not applicable, "separate" for 7 to 9), evidence (verified or self-reported), one-sentence reason.
   - The score as "x out of y (z%)", the band, the note that the bands are Chatty's own rubric and not an industry benchmark, then the levels of lines 7, 8 and 9.
   - What broke last season, each item with its line number.
   - **Fix these three first** (see ranking below), each with its first step and where it is done.
   - Every other line not Ready, same format.
   - Lines marked Not applicable, with the reason.
   - Evidence note: which lines were verified and which self-reported.

## Scoring

Score = points from lines 1 to 6 that were scored and apply, out of 2 x the number of those lines. With all six applying, that is out of 12, exactly as in the report. Bands are set on the percentage so they stay the same when lines drop out:

| Score | Band | Meaning |
|---|---|---|
| 83% or more (10 to 12 of 12) | Ready | Keep it that way; keep the weekly review going if line 5 applies |
| 50% to 82% (6 to 9 of 12) | Foundations exist | Set up but untested under load |
| Below 50% (0 to 5 of 12) | Start here | Basics are missing |

The bands are Chatty's own rubric from its "Before BFCM 2026" report, not an industry benchmark. Say so in the report. If an applicable line of 1 to 6 is Not scored, report "x out of y from the lines scored, n not scored" and give no band.

**Ranking the fixes.** One rule, used for both "Fix these three first" and the rest, across all nine lines: critical lines (3, 4, 6) that are Missing first, then lines tied to what broke last season, then Missing before Partial, then critical lines before the rest, then the nearest deadline in the season. If fewer than three lines are not Ready, list only those.

**Critical-line override.** Lines 3, 4 and 6 outrank the score. A Missing on any of them comes first, whatever the score. Not applicable is never critical.

## What this skill does not do

It does not configure anything, write policies or compute dates. It reads, scores and names the first step. Fixes run through `campaign-rules-policy-qa`, `delivery-cutoff-planner`, `peak-load-cover-planner`, `peak-season-playbook`, `shipping-exception-watch`, or a step in Shopify admin, the merchant's chat or helpdesk app, or with their vendor, named plainly as such.

A Ready line based on self-report is weaker than one checked against a live page or connector, and the report says which kind of evidence backed each line.
