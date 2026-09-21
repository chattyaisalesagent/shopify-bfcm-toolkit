# Where each gap goes

| Line | If not Ready | Route to |
|---|---|---|
| 1. Discount rules | Audit or write the terms | `campaign-rules-policy-qa` (audit mode if text exists, authoring mode if not) |
| 2. Order-by dates per region | Compute per-zone cutoffs | `delivery-cutoff-planner` |
| 3. Automated order lookup | **Not built by this toolkit.** Check the order-lookup setting in Shopify Inbox, or in the merchant's helpdesk. The official Shopify plugin for ChatGPT can read order data (`get-order`, `list-orders`) but does not test or configure the shopper-facing self-serve path. | Point to the merchant's own inbox/helpdesk settings |
| 4. Handoff to a person | **Not built by this toolkit.** This is a policy and staffing decision: who has authority, what they see on handoff. Ask the merchant to write it down themselves, or capture it as an open decision the way `campaign-rules-policy-qa` does for commercial rules, but this toolkit does not configure a handoff path in any vendor's system. | Point to the merchant's helpdesk/inbox escalation settings |
| 5. Weekly review | Sort last week's unanswered messages by type of gap | `conversation-gap-analyzer`, if the merchant's support tool can export a CSV. If they use Shopify Inbox only, say plainly that Shopify Inbox has no conversation export as of this writing, so this line cannot be automated for them; the review has to happen by hand inside Shopify Inbox itself. |
| 6. Plan cap and overage | **Not built by this toolkit.** No API reliably exposes cap and overage behaviour across vendors. | Give the merchant this exact question list to send their support/AI vendor: *"What is our included allowance this billing period? What is the overage price per unit past that? What happens the moment we hit the cap: does the assistant stop, queue to a person, or keep billing? Is there a way to cap spend rather than let it run?"* |
| 7. Holiday returns policy | Audit or write the policy | `campaign-rules-policy-qa` (returns pack) |

## What "not built by this toolkit" means here

Lines 3, 4 and 6 were deliberately not built as skills. Order lookup and handoff are commodity features already shipped by Shopify Inbox and every mainstream helpdesk; building on top of them would duplicate the platform rather than fill a gap. Plan cap and overage behaviour is vendor-specific and mostly undocumented, so the honest deliverable is the question list above, not a fake automated check.

Naming this plainly in the audit output matters more than it looks: a merchant reading a readiness report should never come away thinking every gap has a button to fix it inside this toolkit. Three of the seven don't, and the report should say so in the same breath as it reports the score.
