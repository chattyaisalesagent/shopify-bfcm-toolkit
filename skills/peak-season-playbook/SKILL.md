---
name: peak-season-playbook
description: Write the peak-season playbook a Shopify merchant's human support team works from during BFCM and the holidays. Produces a one-page brief for staff and seasonal hires (active promotions, delivery cutoffs, returns window, where each policy lives), a table of who may decide refunds, exchanges and compensation and up to what amount, and contingency plans for a carrier delay, a stock-out mid-sale and volume above forecast. Use when a merchant asks for a support team brief, onboarding notes for seasonal staff, refund or compensation authority limits, an escalation policy, or a plan for what to do if shipping is delayed, stock runs out or the team is overwhelmed during peak season.
license: MIT
compatibility: Works with no integrations and no scripts. The merchant supplies their own terms, policies, cutoff dates and limits, optionally as the output of campaign-rules-policy-qa and delivery-cutoff-planner.
metadata:
  version: "0.1"
---

# Peak season playbook

In November a support agent answers questions about rules somebody else decided: which codes stack, when the last order ships for Christmas, how long a gift can be returned. In the first week of December a seasonal hire who started on Monday gets asked for a refund on a late order, and nobody told them whether they may give one. This skill writes the document that tells them, before they are asked.

It is written for people, not for an AI assistant. Short sentences, one fact per line, readable on a phone between two chats.

## The rule that governs everything here

**Money limits and commercial rules come only from the merchant. Never fill one in.**

How much an agent may refund without asking, what compensation a late order earns, whether a sale item can be exchanged: each of these is money the merchant will pay, and an agent will do exactly what the playbook says. A reasonable-sounding default is worse than a visible gap, because the gap gets answered and the default gets followed.

Every unknown is marked `[DECISION NEEDED: <the question>]` inline, where it would be used, and repeated in an Open decisions list at the end. Do not smooth over an ambiguous policy either: if the merchant's returns page says "30 days" and does not say from order or from delivery, that goes in the brief as a marked question, not as your best guess.

## Inputs, in this order

Ask one question at a time and wait for the answer.

1. **Outputs from the other kit tools, if they have them.** Ask the merchant to paste:
   - the terms, FAQ and staff decision table from `campaign-rules-policy-qa`;
   - the cutoff table and the three delivery messages from `delivery-cutoff-planner`.

   Treat these as merchant-stated; they are what the merchant approved. If either still contains `[DECISION NEEDED]` markers, carry them over unchanged.
2. **If they do not have those outputs, ask directly** for: each active promotion (what, dates with time and timezone, exclusions, stacking); delivery cutoff dates per region; the returns and exchange window for holiday purchases, including when it starts and ends; and the URL or location of each policy.
3. **Who is on the team.** Roles, not only names: owner, lead, permanent agent, seasonal hire. Who is the escalation contact on weekends and holidays.
4. **Authority limits, one decision type at a time**: refunds, exchanges, compensation for a problem (discount code, gift card, free shipping on the next order, partial refund). For each role: allowed or not, and the maximum amount. Then: what always goes to the owner, whatever the amount.
5. **Contingency decisions**, per scenario in `references/contingency-templates.md`: the trigger, who acts, what the shopper is offered. Ask; do not propose an offer.

If a message is pasted instead of answered, read it for the facts it contains and ask only for what is still missing.

## What to produce

Three parts, in this order, using the templates in `references/`.

1. **One-page brief** (`references/brief-template.md`). Active promotions, delivery cutoffs by region, returns window, where each policy lives, who to ask. If it runs past one page, cut explanation, not facts.
2. **Who may decide what** (`references/authority-table-template.md`). Rows are decision types, columns are roles, cells are "yes up to [amount]", "no, escalate to [role]", or a marked gap. Then the list of things that always go to the owner.
3. **Contingency plans** (`references/contingency-templates.md`) for three scenarios: carrier delay, stock-out mid-sale, volume above forecast. Each has a trigger, who does what, what shoppers are told, and when to stand down.

Close with **Open decisions**: every `[DECISION NEEDED]` item, with the ones that block the playbook from being handed out listed first. Any blank money limit blocks it.

## Checks before handing it over

- Every amount in the authority table traces to something the merchant said. If you cannot point to the answer it came from, mark it.
- Dates in the brief match the cutoff table and the promotion terms the merchant gave. If two sources disagree, show both and mark the conflict; do not choose.
- Shopper-facing wording in the contingency plans offers only what the authority table allows. A contingency plan that promises a gift card the agent is not allowed to give creates the escalation it was meant to prevent.
- Nothing in the playbook is an instruction to an AI or a bot. If the merchant wants their AI assistant to follow the same rules, that is a separate job: point them to the terms from `campaign-rules-policy-qa`.

## Scope

This writes the team document. It does not write or check the sale terms (`campaign-rules-policy-qa`), compute cutoff dates (`delivery-cutoff-planner`), forecast volume or build a roster (`peak-load-cover-planner`), or change anything in the store. It does not give legal advice on refunds or consumer rights; if the merchant asks whether a limit is legal in a market, say so and send them to someone qualified.
