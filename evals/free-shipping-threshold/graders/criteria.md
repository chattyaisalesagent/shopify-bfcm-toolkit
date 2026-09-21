---
type: llm
weight: 1
---

A narrow, checkable question about how the merchant's platform actually behaves, plus what to publish about it.

**The verified behaviour:** on Shopify, when a free-shipping discount combines with an order or product discount, the free-shipping threshold is evaluated against the **discounted** cart value. So a $90 cart that becomes $67.50 falls below a $75 threshold and does not get free shipping, unless the merchant changes the threshold or the combination settings.

**Scoring.**

1.0 — Answers the question directly and correctly: at $67.50 the order no longer clears a $75 threshold, because the threshold is measured after the discount. Then tells the merchant this is the exact case shoppers complain about during a sitewide sale, gives them the two levers they actually have (lower the threshold for the sale period, or state the rule explicitly), and supplies terms wording that says plainly which price the threshold is measured against.

0.5 — Identifies that the order of operations matters and that the merchant must decide or verify it, but does not state Shopify's actual behaviour, or states it with visible uncertainty.

0.0 — Asserts the shopper still gets free shipping because the cart was $90 before the discount, or gives a confident answer in either direction without connecting it to how the platform computes the threshold. Also zero for answering only with generic advice to "check your settings" while writing terms wording that leaves the ambiguity in place.

The wording supplied for the terms page must remove the ambiguity. "Free shipping on orders over $75" is the defective sentence being tested and must not be reproduced unchanged.
