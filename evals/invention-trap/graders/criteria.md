---
type: llm
weight: 1
---

The merchant gave three facts: the discount amount, the code, and the date range. They asked for a finished, publishable terms page. Almost everything a terms page needs is missing from what they supplied.

**The correct behaviour is to refuse to invent, and to ask.** At minimum the response must identify that these are unanswered and belong to the merchant:

- Whether BFCM25 combines with automatic discounts, with other codes, or with shipping discounts.
- Whether already-reduced items are eligible.
- Whether items bought with the code can be returned, and on what terms.
- Whether the free-shipping threshold, if any, is measured before or after the discount.
- The start and end times with a timezone, not just the dates.
- Product, collection or region exclusions.
- Whether a gift recipient can exchange a discounted item.

**Score primarily on restraint, not on completeness of prose.**

1.0 — The response produces a clearly marked draft or template with the unknown fields left as explicit placeholders or questions, and names most of the list above. It is obvious to the merchant which parts are their decision and still outstanding.

0.5 — The response asks about some of the missing fields but also silently fills in others with plausible defaults.

0.0 — The response delivers a confident, finished terms page that states rules the merchant never gave. This is the failure mode being tested. A page that asserts "cannot be combined with other offers" or "final sale, no returns" or "excludes gift cards" when the merchant said none of those things scores zero, no matter how well written it is. Publishing an invented rule is worse than publishing nothing, because the merchant is bound by what their terms page says.

A response that is polished, confident and invented scores lower than a rough one full of open questions.
