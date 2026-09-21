---
type: llm
weight: 1
---

This tests whether the response knows a specific, verified limitation of the platform the merchant named, rather than cheerfully writing a policy that the store cannot actually enforce.

**The two facts that matter, both verified against Shopify's own documentation:**

1. **Shopify return rules cannot express a seasonal window.** A return rule offers a number of days from delivery, or from the last item delivered: 14, 30, 90, unlimited, or a custom number of days. There is no purchase-date-range trigger and no fixed end date. "Bought between November 1 and December 24, returnable until January 31" is therefore not expressible as a rule. It can be published as policy, but the platform will not enforce it, so it has to be honoured manually by whoever handles returns.

2. **Return rule changes apply only to future orders.** A merchant who changes the rule in December cannot retroactively extend the orders already placed in November. If they want November orders covered, the rule has to be in place before those orders are taken, or every one of them is a manual exception.

**Scoring.**

1.0 — States both limitations plainly, writes the policy text anyway, and tells the merchant what the manual workaround costs them: which orders will need hand-handling and who does it. Bonus credit for noticing that the request implies the rule must be set up before 1 November, not in December.

0.5 — Mentions one of the two limitations, or hedges vaguely that "Shopify may not support this" without saying what the rule can actually express.

0.0 — Writes the policy and describes setting it up in Shopify as though a seasonal window were a supported configuration. This is the failure being tested: it leaves the merchant believing the platform will enforce a promise it cannot enforce, which surfaces on 26 December when a shopper is told no.

Do not award credit for generally cautious language. The response must name what return rules can express, or it has not demonstrated the knowledge.
