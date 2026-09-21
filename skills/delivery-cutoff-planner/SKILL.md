---
name: delivery-cutoff-planner
description: Compute per-region last-order (cutoff) dates so a shipment arrives by a target date, from the store's own processing time and carrier transit estimates, and write the three delivery messages Shopify does not provide (on track, running late, will not arrive in time). Use when someone asks when customers have to order to get something by a holiday, wants a per-zone shipping deadline, or needs a message for a delayed or missed delivery.
license: MIT
compatibility: Runs the bundled Python script with the standard library only, no network access and no dependencies. Falls back to guided manual arithmetic if scripts cannot run in the environment.
metadata:
  version: "0.1"
---

# Delivery cutoff planner

December, not sale week, is the longest exposure of the peak season, and delivery is the most-asked subject across every phase of it. Shopify has no built-in way to back-solve a target arrival date into a per-region last-order date, and no template at all for the message a shopper needs when their order is going to be late. This skill produces both.

## The rule that governs everything here

**The transit time is a fact, not something to estimate.** The buffer is a judgment call, and it belongs to the merchant. Never blend the two, and never invent either.

Read `references/where-transit-times-come-from.md` before asking the merchant anything. It explains why Shopify's own tools do not hand you a transit time for free, and it is the reason this skill asks rather than assumes.

If a zone's transit time is not known, mark it `[DECISION NEEDED: confirm carrier transit time for <zone>]` and do not run the calculation on a guess. A wrong transit number produces a cutoff date that is wrong in the direction of promising too much time, which is the most damaging error this skill can make.

## If the message is a plain question, answer it first

Not every request is "compute my cutoffs." Some are a yes-or-no question about what Shopify itself can do, such as "can Shopify set a different cutoff per region natively." Answer that plainly and first, in one direct sentence, before offering to run the full workflow. `references/where-transit-times-come-from.md` has the verified facts: Shopify's manual delivery dates are a single global setting with one cutoff, and automated delivery dates are a per-order estimate, not a published per-region cutoff. State the fact, do not hedge it into "partially" and do not lead with an adjacent feature (such as per-zone shipping-rate labels) that does not actually answer what was asked. Offer to run the workflow after the direct answer, not instead of it.

## How to work

1. **Gather the zones.** Ask which regions or shipping profiles the merchant wants cutoffs for. One profile for the whole country is one zone; different transit times per region need one zone each, because a single blended cutoff understates the risk for the slower zones.

2. **Get the target arrival date.** Usually a holiday or the day before it. Do not assume; some merchants target earlier to leave gift-wrapping time for the recipient.

3. **Get the transit time per zone**, from the merchant's own carrier data for this year, never from memory or a stale published deadline. See `references/where-transit-times-come-from.md`.

4. **Get the store's own processing time**, and any warehouse or carrier closures between now and the target date, especially the days the season adds that an ordinary week does not have.

5. **Ask about the buffer.** This is the one number in the calculation that is a judgment call rather than a fact. Frame it as a trade-off: a larger buffer costs orders near the cutoff, a smaller one risks a promise the carrier does not keep. Do not pick a default silently.

6. **Build the input and run the script.** Assemble the JSON described in `references/cutoff-input-schema.md` and run:

   ```
   python3 scripts/cutoff.py <input.json>
   ```

   If Bash or script execution is unavailable in this environment, or the merchant's platform disables it, do the same subtraction by hand: walk backward from the target date by transit plus processing plus buffer working days, skipping weekends and any named closures, and show the working days you skipped so the merchant can check it. The arithmetic is simple enough to verify either way; that is why it lives in a script rather than in prose.

7. **Report every zone**, including any the script marks infeasible. An infeasible zone is not a bug in the calculation, it is information: standard processing cannot meet the target for that zone today, and the merchant needs to know it before a shopper finds out the hard way. State the two ways out plainly: expedite the remaining orders, or move the published target date for that zone.

8. **Write the delivery messages** the merchant needs, from `references/delivery-templates.md`. Fill only what the merchant has confirmed: the offer in the late-delivery and missed-delivery templates (a partial refund, a gift card, a cancellation option) is the merchant's decision, and an unconfirmed offer must not appear in a template that goes out under the store's name.

## What to publish, and where

The cutoff table is meant to be published, one line per zone, plain language: "Order by **[date]** for [zone]." Ask the merchant where it goes: a banner, the shipping policy page, product pages, or all three. A correct cutoff nobody can find fails the same way as a wrong one.

The three templates are meant to be ready before they are needed, loaded wherever the merchant sends order updates from, not written for the first time on the day a shipment is actually late.

## Scope

This computes and publishes shipping deadlines and writes the messages for delivery problems. It does not touch Shopify's discount or returns configuration, which is `campaign-rules-policy-qa`, and it does not track a real shipment or call a carrier API. If the merchant wants live tracking data reflected in these messages, that needs an integration this skill does not have; say so rather than fabricating a tracking status.
