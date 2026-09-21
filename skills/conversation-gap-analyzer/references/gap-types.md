# The five gap types

Every row lands in exactly one. Never invent a sixth. This taxonomy replaces the single "unanswered = content gap" assumption the research found to be wrong: in a hand-read sample of 99 unanswered messages, only 33 needed new content; the rest split across the other four types below.

**needs_content** — a genuine question the store's existing content does not answer. This is the only bucket that becomes writing work, and it routes to `campaign-rules-policy-qa` or `delivery-cutoff-planner` depending on subject.

**needs_action** — the shopper wants something done, not explained: notify me when it's back in stock, cancel this order, change my address. No page fixes this; it needs a workflow or an integration.

**needs_context** — the message references an order number, a tracking number, or an account detail. The assistant most likely needs order-lookup or account data it does not have, not new content.

**needs_handoff** — an explicit request for a human, or language strong enough that automation should not be the one to respond (anger, a threat to escalate, a request for a manager).

**needs_nothing** — thank-yous, short acknowledgements, button-click artifacts, empty rows. No answer was ever required. The research found this is the largest single bucket in a typical unanswered-message list, which is exactly why treating the whole list as a content backlog overstates the writing work by several times over.

## Reporting

Report the count and share of each type, for this file, this week. **Never state an expected ratio as if it were a platform norm** ("about a third should be real content questions") — the research sample was 99 messages, one reader, no second coder, and it is not a benchmark. Every number in the output belongs to the file the merchant gave you, not to the research behind this toolkit.

## Comparing weeks

If the merchant runs this skill on consecutive weeks, compare the gap-type shares between runs, not the raw counts (volume changes week to week for reasons that have nothing to do with content gaps). A rising needs_content share in one subject area is the signal worth acting on; a rising needs_nothing share usually means more noise got exported, not more work.
