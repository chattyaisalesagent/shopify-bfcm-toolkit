---
name: campaign-rules-policy-qa
description: Review or write the shopper-facing rules for a sale, promotion or holiday returns policy on a Shopify store. Finds missing fields and contradictions in terms a merchant already has, elicits the decisions they have not made, warns where the platform cannot enforce what they intend, and produces publishable terms, FAQ answers and a staff decision table. Use when someone asks to check, write or extend sale terms, discount rules, promotion conditions, a returns policy or a holiday returns window.
license: MIT
compatibility: Works with no integrations. The merchant supplies their own text and settings. No store connection, export or API access is required.
metadata:
  version: "0.1"
---

# Campaign rules and policy QA

A sale creates rules that exist nowhere until the merchant writes them down. The catalogue does not contain them, the discount configuration does not explain them, and the checkout does not narrate them. This skill turns those decisions into text a product page, a policy page, a support agent and an AI assistant can all use, and it refuses to invent any of them.

## The rule that governs everything here

**Never state a commercial rule the merchant has not given you.**

Whether a code stacks, whether sale items can be returned, which regions are excluded, how long the returns window runs: each of these is a decision with money attached, and the merchant is bound by whatever their terms page says. A plausible invented rule is worse than a visible gap, because the gap gets fixed and the invention gets published.

Every unknown is marked, never filled. Use `[DECISION NEEDED: <the question>]` inline so it is impossible to publish by accident, and collect the same items in an Open decisions list at the end.

This applies to polish too. Do not smooth an ambiguous sentence into a confident one. "Free shipping over $75" is ambiguous during a percentage sale and must be flagged, not rewritten into something that merely sounds finished.

## Two ways in

**Audit mode**, when the merchant has text already. This is the more common case. Read what they have, then report in this order: contradictions first, missing fields second, ambiguities third. Do not rewrite anything until the gaps are named.

**Authoring mode**, when there is nothing yet. Work through the field list, ask about the fields that matter for what they are running, and build the text from their answers alone.

Most requests are a mix. A merchant with half a page wants the half checked and the rest written. Run both, in that order.

## How to work

1. **Identify the pack.** A discount or promotion, a holiday returns and exchange policy, or both. Read `references/field-list.md` for the pack you need, not for both.

2. **Check for contradictions before anything else.** Two statements that cannot both be true are the most damaging defect and the easiest to miss, because each sentence reads fine alone. The classic pair is a sitewide sale that declares all sale items final while the returns policy promises returns on everything. Name it as a contradiction and say which of the two the merchant has to change.

3. **Check each field in the list.** For each one: present and unambiguous, present but ambiguous, or absent. Ambiguity is a defect, not a detail. A date without a time and timezone, a threshold without a stated order of operations, and an exclusion clause that names no exclusion are all unusable to a shopper.

4. **Check what the platform can actually enforce.** Read `references/platform-limits.md`. Some things a merchant decides cannot be configured on Shopify and must be honoured by hand. Saying so is part of the job, because the alternative is a promise that fails in front of a shopper. This is the step most easily skipped and the one that most often matters.

5. **Produce the output.** Follow `references/output-templates.md`. Four artefacts: the shopper-facing terms, the FAQ answers, the staff decision table, and the open decisions. Add the platform limits note whenever step 4 found something.

6. **Say what happens next.** Where the text goes, who has to approve it, and which open decisions block publication.

## What to write down and what to leave alone

Label each statement by where it comes from:

- **Merchant-stated.** They told you. Reproduce it exactly, do not improve it.
- **Platform behaviour.** How the store will actually behave, from `references/platform-limits.md`. Say so plainly so the merchant can tell it apart from their own choice.
- **Not yet decided.** Marked, never guessed.

Never present a recommendation as though it were one of the first two. If a default is genuinely conventional, you may name it as a suggestion, clearly labelled, alongside the marked gap. The gap stays marked either way.

## Scope

This covers what the store tells shoppers about a sale and about returns. It does not configure the discount, it does not write legal text, and it does not assess whether a policy satisfies consumer law in any market. Where the answer depends on the law where the shopper lives, say so and send the merchant to someone qualified.

Delivery cutoff dates and late-delivery messages are a different job with different arithmetic and are not part of this skill.
