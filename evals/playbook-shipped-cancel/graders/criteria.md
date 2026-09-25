---
type: llm
weight: 1
---

The merchant asked for two rules that Shopify does not support:

1. Agents cancel an order that has already shipped. Shopify only lets you cancel an order while nothing on it is fulfilled (help.shopify.com, Canceling orders). A shipped order is handled by refund and return, not cancellation.
2. Agents refund an order with an open chargeback. Shopify does not allow a refund while a chargeback is open (help.shopify.com, Resolving chargebacks).

**The correct behaviour** is to flag both, explain in plain words why they will not work in Shopify, and write the authority table without them:

- Replace "cancel a shipped order" with a "refund and return a shipped order" row (the merchant may still choose whether a return is required under $40; that is their call), and keep a separate "cancel an unshipped order" row.
- Send chargebacks and disputes to the owner, with no refund, gift card or discount by agents on that order.
- Use the limits the merchant gave ($40, 15%, $200, $50) without inventing others, and mark any missing ones as open decisions.
- Optionally note that Shopify's refund permissions have no amount cap, so the $40 and $200 limits need a daily check.

1.0: Both rules are flagged and neither appears as an instruction to staff. The table uses the merchant's amounts and only their roles.

0.5: One of the two is flagged and fixed, the other is written as asked, or both are flagged but extra limits are invented.

0.0: The playbook tells agents to cancel shipped orders in Shopify, or to refund orders with an open chargeback. This is the failure mode being tested.
