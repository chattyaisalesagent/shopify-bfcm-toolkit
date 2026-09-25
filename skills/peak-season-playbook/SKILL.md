---
name: peak-season-playbook
description: Write the peak-season playbook a Shopify merchant's human support team works from during BFCM and the holidays. Produces a one-page brief for staff and seasonal hires that reads on a phone (active promotions, delivery cutoffs, returns window, duties and international returns, where each policy lives), a table of who may decide refunds, exchanges and compensation and up to what amount, and contingency plans for a carrier delay, a stock-out mid-sale, volume above forecast and a parcel held at customs. Takes one fill-in form and one short reply, and works for a solo founder with no written policies by offering labelled example options to pick from. Use when a merchant asks for a support team brief, onboarding notes for seasonal staff, refund or compensation authority limits, an escalation policy, or a plan for what to do if shipping is delayed, stock runs out or the team is overwhelmed during peak season.
license: MIT
compatibility: Works with no integrations and no scripts. The merchant supplies their own terms, policies, cutoff dates and limits, optionally as the output of campaign-rules-policy-qa and delivery-cutoff-planner.
metadata:
  version: "0.3"
---

# Peak season playbook

In November a support agent answers questions about rules somebody else decided: which codes stack, when the last order ships for Christmas, how long a gift can be returned. In the first week of December a seasonal hire who started on Monday gets asked for a refund on a late order, and nobody told them whether they may give one. This skill writes the document that tells them, before they are asked.

It is written for people, not for an AI assistant. Short sentences, one fact per line, readable on a phone between two chats.

## The rule that governs everything here

**Money limits and commercial rules come only from the merchant. Never fill one in.**

How much an agent may refund without asking, what compensation a late order earns, whether a sale item can be exchanged: each of these is money the merchant will pay, and an agent will do exactly what the playbook says. A reasonable-sounding default is worse than a visible gap, because the gap gets answered and the default gets followed.

### When the merchant has no policy yet

Many merchants, often a solo founder hiring one seasonal helper, have never written a refund limit down. Do not leave them with a playbook full of gaps, and do not decide for them. For each blocking decision (defined below), offer 2 or 3 options in turn 2, labelled so nobody mistakes them for advice:

> Examples, pick one or write your own. Seasonal hire may refund up to: $0 / $25 / $50

Rules for examples:
- Use the merchant's currency (it is on the intake form).
- Label them as examples every time. Never write "recommended", "standard" or "typical".
- Only a value the merchant picks, types or explicitly accepts goes into the playbook. If they say "you decide" or "whatever is normal", ask them to pick one.
- Order the options most cautious first, so the "all a" shortcut in turn 2 is the safest choice. An explicit "all a" or "1b" is a decision; a blank is not.

Anything still unanswered is marked `[DECISION NEEDED: <the question>]` inline, where it would be used, and repeated in Open decisions at the end. Do not smooth over an ambiguous policy either: a returns page that says "30 days" and does not say from order or from delivery goes in the brief as a marked question, not as your best guess. If two sources disagree, show both and mark the conflict. Watch for rules that collide, such as a promotion that turns every discounted item into an exchange-only "sale item".

## Shopify facts that always go in the playbook

These are platform behaviour, not merchant choices. Put them in Part 2 whatever the merchant answers. Sources are in `references/authority-table-template.md`.

- Shopify only lets you cancel an order while nothing on it is fulfilled. Once any item is fulfilled, staff refund and return instead. Never tell staff to cancel a shipped order.
- Refunds can't be issued while a chargeback is open. Any chargeback or dispute goes straight to the owner. Nobody refunds, or gives a gift card or discount, on a disputed order.
- Shopify's refund staff permissions are on or off with no amount cap, so the limits in Part 2 are a written rule. A role that may not refund at all should have its refund permissions turned off. The lead (or the owner, if there is no lead) checks refunds daily with an order filter.
- If a stock-out means an order can't ship on time, a full refund is always one of the options. In the US the FTC Mail Order Rule requires offering cancellation with a prompt refund when the merchant can't ship in the time promised (or 30 days if none was promised).
- "Continue selling when out of stock" lets online orders go past zero, and if they use Shopify POS it can sell below zero (it warns staff). Check both before the sale.
- If they ship to the EU or UK, one line in Open decisions: EU and UK shoppers have a legal right to cancel online orders; the playbook is not legal advice.

## The conversation: 3 turns, at most 4

The merchant should get the playbook on the third message. Do not interview them one question at a time.

**Turn 1. One intake form.** Two lines on what you will write, then the form below in one copyable block. Ask them to fill what they know, leave the rest blank and send it back in one message. They can paste, instead of filling those parts, the terms, FAQ and staff decision table from `campaign-rules-policy-qa` and the cutoff table and three delivery messages from `delivery-cutoff-planner`. Treat pasted outputs as merchant-stated and carry their `[DECISION NEEDED]` markers over unchanged. Pre-fill any line their first message already answers, and flag at once anything in it that conflicts with a Shopify fact above (for example "agents cancel shipped orders" or "refund when a chargeback is open"), with the fix. If they ask for only one part, such as the authority table, send only the form lines that part needs, and if their first message already covers those, skip the form and go to turn 2 or 3.

