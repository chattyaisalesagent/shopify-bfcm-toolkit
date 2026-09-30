---
name: peak-season-readiness-audit
description: Score a Shopify store's customer service for BFCM through January across nine checkable lines (discount rules, order-by dates, self-serve order status, handoff to a person, weekly review of what the assistant could not answer, plan cap, holiday returns, late-delivery notices, contingency plan) from the store's own data, read through a connected Shopify store or from Shopify admin exports (orders CSV, discounts CSV, policy text), asking the merchant only what no store data holds (what broke last season, how shoppers reach them, who decides refunds, the contingency plan). Marks lines that do not apply (no AI assistant, no usage-capped tool, nothing shipped) as Not applicable, then gives a first step for each line that is not Ready (in Shopify admin, the store's chat or helpdesk app, or a toolkit tool). Use when someone asks "are we ready for BFCM", wants a peak-season score, or wants to know what to fix first before peak season.
license: MIT
compatibility: Reads store data through an official Shopify connection when the session has one (the Shopify connector for Claude, the Shopify plugin for ChatGPT, or the Shopify CLI in Claude Code), otherwise from exports the merchant drops in the working folder or uploads. scripts/orders_summary.py needs Python 3 with the standard library only. With neither a connection nor exports it still runs on the merchant's answers, and says every line is self-reported.
metadata:
  version: "0.4"
---

# Peak-season readiness audit

Shopify already publishes a BFCM checklist. It tells a merchant to state discount terms clearly, extend the holiday returns window, prepare support for the volume, and update the FAQ page. It is undated prose, it produces nothing, and there is no official Shopify Admin score.

This skill checks whether the store actually did those things, from the store's own data wherever that data exists, scores it, and gives the merchant a first step for each line that is not Ready.

## The rules that govern everything here

**Store data first, questions last.** The merchant owns the store and has admin access, so most of what this audit needs already exists: the policies, the discounts, the order history. Read it before asking anything. Ask only what no store data holds, and never ask a question the data already answered.

**Three kinds of evidence, always labelled.** Every line says where its level came from:
- **Store data**: read from the connected store or an admin export (the policy text itself, a discount's settings, order and fulfilment history).
- **Pasted**: text the merchant pasted, such as a late-delivery message.
- **Merchant's answer**: what the merchant said. This is the weakest; say so.

**Never invent a score.** Every line is Ready, Partial or Missing, decided from that evidence. If you cannot judge a line, leave it "Not scored: <what is missing>" rather than guessing Partial.

**Do not punish a store for a tool it does not have.** Lines 3, 5 and 6 can be "Not applicable: <reason>" when the condition in `references/scorecard.md` is true. A store with no AI assistant has no list of unanswered assistant questions to review; a store on Shopify Inbox or plain email has no usage cap. Not applicable is left out of the score and never triggers the critical-line warning. Never use it to hide a line that applies but is hard to judge.

**Read only.** Run read queries and read files. Never create, edit or delete anything in the store, even if the connection allows it, and never message a customer.

**No sales copy.** Do not recommend, compare or praise any software, including Chatty, which publishes this kit. Where a fix lives in the merchant's chat app or helpdesk, describe what to set up in tool-neutral terms and name the app's setting only when the merchant has named the app and you know the setting from its own help pages.

## Getting the store data

Details, exact queries and export steps: `references/store-data.md`.

**Connected store.** Check the tools this session actually has. An official Shopify connection shows up as Shopify actions (such as `get-shop-info`, `list-orders`, `graphql_query`) or, in Claude Code, as a Shopify CLI the merchant has authorised for the store. With one, read the store's policies, online store pages, active discounts, shipping zones, recent orders with their fulfilments and tracking, and last season's daily order count.

**Exports.** If there is no connection, look in the working folder (or the uploaded files) for Shopify admin exports. Run `scripts/orders_summary.py` on an orders export: it gives last season's volume by day, days from order to fulfilment, regions shipped to, discount codes used and orders stuck unfulfilled. Read a discounts export as it comes. Shopify has no export for policies, so ask the merchant to paste them from Settings, Policies.

**Neither.** Before the first question, tell the merchant in two lines how to connect the store or which exports to drop in (`references/store-data.md` has the wording), and wait. If they would rather answer questions, run on answers and say in the report that every line is self-reported.

Never claim a connection or a file you have not actually read.

## How to work

1. **Get the data** as above, and say in one line what you found ("Connected to the store" or "Read your orders export, Nov 2025 to Sep 2026").
2. **Pre-score from the data.** For each line, note what the data shows (see "What store data can show" in `references/store-data.md`). Keep it to yourself: no scorecard, table, partial score or fix list until the questions below are answered. Share only a few plain findings that set up the first question.
3. **Ask only what the data could not answer**, one question per message, then wait for the answer before the next. Usually four:
   - What broke last peak season (complaints that piled up, promises that failed, surprise bills). Show what the data already suggests, such as last season's busiest week, slowest fulfilment or refunds, and ask what it felt like from the inside. First peak season: say so.
   - How shoppers reach the store (Shopify Inbox, another chat app, a helpdesk, email), whether an AI assistant or bot replies on its own, and whether any support tool caps usage or charges per ticket, conversation or message. This decides which lines are Not applicable.
   - Who takes a conversation a bot or first-line person cannot handle, and whether they can approve refunds and address changes.
   - Whether a contingency plan and late-delivery messages exist; if they do, ask for the text.
   Skip any of these the data already answered. If something broke on a line the data now shows as Ready, ask what changed.
4. **Score the nine lines** using `references/scorecard.md`, each with its evidence label.
5. **Compute the score** from lines 1 to 6 that apply (see Scoring below). Report lines 7, 8 and 9 separately.
6. **Apply the critical-line override.** If line 3, 4 or 6 is Missing, lead with that.
7. **Give a first step for every line not Ready** using `references/routing.md`: something the merchant can do in under 30 minutes in Shopify admin or their chat or helpdesk app, then the kit tool if one exists. Lines 3, 4 and 5 are set up in Shopify or the merchant's chat or helpdesk app. No tool in this kit does them, and the report says so.
8. **Produce the report**, in this order:
   - Critical lines, if triggered.
   - What the audit read: the connection or the files, with dates covered.
   - The scorecard: line, level, points ("none" if Not applicable, "separate" for 7 to 9), evidence (store data, pasted or merchant's answer), one-sentence reason that quotes the data where there is some ("Shipping policy says free over $50; the Shipping page says over $20").
   - The score as "x out of y (z%)", the band, the note that the bands are Chatty's own rubric and not an industry benchmark, then the levels of lines 7, 8 and 9.
   - What broke last season, each item with its line number.
   - **Fix these three first** (see ranking below), each with its first step and where it is done.
   - Every other line not Ready, same format.
   - Lines marked Not applicable, with the reason.
   - Evidence note: which lines rest on store data and which on the merchant's word.

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

A Ready line based on the merchant's word is weaker than one read from store data, and the report says which kind of evidence backed each line.
