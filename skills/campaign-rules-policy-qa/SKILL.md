---
name: campaign-rules-policy-qa
description: Review or write the shopper-facing rules for a sale, promotion, holiday returns policy or international orders on a Shopify store. Cross-checks the same term across every place it appears (policy page, FAQ, banner, email, product page, saved replies) and flags every mismatch, finds missing fields and contradictions, checks that product claims read the same everywhere, elicits the decisions the merchant has not made, asks the blocking decisions in one round, says what the platform does automatically and what staff honour by hand, and then produces one clean publishable version with terms, FAQ answers, a staff decision table and replacement text per place. Use when someone asks to check, write or line up sale terms, discount rules, free shipping thresholds, a returns or holiday returns policy, duties and taxes wording, or wants to know if their pages contradict each other.
license: MIT
compatibility: Works with no integrations. The merchant supplies their own text and settings. No store connection, export or API access is required.
metadata:
  version: "0.3"
---

# Campaign rules and policy QA

A sale creates rules that exist nowhere until the merchant writes them down. The catalogue does not contain them, the discount configuration does not explain them, and the checkout does not narrate them. And once they are written, they get written again: on the banner, in the email, in the FAQ, in a saved reply, each time slightly differently. This skill turns those decisions into text a product page, a policy page, a support agent and an AI assistant can all use, makes every copy say the same thing, and refuses to invent any of them.

## The rule that governs everything here

**Never state a commercial rule the merchant has not given you.**

Whether a code stacks, whether sale items can be returned, which regions are excluded, how long the returns window runs, who pays import duties: each of these is a decision with money attached, and the merchant is bound by whatever their pages say. A plausible invented rule is worse than a visible gap, because the gap gets fixed and the invention gets published.

Every unknown is marked, never filled. Use `[DECISION NEEDED: <the question>]` inline so it is impossible to publish by accident, and collect the same items in an Open decisions list at the end.

This applies to polish too. Do not smooth an ambiguous sentence into a confident one. "Free shipping over $75" is ambiguous during a percentage sale and must be flagged, not rewritten into something that merely sounds finished.

It applies to mismatches most of all. When two places disagree, never pick the version that looks more recent, more generous or more common. The merchant picks. Until they do, the term is `[DECISION NEEDED: ...]` everywhere it appears.

## Three ways in

**Cross-check mode**, when the same terms appear in more than one place. This is the highest-value mode and the one to offer first whenever the merchant mentions a banner, an email, an FAQ or saved replies alongside a policy page. Shoppers read the banner, staff answer from a macro, the policy page says a third thing, and every version is binding on someone. See "How to cross-check" below.

**Audit mode**, when the merchant has one text already. Read what they have, then report in this order: contradictions first, missing fields second, ambiguities third. Do not rewrite anything until the gaps are named.

**Authoring mode**, when there is nothing yet. Work through the field list, ask about the fields that matter for what they are running, and build the text from their answers alone.

Most requests are a mix. A merchant with a half-written policy and a live banner wants the two lined up, the half checked and the rest written. Run cross-check first, then audit, then authoring.

## How to cross-check

1. **Collect every source, pasted, labelled.** Ask the merchant to paste the actual text from each place a shopper or a staff member reads the terms: policy pages (returns, shipping, terms), FAQ, sale banner or announcement bar, promotional emails and SMS, product pages, cart or checkout notes, saved replies and macros, the knowledge base an AI assistant answers from, social posts. Label each block by its source. If the merchant describes a source from memory instead of pasting it, include it but mark it "described, not pasted"; a paraphrase cannot be checked word for word.
2. **Extract every statement per term.** Use the cross-check term list in `references/field-list.md`: free shipping threshold, returns window, return of sale items, code stacking, already-reduced items, sale start and end, exclusions, who pays return shipping, refund method, gift returns, order-by dates, duties and taxes, and every product claim. Quote each statement exactly.
3. **Line them up side by side, one table per term.** Every source that mentions the term gets a row with its exact wording. Sources that are silent on a term are listed as silent only where a shopper would expect to find it there (a banner that advertises free shipping but never states the threshold).
4. **Classify each term.** Consistent; Mismatch (a shopper would get a different answer depending on where they read: different values, dates, conditions or scopes, so "30 days of delivery" against "until January 31" is a Mismatch); Incomplete (one source leaves out a condition another states, but what it says is not wrong); or Stale (a date, year or amount left over from a previous campaign).
5. **For every mismatch, name the choice.** List each distinct version as an option (A, B, C) with the sources that carry it, and say plainly: the merchant must pick one version, then every listed source changes to match. Do not choose. Where `references/platform-limits.md` shows how the store will actually behave (for example, a shopper who gets both the discount and free shipping has the threshold measured on the discounted cart), state that as platform behaviour next to the options, because a version the checkout cannot honour is a trap whichever one they pick. Mark the term `[DECISION NEEDED: pick one version of <term>: A, B or C]`.
6. **Test the answers against real shoppers.** Read every saved reply, FAQ answer and assistant answer as four people: a buyer who checked out as a guest, a gift recipient, a shopper who wants an exchange, and a shopper in each country the store ships to. "Just log in and click Return items" works for a guest buyer (they sign in with the order email and a code) but not for a gift recipient or an exchange. "Free returns on all orders" has to be true in every shipping country or say where it applies.
7. **Give the update list.** Once a version is picked, the output names every source that has to be edited and gives its replacement text, so nothing is left saying the old thing.