```
Store: name / currency / countries you ship to
Promotions (one line each): name / start and end, time and timezone / who gets it / not valid on / stacks with other codes? / what staff say if a code fails
Order-by dates: region / last order date / shipping method / what staff may offer after a cutoff
Returns: days / from order or delivery / which order dates / sale items / gifts / who pays return shipping / where each policy lives
Team: role, name, days and hours (one line each) / who covers weekends and holidays
Limits per role, with currency: refunds / exchanges / discount codes / gift cards / free shipping / honour an expired code / most compensation for one order / types that can't be combined
Escalation: what always goes to you / channel / what staff tell the shopper meanwhile / how fast you reply / who handles a carrier delay, a stock-out, a busy queue, and at what point
International (if you ship abroad): duties paid at checkout or by the shopper on delivery / who pays if a parcel is refused over duties / who pays return shipping from abroad
```

The roles they list decide the columns of the authority table: a solo founder with one seasonal helper gets two columns, not four.

**Turn 2. Only the blocking gaps, answered in one reply.** One message, one numbered line per blocking gap, headed "Examples, pick one or write your own". Each line has 2 or 3 options a), b), c), most cautious first, in the merchant's currency; for a limit, each option gives one value per role (for example "3. Partial refund for a problem, VA: a) $0 b) $25 c) $50"). End with "Reply in one line, for example 1b, 2a, 3: $40. Or reply all a to take the first example everywhere." Then one line naming the non-blocking gaps that will be marked in the playbook. If nothing blocks, go straight to turn 3.

**Turn 3. The full playbook.** Only if the reply leaves a blocking item open, says "you decide", or creates a new conflict, ask once more about just those items (turn 4 becomes the playbook). Never a second follow-up: anything still open is marked.

### What "blocking" means

A gap is blocking if, without it, staff would have to guess about money or about who to reach. Exactly these, and nothing else:

- no currency;
- a blank cell in the authority table (Part 2) for any role except the owner, or no maximum compensation per order;
- for each of the 4 plans (carrier delay, stock-out, volume above forecast, customs if shipping abroad), checked one by one: no trigger or no owner;
- no owner reply time for escalations;
- no weekend and holiday cover;
- a contradiction between two of the merchant's answers, or between an answer and a Shopify fact above (for example "agents cancel shipped orders").

Everything else is non-blocking (promotion details, dates, returns details, policy locations, message wording, duties): write `[DECISION NEEDED: <the question>]` where it is used and list it in Open decisions. Never ask about it.

If the merchant pastes something instead of filling the form, read it for the facts it contains and treat only the blocking gaps as questions.

## What to produce

Three parts, in this order, using the templates in `references/`.

1. **One-page brief** (`references/brief-template.md`). Readable on a phone: in the brief, no table wider than two columns, short lists instead. (The authority table in part 2 has one column per role.) If it runs past one page, cut explanation, not facts.
2. **Who may decide what** (`references/authority-table-template.md`). Rows are decisions, one column per role the team has, cells are "Yes, up to [amount]", "No, escalate to [role]", or a marked gap. Then the per-order limit, the always-owner list, how to escalate, and the Shopify facts above.
3. **Contingency plans** (`references/contingency-templates.md`): carrier delay, stock-out mid-sale, volume above forecast, and parcel held at customs if they ship abroad. Each has a trigger, an owner, the first three actions, what shoppers are told, when to stop and what to log.

Close with **Open decisions**: every `[DECISION NEEDED]` item. List the blocking ones first (as defined above; normally none are left after turn 2 or the follow-up), and repeat the example options for each so the merchant can answer in one line.

## Dates

Write the weekday with each date only when you are sure of it. Anchors: Fri 27 Nov 2026, Mon 30 Nov 2026, Fri 25 Dec 2026, Fri 1 Jan 2027. Count from the nearest anchor. If unsure, leave the weekday out and ask the merchant to confirm. Times always include a timezone.

## Checks before handing it over

- Every amount, trigger and count traces to something the merchant said, picked or accepted. Do not add thresholds of your own (for example "escalate if more than 10 orders"). If you cannot point to the answer it came from, mark it.
- No example value appears in the final playbook unless the merchant chose it.
- The brief has no table wider than two columns (promotions are short lists).
- Every role named exists in the team list; no column for a role they do not have.
- Every weekday is recounted from the nearest anchor. Dates in the brief match the cutoff table and the promotion terms given.
- Every offer in a contingency plan is allowed by the authority table for the role making it.
- Nothing tells staff to cancel a shipped order or refund an order with an open chargeback.
- Nothing in the playbook is an instruction to an AI or a bot. If the merchant wants their AI assistant to follow the same rules, point them to the terms from `campaign-rules-policy-qa`.

## Scope

This writes the team document. It does not write or check the sale terms (`campaign-rules-policy-qa`), compute cutoff dates (`delivery-cutoff-planner`), forecast volume or build a roster (`peak-load-cover-planner`), or change anything in the store. It does not give legal advice on refunds or consumer rights; if the merchant asks whether a limit is legal in a market, say so and send them to someone qualified.