Then continue with the audit steps below on the combined text.

## How to work

1. **Identify the pack or packs.** Read `references/field-list.md` for the packs you need, not all of them: A, discount and campaign rules; B, holiday and post-holiday returns; C, international orders, duties and taxes; D, product claims consistency. Pack D applies whenever the merchant pastes product pages or product descriptions from more than one place.

2. **Check for contradictions before anything else.** Two statements that cannot both be true are the most damaging defect and the easiest to miss, because each sentence reads fine alone. The classic pair is a sitewide sale that declares all sale items final while the returns policy promises returns on everything. Name it as a contradiction and say which of the two the merchant has to change. In cross-check mode, the mismatch table already covers disagreements between sources; this step covers statements that clash in meaning even when they are about different terms.

3. **Check each field in the list.** For each one: present and unambiguous, present but ambiguous, or absent. Ambiguity is a defect, not a detail. A date without a time and timezone, a threshold without a stated order of operations, and an exclusion clause that names no exclusion are all unusable to a shopper.

4. **Check what the platform does on its own.** Read `references/platform-limits.md`. Some things a merchant decides cannot be configured exactly on Shopify: say how close the settings get, what staff do by hand for the rest, and when each setting has to change. Never tell the merchant orders are unprotected when staff can create the return manually to honour the page. Only raise the US de minimis point if the store ships into the US from another country; a US store shipping within the US is not affected.

5. **First reply: findings and the blocking decisions.** Follow `references/output-templates.md`: the cross-check table when that mode ran, the findings, then the blocking decisions as one numbered batch the merchant can answer in a single reply, each with its known options. Do not print terms full of placeholders at this stage.

   A decision **blocks publication** if its answer changes whether a shopper qualifies, what they pay, a date or time, eligibility, or the refund amount, method or window. The free shipping threshold measured before or after discount, and the sale start and end time with timezone, always block, as does every product-claim mismatch. Wording, tone and layout never block.

6. **Decision round.** Take the merchant's answers. If one is unclear or opens a new blocking gap, ask again. If nothing blocks, go straight on.

7. **Final reply: one clean version.** Shopper-facing terms, FAQ answers, staff decision table, replacement text per place, what Shopify does automatically versus by hand with the settings and dates to change, and any non-blocking decisions left. No blocking item stays as `[DECISION NEEDED]` in the final text; that is what makes it ready to publish. Say where the text goes and who approves it.

## What to write down and what to leave alone

Label each statement by where it comes from:

- **Merchant-stated.** They told you. Reproduce it exactly, do not improve it.
- **Platform behaviour.** How the store will actually behave, from `references/platform-limits.md`. Say so plainly so the merchant can tell it apart from their own choice.
- **Not yet decided.** Marked, never guessed.

Never present a recommendation as though it were one of the first two. If a default is genuinely conventional, you may name it as a suggestion, clearly labelled, alongside the marked gap. The gap stays marked either way.

Product claims (materials, allergens, safety, certifications) are facts about the product, not decisions, and you cannot see the product. When two sources disagree about a claim, say which sources say what and ask the merchant to confirm the true fact from the supplier's documentation. Never state which version is true.

## Scope

This covers what the store tells shoppers about a sale, about returns, about international orders and about what its products are. It does not configure the discount, it does not write legal text, and it does not assess whether a policy, a duties statement or a product claim satisfies law or customs rules in any market. Where the answer depends on the law where the shopper lives, or on customs rules, say so and send the merchant to someone qualified.

Delivery cutoff dates and late-delivery messages are a different job with different arithmetic and are not part of this skill (see `delivery-cutoff-planner`). If a cross-check finds order-by dates that disagree between sources, report the mismatch here and send the date calculation itself there.
